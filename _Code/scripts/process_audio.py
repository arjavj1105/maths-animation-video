#!/usr/bin/env python3
"""
Audio Processing Script for Arjav Jain's Human Voiceovers
Converts original m4a recordings to standardized WAV files in _Code/audio/processed/
with gentle volume normalization (EBU R128 target I=-18 LUFS, TP=-1.5 dB)
and produces a comprehensive Scene Audio Manifest.
"""

import os
import sys
import json
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

RAW_AUDIO_DIR = os.path.join(PROJECT_ROOT, "Arjav_M3_Voiceovers")
HUMAN_VO_DIR = os.path.join(BASE_DIR, "audio", "human_voiceovers")
PROCESSED_DIR = os.path.join(BASE_DIR, "audio", "processed")

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

SCENES = [
    ("scene_01", "Hook and Context", 34.5),
    ("scene_02", "Concept Introduction", 46.5),
    ("scene_03", "Visual Intuition (3D Geometry)", 41.3),
    ("scene_04", "Worked Example (Step-by-Step)", 84.8),
    ("scene_05", "Interpretation & Verification", 55.3),
    ("scene_06", "Summary & Credits", 54.2)
]

def get_audio_info(filepath):
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels",
        "-of", "json",
        filepath
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    stream = data["streams"][0]
    dur = float(data["format"]["duration"])
    sr = int(stream["sample_rate"])
    ch = int(stream["channels"])
    codec = stream["codec_name"]

    # Volume detect
    cmd_vol = [FFMPEG, "-i", filepath, "-af", "volumedetect", "-f", "null", "/dev/null"]
    res_vol = subprocess.run(cmd_vol, capture_output=True, text=True)
    mean_m = re.search(r"mean_volume:\s+([-\d.]+)\s+dB", res_vol.stderr)
    max_m = re.search(r"max_volume:\s+([-\d.]+)\s+dB", res_vol.stderr)
    mean_v = float(mean_m.group(1)) if mean_m else 0.0
    max_v = float(max_m.group(1)) if max_m else 0.0

    return {
        "duration": dur,
        "sample_rate": sr,
        "channels": ch,
        "codec": codec,
        "mean_volume": mean_v,
        "max_volume": max_v
    }

def process_all():
    os.makedirs(HUMAN_VO_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    manifest = []
    print("=" * 75)
    print("PROCESSING ORIGINAL HUMAN VOICEOVERS")
    print("Student: Arjav Jain | Student ID: E25B070861")
    print("=" * 75)

    for sid, title, target_anim_dur in SCENES:
        src_raw = os.path.join(RAW_AUDIO_DIR, f"{sid}.m4a")
        dst_human = os.path.join(HUMAN_VO_DIR, f"{sid}.m4a")
        dst_wav = os.path.join(PROCESSED_DIR, f"{sid}.wav")

        if not os.path.exists(src_raw):
            print(f"ERROR: Raw audio file missing: {src_raw}")
            sys.exit(1)

        # Copy raw file to human_voiceovers/
        import shutil
        shutil.copy2(src_raw, dst_human)

        # Measure original
        orig_info = get_audio_info(src_raw)

        # Gentle processing:
        # Normalize to EBU R128 (integrated -18 LUFS, true peak -1.5 dB), 44.1kHz 16-bit WAV
        # This equalizes volume without compressing or distorting Arjav's natural voice.
        cmd = [
            FFMPEG, "-y",
            "-i", src_raw,
            "-af", "loudnorm=I=-18:TP=-1.5:LRA=11",
            "-ar", "44100",
            "-ac", "1",
            "-c:a", "pcm_s16le",
            dst_wav
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        proc_info = get_audio_info(dst_wav)

        item = {
            "scene_number": sid,
            "scene_name": title,
            "original_filename": f"{sid}.m4a",
            "processed_filename": f"{sid}.wav",
            "original_duration_s": round(orig_info["duration"], 3),
            "processed_duration_s": round(proc_info["duration"], 3),
            "sample_rate": proc_info["sample_rate"],
            "channels": proc_info["channels"],
            "codec": proc_info["codec"].upper(),
            "mean_volume_dB": proc_info["mean_volume"],
            "max_volume_dB": proc_info["max_volume"],
            "processing_applied": "Gentle EBU R128 volume leveling (I=-18 LUFS, TP=-1.5dB), 44.1kHz 16-bit mono PCM",
            "target_animation_duration_s": target_anim_dur
        }
        manifest.append(item)

        print(f"\n[{sid}] {title}")
        print(f"  Orig:  {orig_info['duration']:.2f}s, mean {orig_info['mean_volume']:.1f} dB, peak {orig_info['max_volume']:.1f} dB")
        print(f"  Proc:  {proc_info['duration']:.2f}s, mean {proc_info['mean_volume']:.1f} dB, peak {proc_info['max_volume']:.1f} dB")
        print(f"  Anim:  Target duration {target_anim_dur:.2f}s (slack: +{target_anim_dur - proc_info['duration']:.2f}s)")

    # Save manifest as JSON and Markdown
    manifest_json = os.path.join(BASE_DIR, "audio", "scene_audio_manifest.json")
    with open(manifest_json, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    manifest_md = os.path.join(BASE_DIR, "audio", "scene_audio_manifest.md")
    with open(manifest_md, "w", encoding="utf-8") as f:
        f.write("# Scene Audio Manifest: Arjav Jain Human Voiceover\n\n")
        f.write("**Student**: Arjav Jain  \n")
        f.write("**Student ID**: E25B070861  \n")
        f.write("**Batch**: Ramanujan  \n")
        f.write("**Course**: Mathematics 3 – Linear Algebra and Calculus  \n\n")
        f.write("| Scene | Audio File | Orig Duration | Proc Duration | Sample Rate | Format | Processing Applied | Anim Duration |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for m in manifest:
            f.write(f"| {m['scene_number']} | `{m['processed_filename']}` | {m['original_duration_s']}s | {m['processed_duration_s']}s | {m['sample_rate']} Hz | {m['codec']} | {m['processing_applied']} | {m['target_animation_duration_s']}s |\n")
        total_audio = sum(m["processed_duration_s"] for m in manifest)
        total_anim = sum(m["target_animation_duration_s"] for m in manifest)
        f.write(f"\n**Total Human Voice Duration**: {total_audio:.2f}s ({total_audio/60:.2f} mins)  \n")
        f.write(f"**Total Synchronized Animation Duration**: {total_anim:.2f}s ({total_anim/60:.2f} mins)  \n")

    print("\n" + "=" * 75)
    print("SUCCESS: Audio processing complete.")
    print(f"Manifest written to:\n - {manifest_json}\n - {manifest_md}")
    print("=" * 75)

if __name__ == "__main__":
    process_all()
