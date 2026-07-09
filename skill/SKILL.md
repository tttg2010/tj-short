---
name: tj-short
description: Codex ecommerce short-drama skill v0.8.29. Use when the user wants to create product-selling short dramas, generate product-proof scripts, subject libraries, character dossier boards, filed role assets, Seedance2 production references, storyboard grids, first frames, salpx gpt-image-2 images, salpx video prompts, captions, manifests, delivery checklists, cinematic shot design, and Seedance2 visible-face repair inside Codex.
---

# TJ Short

TJ Short is a Codex Skill for ecommerce short dramas.

Version: `short-drama-ecommerce v0.8.29`

## v0.8.29 Changelog

- Added `Cinematic Shot-Design Rule`: seven shot-design elements (frame size, angle, composition, lighting, color grade, camera movement, pacing) and four reusable scene formulas (emotional build-up, suspense, romance, pressure) to fill the `camera:` and `emotion_shift:` fields of the shot production table.
- Added `Camera-as-Witness Prompt Law`: three rules for writing realistic AI-video prompts — describe the shooting process/imperfection instead of the finished picture, pair every "has" list with a "has not" exclusion list, and make each timeline segment carry camera behavior, not only character action.
- Added the six-block director-level prompt formula: 镜头语言 + 光影色彩 + 场景细节 + 角色表演 + 情绪风格 + 技术参数.
- Added a PPT-look precheck: every shot needs foreground/midground/background layering, and frame size must vary across the 12-shot sequence instead of holding one medium shot throughout.
- Clarified that handheld-imperfection language (Rule 1) is a selective realism layer, not a blanket rule, and must not be applied to official Seedance2 face-compliance candidates (`face_pencil_strong/medium`, `blur_feature`).
- Source: distilled from a shared cinematography/prompt-engineering note on AI short-drama shot design (七要素/四公式/摄影机行为日志三铁律), adapted to fit TJ Short's existing subject-library and Seedance2 rules rather than adopted verbatim.

## v0.8.28 Changelog

- Added grid-first cost-control rule: generate one 4x3 storyboard/first-frame contact sheet first, then auto-cut 12 independent 9:16 frames.
- Prohibited generating 12 independent first frames upfront unless the user explicitly requests it or the grid/cut workflow fails.
- Clarified that independent first-frame generation is only for failed grid cells, selected retakes, or 3-shot trial clips after the grid is reviewed.
- Updated the default flow from "generate three first frames" to "generate 12-panel grid -> cut -> precheck -> retake selected cells".

## v0.8.27 Changelog

- Clarified the difference between API smoke tests and production Seedance2 visible-face workflow.
- Added hard rule: a no-person/product-only first frame may be used only to isolate salpx API availability, never as the default replacement for a short-drama acting shot.
- Added required Seedance2 visible-face candidate set from the grid/first-frame stage: `face_pencil_strong`, `face_pencil_medium`, and `blur_feature` (`blurred_main + facial_feature_sheet`).
- Added precheck workflow: test candidates one by one; record pass/fail and reason; among passing candidates choose the one with the most complete face, expression, lip-shape, and acting information.
- Repeated that failed images are not retried unchanged, and full manga/anime/storyboard style remains preview-only, not an official first frame.

## v0.8.26 Changelog

- Added `docs/salpx-api-production.md`: a production-ready salpx API guide for `gpt-image-2` image generation and `omni_flash`, `gemini_omni_flash`, `seedance-2-mini-480p`, and Veo video generation.
- Added `scripts/salpx_production_client.py`: a reusable public-safe client with `image` and `video` commands, base64 first-frame upload, async polling, video download, and result JSON output.
- Added environment variables `SALPX_IMAGE_MODEL` and `SALPX_VIDEO_MODEL`, while keeping `SALPX_OMNI_MODEL` for backwards compatibility with the old omni sample script.
- Added model-name mapping: `seedance2-mini-480p` in user language maps to API model `seedance-2-mini-480p`; `omni` maps to `omni_flash`; Veo model IDs must come from the salpx console and be recorded in the manifest.
- Added distribution rule: public TJ Short releases must include working salpx production docs and scripts, not only prompts.
- Added privacy rule: real salpx API keys stay in `.env` or runtime secrets only, never in skill files, prompts, manifests, docs, or chat output.

