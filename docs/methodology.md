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

## 16. Cinematic Shot-Design Language (Seven Elements)

AI short drama looks like a slideshow when every shot only proves the picture is pretty. Cinematic feel comes from what a shot does to the audience and how it connects to the shot before and after it.

Before writing camera work for a shot, answer:

```text
what information does this shot deliver?
what emotion does it produce?
how does it relate to the previous shot?
does it move the story forward?
does it make the next shot worth waiting for?
```

Seven elements to set per shot:

```text
1. 景别 frame size (psychological distance)
   远景 extreme wide: environment, world, isolation
   全景 wide/full body: full-body action, spatial relation
   中景 medium: dialogue, everyday narrative
   近景 close: emotional intensity
   特写 close-up: detail, inner change
   大特写 extreme close-up: shock, fear, key clue

2. 角度 camera angle (psychological position)
   平视 level: equal, restrained
   仰拍 low angle: power, heroism
   俯拍 high angle: helpless, isolated
   侧面 profile: distant, observing
   背影 back view: unknown, lonely, departure
   主观视角 POV: immersive, tense

3. 构图 composition (directs attention)
   三分法 rule-of-thirds: dialogue, walking, everyday narrative, natural breathing room
   居中构图 centered: ritual, pressure, character entrance, fate-weight scenes
   留白构图 negative space: loneliness, loss, emptiness, waiting, helplessness

4. 光影 lighting (sets mood)
   柔光 soft: warm, romantic, memory
   硬光 hard: tense, conflict, danger
   逆光 backlight: mysterious, dreamlike, lonely
   侧光 side: complicated, conflicted, suspenseful
   顶光 top: oppressive, cold, uneasy
   低光 low light: horror, strange, threatening

5. 色调 color grade (emotional register)
   暖色调 warm -> tenderness, nostalgia, intimacy -> romance, family, memory
   冷色调 cool -> distance, reason, loneliness -> suspense, sci-fi, urban
   低饱和 desaturated -> restraint, realism, oppression -> drama, crime, bleak
   高饱和 saturated -> dreamlike, exaggerated, fairytale -> fantasy, comedy, youth

6. 动势 camera movement (makes the frame happen)
   推进 push-in: entering, focusing attention
   拉远 pull-out: detaching, revealing scale
   跟随 follow: putting the audience inside the action
   摇移 pan/drift: exploring, discovering

7. 节奏 pacing (controls the audience's breathing)
   快剪 fast cut: tension
   慢镜 slow motion: emotion
   停顿 hold/pause: reflection
   切黑 cut to black: negative space, ending a beat
```

Universal pacing law:

```text
shot duration should shrink while emotional intensity rises
alternate tight and loose rhythm; a held pause carries more weight than another quick cut
sound and picture rhythm should move together, not picture cuts alone
```

Standard emotional arc for an episode or a scene block:

```text
铺垫期 setup -> 发展期 build -> 冲突期 conflict -> 高潮期 peak -> 回落期 release -> 收尾期 close
```

### Four Reusable Scene Formulas

Use these as starting templates for the shot production table's `camera:` and `emotion_shift:` fields (Section 6), then adapt to the actual role/scene/evidence subjects. Do not paste a formula verbatim without matching it to the current beat's narrative job.

```text
情绪递进 emotional build-up:
远景(交代环境) -> 中景(建立人物) -> 近景(捕捉情绪) -> 特写(强调线索) -> 停顿(制造悬念)

悬疑 suspense:
冷色调 + 低照度光影 + 前景遮挡 + 缓慢推进 + 角色停顿 + 关键物体特写 + 突然切黑

浪漫 romance:
暖色调 + 柔光 + 浅景深 + 慢动作 + 眼神特写 + 环境光斑 + 镜头缓慢环绕

压迫 pressure/threat:
低角度仰拍 + 居中构图 + 硬光阴影 + 低饱和色调 + 人物缓慢逼近 + 镜头轻微后退 + 节奏逐渐加快
```

### Avoiding the "PPT Look"

AI short drama looks flat and slide-like when shots have no spatial layers. Common mistakes:

```text
character always dead-center
background is decoration only, has no narrative job
frame is too full, no breathing room
subject has no relationship with environment
every frame looks like a poster, not a shot
missing foreground/midground/background layering
```

Fix by giving every shot three depth layers:

```text
foreground: doorframe, curtain, tree shadow, passerby, blurred object
midground: character action
background: environment info, lighting, architecture, weather
```

Also vary frame size within a scene instead of holding medium shot for the whole sequence. Example progression for "character returns to an empty room":

```text
远景: character at the doorway, space feels large and cold
全景: character walks slowly into the room
中景: character stops at the table, sees an old photo
近景: expression changes
特写: fingertip brushes dust off the photo
```

This progression carries more story than one static "character standing in room" shot.

## 17. Camera-as-Witness Prompt Law

The strongest AI video prompts do not describe "a beautiful finished picture." They describe a camera recording a real event as it happens, including the camera's own limitations. Drop the "a camera is on-site recording an event" framing and shot logic, timeline logic, and spatial-layer logic all weaken together — keep that framing as the base assumption for every prompt, then decide how much documentary imperfection fits the shot's style.

