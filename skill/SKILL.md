---
name: tj-short
description: 电商短剧带货创作总流程 skill v0.9.1。当用户说「短剧带货」「短剧带货启动」「启动短剧带货」「电商短剧」「产品短剧」「带货短剧」「产品图生成短剧」，或要求做产品证明脚本、主体库（角色/场景/产品道具/证据）、人物备案板/角色设定板、Seedance2 参考包与人物备案资产、12 镜头分镜表、首帧宫格、首帧图、salpx / gpt-image-2.5-sunburst 生图、salpx Wan 3.0 视频（文生/首帧/首尾帧/多素材参考：参考图·参考视频·参考音频·文档·网页，单次 2–30 秒直出、原生音轨与口型同步）及其提示词、字幕与投放切片、generation_manifest、交付清单、电影感镜头设计、剧本保真核对（对白/动作 ID 与覆盖台账）、美国市场本地化（脚本/字幕/CTA）、Seedance2 露脸合规修复时，使用本 skill。
---

# TJ Short

TJ Short 是电商短剧带货的完整生产流程 skill，可在 WorkBuddy / Codex 等宿主 agent 里直接安装使用。

Version: `short-drama-ecommerce v0.9.1`

## 安装与调用

- 安装位置（WorkBuddy）：`~/.workbuddy/skills/tj-short`（slug=`tj-short`）。本文件里的相对路径 `docs/…`、`scripts/…`、`prompts/…` 都相对这个目录。
- 宿主映射：下文所有 **Codex** 一律读作当前宿主 agent（WorkBuddy / Codex 均可），流程与方法论与宿主无关。
- 依赖：
  - `python3` / `ffmpeg` / `ffprobe`。
  - `scripts/wan3_video_client.py` 是纯标准库，任何 python3 都能直接跑；`scripts/salpx_production_client.py`（生图）需要 `requests`。
- 调用方式：

  ```bash
  # 生图（分镜宫格 / 首帧 / 产品证明图）
  python3 scripts/salpx_production_client.py --env .env image \
    --prompt "..." --out-dir outputs/images --name ep01-shot01

  # 视频（以首帧图生视频为例）
  python3 scripts/wan3_video_client.py --env .env video \
    --model wan3.0-720p --prompt "..." --duration 8 --ratio 9:16 \
    --first-frame first_frames/EP01-03.png --wait --out outputs/videos/ep01-03.mp4
  ```

- 唯一付费凭证：`SALPX_API_KEY`。同一个 key 同时管生图（`gpt-image-2.5-sunburst`）和视频（`wan3.0-*`）。注册：<https://www.salpx.com>
  - 取 key 顺序：环境变量 → `--env` 指定的文件（项目 `.env`）→ `~/.config/salpx/credentials.env`。
  - 不要把真 key 写进 skill 文件、提示词、manifest 或聊天输出。
  - **视频只走 salpx**。`H3_API_KEY` / `h3.zhongbiao.cloud` 已废弃，脚本与文档已删除；客户端检测到 base URL 含 `zhongbiao` 或 `h3.` 会直接报错退出。
- 生图/生视频会**真实扣费**。提交任何生成任务之前，先把模型、张数/条数、时长、预计金额报给用户并取得同意；用户只要脚本和提示词时，不要擅自出图。`--dry-run` 可以先算价不花钱。
- 出片产物一律落到**当前项目目录**（`outputs/images`、`outputs/videos` 等）。
- 安全：脚本只访问 `https://www.salpx.com`，无 `curl | bash`、无 `rm -rf`、无外发用户数据，仅读取用户自填的 API key。
- 来源：<https://github.com/tttg2010/tj-short>，License 见 `LICENSE`。

## v0.9.1 Changelog

Default image model raised from `gpt-image-2` to `gpt-image-2.5-sunburst`.