## v0.8.25 Changelog

- Added official Seedance2 prompt lessons from Volcengine docs.
- Clarified that `Asset ID` belongs in the request URL such as `asset://...`, while prompts must still refer to `图片1`, `视频1`, or `音频1` by content order.
- Reframed character dossier boards as planning, filing, and extraction masters, not always the best direct Seedance2 video reference.
- Added production rule: use dossier boards to create clean single-person references, then submit face close-up + full-body/wardrobe reference + scene/shot/audio references for Seedance2.
- Added prompt rules for subject labels, time-sequenced shots, restrained motion, one camera move per shot, no subtitles/logos/watermarks, and model duration/ratio handling.
- Added model routing rule: do not write one generic video prompt for Omni, Seedance2, and Veo. Choose model-specific prompt shape, duration, references, and review strategy.
- Added hard gate: Seedance2 visible-human projects must create role dossier board deliverables before first-frame grids or video prompts.
- Added strict phase gate: startup, brief selection, project-file generation, dossier creation, storyboard, first-frame grid, and video prompt/submission must not collapse into one chat response.
- Added user-facing prefix rule: TJ Short recommendations, status reports, and next-step suggestions should start with `短剧带货：`.
- Added Seedance2 first-frame compliance rule: use local face-only `face_pencil` from grid/first-frame production; do not downgrade the whole frame to manga/anime/commercial storyboard style.

## v0.8.24 Changelog

- Added Seedance2 role-filing asset chain learned from AniShort-style filed character boards.
- Treat human/realistic role filing as a server-side asset status, not as a watermark or a prompt phrase.
- When a provider supports filing, register the approved character dossier board first, record the returned filed asset ID, and use that platform-scoped asset in Seedance2 generation.
- Clarified that downloaded and re-uploaded images may lose filing status; keep the original filed asset reference.
- Added manifest fields for `filed_asset_id`, `filing_status`, `filing_scope`, `role_board_version`, and `source_asset_url`.

## v0.8.23 Changelog

- Added character dossier board workflow for role subjects.
- Role subject images should be reference boards, not only single cinematic portraits.
- A character dossier board should include main portrait, front/side/back full-body views, expression sheet, wardrobe/product-contact details, and a concise info panel.
- Shot prompts should reference the approved role dossier board and avoid re-describing the full face, wardrobe, and product-contact setup in every shot.

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

For production calls, use `docs/salpx-api-production.md` and `scripts/salpx_production_client.py`. The script supports:

```text
image: gpt-image-2 for storyboards, first frames, product-proof images
video: omni_flash, gemini_omni_flash, seedance-2-mini-480p, and provider-supported Veo model IDs
```

## Startup Gate Rule

When the user says `短剧带货启动`, do not immediately generate a full script, a video package, a generic workplace story, a fashion story, or a made-up sample project.

The first response must start the diagnostic flow:

1. Ask for or inspect the product image/material.
2. If no product is provided, ask the user for product information before writing any story.
3. Remind the user that full salpx video submission requires registration at `https://www.salpx.com` and a local `SALPX_API_KEY`.
4. Produce only a short product diagnosis and three selectable briefs.
5. End with a copyable next-step line that exposes model choices.
6. Wait for the user to choose A, B, or C before writing the product proof bible, episode script, storyboard, first frames, or salpx prompts.

Startup copyable next-step template:

```text
短剧带货：建议下一步（可复制）：短剧带货，选 [A/B/C]，视频模型 salpx / seedance-2-mini-480p（可选 salpx / omni_flash，salpx / seedance-2-fast），产品是：[产品名/产品一句话]
```

Do not default the copyable next-step line to `salpx / omni_flash` only. Recently, Seedance2 is the priority route, while Omni and Seedance2 Fast should remain visible alternatives.

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

