# Changelog

## short-drama-ecommerce v0.9.2

Banner 换图。删除 `assets/salpx-banner.svg`（矢量版，画面上仍写着已下线的 MiniMax H3），替换为 `assets/salpx-banner.png`（1280×427）。

- 新图由 salpx `gpt-image-2.5-sunburst` 一次生成，文字与主视觉在同一张图里出，没有后期单独叠加排版。
- 画面内容对齐当前链路：`salpx` 生图 + Wan 3.0 生视频、2–30 秒直出、原生音轨、口型同步。
- 中英 README 的图片引用与 alt 文案同步更新。

## short-drama-ecommerce v0.9.1

默认图片模型从 `gpt-image-2` 升级为 `gpt-image-2.5-sunburst`。

- `.env.example`、`scripts/salpx_production_client.py`、SKILL.md 的提示词模板与 SOP 步骤，`SALPX_IMAGE_MODEL` 默认值统一改为 `gpt-image-2.5-sunburst`。
- 补充可用图片模型变体说明：`gpt-image-2.5-flare`、`gpt-image-2.5-1k`，以及 `XY-` 前缀的 1k/2k/4k 线路；`gpt-image-2` 保留为上一代可选。
- 接口形态不变：仍是 `POST /v1/images/generations`，`--size` / `--out-dir` / `--name` 参数不变。已有 `.env` 里写死 `SALPX_IMAGE_MODEL=gpt-image-2` 的项目继续可用。
- 凭证不变：一个 `SALPX_API_KEY` 同时覆盖图片与视频。

## short-drama-ecommerce v0.9.0

视频层迁移：MiniMax H3 下线，salpx Wan 3.0 上线。对仍在调用 H3 路线的项目属破坏性变更。

- 默认且唯一的视频路线改为 salpx Wan 3.0（`wan3.0-480p` / `wan3.0-720p` / `wan3.0-1080p`，另有独立线路 `wan3.0-hm-*`）。图片与视频共用同一个凭证 `SALPX_API_KEY`。
- 新增 `scripts/wan3_video_client.py`（纯标准库）：`video` / `status` / `download` / `models` 四个子命令；支持 `first_frame`、`last_frame`、`reference_image`×10、`reference_video`×5、`reference_audio`×5、`file`、`link`；本地素材自动转 base64；`--dry-run` 只校验和报价，不产生费用。
- 新增 `docs/wan3-api-production.md`：端点、模型与单价阶梯、按秒计费与参考视频预扣、素材组合规则、请求构造、轮询与下载、错误码表、提示词写法。
- 视频能力扩展：2–30 秒整数单镜直出、原生音轨、参考音频驱动的口型同步与演唱、多参考素材（图/视频/音频）身份锁定。
- 新增硬性成本门禁：每次提交前必须向用户说明模型、分辨率、出片秒数、是否带参考视频、以及算出的价格，取得同意后才提交。
- 删除 `scripts/h3_video_client.py`、`docs/h3-api-production.md`、`scripts/submit_salpx_omni_i2v.py`；`.env.example` 移除全部 `H3_*`；客户端对含 `zhongbiao` 或 `h3.` 的 base URL 直接报错退出。
- `scripts/salpx_production_client.py` 收窄为纯生图，`video` 子命令改为提示使用 Wan 3.0 客户端。
- `SKILL.md` 的视频生产章节整体重写为 `salpx Wan 3.0 Video Production Rule`，含价格阶梯、素材约束与 30 秒预算规则。
- 破坏性：仍调用 H3 路线、传入 `H3_API_KEY` 或解析 H3 任务返回体的项目，需迁移到 `SALPX_API_KEY` + `wan3.0-*`。

## short-drama-ecommerce v0.8.30

Script fidelity and traceability update, triggered by two real production failures in the same episode: a shot table silently dropped 2 of 4 script dialogue lines with no shot ever picking them up, and a first-frame generation added an unrequested prop (a physical invitation card the script never described) that survived review and was inherited into the final video.

