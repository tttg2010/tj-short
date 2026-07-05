# 项目与 Skill 对比

这份对比的目的不是证明 TJ Short 最大，而是帮助用户判断：什么时候该用 TJ Short，什么时候该用其他项目、模型或工具。

## 中文对比表

| 项目 / Skill / 工具 | 核心定位 | 优势 | 局限 | 最适合 | 不适合 |
|---|---|---|---|---|---|
| **TJ Short** | Codex 里的短剧带货执行 Skill：产品图 -> brief -> 剧本 -> 分镜 -> 首帧 -> salpx prompt -> 字幕/交付检查 | 路径短，交付物明确；强调产品证据位；适合快速做 1 集正片 + 2 条切片验证；公开安全边界清楚 | 不是视频模型本身；不替代剪辑软件；当前案例和模板还需要继续扩充 | 想在 Codex 里自动生成短剧带货项目并接 salpx 图生视频的人 | 只想直接生成视频、不需要脚本和交付物的人 |
| **OnlyShot** | 更完整的短剧带货方法论和项目化出片体系 | 规则密、经验多、覆盖从脚本到出片复盘；对“广告小剧情”识别强 | 体系较重，新用户需要时间理解；不一定是公开可直接安装的轻量包 | 团队级短剧带货 SOP、复杂项目复盘 | 只想快速试一个产品钩子的用户 |
| **short-drama** | 通用短剧创作、分镜和出片流程 | 短剧结构完整，适合娱乐短剧、爽剧、系列化叙事 | 带货转化、产品证据和 CTA 不是默认核心 | 娱乐短剧、剧情 IP、系列故事 | 明确以成交/投放为第一目标的产品短剧 |
| **Emily2040/seedance-2.0** | 视频生成生产纪律：镜头契约、状态胶囊、参考资产职责、单变量补拍 | 对视频生成稳定性帮助大；能减少乱补拍和连续性漂移 | 更偏视频生成 OS，不负责完整带货剧本和产品证明 | 已经进入视频生成阶段，需要控质量和复盘 | 还没有产品定位、剧本和转化目标的早期项目 |
| **salpx 中转站 / omni_flash** | 图生视频执行通道 | 能把首帧变成固定 10 秒视频素材；适合接入 Codex 工作流 | 不负责判断剧情是否能卖；不负责字幕、剪辑和产品证明 | 已有首帧和剧本锁定 prompt，需要生成视频 | 期待模型自动理解整集商业逻辑 |
| **通用剪辑工具** | 剪辑、字幕、配音、合成和发布 | 后期能力强，适合精修成片 | 不负责产品诊断、剧本结构和图生视频提示词 | raw clips 已生成后的成片包装 | 从零开始做短剧带货策略 |

## English Comparison Table

| Project / Skill / Tool | Core Positioning | Strengths | Limits | Best For | Not For |
|---|---|---|---|---|---|
| **TJ Short** | Codex ecommerce short-drama execution skill: product image -> briefs -> script -> storyboard -> first frames -> salpx prompts -> captions/checks | Short path, concrete deliverables, product-as-proof logic, good for 1 main episode + 2 ad cutdowns, public-safe boundary | Not a video model; not an editing suite; examples and templates still need expansion | Users who want Codex to generate structured ecommerce short-drama projects and connect to salpx I2V | Users who only want direct video generation without scripts or delivery artifacts |
| **OnlyShot** | Larger ecommerce short-drama methodology and production system | Deep rules, strong project delivery, strong anti-ad-story guardrails, covers postmortems | Heavier system, slower for new users, not necessarily a lightweight public install package | Team SOPs and complex ecommerce short-drama production | Users who only need a quick product-hook test |
| **short-drama** | General short-drama creation, story structure, storyboard and production workflow | Strong drama structure, good for entertainment series and IP-style stories | Conversion, product proof, and CTA are not the default center | Entertainment short dramas and serialized story projects | Product-first campaigns where sales proof is the main objective |
| **Emily2040/seedance-2.0** | Video generation operating discipline: clip contracts, state capsules, reference roles, one-variable retakes | Helps stabilize video generation and reduce random rerolls | More of a video-generation OS than a complete ecommerce script system | Projects already in video generation and quality-control phase | Early projects without product proof, script, or conversion target |
| **salpx relay / omni_flash** | Image-to-video execution route | Turns first frames into fixed 10-second raw clips; easy to connect with Codex output | Does not decide whether the story sells; does not handle captions, editing, or product proof | Users with first frames and script-locked prompts ready | Users expecting the model to infer the full business logic |
| **General editing tools** | Editing, subtitles, dubbing, compositing and publishing | Strong post-production capability | Does not provide product diagnosis, script structure or I2V prompts | Packaging raw clips into final videos | Starting a product short-drama strategy from scratch |

## 公平结论

TJ Short 的强项不是“比所有项目都完整”，而是把最关键的一段链路压短：

```text
产品图 -> Codex 内短剧带货项目 -> salpx / omni_flash 三镜试生 -> 可判断是否继续投入
```

如果你要做完整团队级体系，OnlyShot 和 short-drama 更重、更全。

如果你已经有剧本和首帧，只缺视频生产纪律，Emily2040/seedance-2.0 的思路更关键。

如果你只需要图生视频，salpx / omni_flash 就是执行层，不需要 TJ Short。

如果你想在 Codex 里把一个产品快速变成可执行短剧带货项目，TJ Short 的价值最高。