- `SALPX_IMAGE_MODEL` now defaults to `gpt-image-2.5-sunburst` in `.env.example`, in `scripts/salpx_production_client.py`, and in every prompt template and SOP step.
- Documented the available salpx image variants: `gpt-image-2.5-flare`, `gpt-image-2.5-1k`, and the `XY-` prefixed 1k/2k/4k lines; `gpt-image-2` remains selectable as the previous generation.
- No API shape change: still `POST /v1/images/generations`, same `--size` / `--out-dir` / `--name` flags. Existing `.env` files that pin `SALPX_IMAGE_MODEL=gpt-image-2` keep working.
- Same credential: one `SALPX_API_KEY` covers image and video.

## v0.9.0 Changelog

Video layer migration: MiniMax H3 out, salpx Wan 3.0 in. This is a breaking change for anything still pointing at the old H3 route.

- Replaced the default and only video route with salpx Wan 3.0 (`wan3.0-480p` / `wan3.0-720p` / `wan3.0-1080p`, plus the independent `wan3.0-hm-*` line). Image and video now share a single credential: `SALPX_API_KEY`.
- Added `scripts/wan3_video_client.py` (stdlib only, no third-party deps): `video` / `status` / `download` / `models` subcommands; supports `first_frame`, `last_frame`, `reference_image` x10, `reference_video` x5, `reference_audio` x5, `file`, `link`; local assets are auto-encoded to base64; `--dry-run` validates and quotes without spending.
- Added `docs/wan3-api-production.md`: endpoint, model/price ladder, per-second billing and reference-video hold, material combination rules, request construction, polling and download, error map, prompt guidance.
- Expanded the video capability set: integer 2-30 second single takes, native audio track, lip-sync and singing driven by reference audio, multi-reference identity lock across images/video/audio.
- Added a hard cost gate: model, resolution, output seconds, whether a reference video is attached, and the computed price must be stated to the user before every submission.
- Removed `scripts/h3_video_client.py`, `docs/h3-api-production.md`, and `scripts/submit_salpx_omni_i2v.py`; dropped all `H3_*` variables from `.env.example`; the client now rejects any base URL containing `zhongbiao` or `h3.`.
- Narrowed `scripts/salpx_production_client.py` to image generation only; its `video` subcommand now points at the Wan 3.0 client.
- Rewrote the video production section of `SKILL.md` as `salpx Wan 3.0 Video Production Rule`, including the price ladder, material constraints, and the 30-second budget rule.
- Breaking: projects that still call the H3 route, pass `H3_API_KEY`, or parse H3 job payloads must migrate to `SALPX_API_KEY` + `wan3.0-*`.

## v0.8.30 Changelog

- Added `Script Fidelity and Traceability Rule` after two real production failures: a shot table silently dropped 2 of 4 script dialogue lines with no shot ever picking them up, and a first-frame generation added an unrequested prop (a physical invitation card the script never described) that survived review and was inherited into the final video.
- Added dialogue/action ID tagging (`[D-<scene>-<n>]`, `[A-<scene>-<n>]`) required in the episode script, and a coverage ledger required at the end of Phase 2 mapping every ID to a shot or a stated deliberate cut. 100% coverage is a hard gate before Phase 3.
- Added a `SOURCE ANCHOR` block requirement: every Phase 4/5 prompt document must open with the exact tagged script lines the shot derives from, so generation happens against the source, not a paraphrase of a paraphrase.
- Added a containment diff check for every image/video generation: prompts must carry MUST HAVE and MUST NOT HAVE lists, and review must answer a mandatory, non-skippable "what did the output add that the prompt never asked for?" field. First-frame drift is a hard gate (cheap retake); video-level drift is a soft gate (record + human decides) unless it violates an explicit MUST NOT HAVE item, which always escalates to blocking.
- Added `保真核对.md` to Required Deliverables: one file per episode carrying the coverage ledger and containment diffs.
- Clarified this adds no dedicated LLM calls: coverage is deterministic ID-string matching, and containment diffs are filled during review that already happens when a human looks at generated output.
- Added `US-Market Localization Hard Rule`: when target region is 美国 / US / United States, the story, dialogue, characters, scene text, subtitles, CTA, compliance wording, and project manifest must fit the United States market instead of translating Chinese ecommerce short-drama habits into English.
- Added current production split: salpx/gpt-image-2 is the default image layer for storyboard grids and first frames; MiniMax H3 was the default video layer for raw clips. salpx video models remain optional alternatives when the user selects them.（v0.9.0 起视频层统一走 salpx Wan 3.0，MiniMax H3 已弃用。）
- Source: architecture review by 肖老师 (xiao-laoshi-agent) after two script-fidelity failures surfaced in a real project; see `docs/methodology.md` Section 18 for the full diagnosis and design rationale.

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