### Rule 1 — Describe the Shooting Process, Not the Finished Result

Do not write "beautiful picture, perfect composition, soft lighting, cinematic color" as the whole instruction. Write what the camera is doing and where it is imperfect. Realism comes from imperfection, not from a flawless composition.

```text
use: handheld micro-shake, focus hunting/racking, exposure drifting, mild compression noise/grain
avoid (as the only instruction): "the picture is beautiful", "perfect composition", "soft lighting", "cinematic color"
```

This rule is a strong fit for documentary, found-footage, hidden-camera, or emotionally raw handheld scenes. For glossy product hero shots or polished romance/beauty shots, use it selectively — for example a slight handheld shake during a tense confrontation, not during a clean product close-up. Do not apply it as a blanket rule to every shot in a polished commercial short drama.

### Rule 2 — Use Exclusion to Set Boundaries

For every few things a scene "has," name at least one thing it must not have. This keeps the model from drifting toward generic or era-mismatched details.

```text
example - old apartment corridor scene:
has: clothesline, utility pole, potted plant, old wall, worn furniture, dim light
has not: modern storefronts, ads/billboards, modern electronics
```

### Rule 3 — The Timeline Must Include Camera Behavior, Not Just Character Action

Break the shot into short time segments. Each segment should combine what the character does with what the camera does technically, plus environment interaction. Do not compress the whole shot into one line of character action only.

```text
weak:
00:00-00:15 the girl walks in and finds the envelope

strong:
00:00-00:03 girl walks into the corridor (handheld follow, shake)
00:03-00:07 the light flickers (exposure drifting)
00:07-00:10 focus racks to the envelope (focus hunting)
00:10-00:15 girl stops (frame micro-shake, cut to black)
```

### Full Prompt Structure Formula

Combine six blocks when writing a director-level shot prompt:

```text
镜头语言 shot language: frame size + focal length + camera position + movement type + duration
光影色彩 light & color: light source + light ratio + color grade + mood
场景细节 scene & detail: setting + props + material + environment detail
角色表演 character performance: look + action + expression + emotion
情绪风格 emotional style: emotional register + art style + genre
技术参数 technical params: aspect ratio + quality + model + other flags
```

Weak baseline prompt: "a girl works in an office, camera looking at her." (flat, low information, low controllability.)

Director-level prompt example:

```text
中景，35mm 电影镜头，女孩坐在靠窗办公桌前，侧脸看向屏幕，窗外城市阴天，柔和自然光从侧面打入形成柔和侧逆光，
背景浅景深虚化，前景有模糊绿植，桌上有咖啡杯和笔记本，整体色调冷静克制，氛围专注略带疲惫，
镜头缓慢微推进，时长4秒，电影级光影，真实细节，微表情自然。
```

### How This Fits TJ Short's Existing Rules

- Apply the seven shot-design elements and the four scene formulas when filling the `camera:` and `emotion_shift:` fields of the shot production table (Section 6).
- Treat camera-as-witness rules 1-3 as an optional realism layer on top of the existing Seedance2 motion rules (Section 9) and model routing rules (Section 10), not a replacement for them. Seedance2's "one camera move per shot, restrained motion" rule and rule 1's "describe imperfection, not perfection" rule reinforce each other.
- Do not apply rule 1's handheld-imperfection language to official Seedance2 face-compliance candidates (`face_pencil_strong/medium`, `blur_feature`, Section 15). Those candidates already carry strict compliance constraints and should stay clean of camera-defect language unless the shot's story specifically calls for a shaky, threatened point of view.
- Run the PPT-look check before finalizing a first-frame grid: does every shot have foreground/midground/background layers, and does frame size vary across the 12-shot sequence instead of holding medium shot throughout?

## 18. Script Fidelity and Traceability

TJ Short's production pipeline (script -> shot table -> first frame -> video prompt) is a chain of lossy transformations: each stage turns a high-detail source (full script prose, first-frame pixels) into a low-detail carrier (a handful of shot-table fields, one English prompt sentence). Loss is not the problem — every compression step loses something. The problem is that, without this section's rules, no stage carries a checksum, so nothing catches what got dropped or what got silently added.

This produces two distinct failure modes:

```text
completeness loss: a script line (dialogue or key action) never lands in any shot table entry
containment drift: an image/video generation adds an element the prompt never asked for, and it survives review because review only checks "is what I wanted present," not "is anything present that I did not ask for"
```

### Why This Is Structural, Not a One-Off Oversight

Three architectural gaps cause this, and all three exist because each stage is generated by summarizing the previous stage's output rather than tracing back to the original script:

```text
1. no single source of truth: script, shot table, and prompts become three peer documents; once the shot table exists, downstream stages treat it as the source and never re-check the script
2. forward-sufficiency checks only, no backward-conservation checks: every stage's implicit review question is "does this have enough for the next step," which cannot detect loss (a shot table missing two lines of dialogue still has enough fields to generate an image) or drift (an extra prop in a first frame does not break the next stage's inputs)
3. human review defaults to checklist confirmation (is what I wanted here) and structurally under-performs subtraction review (is something here that I did not want) unless a check explicitly forces the subtraction question
```

