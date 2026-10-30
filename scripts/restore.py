#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大疆灰片还原（D-Log M → Rec.709）批量脚本

用法：
  python restore.py <输入文件或目录> [目录2 ...] [选项]

选项：
  --style vivid|none|春|夏|秋|冬
         vivid = DJI 官方 D-Log M → Rec.709 vivid 还原（默认）
         none  = 不套 LUT，仅转码（拿去剪映/达芬奇自己调）
         春/夏/秋/冬 = 还原后再套对应大师滤镜（需先还原到 Rec.709）
  --out <目录>   输出目录（默认 <输入目录>/_rec709 或输入文件同目录 _rec709）
  --crf <n>      画质（默认 16，越低越清晰）
  --hevc         输出 H.265（默认 H.264，兼容性更好）
  --dry          只打印命令不执行

示例：
  python restore.py D:/素材/飞行记录
  python restore.py DJI_0001.MP4 --style 夏 --out D:/出片
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LUT_RESTORE = SKILL_DIR / "lut" / "DJI_Action5Pro_D-LogM_to_Rec709_vivid.cube"
LUT_MASTER_DIR = SKILL_DIR / "lut" / "master" / "DJI OSMO Action 5 Pro Rec.709 to Color Grading LUTs"
MASTER_MAP = {"春": "Ju", "夏": "Lan", "秋": "Mei", "冬": "Zhu"}
VIDEO_EXT = {".mp4", ".mov", ".m4v"}


def find_ffmpeg():
    """定位 ffmpeg：系统 PATH → imageio-ffmpeg → local-ffmpeg-tool 自动送达"""
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    # 触发 local-ffmpeg-tool 的自动送达（清华镜像断点续传）
    tool = Path(r"C:\Users\shen\.workbuddy\skills\local-ffmpeg-tool\scripts\ffmpeg_tool.py")
    if tool.exists():
        subprocess.run([sys.executable, str(tool), "--help"], capture_output=True)
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            pass
    raise SystemExit("找不到 ffmpeg，请手动安装后重试")


def collect_inputs(inputs):
    files = []
    for p in map(Path, inputs):
        if p.is_dir():
            files += [f for f in p.rglob("*") if f.suffix.lower() in VIDEO_EXT
                      and "_rec709" not in f.parts]
        elif p.suffix.lower() in VIDEO_EXT:
            files.append(p)
    return sorted(set(files))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--style", default="vivid")
    ap.add_argument("--out", default=None)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--hevc", action="store_true")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    ffmpeg = find_ffmpeg()
    files = collect_inputs(args.inputs)
    if not files:
        raise SystemExit("没找到视频文件（支持 mp4/mov/m4v）")

    style = args.style
    filters = []
    if style == "vivid":
        filters = [str(LUT_RESTORE)]
    elif style in MASTER_MAP:
        m = LUT_MASTER_DIR / f"DJI OSMO Action 5 Pro {MASTER_MAP[style]}.cube"
        filters = [str(LUT_RESTORE), str(m)]
    elif style == "none":
        filters = []
    else:
        raise SystemExit(f"未知风格: {style}（可选 vivid/none/春/夏/秋/冬）")

    for f in files:
        out_dir = Path(args.out) if args.out else f.parent / "_rec709"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{f.stem}_rec709.mp4"
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(f)]
        if filters:
            # ffmpeg 滤镜图里反斜杠是转义符，统一转正斜杠并转义盘符冒号
            parts = ["lut3d=file='" + str(Path(x).resolve()).replace("\\", "/").replace(":", "\\:") + "'"
                     for x in filters]
            cmd += ["-vf", ",".join(parts)]
        cmd += ["-c:v", "libx265" if args.hevc else "libx264",
                "-crf", str(args.crf), "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)]
        print("▶", f.name, "→", out)
        if args.dry:
            print("  ", subprocess.list2cmdline(cmd))
            continue
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            print("  ✓ 完成")
        else:
            print("  ✗ 失败:", (r.stderr or "")[-300:])
    print("done")


if __name__ == "__main__":
    main()