- runs `gpt-image-2` for storyboard grids, first frames, and product-proof images when needed
- receives clean 9:16 first frames
- runs `omni_flash`, Seedance 2.0 variants, Veo variants, or another selected video model
- returns image-to-video clips for review and post-production

## Trigger

Use this skill when the user says:

- 短剧带货
- 短剧带货启动
- 启动短剧带货
- ecommerce short drama
- product short drama
- 用 Codex 生成短剧带货
- salpx / omni_flash 图生视频
- salpx / gpt-image-2 生图
- salpx / seedance-2 / veo 图生视频
- 产品图生成短剧脚本、首帧、提示词、字幕或投放切片

## Core Rule

Do not make the product the hero.

The story must first make the audience care about a person, pet, relationship, or consequence. The product enters later as evidence, a record, a memory object, a relationship token, or a turning point.

## Strict Phase Gate

Do not collapse the workflow into one chat answer. TJ Short must move through phases and produce files at the correct phase.

Phase 0: startup

- Triggered by `短剧带货启动`, `启动短剧带货`, or similar.
- Ask for product material or inspect the provided product.
- Output only product diagnosis and A/B/C brief options.
- Do not write 12 shots, first-frame prompts, video prompts, captions, or sales copy yet.

Phase 1: user selects A/B/C

- Create project files instead of dumping the whole package in chat.
- Required files:

```text
项目首页.md
产品素材分析.md
产品证明圣经.md
短剧主线.md
角色主体库.md
人物备案板需求.md
Seedance2参考包计划.md
场景主体库.md
产品道具库.md
证据主体库.md
项目状态胶囊.md
```

- For Seedance2 visible-human routes, stop here if the dossier files are missing.
- Do not generate first-frame grids yet.
- Do not write full `salpx / omni_flash` or Seedance2 video prompt packs yet, except a short note naming the planned model route.

Phase 2: episode and 12-shot production table

- Generate `完整前三集剧本.md` or the requested episode script.
- Generate `第1集12镜头分镜表.md`, `镜头契约表.md`, `参考资产角色表.md`, and `generation_manifest.csv`.
- Each shot must reference role/scene/product/evidence IDs.
- Apply the Cinematic Shot-Design Rule to each shot's `camera:` and `emotion_shift:` fields; do not leave them as a vague one-line description.

Phase 3: role dossier image or Seedance2 reference package

- Generate or request character dossier boards.
- Extract or plan `图片1=face close-up`, `图片2=full/half-body wardrobe`, `图片3=scene`, `图片4=product`, optional `视频1`, optional `音频1`.
- Do not substitute this with a generic reference-asset table.

Phase 4: first-frame grid

- Generate a 12-panel grid only after Phase 1-3 gates are satisfied.
- Cost-control default: generate one 4x3 grid/contact sheet first, then cut it into 12 independent 9:16 first frames.
- Do not generate 12 independent first-frame images upfront. That wastes image-generation budget and breaks storyboard consistency.
- Independent first-frame generation is allowed only when:
  - the user explicitly asks for standalone frames,
  - the grid generator cannot produce a cuttable 4x3 layout after a reasonable retry,
  - one or more grid cells fail precheck and need retake,
  - the team has selected 3 key trial clips and wants higher-quality retakes for those cells.
- The official output should include both `storyboards/contact_sheet.png` and `first_frames/EP01-01.png` through `EP01-12.png` cut from the grid when possible.
- If a grid appears before role dossier assets for a Seedance2 visible-human route, mark the grid as `preview_only_invalid_missing_role_dossier`.
- For Seedance2 visible-human routes, official first frames must preserve realistic photographic body, wardrobe, product, props, and scene. Only the face regions may receive `face_pencil` colored-pencil/sketch treatment.
- Do not generate the official grid as full manga, anime, illustration, commercial storyboard, or cartoon style merely because face review is risky.
- A full illustrated grid may only be marked `preview_only_style_board`, never `official_first_frame`.

Phase 5: model-specific video prompts and submission