After installing or updating this skill, reload WorkBuddy (new session) before testing the trigger phrase. The host may keep an old skill cache until reload.

User-facing reminder:

```text
短剧带货 skill 已装好，新开一个会话（或重启 WorkBuddy）后再测触发词。
```

Then test with:

```text
短剧带货启动
```

Image generation through salpx requires a salpx API key. Tell users to register at `https://www.salpx.com`, create or copy their API Key, and put it into local `.env` as `SALPX_API_KEY`.

Video generation uses salpx Wan 3.0 (`wan3.0-*`) and needs the same `SALPX_API_KEY`. Without it, WorkBuddy can still generate scripts, storyboards, first frames, prompts, and manifests, but it cannot submit video tasks.

For production image calls, use `docs/salpx-api-production.md` and `scripts/salpx_production_client.py`. For production Wan 3.0 video calls, use `docs/wan3-api-production.md` and `scripts/wan3_video_client.py`.

```text
image: gpt-image-2.5-sunburst for storyboards, first frames, product-proof images
video: salpx Wan 3.0 (wan3.0-480p / wan3.0-720p / wan3.0-1080p, or the -hm- line), 2-30s per clip, native audio
optional alternative video routes: omni_flash, gemini_omni_flash, seedance-2x, and provider-supported Veo model IDs
```

## Startup Gate Rule

When the user says `短剧带货启动`, do not immediately generate a full script, a video package, a generic workplace story, a fashion story, or a made-up sample project.

The first response must start the diagnostic flow:

1. Ask for or inspect the product image/material.
2. If no product is provided, ask the user for product information before writing any story.
3. Remind the user that both salpx image generation and salpx Wan 3.0 video generation require the same `SALPX_API_KEY`.
4. Ask or infer the target region. If the user selects 美国 / US / United States / North America for US sale, immediately lock `target_region=US` and apply the US-Market Localization Hard Rule below.
5. Produce only a short product diagnosis and three selectable briefs.
6. End with a copyable next-step line that exposes model choices and target region.
7. Wait for the user to choose A, B, or C before writing the product proof bible, episode script, storyboard, first frames, or salpx prompts.

Startup copyable next-step template:

```text
短剧带货：建议下一步（可复制）：短剧带货，选 [A/B/C]，地区 [中国/美国/其他]，图片模型 salpx / gpt-image-2.5-sunburst，视频模型 salpx / wan3.0-720p（可选 wan3.0-1080p、wan3.0-hm-*、omni_flash、seedance-2x），产品是：[产品名/产品一句话]
```

Current default production is salpx/gpt-image-2.5-sunburst for images and salpx Wan 3.0 (`wan3.0-720p` as the cost/quality default) for videos. Video must never route through a non-salpx host.

If the user says "generate video" before product diagnosis is complete, still follow the gate: product diagnosis -> three briefs -> user chooses A/B/C -> then production.

WorkBuddy is the production brain:

- analyzes product assets
- writes product-proof briefs
- creates scripts and storyboards
- generates first-frame directions
- writes salpx image prompts and salpx Wan 3.0 video prompts
- builds caption and delivery plans
- checks privacy before publishing

salpx is the execution relay for both image and video:

- image: runs `gpt-image-2.5-sunburst` for storyboard grids, first frames, and product-proof images
- video: runs `wan3.0-*` for raw clips — text-to-video, first-frame, first+last-frame, or Omni reference (reference images / videos / audio / document / web link)
- returns raw clips for review and post-production

## Trigger

Use this skill when the user says:

