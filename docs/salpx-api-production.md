# salpx API 生产 SOP

适用场景：短剧带货项目需要通过 salpx / NewAPI 兼容接口生成图片和视频，包括 `gpt-image-2` 生图，以及 `omni_flash`、`gemini_omni_flash`、`seedance-2-mini-480p`、Veo 系列模型生视频。

目标：让 skill 从 GitHub 下载后，不只会写 prompt，还能直接生产宫格图、首帧图和视频段。

## 1. 环境变量

真实 key 只放在 `.env`、shell 环境或 CI secret，不写进项目文档、prompt、manifest 或聊天回复。

```bash
export SALPX_API_KEY="your_salpx_api_key_here"
export SALPX_BASE_URL="https://www.salpx.com/v1"

# 可选，项目可覆盖
export SALPX_IMAGE_MODEL="gpt-image-2"
export SALPX_VIDEO_MODEL="omni_flash"
```

如果用户给的 url 是 `https://www.salpx.com`，脚本里统一补成 `https://www.salpx.com/v1`。

## 2. 模型名规范

| 用户说法 | API model 默认值 | 用途 |
|---|---|---|
| gpt-image2 / gpt-image-2 | `gpt-image-2` | 宫格图、首帧、产品图再创作 |
| omni / salpx omni | `omni_flash` | 默认短剧带货图生视频，固定 10 秒策略 |
| gemini omni | `gemini_omni_flash` | 用户明确选择 Gemini Omni 时使用 |
| seedance2-mini-480p | `seedance-2-mini-480p` | Seedance2 mini 480p 图生视频 |
| veo | 以 salpx 控制台实际模型 ID 为准 | Veo 文生/图生视频 |

Veo 的具体模型 ID 可能随 salpx 渠道变化。不要在 skill 里死写唯一 ID；项目 manifest 必须记录实际 `model_name`，例如 `veo3`、`veo-3`、`veo2` 或 salpx 控制台显示的完整 ID。

## 3. gpt-image-2 生图

默认 endpoint：

```text
POST {SALPX_BASE_URL}/images/generations
Authorization: Bearer {SALPX_API_KEY}
Content-Type: application/json
```

最小请求：

```json
{
  "model": "gpt-image-2",
  "prompt": "vertical 9:16 cinematic short-drama first frame...",
  "size": "1024x1792",
  "n": 1
}
```

脚本必须同时兼容两种返回：

- `data[0].b64_json`：解码保存为 PNG。
- `data[0].url`：下载保存为 PNG/JPG。

短剧带货默认用途：

- 12 镜头宫格图：推荐 3:4 整图，格内每格为 9:16。
- 9:16 独立首帧：推荐 `1024x1792` 或后期规范到 `720x1280` / `1080x1920`。
- 产品证明图：UI、对比、使用场景、包装/材质特写。

Seedance2 可见人物镜头的正式首帧不能只生成一张高拟真人脸图。宫格/首帧阶段必须按同一镜头生成三候选：

```text
candidate A: face_pencil_strong
candidate B: face_pencil_medium
candidate C: blur_feature = blurred main frame + facial-feature sheet
```

逐张做 Seedance2 预检测或受控单镜头测试。能过的候选里，选择人脸信息、表情、唇形、眼神和表演最完整的一张；失败图不重复原图硬撞，记录原因后换资产路线。

无人物产品首帧只用于产品证据镜头或 API 冒烟测试。它可以证明 salpx `/videos` 接口、轮询和下载链路可用，但不能作为人物表演镜头被拒后的默认正式替代。

生图结果必须复制进项目目录，例如：

```text
storyboards/
first_frames/
product_proof/
previews/drafts/
```

不要只保留默认下载目录。

## 4. 视频生成通用接口

默认 endpoint：

```text
POST {SALPX_BASE_URL}/videos
Authorization: Bearer {SALPX_API_KEY}
Content-Type: application/json
```

文生视频最小请求：

```json
{
  "model": "omni_flash",
  "prompt": "10-second vertical 9:16 cinematic short-drama video...",
  "aspect_ratio": "9:16",
  "size": "720x1280",
  "duration": 10
}
```

图生视频最小请求：

```json
{
  "model": "seedance-2-mini-480p",
  "prompt": "7-second vertical 9:16 image-to-video from the provided first frame...",
  "image": "data:image/png;base64,...",
  "aspect_ratio": "9:16",
  "size": "480x854",
  "duration": 7
}
```

如果 salpx 返回任务 ID，而不是直接 URL，按顺序轮询：

```text
GET {SALPX_BASE_URL}/videos/{task_id}
GET {SALPX_BASE_URL}/videos/{task_id}/result
GET {SALPX_BASE_URL}/videos/generations/{task_id}
```

脚本要从这些常见字段里找视频 URL：

```text
url
video_url
videoUrl
download_url
output_url
result_url
metadata.url
data.url
```

