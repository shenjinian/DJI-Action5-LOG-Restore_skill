# DJI-Action5-LOG-Restore_skill

大疆 Osmo Action 5 Pro **D-Log M 灰片批量还原** WorkBuddy Skill —— 用 DJI 官方 LUT 把发灰、低饱和的 log 素材一键还原为 Rec.709 正常色彩，可再叠加春/夏/秋/冬大师滤镜，全程本地 ffmpeg 离线处理，不上传任何文件。

## 功能

- 🎨 **灰片还原**：D-Log M → Rec.709（DJI 官方 vivid LUT）
- 🌸 **大师滤镜**：还原后可叠加 春 / 夏 / 秋 / 冬 官方调色 LUT
- 🎬 **批量转码**：整目录递归处理，输出 H.264（可选 H.265）
- ⚡ **离线本地**：不需要任何云端服务，ffmpeg 直接跑

## 安装

把整个目录放到 `~/.workbuddy/skills/DJI-Action5-LOG-Restore_skill`（或项目 `.workbuddy/skills/` 下）即可，WorkBuddy 会自动识别。

依赖：本机安装 [ffmpeg](https://ffmpeg.org/download.html) 并加入 PATH。

## 使用

对 WorkBuddy 说：

> 帮我把 D:/素材/飞行记录 里的灰片还原一下，套夏季滤镜

或直接运行脚本：

```bash
# 基础还原（默认 vivid LUT → Rec.709）
python scripts/restore.py D:/素材/飞行记录

# 还原 + 夏季大师滤镜
python scripts/restore.py D:/素材/飞行记录 --style 夏

# 只转码不套 LUT（拿到剪映/达芬奇自己调）
python scripts/restore.py DJI_0001.MP4 --style none

# 常用参数
#   --out <目录>   输出目录（默认输入目录下 _rec709）
#   --crf <n>      画质，默认 16，越低越清晰
#   --hevc         输出 H.265
#   --dry          只打印 ffmpeg 命令不执行
```

## 文件结构

```
DJI-Action5-LOG-Restore_skill/
├── SKILL.md                  # WorkBuddy skill 定义
├── scripts/
│   └── restore.py            # 批量还原脚本
└── lut/
    ├── DJI_Action5Pro_D-LogM_to_Rec709_vivid.cube   # D-Log M → Rec.709 还原 LUT
    └── master/DJI OSMO Action 5 Pro Rec.709 to Color Grading LUTs/
        ├── DJI OSMO Action 5 Pro Ju.cube            # 春
        ├── DJI OSMO Action 5 Pro Lan.cube           # 蓝（冬）
        ├── DJI OSMO Action 5 Pro Mei.cube           # 梅（冬韵）
        └── DJI OSMO Action 5 Pro Zhu.cube           # 朱（秋）
```

LUT 文件版权归 DJI 所有，仅随本 skill 分发供个人调色使用。

## License

MIT（LUT 文件除外，归 DJI 所有）