- 短剧带货
- 短剧带货启动
- 启动短剧带货
- ecommerce short drama
- product short drama
- 用 Codex 生成短剧带货
- 用 WorkBuddy 生成短剧带货
- salpx / wan3.0 图生视频
- salpx / gpt-image-2.5-sunburst 生图
- wan3 / 万相3.0 / wan3.0-720p / wan3.0-1080p 视频
- 30 秒视频直出、多图参考、视频参考、声音参考、人物唱歌对口型
- salpx / omni_flash / seedance-2 / veo 图生视频
- 产品图生成短剧脚本、首帧、提示词、字幕或投放切片

## Core Rule

Do not make the product the hero.

The story must first make the audience care about a person, pet, relationship, or consequence. The product enters later as evidence, a record, a memory object, a relationship token, or a turning point.

## US-Market Localization Hard Rule

When the target region is 美国, US, United States, North America for US sale, or a US marketplace such as TikTok Shop US / Amazon US, do not write a Chinese short-drama script and translate it into English. Rebuild the content for the United States market from the start.

Hard manifest fields:

```text
target_region: US
locale_lock_status: locked
dialogue_language: en-US
subtitle_language: en-US
scene_locale: United States
cta_locale: US ecommerce / TikTok Shop US / Amazon US as selected
compliance_market: US
locale_mismatch_status: pass | blocked
```

Required behavior:

- Dialogue and subtitles default to natural American English unless the user explicitly requests bilingual output. Character names, occupations, relationships, humor, conflict style, and emotional pacing must sound plausible for US short-form ecommerce drama.
- Scenes must match US everyday life: apartments, suburban homes, kitchens, dorms, garages, local clinics, gyms, pet stores, offices, driveways, sidewalks, school pickup, or other US-appropriate contexts selected for the product.
- On-screen phone/chat/order scenes must use US-native labels, currency, time format, address style, and CTA wording such as `Shop now`, `Check TikTok Shop`, `Get yours today`, `Available on Amazon`, or user-provided platform language.
- Product claims must follow US market caution. For medical, supplement, financial, child, pet-health, beauty, safety, or regulated claims, write evidence-based phrasing, avoid guaranteed results, and add review-needed notes where appropriate.
- Character wardrobe, home layout, appliances, packaging visibility, props, background signage, and scene text must fit the US locale.

Forbidden in US-locked projects unless the user explicitly asks for a Chinese-diaspora setting and labels it as such:

```text
家人们
直播间
橱窗
点小黄车
私信我
加微信
9块9包邮
人民币/RMB pricing
Chinese hospital/community/compound scenes as the default
Chinese app UI, Chinese delivery lockers, Chinese street signage, or Chinese ecommerce jargon
```

Locale gate:

- If any script, shot table, first-frame prompt, video prompt, subtitle file, scene text, or CTA contains the forbidden US-mismatch items above, mark `locale_mismatch_status=blocked`, write `invalid_reason=locale_mismatch_us_market`, and fix the artifact before Phase 3, Phase 4, or Phase 5 can continue.
- The US locale lock does not override script fidelity, subject libraries, Seedance2 face rules, salpx/Wan 3.0 model rules, or safety checks. It is an additional gate that all downstream artifacts must carry.

## Strict Phase Gate

Do not collapse the workflow into one chat answer. TJ Short must move through phases and produce files at the correct phase.

Phase 0: startup

- Triggered by `短剧带货启动`, `启动短剧带货`, or similar.
- Ask for product material or inspect the provided product.
- Output only product diagnosis and A/B/C brief options.
- Do not write 12 shots, first-frame prompts, video prompts, captions, or sales copy yet.

Phase 1: user selects A/B/C

- Create project files instead of dumping the whole package in chat.
- If `target_region=US`, every file created in this phase must carry the locale manifest fields from the US-Market Localization Hard Rule.
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
- Do not write full Wan 3.0, `salpx / omni_flash`, or Seedance2 video prompt packs yet, except a short note naming the planned model route.

Phase 2: episode and 12-shot production table

