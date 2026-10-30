---
name: DJI-Action5-LOG-Restore_skill
version: 1.0.0
display_name: 大疆灰片还原
display_name_en: DJI D-Log M Restore
description: 将大疆 Osmo Action 5 Pro 的 D-Log M 灰片素材用 DJI 官方 LUT 批量还原为 Rec.709 正常色彩，可叠加春/夏/秋/冬大师滤镜，一键批量转码出片，全程本地离线。触发词：大疆灰片、灰片还原、D-Log M、D-Log、Action 5、套LUT、调色还原。
description_zh: 大疆 Action 5 Pro 灰片（D-Log M）批量还原为 Rec.709，支持叠加大师滤镜，本地 ffmpeg 离线处理。
description_en: Batch-restore DJI Osmo Action 5 Pro D-Log M gray footage to Rec.709 with official LUTs, optional master-look LUTs, offline ffmpeg.
license: MIT
author: WorkBuddy Agent
category: media-processing
tags: 大疆, 灰片, D-Log M, LUT, 调色, ffmpeg, Action5
---

# 大疆灰片还原（DJI-Action5-LOG-Restore_skill）

## 概述

把大疆 Osmo Action 5 Pro 拍摄的 **D-Log M 灰片**（发灰、低饱和的 log 素材）用 **DJI 官方 LUT** 批量还原成 Rec.709 正常色彩，全程本地 ffmpeg 离线处理，不上传任何文件。

内置 LUT（均来自 DJI 官网下载中心）：

| LUT | 用途 |
|---|---|
| `lut/DJI_Action5Pro_D-LogM_to_Rec709_vivid.cube` | **还原**：D-Log M → Rec.709（灰片变正常色彩） |
| `lut/master/`（春/夏/秋/冬 = Ju/Lan/Mei/Zhu） | **调色**：作用于已还原的 Rec.709 素材，对应 DJI Mimo"春夏秋冬"大师滤镜风格 |

## 何时调用

- 用户提到"大疆灰片 / 灰片还原 / D-Log M / Action 5 套 LUT / 素材发灰"
- 用户给了 Action 5 Pro 拍的 mp4/mov，要求还原色彩或调色

**注意**：本技能 LUT 专为 Osmo Action 5 Pro 的 D-Log M 制作；其他机型（Mavic/Air/Pocket）的曲线不同，直接套用会偏色——那种情况建议去 DJI 官网下载对应机型 LUT 后手动指定。

## 使用方法

```bash
# 最常用：整目录批量还原（输出到 素材目录/_rec709/）
python scripts/restore.py D:/素材/飞行记录

# 还原 + 套"夏"大师滤镜
python scripts/restore.py D:/素材 --style 夏

# 只转码不套 LUT（拿去剪映/达芬奇自己调）
python scripts/restore.py DJI_0001.MP4 --style none

# 输出 H.265 更省空间；--crf 越低画质越高
python scripts/restore.py D:/素材 --hevc --crf 14
```

参数：`--style vivid|none|春|夏|秋|冬`（默认 vivid）、`--out 输出目录`、`--crf`（默认 16）、`--hevc`、`--dry` 只看命令不执行。

## ffmpeg 定位

脚本自动按顺序找：系统 PATH → `imageio-ffmpeg` 包 → 触发 `local-ffmpeg-tool` 技能的国内镜像自动送达（清华镜像断点续传）。首次使用无需任何手动安装。

## 边界（不做）

- 不做 AI 语义理解、字幕、剪辑拼装
- 不处理其他机型的 D-Log/D-Log M 曲线（会偏色）
- 10-bit H.265 素材输出默认转 8-bit H.264 保证兼容；需保留 10-bit 后期空间时用 `--hevc` 并自行达芬奇处理
