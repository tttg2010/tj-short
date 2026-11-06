#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""salpx Wan 3.0 (wan3.0-*) video client for TJ Short.

纯标准库实现，无第三方依赖。视频只走 https://www.salpx.com/v1。

用法示例：
  # 文生视频
  wan3_video_client.py video --prompt "..." --duration 5 --ratio 16:9

  # 首帧图生视频（默认短剧路线）
  wan3_video_client.py video --prompt "..." --duration 8 --ratio 9:16 \
      --first-frame first_frames/EP01-03.png --wait --out outputs/videos/ep01-03.mp4

  # 多素材参考（参考图 + 参考视频 + 参考音频）
  wan3_video_client.py video --prompt "图1 的角色跟着视频1 的动作跳舞，口型贴合音频1" \
      --duration 10 --ratio 9:16 \
      --ref-image char.png --ref-image product.png \
      --ref-video dance.mp4 --ref-audio voice.mp3 --wait --out outputs/videos/dance.mp4

  wan3_video_client.py status <task_id>
  wan3_video_client.py download <task_id> --out outputs/videos/x.mp4
  wan3_video_client.py models
"""

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://www.salpx.com/v1"
DEFAULT_MODEL = "wan3.0-720p"
CRED_FILE = os.path.expanduser("~/.config/salpx/credentials.env")

# 人民币 / 秒
PRICES = {
    "wan3.0-480p": 0.21,
    "wan3.0-720p": 0.42,
    "wan3.0-1080p": 0.84,
    "wan3.0-hm-480p": 0.28,
    "wan3.0-hm-720p": 0.56,
    "wan3.0-hm-1080p": 1.11,
}

REFERENCE_TYPES = {"reference_image", "reference_video", "reference_audio", "file", "link"}
FRAME_TYPES = {"first_frame", "last_frame"}

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXT = {".mp4", ".mov"}
AUDIO_EXT = {".wav", ".mp3"}
DOC_EXT = {".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md"}


def die(message, code=2):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    raise SystemExit(code)


def read_env_file(path):
    values = {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                value = value.strip().strip('"').strip("'")
                if key.strip():
                    values[key.strip()] = value
    except FileNotFoundError:
        pass
    return values


def config(env_path):
    """优先级：环境变量 > --env 文件 > ~/.config/salpx/credentials.env"""
    values = read_env_file(CRED_FILE)
    if env_path:
        values.update(read_env_file(env_path))
    for key in list(values) + ["SALPX_API_KEY", "SALPX_BASE_URL", "SALPX_VIDEO_MODEL"]:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def api_key(values):
    key = (values.get("SALPX_API_KEY") or "").strip()
    if not key:
        die(
            "SALPX_API_KEY 缺失。请写入环境变量、项目 .env，"
            "或在 ~/.config/salpx/credentials.env 里设置 SALPX_API_KEY=sk-xxx"
        )
    return key


def base_url(values):
    url = (values.get("SALPX_BASE_URL") or DEFAULT_BASE_URL).strip().rstrip("/")
    if url.startswith("https://www.salpx.com") and not url.endswith("/v1"):
        url = url + "/v1"
    if "zhongbiao" in url or "h3." in url:
        die(f"拒绝使用已废弃的视频端点：{url}。视频只允许走 https://www.salpx.com/v1")
    return url


def request(values, method, path, payload=None, timeout=600):
    url = base_url(values) + path
    data = None
    headers = {"Authorization": "Bearer " + api_key(values)}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body[:800]}
        message = parsed.get("message") or parsed.get("error") or parsed
        die(f"HTTP {exc.code} {path}: {message}")
    except urllib.error.URLError as exc:
        die(f"网络错误 {path}: {exc.reason}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        die(f"响应不是 JSON: {body[:400]}")


def probe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        return float(out.stdout.strip())
    except Exception:
        return None


def to_media_url(value, kind):
    """本地文件转 data URI；http(s) 直链原样返回。"""
    lowered = value.lower()
    if lowered.startswith(("http://", "https://", "data:")):
        return value
    path = Path(value).expanduser()
    if not path.exists():
        die(f"素材不存在：{value}")
    allowed = {
        "image": IMAGE_EXT | {".jpeg"},
        "video": VIDEO_EXT,
        "audio": AUDIO_EXT,
        "file": DOC_EXT,
        "link": set(),
    }.get(kind, set())
    if allowed and path.suffix.lower() not in allowed:
        die(f"素材后缀不支持：{path.name}（{kind} 允许 {sorted(allowed)}）")
    size = path.stat().st_size
    limits = {"image": 20 * 1024 * 1024, "video": 100 * 1024 * 1024,
              "audio": 15 * 1024 * 1024, "file": 100 * 1024 * 1024}
    if kind in limits and size > limits[kind]:
        die(f"素材过大：{path.name} {size/1048576:.1f}MB > {limits[kind]//1048576}MB")
    mime = mimetypes.guess_type(path.name)[0] or {
        "image": "image/png", "video": "video/mp4", "audio": "audio/mpeg",
        "file": "application/octet-stream",
    }.get(kind, "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_media(args):
    media = []
    if args.first_frame:
        media.append({"type": "first_frame", "url": to_media_url(args.first_frame, "image")})
    if args.last_frame:
        media.append({"type": "last_frame", "url": to_media_url(args.last_frame, "image")})
    for item in args.ref_image or []:
        media.append({"type": "reference_image", "url": to_media_url(item, "image")})
    for item in args.ref_video or []:
        media.append({"type": "reference_video", "url": to_media_url(item, "video")})
    for item in args.ref_audio or []:
        media.append({"type": "reference_audio", "url": to_media_url(item, "audio")})
    if args.ref_file:
        media.append({"type": "file", "url": to_media_url(args.ref_file, "file")})
    if args.ref_link:
        media.append({"type": "link", "url": args.ref_link})
    return media


def count_type(media, wanted):
    return sum(1 for item in media if item["type"] == wanted)


def validate(media, duration):
    has_frame = any(item["type"] in FRAME_TYPES for item in media)
    has_ref = any(item["type"] in REFERENCE_TYPES for item in media)
    if has_frame and has_ref:
        die("首帧/尾帧不能和 reference_* / file / link 混用，请二选一")
    if args_file_and_link(media):
        die("file 和 link 只能二选一")
    if count_type(media, "reference_image") > 10:
        die("reference_image 最多 10 张")
    if count_type(media, "reference_video") > 5:
        die("reference_video 最多 5 段")
    if count_type(media, "reference_audio") > 5:
        die("reference_audio 最多 5 段")
    if not 2 <= duration <= 30:
        die("duration 必须是 2-30 的整数秒")


def args_file_and_link(media):
    return count_type(media, "file") > 0 and count_type(media, "link") > 0


def submit(values, args, media):
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "duration": args.duration,
        "ratio": args.ratio,
    }
    parameters = {"audio": not args.no_audio}
    if args.seed is not None:
        parameters["seed"] = args.seed
    if args.no_prompt_extend:
        parameters["prompt_extend"] = False
    payload["metadata"] = {"parameters": parameters}
    if media:
        payload["metadata"]["media"] = media
        if len(media) == 1 and media[0]["type"] == "first_frame":
            payload["input_reference"] = media[0]["url"]
    return request(values, "POST", "/videos", payload)


def poll(values, task_id, interval, timeout):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        time.sleep(interval)
        last = request(values, "GET", "/videos/" + task_id, timeout=120)
        status = last.get("status")
        print(json.dumps({"status": status, "progress": last.get("progress")}),
              file=sys.stderr, flush=True)
        if status in ("completed", "failed"):
            return last
    die(f"轮询超时（{timeout}s），任务 {task_id} 仍为 {last.get('status') if last else 'unknown'}"
        f"，稍后可用 status 子命令继续查询")


def result_url(payload):
    meta = payload.get("metadata") or {}
    if isinstance(meta, dict):
        url = meta.get("url") or meta.get("video_url")
        if url:
            return url
    for key in ("url", "video_url", "output_url", "download_url", "result_url"):
        if payload.get(key):
            return payload[key]
    return None


def download(url, out_path):
    out = Path(out_path).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "tj-short/wan3"})
    with urllib.request.urlopen(req, timeout=600) as response, open(out, "wb") as handle:
        while True:
            chunk = response.read(1 << 20)
            if not chunk:
                break
            handle.write(chunk)
    return out


def media_summary(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries", "format=duration,size",
         "-of", "json", str(path)],
        capture_output=True, text=True, timeout=30,
    )
    try:
        data = json.loads(out.stdout or "{}")
        stream = (data.get("streams") or [{}])[0]
        fmt = data.get("format") or {}
        return {
            "width": stream.get("width"),
            "height": stream.get("height"),
            "duration_seconds": round(float(fmt.get("duration", 0)), 2) if fmt.get("duration") else None,
            "bytes": int(fmt["size"]) if fmt.get("size") else path.stat().st_size,
        }
    except Exception:
        return {"bytes": path.stat().st_size}


def cmd_video(values, args):
    args.model = args.model or values.get("SALPX_VIDEO_MODEL") or DEFAULT_MODEL
    if not str(args.model).startswith("wan3.0"):
        print(json.dumps({"warning": f"{args.model} 不是 wan3.0 系列，字段与 Wan 3.0 不同，"
                                     "本客户端只保证 wan3.0-* 可用"}, ensure_ascii=False),
              file=sys.stderr)
    media = build_media(args)
    validate(media, args.duration)
    price = PRICES.get(args.model)
    ref_videos = [p for p in (args.ref_video or []) if p]
    ref_seconds = 0
    for item in ref_videos:
        if not item.lower().startswith(("http://", "https://")):
            probed = probe_duration(Path(item).expanduser())
            if probed:
                ref_seconds += probed
    if ref_videos and ref_seconds and ref_seconds + args.duration > 30:
        die(f"带参考视频时 参考秒数({ref_seconds:.1f}s) + 出片秒数({args.duration}s) 必须 <= 30")
    estimate = None
    if price:
        estimate = round(price * (args.duration + ref_seconds), 2)
        print(
            json.dumps({
                "cost_notice": "即将提交付费任务",
                "model": args.model,
                "duration_seconds": args.duration,
                "reference_video_seconds": round(ref_seconds, 1),
                "estimated_cny": estimate,
                "note": "带参考视频时按 15s 上限预扣，完成后多退少补",
            }, ensure_ascii=False),
            file=sys.stderr, flush=True,
        )
    if args.dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "payload_media_types":
                          [item["type"] for item in media],
                          "estimated_cny": estimate}, ensure_ascii=False))
        return
    created = submit(values, args, media)
    task_id = created.get("id") or created.get("task_id")
    if not task_id:
        die(f"提交响应里没有任务 ID：{json.dumps(created, ensure_ascii=False)[:400]}")
    print(json.dumps({"ok": True, "task_id": task_id, "model": args.model,
                      "status": created.get("status"), "estimated_cny": estimate},
                     ensure_ascii=False))
    if not args.wait:
        print("提示：任务已提交，用 status / download 子命令继续。", file=sys.stderr)
        return
    final = poll(values, task_id, args.poll_interval, args.timeout)
    if final.get("status") != "completed":
        die(f"任务失败：{json.dumps(final.get('error') or final, ensure_ascii=False)[:600]}")
    url = result_url(final)
    if not url:
        die("任务已完成但没找到成片地址")
    if not args.out:
        print(json.dumps({"ok": True, "task_id": task_id, "url": url,
                          "warning": "成片链接 24 小时失效，请尽快下载"}, ensure_ascii=False))
        return
    out = download(url, args.out)
    info = media_summary(out)
    result = {
        "ok": True, "task_id": task_id, "model": args.model, "status": "completed",
        "output_path": str(out), "source_url": url,
        "requested_duration_seconds": args.duration,
        "duration_acceptance": "check" if info.get("duration_seconds") is None else
        ("pass" if abs((info.get("duration_seconds") or 0) - args.duration) <= 0.5 else "mismatch"),
        **info,
        "completed_at": final.get("completed_at"),
    }
    if args.result_json:
        Path(args.result_json).expanduser().write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


def cmd_status(values, args):
    payload = request(values, "GET", "/videos/" + args.task_id, timeout=120)
    url = result_url(payload)
    print(json.dumps({
        "ok": True, "task_id": args.task_id, "status": payload.get("status"),
        "progress": payload.get("progress"), "model": payload.get("model"),
        "url": url, "error": payload.get("error"),
    }, ensure_ascii=False))


def cmd_download(values, args):
    payload = request(values, "GET", "/videos/" + args.task_id, timeout=120)
    if payload.get("status") != "completed":
        die(f"任务未完成，当前状态：{payload.get('status')}")
    url = result_url(payload)
    if not url:
        die("找不到成片地址")
    out = download(url, args.out)
    print(json.dumps({"ok": True, "output_path": str(out), **media_summary(out)},
                     ensure_ascii=False))


def cmd_models(values, args):
    payload = request(values, "GET", "/models", timeout=120)
    rows = []
    for item in payload.get("data", []):
        model_id = item.get("id", "")
        if not model_id.startswith("wan3.0"):
            continue
        meta = item.get("salpx_metadata") or {}
        rows.append({
            "id": model_id,
            "cny_per_second": PRICES.get(model_id),
            "min_duration": meta.get("min_duration"),
            "max_duration": meta.get("max_duration"),
        })
    rows.sort(key=lambda row: (row["cny_per_second"] or 99))
    print(json.dumps({"ok": True, "count": len(rows), "models": rows},
                     ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="salpx Wan 3.0 video client (TJ Short)")
    parser.add_argument("--env", default=".env", help="项目 .env 路径（可选）")
    sub = parser.add_subparsers(dest="command", required=True)

    video = sub.add_parser("video", help="提交视频任务")
    video.add_argument("--model", default=None,
                       help=f"默认取 SALPX_VIDEO_MODEL，再回退 {DEFAULT_MODEL}")
    video.add_argument("--prompt", required=True)
    video.add_argument("--duration", type=int, required=True, help="2-30 整数秒")
    video.add_argument("--ratio", default="adaptive",
                       choices=["adaptive", "16:9", "9:16", "4:3", "3:4", "1:1", "21:9"])
    video.add_argument("--first-frame")
    video.add_argument("--last-frame")
    video.add_argument("--ref-image", action="append", help="参考图，最多 10 张，可重复")
    video.add_argument("--ref-video", action="append", help="参考视频，最多 5 段，可重复")
    video.add_argument("--ref-audio", action="append", help="参考音频，最多 5 段，可重复")
    video.add_argument("--ref-file", help="参考文档（pdf/docx/pptx/xlsx/txt/md）")
    video.add_argument("--ref-link", help="公开网页 URL")
    video.add_argument("--no-audio", action="store_true", help="关闭原生音频")
    video.add_argument("--no-prompt-extend", action="store_true")
    video.add_argument("--seed", type=int)
    video.add_argument("--wait", action="store_true", help="提交后轮询直到完成")
    video.add_argument("--poll-interval", type=int, default=15)
    video.add_argument("--timeout", type=int, default=1800)
    video.add_argument("--out", help="完成后下载到这里")
    video.add_argument("--result-json", help="把结果写进 JSON 文件")
    video.add_argument("--dry-run", action="store_true", help="只校验参数和报价，不提交")

    status = sub.add_parser("status", help="查询任务状态")
    status.add_argument("task_id")

    download_cmd = sub.add_parser("download", help="下载已完成任务的成片")
    download_cmd.add_argument("task_id")
    download_cmd.add_argument("--out", required=True)

    models = sub.add_parser("models", help="列出 wan3.0 系列模型与单价")
    models.set_defaults(_models=True)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    values = config(args.env)
    if args.command == "video":
        cmd_video(values, args)
    elif args.command == "status":
        cmd_status(values, args)
    elif args.command == "download":
        cmd_download(values, args)
    elif args.command == "models":
        cmd_models(values, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
