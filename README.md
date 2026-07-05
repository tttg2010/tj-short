# TJ Short

<a href="https://www.salpx.com">
  <img src="assets/salpx-banner.svg" alt="salpx 中转站：把首帧变成 10 秒短剧镜头" width="100%">
</a>

## 中文介绍

TJ Short 是一个面向「短剧带货」的公开安全工作流：先写人物、宠物、关系和冲突，再让产品作为证据、记忆、信物或转折点进入剧情。

它的目标不是把广告词套进剧情，而是让观众先关心一个人、一只宠物、一段关系，然后在关键时刻看见产品如何证明真相、改变行为或推动选择。

这个仓库包含：

- 短剧带货方法论
- 高冲突单集结构
- `salpx / omni_flash` 固定 10 秒图生视频模板
- 三镜试生思路：剧情钩子、产品证据位、结尾追更钩子
- 脱敏案例截图和脚本样例
- 公开发布前的隐私与 key 检查清单

> 注意：本仓库是公开安全版，不包含真实 API key、`.env`、私有产品素材、生成任务响应、下载链接或本地绝对路径。

TJ Short is a lightweight workflow for ecommerce short dramas: write a short-drama story first, then let the product enter as evidence, memory, relationship proof, or a turning point.

The repo is intentionally public-safe. It contains methodology, prompt templates, a sanitized sample episode, and a generic `salpx / omni_flash` submission helper. It does not include private product images, generated videos, API keys, task IDs, download URLs, local absolute asset paths, or `.env` files.

## What This Project Does

- Builds ecommerce short-drama scripts that avoid the common "pain point -> product -> happy customer -> CTA" ad pattern.
- Keeps the first half of each episode focused on people, pets, conflict, pressure, and misunderstanding.
- Introduces the product later as proof of a changed behavior or revealed truth.
- Uses `salpx / omni_flash` as a 10-second fixed-duration image-to-video route.
- Treats captions as post-production assets: Omni raw clips should not burn in subtitles.

## Case Preview

Sanitized example from a pet ecommerce short drama. These are AI-generated first-frame screenshots for three test clips: hook, product evidence, and ending hook.

| Hook: send-away pressure | Product evidence | Ending hook |
|---|---|---|
| ![EP01-HC-01 hook](examples/xiderdl-lucky/screenshots/ep01-hc-01-hook.jpg) | ![EP01-HC-09 product evidence](examples/xiderdl-lucky/screenshots/ep01-hc-09-product-evidence.jpg) | ![EP01-HC-12 ending hook](examples/xiderdl-lucky/screenshots/ep01-hc-12-ending-hook.jpg) |

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
│       ├── ep01-high-conflict.md
│       └── screenshots/
├── prompts/
│   └── omni-fixed-10s-template.md
├── assets/
│   └── salpx-banner.svg
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
