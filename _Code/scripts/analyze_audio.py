#!/usr/bin/env python3
"""
Audio Analysis Script for Arjav's Voiceovers
Measures exact durations, leading/trailing silence, volume levels, and speech segments.
"""

import os
import re
import subprocess
import json

AUDIO_DIR = os.path.abspath("Arjav_M3_Voiceovers")
SCENES = ["scene_01", "scene_02", "scene_03", "scene_04", "scene_05", "scene_06"]

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

def get_audio_info(filepath):
    # Duration and basic stream info
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels",
        "-of", "json",
        filepath
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    probe_data = json.loads(res.stdout)
    stream = probe_data["streams"][0]
    duration = float(probe_data["format"]["duration"])
    sample_rate = int(stream["sample_rate"])
    channels = int(stream["channels"])
    codec = stream["codec_name"]

    # Volume detect
    cmd_vol = [
        FFMPEG, "-i", filepath,
        "-af", "volumedetect",
        "-f", "null", "/dev/null"
    ]
    res_vol = subprocess.run(cmd_vol, capture_output=True, text=True)
    mean_vol_match = re.search(r"mean_volume:\s+([-\d.]+)\s+dB", res_vol.stderr)
    max_vol_match = re.search(r"max_volume:\s+([-\d.]+)\s+dB", res_vol.stderr)
    mean_vol = float(mean_vol_match.group(1)) if mean_vol_match else 0.0
    max_vol = float(max_vol_match.group(1)) if max_vol_match else 0.0

    # Silence detect
    cmd_silence = [
        FFMPEG, "-i", filepath,
        "-af", "silencedetect=noise=-30dB:d=0.3",
        "-f", "null", "/dev/null"
    ]
    res_silence = subprocess.run(cmd_silence, capture_output=True, text=True)
    silences = []
    for line in res_silence.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s+([-\d.]+)", line)
            if m:
                silences.append({"type": "start", "time": float(m.group(1))})
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s+([-\d.]+)\s+\|\s+silence_duration:\s+([-\d.]+)", line)
            if m:
                silences.append({"type": "end", "time": float(m.group(1)), "duration": float(m.group(2))})

    # Find leading silence and trailing silence
    # Let's also run a more sensitive noise gate check for speech start
    # using silencedetect with lower noise floor like -35dB
    cmd_silence2 = [
        FFMPEG, "-i", filepath,
        "-af", "silencedetect=noise=-38dB:d=0.2",
        "-f", "null", "/dev/null"
    ]
    res_sil2 = subprocess.run(cmd_silence2, capture_output=True, text=True)
    
    # Calculate speech intervals
    # If first silence starts at 0, voice starts after silence_end
    first_speech_time = 0.0
    for line in res_sil2.stderr.splitlines():
        if "silence_start: 0" in line or "silence_start: 0.0" in line:
            continue
        if "silence_end:" in line:
            m = re.search(r"silence_end:\s+([-\d.]+)", line)
            if m and first_speech_time == 0.0:
                first_speech_time = float(m.group(1))
                break

    return {
        "file": os.path.basename(filepath),
        "duration": duration,
        "sample_rate": sample_rate,
        "channels": channels,
        "codec": codec,
        "mean_volume": mean_vol,
        "max_volume": max_vol,
        "clipping": max_vol >= 0.0,
        "silences": silences
    }

def main():
    print("=" * 70)
    print("ARJAV VOICE-OVER ANALYSIS MANIFEST")
    print("=" * 70)
    total_dur = 0.0
    for sid in SCENES:
        fpath = os.path.join(AUDIO_DIR, f"{sid}.m4a")
        info = get_audio_info(fpath)
        total_dur += info["duration"]
        print(f"\n[{info['file']}]")
        print(f"  Duration:     {info['duration']:.3f} s")
        print(f"  Format:       {info['codec'].upper()}, {info['sample_rate']} Hz, {info['channels']} channel(s)")
        print(f"  Volume:       Mean: {info['mean_volume']:.1f} dB, Max: {info['max_volume']:.1f} dB")
        print(f"  Clipping:     {'DETECTED' if info['clipping'] else 'None (Clean)'}")
        print(f"  Silences detected (>0.3s @ -30dB): {len([s for s in info['silences'] if s['type'] == 'end'])}")
        for s in info['silences']:
            if s['type'] == 'end':
                print(f"    Pause ended at {s['time']:.2f}s (duration {s['duration']:.2f}s)")
    print("\n" + "=" * 70)
    print(f"TOTAL HUMAN AUDIO DURATION: {total_dur:.3f} s ({total_dur/60:.2f} minutes)")
    print("=" * 70)

if __name__ == "__main__":
    main()