The deepest cause: a "summarize, then regenerate" pipeline makes each generation step responsible only for the summary it was shown, never for the original source it never saw. The model writing the shot table has no way to feel that it dropped two lines of dialogue, because it was never shown a script with those lines individually accounted for. Fixing this requires forcing every downstream stage to carry the source forward, not just its summary.

### Three Mechanisms

**1. Dialogue/action ID tagging + coverage ledger (prevents loss).** When writing the episode script, tag every dialogue line and every plot-relevant action with a stable ID: `[D-<scene>-<n>]` for dialogue, `[A-<scene>-<n>]` for key non-dialogue actions.

```text
[D-S3-01] 苏晴："想什么呢，请柬都不回？"
[D-S3-02] 林晚："回什么，随便去看看就行。"
[D-S3-03] 苏晴（朝衣柜方向努努嘴）："随便？你这半年衣柜里就没添过一件新东西。"
[D-S3-04] 林晚（转身，语气防备）："我乐意。"
[A-S3-01] 手机屏幕亮起婚礼请柬确认消息（一条手机短信，非纸质）
```

Every shot table `dialogue_or_lip_sync` field must cite the IDs it carries, not just paraphrase them. After the shot table is written, produce a coverage ledger that lists every ID from the script and where it landed:

```text
| source ID | landed in | status |
| D-S3-01   | SHOT-04   | covered |
| D-S3-03   | (none)    | LOST |
```

Every ID must resolve to `covered` or `deliberately cut (reason: ...)`. `LOST` (no shot, no stated reason) is not an allowed terminal state. Coverage must be 100% before the shot table counts as done — this is deterministic text matching (does this ID string appear somewhere downstream), not a judgment call, so it costs no extra model reasoning.

**2. Containment diff per generation (prevents drift).** Every image/video prompt must carry two explicit lists: MUST HAVE (what the prompt requires) and MUST NOT HAVE (what must not appear — this is the existing exclusion-list technique from Section 17, now mandatory rather than optional, applied specifically to entities the model tends to invent: physical stand-ins for digital objects, extra people, extra props). After each generation, fill a containment check with a mandatory, non-skippable field:

```text
what did the output add that the prompt never asked for? (must answer; write "none" if nothing)
```

That field is the whole point: making "nothing extra" an explicit answer forces the subtraction review that unprompted checklist-style review structurally skips. Verdict is binary: `match` or `drift`. Drift means regenerate or tighten the prompt — no "close enough, ship it."

**3. Source anchor block (fixes the pipeline itself).** Every Phase 4/5 prompt document must open with a read-only block that pastes the exact tagged script lines that shot is derived from, before the actual prompt text:

```text
# SOURCE ANCHOR (from script, read-only)
[A-S3-01] 手机屏幕亮起婚礼请柬确认消息（一条手机短信，非纸质）
---
# shot prompt
...
```

This is the mechanism that fixes the root cause rather than just catching symptoms: it turns "summarize, then regenerate" into "regenerate against the source," because the generation step now has the original line in front of it, including its exclusion constraint (non-纸质), not just a paraphrase.

### Gate Placement

```text
coverage ledger (script -> shot table): hard gate, end of Phase 2 — cheap, catches loss at the point where it is still free to fix, and loss compounds if it survives into images/video
source anchor block (shot table -> Phase 4/5 prompts): hard gate — near-zero cost (copy-paste), and it is the precondition that makes the other two mechanisms possible
first-frame containment diff (Phase 4): hard gate per cell — a drifted first frame gets inherited and amplified by image-to-video, so catching it here trades a cheap image regeneration for an expensive video regeneration
video containment diff (Phase 5): soft gate (record + human decides) — regenerating a video is the most expensive retry in the pipeline, so default to recording drift severity rather than auto-blocking; escalate to a hard block only when the drift violates an explicit MUST NOT HAVE item
```

Rule of thumb: gates get stricter the closer they sit to the source and the cheaper they are to enforce; gates get looser the closer they sit to the expensive end of the pipeline, except for explicit MUST NOT HAVE violations, which always block regardless of stage.

### Cost Discipline

All three mechanisms are designed to add zero extra model calls. The coverage ledger and source anchor are extra output inside a generation TJ Short already runs (the shot table pass, the prompt-writing pass) — a few hundred extra tokens, not a new pass. The containment diff's checklist is generated alongside the prompt; filling it in happens during the human review that already occurs when looking at a produced image or video. The only real cost increase is retaking first frames that fail containment — and that is a deliberate trade: a cheap image retake instead of an expensive video-level failure discovered downstream, which is a net cost reduction, not an increase.

Do not add a dedicated LLM call whose only job is comparing script to shot table, or a computer-vision pass to detect drifted objects in first frames. ID-string matching makes coverage a deterministic lookup, not a judgment call; a human glance at a short, forced-field checklist is enough to catch containment drift. Keep the fidelity record for one episode in a single `保真核对.md` rather than fragmenting it across many small files.