- Generate `完整前三集剧本.md` or the requested episode script. Tag every dialogue line and plot-relevant action with a stable ID per the Script Fidelity and Traceability Rule.
- Generate `第1集12镜头分镜表.md`, `镜头契约表.md`, `参考资产角色表.md`, and `generation_manifest.csv`.
- Each shot must reference role/scene/product/evidence IDs.
- If `target_region=US`, every dialogue line, scene note, subtitle source, CTA, and any visible text in the shot table must be en-US and US-localized.
- Apply the Cinematic Shot-Design Rule to each shot's `camera:` and `emotion_shift:` fields; do not leave them as a vague one-line description.
- Generate the coverage ledger inside `保真核对.md`. Coverage must be 100% (every script ID is `covered` or `deliberately cut (reason: ...)`, none `LOST`) before Phase 3 starts.

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
- Every first-frame/grid-cell prompt must open with the `SOURCE ANCHOR` block for that shot and carry MUST HAVE / MUST NOT HAVE lists per the Script Fidelity and Traceability Rule. After generation, fill the containment check's "what did the output add that the prompt never asked for?" field — never leave it blank. A cell that adds an unrequested element is `drift`: retake it or tighten the prompt before it enters the official first-frame set. This is a hard gate.

Phase 5: model-specific video prompts and submission

- Only now write the full model-specific prompt pack.
- Use separate prompt rules for Wan 3.0, `omni_flash`, `seedance2`, and `veo`.
- Every prompt document must open with the `SOURCE ANCHOR` block for that shot (the exact tagged script lines it derives from) and carry MUST HAVE / MUST NOT HAVE lists.
- Do not submit video tasks until `generation_manifest.csv` has model route, duration rule, reference rule, prompt syntax rule, face review rule, output ratio, and audio mode.
- After each video generation, fill the containment check for that clip. Video-level drift is a soft gate — record it and let the user decide whether to retake — unless the drift violates an explicit MUST NOT HAVE item, which always escalates to a hard block.

## Script Fidelity and Traceability Rule

The script -> shot table -> first frame -> video prompt pipeline is a chain of lossy compressions. Without this rule, nothing catches what a stage drops or what a generation silently adds. See `docs/methodology.md` Section 18 for the full diagnosis. This rule exists because both failure modes have happened in production: a shot table dropped 2 of 4 script dialogue lines with no shot ever picking them up, and a first-frame generation added a prop the script never described, and it survived review into the final video.

### Dialogue/Action ID Tagging (Phase 2)

Tag every dialogue line and plot-relevant action in the episode script with a stable ID:

```text
[D-<scene>-<n>] for dialogue, e.g. [D-S3-01] 苏晴："想什么呢，请柬都不回？"
[A-<scene>-<n>] for key non-dialogue actions, e.g. [A-S3-01] 手机屏幕亮起婚礼请柬确认消息（一条手机短信，非纸质）
```

Every shot table `dialogue_or_lip_sync` field must cite the IDs it carries, not just paraphrase the line.

### Coverage Ledger (hard gate, end of Phase 2)

List every script ID and where it landed:

```text
source ID -> landed in shot -> status: covered | deliberately cut (reason: ...) | LOST
```

`LOST` (no shot, no stated reason) is not an allowed terminal state. Coverage must be 100% before Phase 3 starts. This is deterministic ID-string matching — do not spend a dedicated LLM call comparing script to shot table; check whether each ID string appears downstream.

### Source Anchor Block (hard gate, Phase 4/5)

Every image/video prompt document must open with a read-only block pasting the exact tagged script lines that shot derives from, before the actual prompt text:

```text
# SOURCE ANCHOR (from script, read-only)
[A-S3-01] 手机屏幕亮起婚礼请柬确认消息（一条手机短信，非纸质）
---
# shot prompt
...
```

A prompt document missing this block is not a valid production artifact. This is what turns "summarize, then regenerate" into "regenerate against the source" — the generation step sees the original line, including its exclusion constraint, not a paraphrase of a paraphrase.

### Containment Diff (Phase 4 hard gate per cell, Phase 5 soft gate)

Every prompt carries two lists:

```text
MUST HAVE: what the prompt requires
MUST NOT HAVE: entities the model tends to invent — physical stand-ins for digital objects, extra people, extra props (this is the existing has/has-not exclusion technique from the Camera-as-Witness Prompt Law, now mandatory, not optional)
```

