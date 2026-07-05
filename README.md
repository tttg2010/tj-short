# TJ Short

TJ Short is a lightweight workflow for ecommerce short dramas: write a short-drama story first, then let the product enter as evidence, memory, relationship proof, or a turning point.

The repo is intentionally public-safe. It contains methodology, prompt templates, a sanitized sample episode, and a generic `salpx / omni_flash` submission helper. It does not include private product images, generated videos, API keys, task IDs, download URLs, local absolute asset paths, or `.env` files.

## What This Project Does

- Builds ecommerce short-drama scripts that avoid the common "pain point -> product -> happy customer -> CTA" ad pattern.
- Keeps the first half of each episode focused on people, pets, conflict, pressure, and misunderstanding.
- Introduces the product later as proof of a changed behavior or revealed truth.
- Uses `salpx / omni_flash` as a 10-second fixed-duration image-to-video route.
- Treats captions as post-production assets: Omni raw clips should not burn in subtitles.

## References

This project was shaped by and openly credits these references:

- **OnlyShot**: ecommerce short-drama production thinking, especially product-as-proof and projectized delivery.
- **short-drama**: short-drama structure, episode beats, storyboard and video-production discipline.
- **Emily2040/seedance-2.0**: clip-contract style production thinking, state tracking, reference-role separation, and one-variable retake discipline.

This repository is not an official distribution of those projects. It is a practical, sanitized working template inspired by them.

## Core Rule

Do not make a product the hero.

Let the audience care about a person, pet, relationship, or consequence first. Then use the product to prove what changed.

## Folder Structure

```text
.
├── docs/
│   ├── methodology.md
│   └── privacy-and-release.md
├── examples/
│   └── xiderdl-lucky/
│       └── ep01-high-conflict.md
├── prompts/
│   └── omni-fixed-10s-template.md
├── scripts/
│   └── submit_salpx_omni_i2v.py
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Quick Start

1. Pick one product and one emotional pain point.
2. Write three brief concepts, then choose one.
3. Write one 60-90 second episode with high conflict and dense dialogue.
4. Create three test first frames: hook, product evidence, ending hook.
5. Submit only those three `salpx / omni_flash` test clips first.
6. Review the result before generating the full episode.

## salpx / omni_flash Rule

`omni_flash` is treated as a fixed 10-second model path in this workflow.

Even if the edited episode uses 6-8 second information beats, each generated raw clip should be submitted with:

```json
{
  "model": "omni_flash",
  "duration": 10,
  "aspect_ratio": "9:16"
}
```

Cut pacing belongs in post-production, not in the salpx submission duration.

## Public Safety

Before publishing work based on this repo:

- Do not commit `.env`, real keys, private URLs, API responses, or downloaded task JSON.
- Do not commit raw user product assets unless you own the rights and intentionally want them public.
- Do not commit generated videos by default.
- Replace local absolute file paths with relative placeholders.
- Keep product claims compliant: avoid treatment, guaranteed results, instant recovery, or medical promises.

