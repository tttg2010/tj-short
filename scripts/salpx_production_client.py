#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import re
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests


DEFAULT_BASE_URL = "https://www.salpx.com/v1"
VIDEO_URL_RE = re.compile(r"https?://[^\s\"\\]+(?:\.mp4|\.mov|\.webm|\.m3u8)(?:\?[^\s\"\\]*)?")


def normalize_base_url(url: str) -> str:
    url = (url or DEFAULT_BASE_URL).rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    return url


def load_env_file(path: Optional[Path]) -> None:
    if not path or not path.exists():
        return
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and val and key not in os.environ:
            os.environ[key] = val


def headers() -> dict:
    key = os.environ.get("SALPX_API_KEY")
    if not key:
        raise SystemExit("SALPX_API_KEY is required")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def save_url(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with out_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)


def extension_from_url(url: str, fallback: str) -> str:
    suffix = Path(urlparse(url).path).suffix
    return suffix if suffix else fallback


def find_video_url(obj):
    def walk(value):
        if isinstance(value, dict):
            for key in ("url", "video_url", "videoUrl", "download_url", "output_url", "result_url"):
                candidate = value.get(key)
                if isinstance(candidate, str) and candidate.startswith("http"):
                    return candidate
            for child in value.values():
                found = walk(child)
                if found:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found:
                    return found
        return None

    found = walk(obj)
    if found:
        return found
    match = VIDEO_URL_RE.search(json.dumps(obj, ensure_ascii=False))
    return match.group(0) if match else None


def get_task_id(obj):
    if not isinstance(obj, dict):
        return None
    for key in ("task_id", "id", "video_id"):
        if isinstance(obj.get(key), str):
            return obj[key]
    data = obj.get("data")
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in ("task_id", "id", "video_id"):
            if isinstance(data.get(key), str):
                return data[key]
    return None


def poll_video(base_url: str, task_id: str, timeout_s: int = 900):
    deadline = time.time() + timeout_s
    endpoints = (
        f"{base_url}/videos/{task_id}",
        f"{base_url}/videos/{task_id}/result",
        f"{base_url}/videos/generations/{task_id}",
    )
    last = {}
    while time.time() < deadline:
        time.sleep(5)
        for url in endpoints:
            try:
                response = requests.get(url, headers=headers(), timeout=60)
                try:
                    data = response.json()
                except Exception:
                    data = {"status_code": response.status_code, "text": response.text[:1000], "endpoint": url}
                last = data if isinstance(data, dict) else {"data": data}
                if response.status_code != 200:
                    continue
                status = str(last.get("status", "")).lower()
                if status in {"failed", "error", "cancelled", "canceled"}:
                    return None, last
                video_url = find_video_url(last)
                if video_url:
                    return video_url, last
                break
            except Exception as exc:
                last = {"error": str(exc), "endpoint": url}
    return None, last


def generate_image(args):
    base_url = normalize_base_url(os.environ.get("SALPX_BASE_URL", DEFAULT_BASE_URL))
    model = args.model or os.environ.get("SALPX_IMAGE_MODEL", "gpt-image-2")
    body = {"model": model, "prompt": args.prompt, "size": args.size, "n": args.n}
    response = requests.post(f"{base_url}/images/generations", headers=headers(), json=body, timeout=600)
    try:
        data = response.json()
    except Exception:
        data = {"status_code": response.status_code, "text": response.text[:2000]}
    if response.status_code != 200:
        raise SystemExit(json.dumps(data, ensure_ascii=False, indent=2))

    outputs = []
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for idx, item in enumerate(data.get("data", []), 1):
        if "b64_json" in item:
            out_path = out_dir / f"{args.name}_{idx:02d}.png"
            out_path.write_bytes(base64.b64decode(item["b64_json"]))
        elif "url" in item:
            ext = extension_from_url(item["url"], ".png")
            out_path = out_dir / f"{args.name}_{idx:02d}{ext}"
            save_url(item["url"], out_path)
        else:
            continue
        outputs.append(str(out_path))

    result = {"ok": bool(outputs), "model": model, "outputs": outputs, "raw_response": data}
    result_path = out_dir / f"{args.name}_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": result["ok"], "model": model, "outputs": outputs, "result_path": str(result_path)}, ensure_ascii=False))


def generate_video(args):
    base_url = normalize_base_url(os.environ.get("SALPX_BASE_URL", DEFAULT_BASE_URL))
    model = args.model or os.environ.get("SALPX_VIDEO_MODEL", "omni_flash")
    body = {
        "model": model,
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "size": args.size,
        "duration": args.duration,
    }
    if args.image:
        body["image"] = data_uri(Path(args.image))

    started = time.time()
    response = requests.post(f"{base_url}/videos", headers=headers(), json=body, timeout=600)
    try:
        data = response.json()
    except Exception:
        data = {"status_code": response.status_code, "text": response.text[:2000]}
    result = {
        "ok": False,
        "model": model,
        "generation_mode": "image_to_video" if args.image else "text_to_video",
        "requested_duration_seconds": args.duration,
        "post_status": response.status_code,
        "post_response": data,
    }
    if response.status_code != 200:
        write_video_result(args, result)
        raise SystemExit(1)

    video_url = find_video_url(data)
    task_id = get_task_id(data)
    result["task_id"] = task_id
    if not video_url and task_id:
        video_url, poll_data = poll_video(base_url, task_id, args.timeout)
        result["poll_response"] = poll_data
    if not video_url:
        result["error"] = "No video URL returned"
        write_video_result(args, result)
        raise SystemExit(1)

    out_path = Path(args.out)
    save_url(video_url, out_path)
    result.update(
        {
            "ok": out_path.exists() and out_path.stat().st_size > 1000,
            "video_url": video_url,
            "output_path": str(out_path),
            "bytes": out_path.stat().st_size if out_path.exists() else 0,
            "elapsed_seconds": round(time.time() - started, 1),
        }
    )
    write_video_result(args, result)
    print(json.dumps({"ok": result["ok"], "model": model, "task_id": task_id, "output_path": str(out_path)}, ensure_ascii=False))


def write_video_result(args, result: dict):
    result_path = Path(args.result_json) if args.result_json else Path(args.out).with_suffix(".json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="salpx production client for short-drama ecommerce")
    parser.add_argument("--env", default=".env", help="optional .env path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    image = sub.add_parser("image")
    image.add_argument("--prompt", required=True)
    image.add_argument("--out-dir", required=True)
    image.add_argument("--name", default="image")
    image.add_argument("--model")
    image.add_argument("--size", default="1024x1792")
    image.add_argument("--n", type=int, default=1)

    video = sub.add_parser("video")
    video.add_argument("--prompt", required=True)
    video.add_argument("--out", required=True)
    video.add_argument("--image")
    video.add_argument("--model")
    video.add_argument("--aspect-ratio", default="9:16")
    video.add_argument("--size", default="720x1280")
    video.add_argument("--duration", type=int, default=10)
    video.add_argument("--timeout", type=int, default=900)
    video.add_argument("--result-json")

    args = parser.parse_args()
    load_env_file(Path(args.env) if args.env else None)
    if args.cmd == "image":
        generate_image(args)
    elif args.cmd == "video":
        generate_video(args)


if __name__ == "__main__":
    main()