- Only now write the full model-specific prompt pack.
- Use separate prompt rules for `omni_flash`, `seedance2`, and `veo`.
- Do not submit video tasks until `generation_manifest.csv` has model route, duration rule, reference rule, prompt syntax rule, face review rule, output ratio, and audio mode.

## User-Facing Reply Style

During TJ Short workflow, start user-facing recommendations, status reports, and next-step suggestions with:

```text
短剧带货：
```

Examples:

```text
短剧带货：已完成产品诊断，下面给你 A/B/C 三个方向。
短剧带货：当前缺少人物备案板需求文件，先补这个，再做首帧宫格。
短剧带货：建议下一步生成 Seedance2 参考包，不要直接提交视频。
```

Do not use the prefix inside generated script dialogue, subtitles, filenames, CSV rows, or model prompts unless the content itself requires it.

## Subject Library Rule

Use a subject-library workflow before writing image or video prompts.

Do not let every shot reinvent the same people, rooms, products, and proof objects. Build reusable subjects first, then make each shot prompt reference those subjects and focus only on action, emotion, camera, dialogue, and continuity.

Required libraries:

1. Role library: each recurring person or pet gets one stable identity entry with age range, identity, face/fur traits, hair, wardrobe, expression baseline, relationship power, and product-contact behavior. For important recurring human roles, generate a character dossier board instead of a single portrait.
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

## Cinematic Shot-Design Rule

Do not fill the shot table's `camera:` field with a vague phrase like "medium shot, camera looks at her." AI short drama looks flat and PPT-like when every shot only proves the picture is pretty. A cinematic shot must answer: what information does it deliver, what emotion does it produce, how does it relate to the previous shot, does it move the story forward, and does it make the next shot worth waiting for. See `docs/methodology.md` Sections 16-17 for the full explanation.

Seven elements to set per shot when writing `camera:` and `emotion_shift:`:

```text
景别 frame size: 远景/全景/中景/近景/特写/大特写 (distance = information + emotional intensity)
角度 angle: 平视=equal 仰拍=power 俯拍=helpless 侧面=distant 背影=lonely 主观视角=immersive
构图 composition: 三分法=natural/dialogue 居中=ritual/pressure 留白=loneliness/waiting
光影 lighting: 柔光=warm 硬光=tense 逆光=mysterious 侧光=conflicted 顶光=oppressive 低光=threatening
色调 color grade: 暖色调=intimacy 冷色调=distance 低饱和=realism/oppression 高饱和=dreamlike
动势 camera movement: 推进=entering 拉远=detaching 跟随=immersion 摇移=exploring
节奏 pacing: 快剪=tension 慢镜=emotion 停顿=reflection 切黑=beat ending
```

Four reusable scene formulas — use as a starting template, then adapt to the actual subjects:

```text
情绪递进 emotional build-up: 远景(环境) -> 中景(人物) -> 近景(情绪) -> 特写(线索) -> 停顿(悬念)
悬疑 suspense: 冷色调 + 低照度 + 前景遮挡 + 缓慢推进 + 角色停顿 + 关键物体特写 + 突然切黑
浪漫 romance: 暖色调 + 柔光 + 浅景深 + 慢动作 + 眼神特写 + 环境光斑 + 镜头缓慢环绕
压迫 pressure: 低角度仰拍 + 居中构图 + 硬光阴影 + 低饱和 + 人物缓慢逼近 + 镜头轻微后退 + 节奏加快
```

PPT-look precheck before finalizing any first-frame grid:

```text
does every shot have foreground/midground/background layers, not just a subject floating in empty space?
does frame size vary across the 12 shots instead of holding one medium shot throughout?
is the character off-center or intentionally centered for a reason, not centered by default?
```

### Camera-as-Witness Prompt Law

Apply as an optional realism layer on top of the existing Seedance2 motion rules and model routing rules below, not as a replacement for them.

