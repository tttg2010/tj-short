# salpx Wan 3.0（万相 3.0）视频生产 SOP

适用场景：短剧带货项目通过 salpx 生成视频。视频层**只走 salpx**，`h3.zhongbiao.cloud` / `H3_API_KEY` 已废弃。

- 官方文档：<https://www.salpx.com/api-docs/wan3/>
- 客户端脚本：`scripts/wan3_video_client.py`（纯标准库，无第三方依赖）

## 1. 端点与鉴权

```text
Base URL   https://www.salpx.com/v1
提交       POST /v1/videos
查询       GET  /v1/videos/{id}
鉴权       Authorization: Bearer $SALPX_API_KEY
```

- **不能用 `/v1/chat/completions`**，用对话接口调会直接 404。
- 客户端轮询总超时建议 ≥ 900 秒；实际建议轮询间隔 15 秒。

## 2. 模型与价格（人民币 / 秒）

分辨率由**模型名**决定，请求体里的 `size` / `resolution` 会被改写成模型名对应档位，不用传。

| 模型 | 分辨率 | 单价 | 5s | 10s | 30s |
|---|---|---|---|---|---|
| `wan3.0-480p` | 480P | ¥0.21 | ¥1.05 | ¥2.10 | ¥6.30 |
| `wan3.0-720p` | 720P | ¥0.42 | ¥2.10 | ¥4.20 | ¥12.60 |
| `wan3.0-1080p` | 1080P | ¥0.84 | ¥4.20 | ¥8.40 | ¥25.20 |
| `wan3.0-hm-480p` | 480P | ¥0.28 | ¥1.40 | ¥2.80 | ¥8.40 |
| `wan3.0-hm-720p` | 720P | ¥0.56 | ¥2.80 | ¥5.60 | ¥16.80 |
| `wan3.0-hm-1080p` | 1080P | ¥1.11 | ¥5.55 | ¥11.10 | ¥33.30 |

- `hm` 是独立线路，参数、素材规则、计费方式、返回格式与标准版完全一致，只是单价不同；**两组之间不会互相切换**。
- 参考图、参考音频、文档 / 网页素材不加价；有声 / 无声同价。
- 默认路线：短剧用 `wan3.0-720p`（成本 / 质量平衡）；试片用 `wan3.0-480p`；交付级用 `wan3.0-1080p`。

## 3. 计费与退款

- 提交成功即**预扣**；任务失败 / 超时 / 上游报错自动全额退回。
- 不带参考视频：`单价 × 出片秒数`。
- 带参考视频（`reference_video`）：`单价 × (出片秒数 + 参考视频总秒数)`，参考视频按出片同价计费。提交时先按参考视频 15 秒上限预扣，完成后按实际秒数（不足 1 秒按 1 秒）多退少补。
- 例：`wan3.0-720p` 出片 5 秒 + 6 秒参考视频 → 预扣 ¥0.42 × (5+15) = ¥8.40，结算退到 ¥4.62，退回 ¥3.78。
- **给用户报价的义务**：提交前说清模型、分辨率、秒数、是否带参考视频、预计金额，拿到同意再提交。

## 4. 素材类型与组合规则

```text
type              上限   说明
first_frame        1    首帧（只传首帧即首帧图生视频）
last_frame         1    尾帧，配合首帧做首尾帧
reference_image   10    参考图，按顺序在 prompt 里称「图1」「图2」…
reference_video    5    参考视频，总时长 ≤ 15 秒，称「视频1」…（按秒计费）
reference_audio    5    参考音频，总时长 ≤ 15 秒，称「音频1」…
file               1    文档生视频（pdf/docx/pptx/xlsx/txt/md，≤ 100MB、≤ 50 页）
link               1    公开网页生视频（无需登录）
```

组合规则：

- `first_frame` / `last_frame` **不能**和 `reference_*`、`file`、`link` 混用。首尾帧与参考素材二选一。
- `file` 和 `link` 二选一，可与 `reference_*` 组合。
- 三种 `reference_*` 之间可自由组合（图 + 视频 + 音频同时上）。

格式限制：