- Added `docs/methodology.md` Section 18, "Script Fidelity and Traceability": diagnoses why a multi-stage generation pipeline (script -> shot table -> first frame -> video prompt) loses content and gains unrequested content unless every stage carries a checksum back to the source script. Root cause: no single source of truth, forward-sufficiency-only review, and a "summarize, then regenerate" pattern that only holds the model responsible for what it was shown, not the original source.
- Added dialogue/action ID tagging (`[D-<scene>-<n>]`, `[A-<scene>-<n>]`) required in the episode script.
- Added a coverage ledger required at the end of Phase 2, mapping every script ID to a shot or a stated deliberate cut. 100% coverage (no `LOST` entries) is a hard gate before Phase 3.
- Added a `SOURCE ANCHOR` block requirement: every Phase 4/5 prompt document must open with the exact tagged script lines the shot derives from, turning "regenerate against a paraphrase" into "regenerate against the source."
- Added a containment diff check for every image/video generation: MUST HAVE / MUST NOT HAVE lists on the prompt, plus a mandatory "what did the output add that the prompt never asked for?" review field that can never be left blank. First-frame drift is a hard gate; video-level drift is a soft gate (record + human decides) unless it violates an explicit MUST NOT HAVE item, which always escalates to blocking.
- Added `保真核对.md` to Required Deliverables.
- Added `US-Market Localization Hard Rule`: when the target region is 美国 / US / United States / TikTok Shop US / Amazon US, the Skill must rebuild the story, dialogue, character design, scene text, subtitles, CTA, and compliance wording for the United States market instead of translating Chinese ecommerce short-drama habits into English. US-locked artifacts that contain Chinese livestream/ecommerce jargon, RMB pricing, WeChat/private-message CTAs, Chinese default scenes, or direct-translated Chinese short-drama tropes must be marked `locale_mismatch_us_market` and fixed before first-frame or video generation.
- Added the current default production split: salpx `gpt-image-2` generates storyboard grids, first frames, and product-proof images; MiniMax H3 API generates raw video clips through `t2va`, `ref2va`, or `fl2va`. salpx video models remain optional fallback routes.
- Added `docs/h3-api-production.md`, `.env.example` H3 placeholders, and `scripts/h3_video_client.py` for public-safe H3 quote/submit/poll/download.
- Confirmed this adds no dedicated LLM calls: coverage is deterministic ID-string matching, containment diffs are filled during review that already happens, and the only real cost increase is retaking a cheap first-frame image instead of discovering drift in an expensive finished video.
- Source: architecture review by 肖老师 (xiao-laoshi-agent), commissioned after the two script-fidelity failures surfaced in a real project.

## short-drama-ecommerce v0.8.29

Cinematic shot-design update, distilled from a shared cinematography/prompt-engineering note on AI short-drama shot design.

- Added `docs/methodology.md` Section 16, "Cinematic Shot-Design Language (Seven Elements)": frame size, angle, composition, lighting, color grade, camera movement, pacing, plus four reusable scene formulas (emotional build-up, suspense, romance, pressure) and a PPT-look precheck (foreground/midground/background layering, varied frame size).
- Added `docs/methodology.md` Section 17, "Camera-as-Witness Prompt Law": describe the shooting process/imperfection instead of the finished picture, pair "has" lists with "has not" exclusion lists, and make timeline segments carry camera behavior, not only character action. Includes the six-block director-level prompt formula.
- Added `Cinematic Shot-Design Rule` to the skill with compact versions of both sections for direct use when filling the shot production table's `camera:`/`emotion_shift:` fields and writing video prompts.
- Clarified that the camera-imperfection language is a selective realism layer for documentary/handheld-style beats, not a blanket rule, and must not be applied to official Seedance2 face-compliance candidates (`face_pencil_strong/medium`, `blur_feature`).
- Updated Phase 2 and the default flow to require applying the shot-design rule before finalizing the 12-shot table and first-frame grid.

## short-drama-ecommerce v0.8.28

Grid-first first-frame production update.

- Added cost-control rule: generate one 4x3 storyboard/first-frame contact sheet first, then auto-cut 12 independent 9:16 first frames.
- Prohibited generating 12 standalone first frames upfront unless the user explicitly requests that workflow or the grid/cut method fails.
- Clarified valid standalone first-frame use cases: failed grid cells, selected retakes, or 3-shot trial-clip polish after grid review.
- Updated default flow language from "generate three first frames" to "generate 12-panel grid -> cut -> precheck -> retake selected cells".

## short-drama-ecommerce v0.8.27

Seedance2 visible-face first-frame workflow correction.

- Clarified that a no-person/product-only first frame is valid for API smoke tests or product-evidence shots only, not as the default replacement for a visible-face acting shot.
- Moved Seedance2 face handling fully into the grid/first-frame stage: each visible-person shot must generate three candidates before video submission.
- Standardized the candidate set: `face_pencil_strong`, `face_pencil_medium`, and `blur_feature` (`blurred_main + facial_feature_sheet`).
- Added precheck selection logic: test candidates one by one, record pass/fail and reason, then choose the passing candidate with the most complete face information and clearest acting.
- Repeated that failed images should not be submitted unchanged again; change treatment strength, reference package, or shot design instead.
- Repeated that full manga/anime/commercial storyboard style is preview-only and not an official Seedance2 first frame for live-action ecommerce short drama.

## short-drama-ecommerce v0.8.26

salpx API production update.

- Added `docs/salpx-api-production.md`, a concrete API guide for `gpt-image-2` image generation and salpx video generation.
- Added `scripts/salpx_production_client.py`, a reusable client with two commands:
  - `image`: calls `/v1/images/generations`, supports `gpt-image-2`, saves `b64_json` or downloaded image URLs.
  - `video`: calls `/v1/videos`, supports text-to-video and image-to-video, polls async tasks, downloads mp4, and writes result JSON.