## 5. omni / gemini_omni_flash

默认短剧带货推荐 `omni_flash`。

规则：

- 默认固定 10 秒：prompt 写 `10-second vertical 9:16 image-to-video`，请求 `duration=10`，manifest `api_duration_seconds=10`。
- 如果分镜原本是 6-8 秒，要先改成 10 秒镜头或计划后期剪短，不能一边写 7 秒分镜一边用 Omni 固定 10 秒。
- Omni / LTX 路线默认不内嵌字幕，最终成片后期加字幕。

推荐请求：

```json
{
  "model": "omni_flash",
  "prompt": "10-second vertical 9:16 image-to-video from the provided first frame. ... No burned-in subtitles...",
  "image": "data:image/png;base64,...",
  "aspect_ratio": "9:16",
  "size": "720x1280",
  "duration": 10
}
```

## 6. seedance-2-mini-480p

用户说 `seedance2-mini-480p` 时，API 默认 model 写：

```json
{
  "model": "seedance-2-mini-480p"
}
```

规则：

- 默认 `size="480x854"`，`aspect_ratio="9:16"`。
- 可变时长必须先确认当前 salpx 渠道真实支持；提交侧锁定不代表生成端兑现。
- prompt、API `duration`、manifest duration 必须一致。
- 下载后必须读取真实 mp4 时长；偏差超过 0.5 秒，不能进正式合成。
- Seedance2 字幕可以在 prompt 里写 `Burn in Chinese subtitle exactly:`，但字幕乱不能减少人物说话，台词长短按剧本。
- 可见人物镜头提交前，必须先完成三候选首帧预检测：`face_pencil_strong`、`face_pencil_medium`、`blur_feature`。
- 候选选择标准是“通过预检测 + 人脸信息保留最完整 + 表演最清楚”，不是“最重处理优先”。
- 产品无人物图只代表 API 冒烟测试或产品证据镜头通过，不能替代人物表演镜头的正式首帧。

推荐请求：

```json
{
  "model": "seedance-2-mini-480p",
  "prompt": "7-second vertical 9:16 image-to-video from the provided first frame. Exact Chinese dialogue only: ... Burn in Chinese subtitle exactly: ...",
  "image": "data:image/png;base64,...",
  "aspect_ratio": "9:16",
  "size": "480x854",
  "duration": 7
}
```

## 7. Veo 系列

Veo 模型名必须以 salpx 控制台实际可用 ID 为准；不要凭空假定唯一名字。

建议项目配置：

```bash
export SALPX_VIDEO_MODEL="veo3"
```

请求字段仍走 `/videos` 通用接口：

```json
{
  "model": "veo3",
  "prompt": "8-second vertical 9:16 cinematic commercial short-drama shot...",
  "image": "data:image/png;base64,...",
  "aspect_ratio": "9:16",
  "size": "720x1280",
  "duration": 8
}
```

如果 salpx 控制台显示的 Veo 模型不支持图生视频，移除 `image` 字段，按文生视频提交，并在 manifest 写 `generation_mode=text_to_video`。

## 8. 项目 manifest 必填字段

每个 salpx 任务必须写：

```csv
model_provider,model_name,generation_mode,source_frame,prompt_path,api_duration_seconds,manifest_duration_seconds,task_id,status,output_path,actual_duration_seconds,actual_width,actual_height,bytes,invalid_reason
```

下载后必须补：

- `actual_duration_seconds`
- `actual_width`
- `actual_height`
- `bytes`
- `duration_acceptance_status`
- `retake_verdict`

## 9. 最小生产流程

1. 读 `.env`，确认 `SALPX_API_KEY` 和 `SALPX_BASE_URL`。
2. gpt-image-2 生成宫格或首帧，保存进项目目录。
3. 如果是 Seedance2 可见人物镜头，同一镜头生成 `face_pencil_strong`、`face_pencil_medium`、`blur_feature` 三候选。
4. 逐张做 Seedance2 预检测；在通过候选里选人脸和表演信息最完整的一张。
5. 切 9:16 独立首帧，坏首帧隔离到 `rejected/`，失败原因写入 manifest。
6. 生成视频前写 `generation_manifest`。
7. 用 `/videos` 提交 1-3 个关键镜头。
8. 轮询任务，下载 mp4。
9. 用 `ffprobe` 或等价方式验真实时长和尺寸。
10. 写回 manifest 和复盘。
11. 不合格镜头按 one-variable retake 补拍；能后期修的不要重生。

## 10. 安全与密钥

- 不在聊天回复、Markdown、manifest、prompt、JSON 结果里回显 API key。
- 如果用户直接粘贴 key，后续只说“已收到新 key”，不要复述。
- JSON 结果文件只保存 task、url、模型、耗时、输出路径，不保存请求头。
- GitHub 发布 skill 时只提供 `.env.example`，不提交 `.env`。