After generation, fill this field — it must never be left blank:

```text
what did the output add that the prompt never asked for? (answer required; write "none" if nothing)
```

Verdict is binary: `match` or `drift`. No "close enough, ship it." First-frame drift blocks — retake the cheap image rather than let it get inherited and amplified by image-to-video. Video-level drift is recorded and the user decides whether to retake, since video regeneration is the most expensive retry in the pipeline — except a MUST NOT HAVE violation, which always blocks regardless of stage.

### Deliverable

Keep the coverage ledger and every containment diff for one episode in a single `保真核对.md`. Do not fragment fidelity records across many small files, and do not introduce a dedicated LLM call or computer-vision pass for this rule — coverage is a text lookup and containment diffs are filled during the review a human already does when looking at generated output.

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
4. Lock the target region. If it is US, apply the US-Market Localization Hard Rule to all story, scene, caption, CTA, compliance, and manifest artifacts.
5. Create the product proof bible.
6. Build four subject libraries: role, scene, product/prop, and evidence.
7. Create the required role dossier deliverables for key human roles: `角色主体库.md`, `人物备案板需求.md`, and `Seedance2参考包计划.md`.
8. If Seedance2 with visible faces is planned and the provider supports it, file the role boards and record filed asset metadata.
9. Extract Seedance2-ready references from role boards: face close-up, full/half-body wardrobe reference, scene/product references, optional motion/audio references.
10. Write one high-conflict episode.
11. Create a 12-shot production table that references subject IDs and applies the Cinematic Shot-Design Rule (frame size, angle, composition, lighting, color grade, movement, pacing) to each shot's camera field.
12. Generate one 4x3 storyboard/first-frame grid for EP01, then cut it into 12 independent 9:16 first frames. Precheck for PPT-look before finalizing: layered depth and varied frame size across the sequence.
13. Write clip contracts and reference role maps.
14. Write salpx Wan 3.0 prompts and pick the mode per shot: `text_to_video`, `first_frame`, `first_last_frame`, or `reference` (reference_image / reference_video / reference_audio). Declare `duration` (integer 2-30) and `ratio` up front, and tag references as 图1/图2、视频1、音频1 inside the prompt. Apply the Camera-as-Witness Prompt Law selectively where the shot's style calls for realism.
15. Prepare captions, manifest, and delivery checklist.

## salpx Wan 3.0 Video Production Rule

Current default production split:

```text
salpx / gpt-image-2.5-sunburst -> storyboard grids, first frames, product-proof images
salpx / Wan 3.0 (wan3.0-*) -> raw video clips, with native audio
```

Video must never route through any host other than `https://www.salpx.com/v1`. `h3.zhongbiao.cloud` and `H3_API_KEY` are dead: do not call them, do not reference them in manifests, do not ask the user for that key.

Before submitting, read `docs/wan3-api-production.md` and confirm:

```text
SALPX_API_KEY exists in env -> project .env -> ~/.config/salpx/credentials.env
SALPX_BASE_URL defaults to https://www.salpx.com/v1
SALPX_VIDEO_MODEL defaults to wan3.0-720p
endpoint is POST /v1/videos (never /v1/chat/completions)
duration is an integer 2-30, and it is stated to the user before submission
```

Model ladder (resolution is carried by the model name; `size` / `resolution` in the body are ignored):

| model | resolution | price (CNY/s) | 5s | 10s | 30s |
|---|---|---|---|---|---|
| `wan3.0-480p` | 480P | ¥0.21 | ¥1.05 | ¥2.10 | ¥6.30 |
| `wan3.0-720p` | 720P | ¥0.42 | ¥2.10 | ¥4.20 | ¥12.60 |
| `wan3.0-1080p` | 1080P | ¥0.84 | ¥4.20 | ¥8.40 | ¥25.20 |
| `wan3.0-hm-480p` | 480P | ¥0.28 | ¥1.40 | ¥2.80 | ¥8.40 |
| `wan3.0-hm-720p` | 720P | ¥0.56 | ¥2.80 | ¥5.60 | ¥16.80 |
| `wan3.0-hm-1080p` | 1080P | ¥1.11 | ¥5.55 | ¥11.10 | ¥33.30 |