- Added model mappings for production:
  - user-facing `gpt-image2` / `gpt-image-2` -> API `gpt-image-2`
  - user-facing `omni` -> API `omni_flash`
  - user-facing `seedance2-mini-480p` -> API `seedance-2-mini-480p`
  - Veo -> salpx console model ID, recorded in the manifest
- Added `.env.example` fields for `SALPX_IMAGE_MODEL` and `SALPX_VIDEO_MODEL`, while keeping `SALPX_OMNI_MODEL` for the older omni helper script.
- Added public-release rule: TJ Short must ship production scripts and salpx API docs, so a GitHub user can generate images and videos after adding their own key.
- Repeated the key-safety rule: real salpx API keys must stay in `.env` or runtime secrets and must not be committed, echoed, or written into prompts/manifests.

## short-drama-ecommerce v0.8.25

Seedance2 official prompt and production-reference update.

- Added Volcengine Seedance2 prompt rules: prompts must refer to media as `图片1`, `视频1`, `音频1` by request order, even when the request URL uses `asset://<asset ID>`.
- Clarified the production use of character dossier boards: keep them for design, filing, and review, but extract clean single-person references before Seedance2 video generation.
- Added the practical reference package: face close-up, full/half-body wardrobe image, scene image, optional motion-reference video, and optional audio.
- Added prompt structure for subject definition, ordered shot timing, restrained action, one camera move per shot, and global constraints.
- Added Seedance2 API production notes: use `first_frame` / `last_frame` for strict start/end frames, `return_last_frame=true` for continuous clips, `ratio=adaptive` when matching first-frame aspect ratio, and model-specific duration instead of Omni's fixed 10 seconds.
- Added model routing discipline: Omni, Seedance2, and Veo must use separate prompt shapes, duration rules, reference handling, and review strategies.
- Added a Seedance2 visible-human hard gate: role dossier deliverables must exist before first-frame grids or video prompts.
- Added strict workflow phase gate: startup, brief selection, project files, role dossier, storyboard, first-frame grid, and video prompt/submission are separate phases.
- Moved Seedance2 face handling earlier: official first-frame grids should use face-only `face_pencil`; full manga/anime/storyboard style is not an acceptable default fallback.

This update treats official guidance as a production signal, not a blind prohibition. Multi-view boards remain useful, but direct model submission should be decided by actual provider/model behavior and recorded in the manifest.

## short-drama-ecommerce v0.8.24

Seedance2 filed-role asset chain update.

- Added AniShort-style role filing insight: realistic human role references should be treated as platform-scoped filed assets when the provider supports filing.
- Documented that the key object is the provider-side filed asset record and asset ID, not a visible watermark.
- Clarified that downloaded and re-uploaded images may lose filing status; keep the original filed asset URL or provider asset reference.
- Added manifest fields for `filed_asset_id`, `filing_status`, `filing_scope`, `role_board_version`, and `source_asset_url`.
- Clarified the safe route: fictional role design -> character dossier board -> provider filing -> filed asset reference -> Seedance2 generation.
- Kept `face_pencil` and `blur_feature` as fallback repair methods when filing is unavailable or still rejected.

This update does not support fabricating asset IDs, reusing another creator's filed assets, or processing unlicensed real people, celebrities, influencers, public figures, or private people.

## short-drama-ecommerce v0.8.23

Character dossier board update.

- Added role-subject dossier board workflow learned from AniShort-style character boards.
- Key recurring roles should use a horizontal board with main portrait, front/side/back views, expression sheet, wardrobe/material details, product-contact details, and concise info panel.
- Clarified the difference between a single cinematic role portrait and a reusable character dossier board.
- Added prompt guidance so later shot prompts reference the approved role board instead of re-describing identity in every shot.
- README now includes a visible version history section so important updates are shown on the GitHub introduction page, not only in `docs/changelog.md`.

## short-drama-ecommerce v0.8.22

Seedance2 visible-face production update.

- Added AniShort-inspired subject-library workflow: role, scene, product/prop, and evidence libraries before shot prompts.
- Added a startup gate so `短剧带货启动` begins with product diagnosis and three briefs instead of a generic production package.
- Added install/update reminder to restart Codex three times in the user-facing instructions.
- Added salpx.com registration and API Key setup reminder for full video-generation testing from Codex.
- Added `face_pencil` for short-drama clips where facial acting is required: only face regions are stylized, while body, wardrobe, action, props, pet, and scene remain photographic.
- Added `blur_feature` for tougher multi-person or high-realism scenes: the main image keeps composition with blurred faces, and a facial-feature sheet supplies fictional character traits.
- Documented why faceless crops should not be the default when the scene depends on actor expression.
- Documented submission field guidance: keep the blurred main frame as the primary image and put feature sheets into the supported reference field.
- Expanded salpx model language beyond Omni: omni remains fixed 10 seconds, while Seedance2 and Veo follow their model rules.

This update is for fictional or self-owned virtual characters only. It is not a workflow for unlicensed real people, celebrities, influencers, public figures, or identity-review evasion.
