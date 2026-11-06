#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""salpx image client for TJ Short (gpt-image-2).

图片只走 https://www.salpx.com/v1/images/generations。
视频不走这里 —— 用同目录的 `wan3_video_client.py`（salpx Wan 3.0）。
"""

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

DEFAULT_BASE_URL = "https://www.salpx.com/v1"
CRED_FILE = os.path.expanduser("~/.config/salpx/credentials.env")


def normalize_base_url(url: str) -> str:
    url = (url or DEFAULT_BASE_URL).rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    if "zhongbiao" in url or "h3." in url:
        raise SystemExit(f"拒绝使用已废弃的端点：{url}。只允许 https://www.salpx.com/v1")
    return url


def read_env_file(path: Optional[Path]) -> dict:
    values = {}
    if not path or not Path(path).exists():
        return values
    for line in Path(path).read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and val:
            values[key] = val
    return values


def load_env_file(path: Optional[Path]) -> None:
    """优先级：真实环境变量 > --env 文件 > ~/.config/salpx/credentials.env"""
    preexisting = dict(os.environ)
    merged = read_env_file(CRED_FILE)
    merged.update(read_env_file(path))   # 项目 .env 覆盖本机凭证文件
    merged.update(preexisting)           # 真实环境变量最高优先
    for key, val in merged.items():
        os.environ.setdefault(key, val)
        if key in preexisting:
            os.environ[key] = preexisting[key]


def require_requests():
    if requests is None:
        raise SystemExit("缺少依赖 requests。用托管 venv 运行："
                         "/Users/zhang/.workbuddy/binaries/python/envs/default/bin/python")
    return requests


def headers() -> dict:
    key = os.environ.get("SALPX_API_KEY")
    if not key:
        raise SystemExit("SALPX_API_KEY is required")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def save_url(url: str, out_path: Path) -> None:
    http = require_requests()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with http.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with out_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)


def extension_from_url(url: str, fallback: str) -> str:
    suffix = Path(urlparse(url).path).suffix
    return suffix if suffix else fallback


def generate_image(args):
    http = require_requests()
    base_url = normalize_base_url(os.environ.get("SALPX_BASE_URL", DEFAULT_BASE_URL))
    model = args.model or os.environ.get("SALPX_IMAGE_MODEL", "gpt-image-2")
    body = {"model": model, "prompt": args.prompt, "size": args.size, "n": args.n}
    if args.reference:
        body["image"] = data_uri(Path(args.reference))
    response = http.post(f"{base_url}/images/generations", headers=headers(), json=body, timeout=600)
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

    result = {
        "ok": bool(outputs),
        "model": model,
        "size": args.size,
        "outputs": outputs,
        "usage": data.get("usage"),
    }
    result_path = out_dir / f"{args.name}_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": result["ok"], "model": model,
                      "outputs": outputs, "result_path": str(result_path)},
                     ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="salpx image client (gpt-image-2) for TJ Short. "
                    "Video: use wan3_video_client.py instead.")
    parser.add_argument("--env", default=".env", help="optional project .env path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    image = sub.add_parser("image")
    image.add_argument("--prompt", required=True)
    image.add_argument("--out-dir", required=True)
    image.add_argument("--name", default="image")
    image.add_argument("--model")
    image.add_argument("--size", default="1024x1792")
    image.add_argument("--n", type=int, default=1)
    image.add_argument("--reference", help="可选：参考图路径（图生图）")

    video = sub.add_parser("video", help="已废弃：视频改用 wan3_video_client.py")

    args = parser.parse_args()
    load_env_file(Path(args.env) if args.env else None)
    if args.cmd == "image":
        generate_image(args)
    else:
        raise SystemExit(
            "本脚本只负责生图。视频请用：\n"
            "  scripts/wan3_video_client.py video --model wan3.0-720p --prompt '...' --duration 8 --ratio 9:16"
        )


if __name__ == "__main__":
    main()