- `hm` is an independent line with identical parameters, material rules and billing, only a different price. The two lines never fail over into each other.
- Billed per second. A task with a `reference_video` is billed as `price x (output seconds + reference video seconds)`; the submit-time hold assumes the 15s cap and is settled afterwards.
- Failed / timed-out / rejected tasks are refunded in full.
- Cost gate: before every submission, tell the user model, resolution, output seconds, whether a reference video is attached, and the computed price, then wait for consent. A 30s 1080p clip is ¥25.20 — never submit that on assumption.

Request shape (`prompt` top-level, materials under `metadata.media`, each item `{"type": ..., "url": ...}`):

```bash
python3 scripts/wan3_video_client.py --env .env video \
  --model wan3.0-720p \
  --prompt "<script-locked prompt: 图1 的角色..., 视频1 的运镜..., 音频1 的节奏...>" \
  --duration 8 \
  --ratio 9:16 \
  --first-frame first_frames/EP01-03.png \
  --wait \
  --out outputs/videos/ep01-shot03.mp4
```

Other flags: `--last-frame`, `--ref-image` (repeat up to 10), `--ref-video` (repeat up to 5), `--ref-audio` (repeat up to 5), `--ref-file`, `--ref-link`, `--no-audio`, `--seed`, `--poll-interval`, `--timeout`. Local files are auto-converted to `data:{MIME};base64,...`; remote materials must be public direct-download URLs (private, login-gated or hotlink-protected URLs fail the task).

Modes (decided by which material types you attach):

- `text_to_video`: `prompt` only. Use when no first frame is needed.
- `first_frame`: one `first_frame` (or the top-level `input_reference` shorthand). Default TJ Short route after salpx first-frame generation.
- `first_last_frame`: `first_frame` + `last_frame`, when the clip must open and close on exact frames.
- `reference`: `reference_image` (max 10) / `reference_video` (max 5, 15s total) / `reference_audio` (max 5, 15s total) / `file` (1 document) / `link` (1 public webpage). This is the route for identity lock, product consistency, camera transfer, voice/lip-sync and singing.

Material rules:

- `first_frame` / `last_frame` cannot be mixed with `reference_*`, `file` or `link`. `file` and `link` are mutually exclusive; both can combine with `reference_*`. The three `reference_*` types combine freely.
- Output is 2-30s. With a `reference_video` attached, reference seconds + output seconds must stay <= 30.
- Images: JPEG/PNG (no alpha)/BMP/WEBP, side 240-8000 px, aspect <= 8:1, <= 20MB. Video: mp4/mov, 1-15s each, >= 16fps, side 240-4096 px, <= 100MB. Audio: wav/mp3, 1-15s each, <= 15MB.
- Aspect `ratio`: `adaptive` (default), `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `21:9`. For short drama always pass `9:16` explicitly when the first frame is not already vertical.
- `metadata.parameters.audio` defaults to `true`; muted output costs the same, so keep audio on unless the user wants silence.
- `metadata.parameters.prompt_extend` defaults to `true`.

Prompt rules for Wan 3.0:

- Reference order defines the name: the first `reference_image` is 图1, the first `reference_video` is 视频1, the first `reference_audio` is 音频1. State each asset's job in the prompt ("图1 是女主，图3 是产品包装，视频1 定运镜，音频1 是她的声音").
- One continuous take reads differently from a multi-shot run: a 20-30s clip needs action beats with a camera reason, not four stitched scenes in prose.
- For lip-sync / singing, the audio reference is the timing authority: give 1 clean vocal track (<= 15s), state that the mouth must follow 音频1, and keep the face unobstructed and frontal enough for the model to lock the lips.
- For product shots, 6-8 reference images is the stable zone (subject, material close-ups, in-use scene); more than 8 risks feature conflict, fewer than 6 invites hallucinated details.
- Keep the camera-as-witness law and MUST HAVE / MUST NOT HAVE lists from the shot-design rules; drift review still applies.

Polling and delivery:

- `GET /v1/videos/{id}` every 15s, total timeout >= 900s. `status` is `queued` / `in_progress` / `completed` / `failed`.
- The clip URL lives at `metadata.url`, not at the top level. It expires in 24 hours — download immediately into the project directory.
- Every output must be probed with `ffprobe` for real duration, width, height, bytes, and recorded in `generation_manifest.csv` (`model_route=salpx_wan3`, task id kept private in public examples).
- Error map: 403 `token quota is not enough` (insufficient balance, reference-video tasks hold 15s up front), 503 `No available channel` (model name typo or token group not enabled), 400 `duration out of range`, 404 (used `/v1/chat/completions`).

## salpx API Production Rule

TJ Short must be able to produce image assets after a GitHub install. Do not ship only prompt advice.

Before calling salpx, read `docs/salpx-api-production.md` and confirm:

```text
SALPX_API_KEY exists in .env or runtime environment
SALPX_BASE_URL defaults to https://www.salpx.com/v1
SALPX_IMAGE_MODEL defaults to gpt-image-2.5-sunburst
SALPX_VIDEO_MODEL is optional fallback only when the user selected salpx video
```

Use `scripts/salpx_production_client.py` as the default public-safe helper:

```bash
python scripts/salpx_production_client.py --env .env image \
  --model gpt-image-2.5-sunburst \
  --prompt "<storyboard or first-frame prompt>" \
  --size 1024x1792 \
  --out-dir outputs/images \
  --name ep01-shot01