```text
Rule 1 - describe the shooting process, not the finished result:
  use: handheld micro-shake, focus hunting/racking, exposure drifting, mild compression noise
  avoid as the whole instruction: "beautiful picture", "perfect composition", "cinematic color"
  scope: selective realism layer for documentary/found-footage/tense handheld beats, not a blanket
  rule for every shot in a polished commercial short drama, and never applied to official
  Seedance2 face-compliance candidates (face_pencil_strong/medium, blur_feature).

Rule 2 - use exclusion to set boundaries:
  for every few things a scene "has," name at least one thing it "has not"
  example: has = clothesline, utility pole, potted plant / has not = modern storefronts, ads

Rule 3 - the timeline must carry camera behavior, not only character action:
  weak:   00:00-00:15 girl walks in and finds the envelope
  strong: 00:00-00:03 girl walks into corridor (handheld follow, shake)
          00:03-00:07 light flickers (exposure drifting)
          00:07-00:10 focus racks to envelope (focus hunting)
          00:10-00:15 girl stops (frame micro-shake, cut to black)
```

Director-level prompt formula (six blocks): `镜头语言(景别+焦距+机位+运动方式+时长) + 光影色彩(光源+光比+色调+氛围) + 场景细节(场景+道具+材质+环境细节) + 角色表演(造型+动作+表情+情绪) + 情绪风格(情绪基调+艺术风格+电影类型) + 技术参数(画幅比例+画质+模型+其他参数)`.

## Character Dossier Board Rule

When the user asks for a role subject image, default to a character dossier board unless they explicitly ask for a single portrait or first frame.

For any Seedance2 route with recurring visible human roles, character dossier boards are not optional. Do not skip directly from script/storyboard to first-frame grids or video prompts.

Minimum required dossier deliverables before Seedance2 first-frame generation:

```text
角色主体库.md
人物备案板需求.md
Seedance2参考包计划.md
```

If image generation is not requested yet, still create the textual dossier-board spec and reference extraction plan. If image generation is requested, generate the board or clearly mark it as `pending_image_generation`.

Do not treat a generic `参考资产角色表.md` as a substitute for a dossier board. The role asset table tracks references; the dossier board defines and stabilizes the character.

A good role dossier board contains:

- large main portrait
- full-body three views: front, side, back
- expression set: anxious, guilty, tender, relieved, angry, confused, or project-specific emotions
- wardrobe and material details
- product-contact or prop-contact details
- close-up visual memory points such as eyes, hair, hands, accessory, pet interaction, or package handling
- concise identity panel with name, age range, role, relationship, emotional baseline, and product-contact behavior

Prompt pattern:

```text
Create a horizontal premium character reference board / character design sheet.
Layout: large portrait, front/side/back full-body views, expression sheet, detail panels, concise info panel.
Keep the same face, hair, wardrobe, body proportions, and emotional baseline across all panels.
Use fictional characters only. No celebrity resemblance, no real brand logo, no readable private text.
```

For ecommerce short drama, the dossier board must include the character's product-contact behavior, but it must not turn the board into an ad. The product or prop should be shown as a handling reference, evidence object, or relationship object.

Production nuance:

- Keep dossier boards for role design, team review, filing, and consistency.
- Do not blindly submit a full multi-view dossier board as the main Seedance2 person reference.
- For Seedance2 video generation, extract or generate clean single-person references from the dossier board: one face close-up for identity, one full-body/half-body image for wardrobe and posture, and separate scene/product references.
- Multi-view boards can help humans and filing systems, but may confuse the video model if it reads several angles as several people.
- If actual tests show a provider handles a dossier board well, use it deliberately and record that provider/model result in the manifest.

## Seedance2 Role Filing Asset Rule

For Seedance2 clips with visible human faces, the preferred route is:

```text
fictional role design -> character dossier board -> provider/platform filing -> filed asset ID -> extracted Seedance2 references -> video generation
```

This rule is based on the behavior of AniShort-style character boards: filed status is loaded as project asset data, successful filing returns a platform asset number, and the platform states that downloaded/re-uploaded images can lose filed status. Therefore, a visible watermark such as `LibTV` is not proof of filing. The important object is the provider-side filed asset record.

When the selected salpx/provider route supports role filing or real-person/realistic-person asset registration:

