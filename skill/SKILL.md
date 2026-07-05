---
name: tj-short
description: Codex ecommerce short-drama skill. Use when the user wants to create product-selling short dramas, generate product-proof scripts, first frames, salpx / omni_flash prompts, captions, manifests, and delivery checklists inside Codex.
---

# TJ Short

TJ Short is a Codex Skill for ecommerce short dramas.

Codex is the production brain:

- analyzes product assets
- writes product-proof briefs
- creates scripts and storyboards
- generates first-frame directions
- writes `salpx / omni_flash` prompts
- builds caption and delivery plans
- checks privacy before publishing

salpx is the video execution relay:

- receives clean 9:16 first frames
- runs `omni_flash`
- returns fixed 10-second image-to-video clips

## Trigger

Use this skill when the user says:

- 短剧带货
- ecommerce short drama
- product short drama
- 用 Codex 生成短剧带货
- salpx / omni_flash 图生视频
- 产品图生成短剧脚本、首帧、提示词、字幕或投放切片

## Core Rule

Do not make the product the hero.

The story must first make the audience care about a person, pet, relationship, or consequence. The product enters later as evidence, a record, a memory object, a relationship token, or a turning point.

## Default Flow

1. Analyze the product asset or product name.
2. Produce three ecommerce short-drama briefs.
3. Let the user choose one brief.
4. Create the product proof bible.
5. Write one high-conflict episode.
6. Create a 12-shot storyboard.
7. Generate or request three first frames: hook, product evidence, ending hook.
8. Write clip contracts and reference role maps.
9. Write `salpx / omni_flash` prompts with fixed `duration=10`.
10. Prepare captions, manifest, and delivery checklist.

## salpx / omni_flash Rule

`salpx / omni_flash` is fixed at 10 seconds per raw clip.

Never write 5-second, 6-second, or 8-second submission durations for Omni. Fast pacing is done in post-production by cutting the 10-second raw clip.

## Required Deliverables

- Product proof bible
- Three briefs
- High-conflict episode script
- 12-shot storyboard
- Three first-frame prompts or images
- Clip contracts
- Reference role map
- `salpx / omni_flash` prompt pack
- Generation manifest
- Voiceover and caption list
- Caption plan
- Release checklist

## Safety

Never expose or commit:

- API keys
- `.env`
- task IDs
- signed download URLs
- private product assets
- local absolute paths
- raw API responses

