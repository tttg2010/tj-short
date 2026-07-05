# salpx / omni_flash Fixed 10-Second Template

Use this template for each raw clip.

```text
10-second vertical 9:16 image-to-video from the provided first frame.
Shot: <SHOT_ID>, script time: <SCRIPT_TIMECODE>.
Preserve the first frame exactly: <composition locks>.

Only the following action changes happen:
0-3s: <action beat 1>.
3-6s: <action beat 2>.
6-10s: <action beat 3>.

Exact Chinese dialogue/audio only:
<speaker> says "<line>"
<speaker> says "<line>"

Speaker lock:
<speaker rules>
Lip-sync target: only the current speaker's mouth moves during their own line.
Listener rule: non-speaking characters keep lips closed and react only with eyes, hands, or posture.

Narrative boundary:
This clip only <single narrative job>.
Do not show <reserved for later>.

No burned-in subtitles, no captions, no title cards, no speech bubbles, no panel numbers, no watermark, no readable long text in the video.
Do not invent any other dialogue.
Do not create picture-in-picture, inset frames, white borders, collage panels, blurred background extension, or a small vertical image floating over a blurred copy.
```

## Request Body Shape

```json
{
  "model": "omni_flash",
  "prompt": "<prompt>",
  "image": "<data:image/png;base64,...>",
  "aspect_ratio": "9:16",
  "size": "480x854",
  "duration": 10
}
```

## Notes

- `duration` stays `10`.
- Faster pacing is done in editing.
- Raw clips from Omni should not contain subtitles.
- Final subtitles are added in post-production.

