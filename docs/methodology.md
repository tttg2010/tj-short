# Methodology

## 1. Start With Short Drama, Not Product Copy

The first question is not "How do we sell this?"

The first question is:

> Why would the audience care about this person, pet, relationship, or consequence?

The product enters later as proof. It should help the audience understand a truth that was hidden by the conflict.

## 2. Three-Layer Structure

1. Short-drama layer: character, pressure, misunderstanding, consequence, relationship change.
2. Evidence layer: product as proof, memory, relationship token, behavior record, or turning point.
3. Conversion layer: light CTA after the emotional beat, never replacing the story ending.

## 3. First-Half Product Ban

In the first 30-50% of an episode, avoid:

- product functions
- price
- SKU details
- feature lists
- direct CTA
- "this product solves everything" narration

The product can appear as an ordinary prop, but it should not be explained early.

## 4. High-Conflict Episode Beat

A fast ecommerce short-drama episode can use this rhythm:

```text
0-5s: external pressure or relationship threat
5-20s: confrontation through dialogue
20-40s: misunderstanding intensifies
40-55s: truth begins to appear
55-70s: product enters as evidence or action
70-85s: relationship turn and next hook
```

## 5. Product Evidence Rules

Good product evidence:

- shows a real action
- fits the character's changed behavior
- can be seen on screen
- does not rely only on narration
- does not claim guaranteed results

Weak product evidence:

- just shows a logo
- explains features too early
- solves the problem immediately
- uses fake data without process
- can be swapped with any similar product

## 6. Subject Libraries Before Shot Prompts

TJ Short should follow a subject-library workflow inspired by canvas-based short-drama systems such as AniShort.

The key idea: do not ask every shot prompt to reinvent the same actor, pet, room, product, and proof object. Create stable subject libraries first, then make each shot reference those subjects.

Use four libraries:

- Role library: stable identity for every recurring person or pet. Include age range, identity, face/fur traits, hair, wardrobe, expression baseline, relationship power, and product-contact behavior.
- Scene library: stable location entries. Include layout, light, time, mood, camera anchors, and safety notes.
- Product/prop library: product pack, bowl, phone, receipt, report, accessory, package, or tool. Include shape, color, label visibility, handling rule, and what must not change.
- Evidence library: ecommerce-specific proof objects. Include feeding action, before/after behavior, order record, ingredient card, phone chat, packaging detail, comparison table, or report-style note. Each entry must say which misunderstanding it proves or overturns.

Then build a shot production table:

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

This keeps character identity and product proof stable while letting each shot prompt focus on movement, emotion, camera, and dialogue.

## 7. Character Dossier Boards

For important recurring roles, a single vertical portrait is not enough. Generate a character dossier board so later shots can preserve identity, wardrobe, expression range, and product-contact behavior.

A character dossier board should include:

- main portrait
- front, side, and back full-body views
- expression sheet
- wardrobe/material close-ups
- product-contact or prop-contact close-ups
- visual memory points such as eyes, hair, hands, accessories, pet interaction, or package handling
- concise info panel: name, age range, role, relationship, emotional baseline, and product-contact behavior

Use the dossier board as the role subject reference. Later first-frame and video prompts should reference the role ID and board, then focus only on the current shot's action, emotion, camera, dialogue, and continuity locks.

Do not use real celebrities, public figures, influencer likenesses, private people, or readable private data in dossier boards. Use fictional characters only.

Production nuance for Seedance2:

- The dossier board is the master for design, filing, review, and extraction.
- For direct Seedance2 video generation, prefer extracted single-person references over the full multi-view board.
- Recommended extracted set: face close-up for identity, full/half-body image for wardrobe and posture, scene image for environment, optional motion video for camera/action rhythm, optional audio for ambience or voice.
- If a specific provider route proves that full dossier boards work better, use that route deliberately and record it in the manifest.

Hard gate: if the project uses Seedance2 with recurring visible human roles, do not proceed to first-frame grids, image-to-video prompts, or video submission until these exist:

```text
角色主体库.md
人物备案板需求.md
Seedance2参考包计划.md
```

If images have not been generated yet, the dossier-board spec is still required. A generic reference-asset table does not replace it.

## 8. Seedance2 Filed Role Assets

For Seedance2 routes with visible human faces, a character board alone may not be enough. Some short-drama platforms use a filing step that turns a role board into a provider-side asset record.

Working interpretation from AniShort-style boards:

- the filing status is loaded as project asset data
- a successful filing returns a platform asset number
- filed assets are scoped to the platform/project/user route
- downloading and re-uploading an image can break the filed status
- a watermark is not the filing record

Use this chain when the provider supports it:

```text
fictional role design
-> character dossier board
-> provider/platform filing
-> filed asset ID and source asset URL
-> Seedance2 generation using the filed asset reference
```

Public examples should use placeholders such as `asset-YYYYMMDDHHMMSS-xxxxx`. Do not publish real asset IDs, signed URLs, task IDs, or private upload paths.

If hair, clothing, age, facial structure, or other strong identity cues change, treat it as a new role-board version and file again if the provider requires it.

## 9. Seedance2 Prompt Packaging

Seedance2 should receive clear media ordering and subject definitions.

Key rule from official documentation: even when a request passes an asset as `asset://<asset ID>`, the prompt still refers to that media as `图片1`, `视频1`, or `音频1` according to request order. Do not use the asset ID as the subject name inside the prompt.

