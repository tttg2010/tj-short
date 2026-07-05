#!/usr/bin/env python3
"""Minimal public-safe salpx / omni_flash image-to-video helper.

This script intentionally reads secrets only from environment variables.
Do not hardcode keys. Do not commit .env files.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import time
from pathlib import Path

import requests


URL_RE = re.compile(r"https?://[^\s\"\\]+(?:\.mp4|\.mov|\.webm|\.m3u8)(?:\?[^\s\"\\]*)?")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


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
        if isinstance(value, list):
            for child in value:
                found = walk(child)
                if found:
                    return found
        return None

    found = walk(obj)
    if found:
        return found
    match = URL_RE.search(json.dumps(obj, ensure_ascii=False))
    return match.group(0) if match else None


def task_id_from(obj):
    if not isinstance(obj, dict):
        return None
    for key in ("task_id", "id", "video_id"):
        value = obj.get(key)
        if isinstance(value, str):
            return value
    data = obj.get("data")
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        return task_id_from(data)
    return None


def poll(base_url: str, headers: dict, task_id: str, timeout: int):
    deadline = time.time() + timeout
    endpoints = (
        f"{base_url}/videos/{task_id}",
        f"{base_url}/videos/{task_id}/result",
        f"{base_url}/videos/generations/{task_id}",
    )
    last = {}
    while time.time() < deadline:
        time.sleep(5)
        for endpoint in endpoints:
            response = requests.get(endpoint, headers=headers, timeout=60)
            try:
                data = response.json()
            except Exception:
                data = {"status_code": response.status_code, "text": response.text[:300]}
            last = data
            if response.status_code != 200:
                continue
            status = str(data.get("status", "")).lower()
            if status in {"failed", "error", "cancelled", "canceled"}:
                return None, data
            url = find_video_url(data)
            if url:
                return url, data
            break
    return None, last


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=".env", help="Optional local env file, not committed")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--first-frame", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--size", default="480x854")
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    load_env_file(Path(args.env))
    key = os.environ.get("SALPX_API_KEY")
    if not key:
        raise SystemExit("SALPX_API_KEY is required")

    base_url = (args.base_url or os.environ.get("SALPX_BASE_URL") or "https://www.salpx.com/v1").rstrip("/")
    model = args.model or os.environ.get("SALPX_OMNI_MODEL") or "omni_flash"
    frame = Path(args.first_frame)
    prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    output = Path(args.output)

    body = {
        "model": model,
        "prompt": prompt,
        "image": image_data_uri(frame),
        "aspect_ratio": "9:16",
        "size": args.size,
        "duration": 10,
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    response = requests.post(f"{base_url}/videos", headers=headers, json=body, timeout=600)
    try:
        data = response.json()
    except Exception:
        data = {"status_code": response.status_code, "text": response.text[:500]}

    if response.status_code != 200:
        raise SystemExit(json.dumps({"ok": False, "status": response.status_code, "response": data}, ensure_ascii=False))

    url = find_video_url(data)
    task_id = task_id_from(data)
    if not url and task_id:
        url, data = poll(base_url, headers, task_id, args.timeout)
    if not url:
        raise SystemExit(json.dumps({"ok": False, "task_id": task_id, "response": data}, ensure_ascii=False))

    output.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=300) as download:
        download.raise_for_status()
        with output.open("wb") as file:
            for chunk in download.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    print(json.dumps({"ok": True, "model": model, "duration": 10, "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

