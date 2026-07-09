# Changelog

## short-drama-ecommerce v0.8.30

Script fidelity and traceability update, triggered by two real production failures in the same episode: a shot table silently dropped 2 of 4 script dialogue lines with no shot ever picking them up, and a first-frame generation added an unrequested prop (a physical invitation card the script never described) that survived review and was inherited into the final video.

- Added `docs/methodology.md` Section 18, "Script Fidelity and Traceability": diagnoses why a multi-stage generation pipeline (script -> shot table -> first frame -> video prompt) loses content and gains unrequested content unless every stage carries a checksum back to the source script. Root cause: no single source of truth, forward-sufficiency-only review, and a "summarize, then regenerate" pattern that only holds the model responsible for what it was shown, not the original source.
- Added dialogue/action ID tagging (`[D-<scene>-<n>]`, `[A-<scene>-<n>]`) required in the episode script.
- Added a coverage ledger required at the end of Phase 2, mapping every script ID to a shot or a stated deliberate cut. 100% coverage (no `LOST` entries) is a hard gate before Phase 3.
- Added a `SOURCE ANCHOR` block requirement: every Phase 4/5 prompt document must open with the exact tagged script lines the shot derives from, turning "regenerate against a paraphrase" into "regenerate against the source."
- Added a containment diff check for every image/video generation: MUST HAVE / MUST NOT HAVE lists on the prompt, plus a mandatory "what did the output add that the prompt never asked for?" review field that can never be left blank. First-frame drift is a hard gate; video-level drift is a soft gate (record + human decides) unless it violates an explicit MUST NOT HAVE item, which always escalates to blocking.
- Added `保真核对.md` to Required Deliverables.
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
