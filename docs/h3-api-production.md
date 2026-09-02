# MiniMax H3 API Production Route

Goal: use salpx for storyboard grids and first-frame images, then use MiniMax H3 for video generation.

This is the current recommended TJ Short production split:

```text
Codex -> script / shot table / SOURCE ANCHOR / prompt / manifest
salpx -> gpt-image-2 storyboard grid and 9:16 first frames
MiniMax H3 -> final raw video clips
Codex -> review, captions, delivery checklist, ad cutdowns
```

Keep real H3 keys in `.env`, shell environment, or CI secrets only. Do not commit keys, task IDs from private jobs, signed URLs, private product images, or raw API responses.

## Environment

```env
H3_API_KEY=
H3_BASE_URL=https://h3.zhongbiao.cloud/api
H3_VIDEO_RESOLUTION=576P
H3_VIDEO_DURATION=5
H3_VIDEO_STEPS=10
H3_VIDEO_ASPECT_RATIO=9:16
```

H3 uses Bearer authentication:

```bash
Authorization: Bearer $H3_API_KEY
```

## Capabilities

```bash
python3 scripts/h3_video_client.py --env .env capabilities
```

Direct API shape:

```bash
curl https://h3.zhongbiao.cloud/api/videos/capabilities
```

Use this before production to confirm the currently supported resolutions, durations, modes, and pricing version.

## Quote

```bash
python3 scripts/h3_video_client.py --env .env quote \
  --resolution 576P \
  --duration 5 \
  --count 1 \
  --steps 10
```

Common TJ Short defaults:

| Field | Default |
|---|---|
| `resolution` | `576P` |
| `duration` | `5` |
| `steps` | `10` |
| `aspectRatio` | `9:16` |
| `mode` | `t2va`, `ref2va`, or `fl2va` |

## Text-to-Video

Use `t2va` for a shot that does not need a first frame or product reference:

```bash
python3 scripts/h3_video_client.py --env .env video \
  --mode t2va \
  --prompt "5-second vertical 9:16 realistic TikTok drama clip, warm home kitchen, restrained family emotion, no subtitles, no medical claims." \
  --resolution 576P \
  --duration 5 \
  --steps 10 \
  --aspect-ratio 9:16 \
  --wait \
  --out outputs/videos/ep01-shot01-h3.mp4
```

## Reference-to-Video

Use `ref2va` when the product image or first-frame image should guide product appearance, scene, wardrobe, or character consistency.

```bash
python3 scripts/h3_video_client.py --env .env video \
  --mode ref2va \
  --reference-image first_frames/EP01-03.png \
  --prompt "Use the reference image as the opening composition and product appearance. 5-second vertical 9:16 US TikTok Shop short-drama clip. Natural handheld kitchen moment, no subtitles, no logos, no medical promises." \
  --resolution 576P \
  --duration 5 \
  --steps 10 \
  --aspect-ratio 9:16 \
  --wait \
  --out outputs/videos/ep01-shot03-h3.mp4
```

H3 reference limits from the project guide:

| Asset | Limit |
|---|---|
| `referenceImages` | up to 9 images |
| `referenceVideos` | up to 1 video, max 15 seconds |
| `referenceAudios` | up to 3 audios |

Keep reference assets small enough to avoid upload errors.

## First/Last-Frame Video

Use `fl2va` when the clip must start and/or end on specific frames:

```bash
python3 scripts/h3_video_client.py --env .env video \
  --mode fl2va \
  --start-frame first_frames/EP01-03.png \
  --end-frame first_frames/EP01-04.png \
  --prompt "Animate naturally from the first frame and finish on the last frame. No subtitles, no watermarks, no extra props." \
  --resolution 576P \
  --duration 5 \
  --steps 10 \
  --aspect-ratio 9:16 \
  --wait \
  --out outputs/videos/ep01-shot03-to-04-h3.mp4
```

Rules:

- `endFrame` cannot be used without `startFrame`.
- First and last frames should match the target aspect ratio.
- Do not combine `startFrame`/`endFrame` with unrelated reference images unless the current H3 capability check explicitly supports that route.
- A formal TJ Short first frame must be a clean full-screen 9:16 image: no inset frame, white border, screenshot border, burned-in subtitles, or blurred background padding.

## Status and Download

```bash
python3 scripts/h3_video_client.py --env .env status JOB_ID
python3 scripts/h3_video_client.py --env .env download JOB_ID --out outputs/videos/shot.mp4
```

Direct API shape:

```bash
curl https://h3.zhongbiao.cloud/api/videos/JOB_ID \
  -H "Authorization: Bearer $H3_API_KEY"

curl https://h3.zhongbiao.cloud/api/videos/JOB_ID/content \
  -H "Authorization: Bearer $H3_API_KEY" \
  -o h3-video.mp4
```

## Review

After download, inspect actual media properties:

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=width,height,codec_type \
  -of json outputs/videos/shot.mp4
```

Record these fields in `generation_manifest.csv`:

```text
video_model: minimax_h3
h3_mode: t2va | ref2va | fl2va
h3_job_id: private, do not publish in public examples
resolution:
duration:
steps:
aspect_ratio:
first_frame_path:
output_path:
downloaded_bytes:
actual_duration:
actual_width:
actual_height:
containment_diff:
locale_mismatch_status:
```

For US-market projects, keep the US locale lock through H3 prompts: American English dialogue/captions, US scenes, US CTA wording, and no Chinese ecommerce jargon unless the story explicitly uses a Chinese-diaspora setting.