| 类型 | 格式 | 限制 |
|---|---|---|
| 图片 | JPEG / PNG（无透明通道）/ BMP / WEBP | 单边 240–8000px，长宽比 ≤ 8:1，≤ 20MB |
| 视频 | mp4 / mov | 单段 1–15s，帧率 ≥ 16fps，单边 240–4096px，≤ 100MB |
| 音频 | wav / mp3 | 单段 1–15s，≤ 15MB |
| 出片 | — | 2–30 秒整数；带参考视频时 参考秒数 + 出片秒数 ≤ 30 |

媒体地址必须是**公网可直接下载**的 URL，或用 `data:{MIME};base64,...`。私有云链接、需登录、带防盗链的地址会让任务失败。脚本对本地文件自动转 base64，对 `http(s)` 直链原样透传。

## 5. 请求构造

文本放顶层 `prompt`，素材放 `metadata.media`，每项 `{"type": ..., "url": ...}`。

| 参数 | 位置 | 说明 |
|---|---|---|
| `model` | 顶层 | 必填，见第 2 节 |
| `prompt` | 顶层 | 必填，≤ 20000 字符 |
| `duration` | 顶层 | 必填，2–30 整数秒 |
| `ratio` | 顶层 | 可选：`adaptive`(默认) / `16:9` / `9:16` / `4:3` / `3:4` / `1:1` / `21:9` |
| `input_reference` | 顶层 | 可选，首帧图 URL 的简写，等同 `metadata.media` 里一项 `first_frame` |
| `metadata.media` | metadata | 素材数组，见第 4 节 |
| `metadata.parameters.audio` | metadata | 是否生成声音，默认 `true`，同价 |
| `metadata.parameters.seed` | metadata | 随机种子 0–2147483647 |
| `metadata.parameters.prompt_extend` | metadata | 提示词智能改写，默认 `true`（文档 / 网页生视频必须为 `true`） |

### 5.1 纯文生视频

```bash
curl -X POST https://www.salpx.com/v1/videos \
  -H "Authorization: Bearer $SALPX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan3.0-720p",
    "prompt": "一只橘猫在窗台上伸懒腰，阳光洒进来，镜头缓慢推近",
    "duration": 5,
    "ratio": "16:9"
  }'
```

### 5.2 首帧 / 首尾帧

```bash
curl -X POST https://www.salpx.com/v1/videos \
  -H "Authorization: Bearer $SALPX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan3.0-720p",
    "prompt": "从第一张图自然过渡到第二张图",
    "duration": 5,
    "metadata": {
      "media": [
        {"type": "first_frame", "url": "https://your-cdn.com/first.png"},
        {"type": "last_frame",  "url": "https://your-cdn.com/last.png"}
      ]
    }
  }'
```

只做首帧图生视频时，也可以用顶层 `"input_reference": "https://your-cdn.com/first.png"`。

### 5.3 多素材参考（参考图 + 参考视频 + 参考音频）

```bash
curl -X POST https://www.salpx.com/v1/videos \
  -H "Authorization: Bearer $SALPX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan3.0-1080p",
    "prompt": "图1的角色跟着视频1的动作跳舞，节奏贴合音频1",
    "duration": 8,
    "ratio": "16:9",
    "metadata": {
      "media": [
        {"type": "reference_image", "url": "https://your-cdn.com/char.png"},
        {"type": "reference_video", "url": "https://your-cdn.com/dance.mp4"},
        {"type": "reference_audio", "url": "https://your-cdn.com/bgm.mp3"}
      ]
    }
  }'
```

### 5.4 文档 / 网页生视频

```bash
-d '{"model":"wan3.0-720p","prompt":"把这份产品介绍做成一段 30 秒的宣传短片","duration":30,
     "metadata":{"media":[{"type":"file","url":"https://your-cdn.com/intro.pdf"}]}}'
```

网页生视频把 `type` 换成 `link`，`url` 填公开网页地址。

### 5.5 提交响应

```json
{
  "id": "task_xeYwLgSoqtHyMKrKDeFcuzfkzFPRB8uu",
  "task_id": "task_xeYwLgSoqtHyMKrKDeFcuzfkzFPRB8uu",
  "object": "video",
  "model": "wan3.0-720p",
  "status": "queued",
  "progress": 0,
  "created_at": 1791960031
}
```

## 6. 轮询与取片

```bash
curl https://www.salpx.com/v1/videos/task_xxx -H "Authorization: Bearer $SALPX_API_KEY"
```