1. File the approved fictional character dossier board before Seedance2 generation.
2. Record the returned asset ID as a provider-scoped reference. Use a placeholder format in public docs: `asset-YYYYMMDDHHMMSS-xxxxx`.
3. Keep and reuse the original filed asset URL or provider asset reference. Do not download and re-upload it as a new image.
4. If hair, clothing, age, face, or strong visual identity changes, treat it as a new role-board version and file again if the provider requires it.
5. Put filing metadata in the manifest:

```text
role_id:
role_board_version:
filing_status: filed | not_supported | pending | failed
filed_asset_id:
filing_scope:
source_asset_url:
model_route:
```

Never fabricate asset IDs, reuse another creator's filed assets, claim a watermark equals authorization, or use filing to process unlicensed real people, celebrities, influencers, public figures, or private people.

## Seedance2 Official Prompt Rule

For Seedance2 routes, build prompts around content-order references:

- Request payload may use normal URLs or `asset://<asset ID>` when the provider supports filed or authorized assets.
- Prompt text must still refer to media as `图片1`, `图片2`, `视频1`, `音频1` according to the order in the request content. Do not write "asset-xxxx is the actor" in the prompt.
- If a subject has multiple references, define the binding explicitly: `图片1中的面部特征和图片2中的服装造型定义为林夏`.
- Every later mention should use the same label: `林夏（图片1面部，图片2服装）`.
- For multi-person shots, define each person separately and keep labels stable.

Seedance2 prompt structure:

```text
素材定义:
图片1 = 角色面部特写
图片2 = 角色全身/半身服装参考
图片3 = 场景参考
视频1 = 运镜/动作节奏参考
音频1 = 环境声/对白音色/音乐氛围

主体定义:
将图片1中的面部特征、图片2中的服装造型定义为角色A。

镜头1:
运镜或切换方式 + 角色动作与表情 + 位置/空间变化 + 音频/台词。

全局约束:
高清真实摄影质感；人物面部稳定不变形；动作自然连贯；避免生成任何字幕、Logo、水印、可读文字；同一画面禁止重复生成同款人物。
```

Motion rules:

- Prefer low, continuous, controllable movement: slowly raises hand, turns head, breathes, pauses, looks down, steps back.
- Describe body parts and intensity: fingers tighten, shoulders relax, eyes avoid contact, jaw tightens.
- Avoid asking one shot to do many high-speed actions unless the clip is intentionally a separate action/montage shot.
- Use one camera move per shot: fixed camera, slow push-in, steady lateral move, handheld follow, or close-up cut. Do not stack push, pull, pan, tilt, and orbit in the same shot.
- Do not over-specify exact seconds inside Seedance2 prompts. Use shot order unless the provider route has proven stable with timing.

Seedance2 reference packaging:

- Recommended 4-5 references, not every available asset.
- For visible-face short drama: face close-up, full-body/wardrobe image, scene image, optional motion-reference video, optional audio.
- For product evidence shots: product image should control product shape only; the first frame controls composition; the prompt controls action and dialogue.
- Use `first_frame` and `last_frame` roles when strict start/end frames matter. Otherwise use multimodal references and clearly name their jobs.
- Use `return_last_frame=true` when generating several continuous clips and the next clip should start from the previous ending.

## Default Flow

1. Analyze the product asset or product name.
2. Produce three ecommerce short-drama briefs.
3. Let the user choose one brief.
4. Create the product proof bible.
5. Build four subject libraries: role, scene, product/prop, and evidence.
6. Create the required role dossier deliverables for key human roles: `角色主体库.md`, `人物备案板需求.md`, and `Seedance2参考包计划.md`.
7. If Seedance2 with visible faces is planned and the provider supports it, file the role boards and record filed asset metadata.
8. Extract Seedance2-ready references from role boards: face close-up, full/half-body wardrobe reference, scene/product references, optional motion/audio references.
9. Write one high-conflict episode.
10. Create a 12-shot production table that references subject IDs and applies the Cinematic Shot-Design Rule (frame size, angle, composition, lighting, color grade, movement, pacing) to each shot's camera field.
11. Generate one 4x3 storyboard/first-frame grid for EP01, then cut it into 12 independent 9:16 first frames. Precheck for PPT-look before finalizing: layered depth and varied frame size across the sequence.
12. Write clip contracts and reference role maps.
13. Write `salpx / omni_flash` prompts with fixed `duration=10`, or Seedance2 prompts with ordered media references. Apply the Camera-as-Witness Prompt Law selectively where the shot's style calls for realism.
14. Prepare captions, manifest, and delivery checklist.

