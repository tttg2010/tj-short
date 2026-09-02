#!/usr/bin/env python3
"""Public-safe MiniMax H3 video client for TJ Short."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - keeps --help usable before dependency install.
    requests = None  # type: ignore[assignment]


DEFAULT_BASE_URL = "https://h3.zhongbiao.cloud/api"


def load_env(path: str | None) -> None:
    if not path:
        return
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def base_url() -> str:
    return os.environ.get("H3_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def auth_headers(require_key: bool = True) -> dict[str, str]:
    key = os.environ.get("H3_API_KEY")
    if require_key and not key:
        raise SystemExit("H3_API_KEY is required in .env or environment")
    return {"Authorization": f"Bearer {key}"} if key else {}


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def require_requests():
    if requests is None:
        raise SystemExit("Missing dependency: requests. Install with: python3 -m pip install requests")
    return requests


def extract_job_id(data: dict[str, Any]) -> str | None:
    job = data.get("job")
    if isinstance(job, dict) and job.get("id"):
        return str(job["id"])
    for key in ("id", "jobId", "task_id", "taskId"):
        if data.get(key):
            return str(data[key])
    return None


def extract_status(data: dict[str, Any]) -> str | None:
    job = data.get("job")
    if isinstance(job, dict) and job.get("status"):
        return str(job["status"])
    if data.get("status"):
        return str(data["status"])
    return None


def cmd_capabilities(_: argparse.Namespace) -> None:
    http = require_requests()
    response = http.get(f"{base_url()}/videos/capabilities", headers=auth_headers(require_key=False), timeout=60)
    response.raise_for_status()
    print_json(response.json())


def cmd_quote(args: argparse.Namespace) -> None:
    http = require_requests()
    payload = {
        "resolution": args.resolution,
        "duration": args.duration,
        "count": args.count,
        "steps": args.steps,
    }
    response = http.post(f"{base_url()}/videos/quote", headers=auth_headers(), json=payload, timeout=60)
    response.raise_for_status()
    print_json(response.json())


def cmd_status(args: argparse.Namespace) -> dict[str, Any]:
    http = require_requests()
    response = http.get(f"{base_url()}/videos/{args.job_id}", headers=auth_headers(), timeout=60)
    response.raise_for_status()
    data = response.json()
    print_json(data)
    return data


def download_content(job_id: str, out_path: str) -> Path:
    http = require_requests()
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with http.get(f"{base_url()}/videos/{job_id}/content", headers=auth_headers(), stream=True, timeout=300) as response:
        response.raise_for_status()
        with target.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return target


def cmd_download(args: argparse.Namespace) -> None:
    target = download_content(args.job_id, args.out)
    print_json({"job_id": args.job_id, "output": str(target), "bytes": target.stat().st_size})


def wait_for_job(job_id: str, interval: int, timeout: int) -> dict[str, Any]:
    http = require_requests()
    deadline = time.time() + timeout
    last_data: dict[str, Any] = {}
    while time.time() < deadline:
        response = http.get(f"{base_url()}/videos/{job_id}", headers=auth_headers(), timeout=60)
        response.raise_for_status()
        last_data = response.json()
        status = extract_status(last_data)
        if status in {"succeeded", "failed", "timeout"}:
            return last_data
        time.sleep(interval)
    raise SystemExit(f"H3 job timed out locally after {timeout}s: {job_id}")


def cmd_video(args: argparse.Namespace) -> None:
    http = require_requests()
    if args.mode == "fl2va" and not args.start_frame:
        raise SystemExit("fl2va requires --start-frame")
    if args.end_frame and not args.start_frame:
        raise SystemExit("--end-frame cannot be used without --start-frame")

    form = {
        "prompt": args.prompt,
        "mode": args.mode,
        "resolution": args.resolution,
        "duration": str(args.duration),
        "steps": str(args.steps),
        "aspectRatio": args.aspect_ratio,
    }
    files: list[tuple[str, tuple[str, Any, str]]] = []
    handles = []
    try:
        for image_path in args.reference_image or []:
            path = Path(image_path)
            handle = path.open("rb")
            handles.append(handle)
            files.append(("referenceImages", (path.name, handle, "application/octet-stream")))
        for field_name, image_path in (("startFrame", args.start_frame), ("endFrame", args.end_frame)):
            if image_path:
                path = Path(image_path)
                handle = path.open("rb")
                handles.append(handle)
                files.append((field_name, (path.name, handle, "application/octet-stream")))

        headers = auth_headers()
        headers["Idempotency-Key"] = args.idempotency_key or str(uuid.uuid4())
        response = http.post(f"{base_url()}/videos", headers=headers, data=form, files=files, timeout=300)
        response.raise_for_status()
        data = response.json()
        print_json(data)
    finally:
        for handle in handles:
            handle.close()

    job_id = extract_job_id(data)
    if args.wait:
        if not job_id:
            raise SystemExit("No job id found in H3 response")
        final_data = wait_for_job(job_id, args.poll_interval, args.timeout)
        print_json(final_data)
        if extract_status(final_data) == "succeeded" and args.out:
            target = download_content(job_id, args.out)
            print_json({"job_id": job_id, "output": str(target), "bytes": target.stat().st_size})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MiniMax H3 video helper for TJ Short")
    parser.add_argument("--env", default=".env", help="Optional .env file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capabilities = subparsers.add_parser("capabilities", help="Query H3 capabilities")
    capabilities.set_defaults(func=cmd_capabilities)

    quote = subparsers.add_parser("quote", help="Quote an H3 job")
    quote.add_argument("--resolution", default="576P")
    quote.add_argument("--duration", type=int, default=5)
    quote.add_argument("--count", type=int, default=1)
    quote.add_argument("--steps", type=int, default=10)
    quote.set_defaults(func=cmd_quote)

    video = subparsers.add_parser("video", help="Submit an H3 video job")
    video.add_argument("--prompt", required=True)
    video.add_argument("--mode", choices=["t2va", "ref2va", "fl2va"], default="t2va")
    video.add_argument("--reference-image", action="append", help="Repeat for ref2va images")
    video.add_argument("--start-frame", help="First frame for fl2va")
    video.add_argument("--end-frame", help="Last frame for fl2va")
    video.add_argument("--resolution", default="576P")
    video.add_argument("--duration", type=int, default=5)
    video.add_argument("--steps", type=int, default=10)
    video.add_argument("--aspect-ratio", default="9:16")
    video.add_argument("--idempotency-key")
    video.add_argument("--wait", action="store_true")
    video.add_argument("--poll-interval", type=int, default=10)
    video.add_argument("--timeout", type=int, default=1800)
    video.add_argument("--out", help="Download mp4 here after --wait succeeds")
    video.set_defaults(func=cmd_video)

    status = subparsers.add_parser("status", help="Check H3 job status")
    status.add_argument("job_id")
    status.set_defaults(func=cmd_status)

    download = subparsers.add_parser("download", help="Download H3 job mp4")
    download.add_argument("job_id")
    download.add_argument("--out", required=True)
    download.set_defaults(func=cmd_download)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    load_env(args.env)
    args.func(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        if requests is None or not isinstance(exc, requests.HTTPError):
            raise
        body = exc.response.text[:1000] if exc.response is not None else ""
        print(f"HTTP error: {exc}\n{body}", file=sys.stderr)
        raise SystemExit(1)