Recommended package for a visible-face ecommerce short-drama shot:

```text
图片1: role face close-up
图片2: role full/half-body wardrobe reference
图片3: scene reference
图片4: product reference
视频1: optional motion/camera reference
音频1: optional ambience, voice, or rhythm reference
```

Prompt skeleton:

```text
将图片1中的面部特征、图片2中的服装造型定义为林夏。
图片3作为客厅场景参考，图片4只用于产品外形参考。

镜头1：固定近景，林夏坐在沙发边缘，手指攥紧包装袋，眼神躲闪，低声说{我不是故意忘记的}。
镜头2：镜头缓慢推近，林夏抬头看向老狗，肩膀逐渐放松，把包装袋放到碗旁。

全程高清真实摄影质感，人物面部稳定不变形，动作自然连贯，避免生成任何字幕、Logo、水印或可读文字。
```

Use a few ordered shots rather than a whole episode script. Prefer small continuous actions and one camera move per shot. Use `first_frame` / `last_frame` roles when strict start/end frames matter, and `return_last_frame=true` when chaining clips.

## 10. Model Routing

Pick the model route before writing prompts. TJ Short should not use one generic video prompt across all providers.

```text
omni_flash:
  fixed 10-second raw clips
  driven mainly by the first frame
  prompt focuses on motion, camera, emotion shift, lip-sync, and continuity locks

seedance2:
  model/provider-specific duration
  supports image, video, audio, text references
  prompt uses ordered media labels such as 图片1, 视频1, 音频1
  needs explicit subject definitions and careful visible-face asset handling

veo:
  provider-specific duration and reference behavior
  prompt should focus on cinematic scene, camera/lens, lighting, motion, continuity, and constraints
  do not assume Seedance2 media-label syntax unless the provider explicitly supports it
```

Recent TJ Short work focuses on Seedance2, but that does not change Omni or Veo rules. The manifest must record `model_route`, `duration_rule`, `reference_rule`, `prompt_syntax_rule`, `face_review_rule`, `output_ratio`, and `audio_mode`.

## 11. Clip Contract

Before generating video, define each clip:

- narrative job
- felt intent
- this clip only
- reserved for later
- planned start state
- planned end state
- continuity locks
- allowed changes

This keeps prompts from trying to generate the whole episode in one clip.

## 12. Reference Role Map

Each reference asset should have one main job:

- first frame controls composition
- product image controls product shape only
- caption file controls post-production subtitles only
- video reference controls motion rhythm only

Do not let one reference control identity, scene, motion, style, product, and dialogue all at once.

## 13. One-Variable Retake

When a clip fails, change only one thing:

- one prompt clause
- seed
- reference image
- generation mode
- shot split
- post-production fix

If the same issue appears twice, stop rerolling and rewrite the clip contract or split the shot.

## 14. Grid-First First-Frame Production

Default first-frame production should be grid-first, not 12 standalone generations.

Standard flow:

```text
4x3 contact sheet
-> cut into EP01-01.png through EP01-12.png
-> run layout and content precheck
-> retake only failed cells or selected trial cells
```

Why:

- one generation call can cover the whole episode rhythm
- the 12 frames share lighting, wardrobe, scene grammar, and visual continuity
- cost is lower than generating 12 standalone images upfront
- cutting from a fixed grid makes review and manifest tracking easier

Required outputs:

```text
storyboards/contact_sheet.png
storyboards/cut_report.md
first_frames/EP01-01.png
...
first_frames/EP01-12.png
```

Standalone first-frame generation is allowed only when:

- the user explicitly asks for standalone frames
- the grid cannot produce a cuttable 4x3 layout after retry
- a specific cell fails precheck
- a selected trial clip needs a higher-quality retake

Do not justify 12 standalone first-frame generations by saying they are "cleaner for Seedance2". Clean Seedance2 frames should come from a clean grid and selective retakes.

## 15. Seedance2 Visible-Face Candidate Flow

Short drama often needs facial acting. For Seedance2 visible-person shots, do not wait until video submission fails. The face-compliance route starts at the grid/first-frame stage.

Use a character-reference and candidate route:

1. If the provider supports role filing, file the dossier board and use the filed asset reference.
2. Extract single-person Seedance2 references from the role board: face close-up plus full/half-body wardrobe reference.
3. Define media by order in the prompt: `图片1`, `图片2`, `视频1`, `音频1`.
4. Generate three candidates for the same shot: `face_pencil_strong`, `face_pencil_medium`, and `blur_feature`.
5. `face_pencil`: stylize only the face regions with colored-pencil/sketch treatment, while keeping body, wardrobe, action, pet, props, and scene photographic.
6. `blur_feature`: use a blurred-face main composition image plus a facial-feature sheet. The main image controls composition, wardrobe, body action, props, and scene. The feature sheet controls fictional facial traits.
7. Precheck candidates one by one. Among passing candidates, choose the one with the most complete face information and clearest acting.
8. Do not resubmit a failed frame unchanged. If all three candidates fail, record the reasons, then change the reference package or ask the user whether the shot design should become product-only/faceless.

No-person product frames are valid for API smoke tests and product-evidence shots only. They are not the default fallback for visible-face acting shots.

This route is only for self-owned fictional virtual characters. It is not for unlicensed real people, celebrities, influencers, or public figures.