## salpx API Production Rule

TJ Short must be able to produce assets after a GitHub install. Do not ship only prompt advice.

Before calling salpx, read `docs/salpx-api-production.md` and confirm:

```text
SALPX_API_KEY exists in .env or runtime environment
SALPX_BASE_URL defaults to https://www.salpx.com/v1
SALPX_IMAGE_MODEL defaults to gpt-image-2
SALPX_VIDEO_MODEL defaults to omni_flash unless the user selected another model
```

Use `scripts/salpx_production_client.py` as the default public-safe helper:

```bash
python scripts/salpx_production_client.py --env .env image \
  --model gpt-image-2 \
  --prompt "<storyboard or first-frame prompt>" \
  --size 1024x1792 \
  --out-dir outputs/images \
  --name ep01-shot01

python scripts/salpx_production_client.py --env .env video \
  --model seedance-2-mini-480p \
  --image first_frames/ep01-shot03.png \
  --prompt "<script-locked video prompt>" \
  --size 480x854 \
  --duration 7 \
  --out outputs/videos/ep01-shot03.mp4
```

Model mappings:

```text
gpt-image2 / gpt-image-2 -> gpt-image-2
omni / salpx omni -> omni_flash
gemini omni -> gemini_omni_flash
seedance2-mini-480p -> seedance-2-mini-480p
veo -> the exact salpx console model ID, recorded in manifest
```

Generation rules:

- Image generation uses `POST /images/generations` and saves either `b64_json` or downloaded image URLs into the project directory.
- Video generation uses `POST /videos`. If the response returns a task ID, poll `/videos/{task_id}`, `/videos/{task_id}/result`, or `/videos/generations/{task_id}` until a video URL appears.
- Do not echo or write real API keys. Real keys stay only in `.env`, shell env, or CI secrets.
- Every generated file must be copied into the project directory and recorded in the manifest.
- Every downloaded video must be inspected for actual duration, width, height, bytes, and whether it can enter final composition.

## Video Model Rules

Always choose the video model route before writing generation prompts.

Do not reuse one generic prompt across Omni, Seedance2, and Veo. Each model has different duration assumptions, reference behavior, motion tolerance, audio behavior, and review risks.

Model route table:

```text
omni_flash:
  role: fast image-to-video raw clip generation through salpx
  duration: fixed 10 seconds
  best_for: one clear first frame, simple acting/action, quick trial clips
  prompt_style: describe only motion, camera, emotion shift, lip-sync target, continuity locks
  avoid: model-specific Seedance2 media numbering, asset_id filing language, overlong multimodal instructions

seedance2:
  role: multimodal video generation/edit/extend with stronger reference control
  duration: selected model/provider capability, commonly seconds such as 4-15 on official routes
  best_for: visible-face acting, product handling, image/video/audio reference mixing, first/last-frame control
  prompt_style: ordered media references (`图片1`, `视频1`, `音频1`), subject definition, shot sequence, restrained actions, one camera move per shot
  review_focus: role filing, authorized/fictional face handling, asset:// references in request body, no direct asset IDs in prompt prose

veo:
  role: cinematic generation with strong scene language and visual continuity, provider-dependent
  duration: selected Veo/provider capability
  best_for: cinematic mood, complex environments, polished motion, broad visual storytelling
  prompt_style: concise cinematic description, camera/lens/lighting, subject continuity, negative constraints if supported
  avoid: assuming Seedance2's 图片1/视频1 syntax unless the selected provider explicitly maps references that way
```

`salpx / omni_flash` is fixed at 10 seconds per raw clip.

Never write 5-second, 6-second, or 8-second submission durations for Omni. Fast pacing is done in post-production by cutting the 10-second raw clip.