```

Model mappings:

```text
gpt-image-2.5-sunburst -> gpt-image-2.5-sunburst (default)
gpt-image-2 / gpt-image2 -> previous generation, optional
gpt-image-2.5-flare / gpt-image-2.5-1k -> optional salpx variants
omni / salpx omni -> omni_flash
gemini omni -> gemini_omni_flash
seedance2-mini-480p -> seedance-2-mini-480p
veo -> the exact salpx console model ID, recorded in manifest
```

Generation rules:

- Image generation uses `POST /images/generations` and saves either `b64_json` or downloaded image URLs into the project directory.
- salpx video generation is the default and only production video route (Wan 3.0). No other video host is allowed.
- Do not echo or write real API keys. Real keys stay only in `.env`, shell env, or CI secrets.
- Every generated file must be copied into the project directory and recorded in the manifest.
- Every downloaded video must be inspected for actual duration, width, height, bytes, and whether it can enter final composition.

## Video Model Rules

Always choose the video model route before writing generation prompts.

Do not reuse one generic prompt across Wan 3.0, Omni, Seedance2, and Veo. Each model has different duration assumptions, reference behavior, motion tolerance, audio behavior, and review risks.

Model route table:

```text
salpx_wan3:
  role: default raw video generation route for TJ Short after salpx first-frame/image production
  duration: integer 2-30 seconds, billed per second; default 5s for trial clips, 8-10s for story beats, up to 30s only when the shot is written as one continuous take
  best_for: 9:16 vertical short-drama clips, 10-30s continuous takes, product handling, multi-reference identity lock, native audio with lip sync
  prompt_style: script-locked target-locale prompt, camera behavior + action + sound, no extra props, tag references as 图1/图2/视频1/音频1
  modes: text_to_video (prompt only), first_frame (input_reference / metadata.media first_frame), first_last_frame (first_frame + last_frame), reference (reference_image x10 / reference_video x5 / reference_audio x5 / file / link)
  review_focus: task status, downloaded bytes, actual duration/size, containment diff, locale mismatch, audio/lip-sync accuracy

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
model_route: salpx_wan3 | omni_flash | seedance2 | veo | other
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
- High-conflict episode script with dialogue/action IDs
- 12-shot production table
- `保真核对.md`: coverage ledger and containment diffs
- Three first-frame prompts or images
- Clip contracts
- Reference role map
- `salpx / omni_flash` prompt pack
- salpx Wan 3.0 prompt pack and job/download record
- Generation manifest
- Voiceover and caption list
- Caption plan
- US locale manifest and `locale_mismatch_status` when target region is US
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