| status | 含义 |
|---|---|
| `queued` | 排队中 |
| `in_progress` | 生成中 |
| `completed` | 已完成，成片地址在 `metadata.url` |
| `failed` | 失败，原因在 `error`，已自动退款 |

完成响应：

```json
{
  "id": "task_xxx", "model": "wan3.0-720p", "status": "completed", "progress": 100,
  "metadata": { "url": "https://dashscope-xxx.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=..." }
}
```

- **成片地址在 `metadata.url`，不在顶层。**
- **链接 24 小时后失效**，必须立刻下载并转存进项目目录。
- 下载后必须 `ffprobe` 验真实时长、宽高、字节数，写进 `generation_manifest.csv`。偏差 > 0.5 秒不能进正式合成。

## 7. 错误处理

| HTTP | 信息 | 处理 |
|---|---|---|
| 404 | `bad response status code 404` | 用了 `/v1/chat/completions`，改用 `POST /v1/videos` |
| 400 | `duration 不在允许范围` | 2–30 秒整数 |
| 400 | `prompt is required` | `prompt` 必填 |
| — | 任务 `failed`：`InvalidParameter … mutually exclusive` | 首尾帧和 `reference_*` / `file` / `link` 混用了 |
| — | 任务 `failed`：素材下载失败 | 媒体 URL 需公网可直接下载 |
| 403 | `token quota is not enough` | 余额不足（带参考视频的任务按 15 秒预扣） |
| 503 | `No available channel` | 模型名拼错，或令牌分组未开通该模型 |

## 8. 客户端用法

```bash
S=scripts/wan3_video_client.py

# 先看模型和单价（免费）
python3 $S models

# 文生视频
python3 $S video --model wan3.0-720p --prompt "..." --duration 5 --ratio 16:9 \
  --wait --out outputs/videos/test.mp4

# 首帧图生视频（短剧本体路线）
python3 $S video --model wan3.0-720p --prompt "..." --duration 8 --ratio 9:16 \
  --first-frame first_frames/EP01-03.png --wait --out outputs/videos/ep01-03.mp4

# 首尾帧
python3 $S video --first-frame a.png --last-frame b.png --duration 6 --ratio 9:16 ...

# 多素材参考（图1 + 视频1 + 音频1）
python3 $S video --model wan3.0-1080p --duration 10 --ratio 9:16 \
  --prompt "图1 是女主，图2 是产品包装；视频1 定运镜，音频1 是她唱歌的声音，口型贴合音频1" \
  --ref-image char.png --ref-image pack.png --ref-video dance.mp4 --ref-audio song.mp3 \
  --wait --out outputs/videos/sing.mp4

# 只校验参数和报价，不花钱
python3 $S video --prompt "..." --duration 30 --dry-run

python3 $S status task_xxx
python3 $S download task_xxx --out outputs/videos/x.mp4
```

`--dry-run` 会做完整校验（素材类型、数量、时长、30 秒预算、文件大小）并打印预估金额，不提交任务。素材混用、超限、超预算都会在本地直接报错。

## 9. Prompt 写法要点

- 素材顺序决定名字：第一张参考图是「图1」，第一段参考视频是「视频1」，第一段参考音频是「音频1」。**每个素材都要在 prompt 里指派职责**，没指派的会被模型自行猜测，猜测就是漂移的来源。
- 20–30 秒是「一个长镜头」而不是「四场戏拼接」：要写动作节拍 + 运镜理由，不要把多场景塞进一段话。
- 口型 / 唱歌：音频参考是时间轴权威。给 1 条干净人声（≤ 15 秒），明确写「口型贴合音频1」，脸不要被道具遮挡、保持可辨认角度。
- 商品镜头：6–8 张参考图是稳定区间（主体、材质特写、使用场景）；超过 8 张容易特征冲突，少于 6 张容易幻觉细节。
- 静音不加价，但仍建议保留 `audio=true`，除非用户明确要无声素材后期配。

## 10. 安全

- 不在聊天回复、Markdown、manifest、prompt、JSON 结果里回显 API key。
- 真实 key 只放 `.env`、环境变量或 `~/.config/salpx/credentials.env`。
- 结果文件只存 task、model、输出路径、耗时，不存请求头。
- 视频只允许 `https://www.salpx.com/v1`；脚本会对包含 `zhongbiao` / `h3.` 的 base URL 直接报错退出。
