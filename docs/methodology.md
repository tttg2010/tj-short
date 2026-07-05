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

## 9. Clip Contract

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

## 10. Reference Role Map

Each reference asset should have one main job:

- first frame controls composition
- product image controls product shape only
- caption file controls post-production subtitles only
- video reference controls motion rhythm only

Do not let one reference control identity, scene, motion, style, product, and dialogue all at once.

## 11. One-Variable Retake

When a clip fails, change only one thing:

- one prompt clause
- seed
- reference image
- generation mode
- shot split
- post-production fix

If the same issue appears twice, stop rerolling and rewrite the clip contract or split the shot.

## 12. Seedance2 Visible-Face Repair

Short drama often needs facial acting. If Seedance2 rejects a realistic fictional-actor first frame as possible real-person content, do not immediately remove the face.

Use a character-reference repair route:

1. If the provider supports role filing, file the dossier board and use the filed asset reference.
2. `face_pencil`: stylize only the face regions with colored-pencil/sketch treatment, while keeping body, wardrobe, action, pet, props, and scene photographic.
3. `blur_feature`: use a blurred-face main composition image plus a facial-feature sheet. The main image controls composition, wardrobe, body action, props, and scene. The feature sheet controls fictional facial traits.
4. If both repair methods fail, create a fuller character design board or three-view reference before more submissions.

This route is only for self-owned fictional virtual characters. It is not for unlicensed real people, celebrities, influencers, or public figures.
