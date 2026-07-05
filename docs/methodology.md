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

## 6. Clip Contract

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

## 7. Reference Role Map

Each reference asset should have one main job:

- first frame controls composition
- product image controls product shape only
- caption file controls post-production subtitles only
- video reference controls motion rhythm only

Do not let one reference control identity, scene, motion, style, product, and dialogue all at once.

## 8. One-Variable Retake

When a clip fails, change only one thing:

- one prompt clause
- seed
- reference image
- generation mode
- shot split
- post-production fix

If the same issue appears twice, stop rerolling and rewrite the clip contract or split the shot.

## 9. Seedance2 Visible-Face Repair

Short drama often needs facial acting. If Seedance2 rejects a realistic fictional-actor first frame as possible real-person content, do not immediately remove the face.

Use a character-reference repair route:

1. `face_pencil`: stylize only the face regions with colored-pencil/sketch treatment, while keeping body, wardrobe, action, pet, props, and scene photographic.
2. `blur_feature`: use a blurred-face main composition image plus a facial-feature sheet. The main image controls composition, wardrobe, body action, props, and scene. The feature sheet controls fictional facial traits.
3. If both fail, create a fuller character design board or three-view reference before more submissions.

This route is only for self-owned fictional virtual characters. It is not for unlicensed real people, celebrities, influencers, or public figures.