Seedance 2.0 and Veo model durations depend on the selected model and provider route. Do not assume Omni's fixed 10-second rule applies to non-Omni models.

For official Seedance2 routes, current common output duration is model-dependent and generally in seconds, often within a 4-15 second range for Seedance 2.0 series routes. Use the selected provider/model capability, not a hardcoded Omni duration.

Use `ratio="9:16"` for native vertical output when supported. Use `ratio="adaptive"` when the first frame's aspect ratio should drive output or when avoiding frame distortion from mismatched image dimensions.

Before submitting any clip, include `model_route` in the manifest and validate that the prompt follows that route's rules:

```text
model_route: omni_flash | seedance2 | veo | other
duration_rule:
reference_rule:
prompt_syntax_rule:
face_review_rule:
output_ratio:
audio_mode:
```

## Seedance2 Visible-Face Rule

When Seedance2 clips need visible actor faces, do not default to faceless crops. Short drama depends on facial acting.

Do not confuse API smoke tests with production first-frame selection:

- API smoke test: allowed to use a no-person product frame to verify salpx `/videos` submit, polling, and download behavior.
- Production Seedance2 acting shot: must preserve the dramatic face route. Do not replace a visible-face acting shot with a product-only or faceless frame unless the user explicitly changes the shot design. If all compliant face candidates fail, record the reasons and ask for a shot-design decision instead of silently switching.

Before generating Seedance2 prompts, first-frame grids, or video submissions, verify:

```text
has_role_subject_library: yes
has_character_dossier_spec: yes
has_seedance2_reference_package_plan: yes
has_filed_asset_status_or_not_supported_reason: yes
```

If any item is missing, stop and create the missing role/dossier files first.

Seedance2 first-frame compliance starts at grid generation, not after a failed video submission.

Required official first-frame route:

```text
photographic first-frame/grid
-> same shot candidate A: face_pencil_strong
-> same shot candidate B: face_pencil_medium
-> same shot candidate C: blur_feature = blurred main frame + facial-feature sheet
-> Seedance2 precheck each candidate one by one
-> select the passing candidate with the most complete face/acting information
-> body, wardrobe, product, props, and scene remain photographic
-> submit as Seedance2 first-frame/reference
```

Forbidden downgrade for official first frames:

```text
full manga style
full anime style
full illustration style
commercial storyboard style
cartoon actor style
```

Those styles reduce the short-drama/live-action selling effect and should not be used as the face-compliance fallback unless the user explicitly asks for an animated/comic campaign.

Use this escalation path:

1. Start with a clean fictional virtual-actor dossier board and first frame.
2. If the provider supports role/person filing, file the dossier board first and pass the filed asset reference into the Seedance2 route.
3. Extract a clean face close-up and full/half-body wardrobe reference from the filed role board when possible.
4. Write prompts with ordered media references such as `图片1`, `图片2`, and stable subject labels. Do not refer to the `asset_id` directly in prompt prose.
5. For official Seedance2 first frames and grids, generate the same shot as three candidates: `face_pencil_strong`, `face_pencil_medium`, and `blur_feature`.
6. Precheck candidates one by one. If the provider has a precheck endpoint, use it; otherwise submit a controlled one-shot test and record the result in the manifest.
7. Choose the passing candidate that preserves the most face information, expression, lip-shape, and acting clarity. Do not choose the strongest stylization just because it is safer if a more face-complete candidate passes.
8. If all candidates fail, record the failure reasons, then ask whether to redesign the shot as product-only/faceless. Do not silently switch.
9. Prompt the model that the main frame controls composition/body/wardrobe/action and the feature sheet controls fictional facial features.

Do not use this process for unlicensed real people, celebrities, influencers, public figures, or attempts to bypass identity review. It is only for self-owned fictional virtual characters.

## Required Deliverables

- Product proof bible
- Role subject library and character dossier boards for key roles
- Filed role asset table for Seedance2 routes when supported
- Seedance2 reference package: ordered face/body/scene/product/motion/audio references
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
