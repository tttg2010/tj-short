---
name: tj-short
description: Codex ecommerce short-drama skill v0.8.22. Use when the user wants to create product-selling short dramas, generate product-proof scripts, first frames, salpx video prompts, captions, manifests, delivery checklists, and Seedance2 visible-face repair inside Codex.
---

# TJ Short

TJ Short is a Codex Skill for ecommerce short dramas.

Version: `short-drama-ecommerce v0.8.22`

## v0.8.22 Changelog

- Added Seedance2 visible-face workflow for short-drama clips where actor expressions matter.
- Added `face_pencil`: stylize only face regions while preserving photographic body, wardrobe, action, pet, props, and scene.
- Added `blur_feature`: use a blurred-face main composition image plus a facial-feature sheet when `face_pencil` still fails.
- Clarified that faceless crops are not the default for dramatic scenes; preserve facial acting through virtual-character reference repair first.
- Clarified multi-model salpx support: `omni_flash`, Seedance 2.0 variants, Veo variants, and user-selected salpx models.
- Added AniShort-inspired subject-library method: role, scene, product/prop, and evidence libraries before shot prompts.

## Install Reload Rule

After installing or updating this skill, the user must restart Codex before testing the trigger phrase. Codex may keep an old skill cache until restart.

User-facing reminder, repeat exactly:

重新启动codex！
重新启动codex！
重新启动codex！

Then test with:

```text
短剧带货启动
```

Full video generation requires a salpx API key. Tell users to register at `https://www.salpx.com`, create or copy their API Key, and put it into local `.env` as `SALPX_API_KEY`. Without a salpx API key, Codex can still generate scripts, storyboards, first frames, prompts, and manifests, but it cannot complete salpx video submission from Codex.

## Startup Gate Rule

When the user says `短剧带货启动`, do not immediately generate a full script, a video package, a generic workplace story, a fashion story, or a made-up sample project.

The first response must start the diagnostic flow:

1. Ask for or inspect the product image/material.
2. If no product is provided, ask the user for product information before writing any story.
3. Remind the user that full salpx video submission requires registration at `https://www.salpx.com` and a local `SALPX_API_KEY`.
4. Produce only a short product diagnosis and three selectable briefs.
5. Wait for the user to choose A, B, or C before writing the product proof bible, episode script, storyboard, first frames, or salpx prompts.

If the user says "generate video" before product diagnosis is complete, still follow the gate: product diagnosis -> three briefs -> user chooses A/B/C -> then production.

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
- runs `omni_flash`, Seedance 2.0 variants, Veo variants, or another selected video model
- returns image-to-video clips for review and post-production

## Trigger

Use this skill when the user says:

- 短剧带货
- ecommerce short drama
- product short drama
- 用 Codex 生成短剧带货
- salpx / omni_flash 图生视频
- salpx / seedance-2 / veo 图生视频
- 产品图生成短剧脚本、首帧、提示词、字幕或投放切片

## Core Rule

Do not make the product the hero.

The story must first make the audience care about a person, pet, relationship, or consequence. The product enters later as evidence, a record, a memory object, a relationship token, or a turning point.

## Subject Library Rule

Use a subject-library workflow before writing image or video prompts.

Do not let every shot reinvent the same people, rooms, products, and proof objects. Build reusable subjects first, then make each shot prompt reference those subjects and focus only on action, emotion, camera, dialogue, and continuity.

Required libraries:

1. Role library: each recurring person or pet gets one stable identity entry with age range, identity, face/fur traits, hair, wardrobe, expression baseline, relationship power, and product-contact behavior.
2. Scene library: each recurring location gets one stable entry with layout, lighting, time of day, mood, camera-friendly anchors, and safety notes.
3. Product/prop library: product pack, bowl, phone, receipt, report, accessory, package, or tool entries with shape, color, label visibility, handling rule, and what must not change.
4. Evidence library: ecommerce-specific proof objects such as feeding action, before/after behavior, order record, vet-style note, ingredient card, comparison table, phone chat, or packaging detail. Each evidence item must say what misunderstanding it proves or overturns.
5. Shot production table: each shot references subject IDs instead of repeating long descriptions.

Shot prompts must be short and production-focused:

```text
shot_id:
subjects:
scene:
evidence_or_prop:
narrative_job:
action:
emotion_shift:
camera:
dialogue_or_lip_sync:
continuity_locks:
must_not_change:
```

For video prompts, write only what is missing from the first frame: action, camera motion, emotion change, dialogue/lip-sync target, timing, and what must remain unchanged. Do not restate the entire character face, wardrobe, product design, or scene if those are already controlled by subject libraries and first frames.

## Default Flow

1. Analyze the product asset or product name.
2. Produce three ecommerce short-drama briefs.
3. Let the user choose one brief.
4. Create the product proof bible.
5. Build four subject libraries: role, scene, product/prop, and evidence.
6. Write one high-conflict episode.
7. Create a 12-shot production table that references subject IDs.
8. Generate or request three first frames: hook, product evidence, ending hook.
9. Write clip contracts and reference role maps.
10. Write `salpx / omni_flash` prompts with fixed `duration=10`.
11. Prepare captions, manifest, and delivery checklist.

## Video Model Rules

`salpx / omni_flash` is fixed at 10 seconds per raw clip.

Never write 5-second, 6-second, or 8-second submission durations for Omni. Fast pacing is done in post-production by cutting the 10-second raw clip.

Seedance 2.0 and Veo model durations depend on the selected model and provider route. Do not assume Omni's fixed 10-second rule applies to non-Omni models.

## Seedance2 Visible-Face Rule

When Seedance2 clips need visible actor faces, do not default to faceless crops. Short drama depends on facial acting.

Use this escalation path:

1. Start with a clean fictional virtual-actor first frame.
2. If a realistic face is rejected as possible real-person content, use `face_pencil`: apply colored-pencil or sketch treatment only to face regions while keeping body, wardrobe, action, and scene photographic.
3. If `face_pencil` still fails, use `blur_feature`: blur the face regions in the main composition image and provide a separate facial-feature sheet as an additional reference.
4. Prompt the model that the main frame controls composition/body/wardrobe/action and the feature sheet controls fictional facial features.

Do not use this process for unlicensed real people, celebrities, influencers, public figures, or attempts to bypass identity review. It is only for self-owned fictional virtual characters.

## Required Deliverables

- Product proof bible
- Role subject library
- Scene subject library
- Product/prop subject library
- Evidence subject library
- Three briefs
- High-conflict episode script
- 12-shot production table
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
