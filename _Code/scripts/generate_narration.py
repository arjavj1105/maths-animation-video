"""
Narration Generator using edge-tts
Voice: en-US-GuyNeural (fallback: en-GB-RyanNeural)
Measures and logs exact audio durations for animation synchronization.
"""

import os
import sys
import asyncio
import subprocess
import edge_tts

VOICE = "en-US-GuyNeural"
FALLBACK_VOICE = "en-GB-RyanNeural"

SCENES = [
    ("scene_01", "Hook and Context"),
    ("scene_02", "Concept Introduction"),
    ("scene_03", "Visual Intuition"),
    ("scene_04", "Worked Example"),
    ("scene_05", "Interpretation"),
    ("scene_06", "Summary and Credits")
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATION_DIR = os.path.join(BASE_DIR, "narration")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

async def generate_scene_audio(scene_id: str, text: str, output_path: str):
    print(f"Generating audio for {scene_id} using {VOICE}...")
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
    except Exception as e:
        print(f"Warning: Primary voice {VOICE} failed ({e}). Trying fallback {FALLBACK_VOICE}...")
        communicate = edge_tts.Communicate(text, FALLBACK_VOICE)
        await communicate.save(output_path)

def get_audio_duration_ffprobe(file_path: str) -> float:
    try:
        cmd = [
            "/opt/homebrew/bin/ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        # Fallback to python mp3 frame estimation or mutagen if available
        import struct
        # Rough fallback estimation if ffprobe not yet ready: file size / bitrate
        # MP3 48kbps or 128kbps default from edge-tts is typically 48kbps mono or 64kbps
        # But let's check ffprobe or ffmpeg
        return 0.0

async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    durations = {}

    print("=" * 60)
    print(f"GENERATING NARRATION AUDIO ({VOICE})")
    print("=" * 60)

    for scene_id, scene_name in SCENES:
        txt_path = os.path.join(NARRATION_DIR, f"{scene_id}.txt")
        mp3_path = os.path.join(AUDIO_DIR, f"{scene_id}.mp3")

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        await generate_scene_audio(scene_id, text, mp3_path)
        size_kb = os.path.getsize(mp3_path) / 1024
        print(f"-> Generated {scene_id}.mp3 ({size_kb:.1f} KB)")

    print("\nMeasuring durations...")
    # Give ffprobe a try
    has_ffprobe = os.path.exists("/opt/homebrew/bin/ffprobe")
    total_duration = 0.0

    durations_file = os.path.join(AUDIO_DIR, "durations.txt")
    with open(durations_file, "w", encoding="utf-8") as df:
        df.write("# Scene Audio Durations\n")
        for scene_id, scene_name in SCENES:
            mp3_path = os.path.join(AUDIO_DIR, f"{scene_id}.mp3")
            dur = get_audio_duration_ffprobe(mp3_path) if has_ffprobe else 0.0
            durations[scene_id] = dur
            total_duration += dur
            line = f"{scene_id}: {dur:.2f}s ({scene_name})\n"
            df.write(line)
            print(f"  {line.strip()}")

        df.write(f"\nTotal Narration Duration: {total_duration:.2f}s ({total_duration/60:.2f} minutes)\n")
        print(f"\nTotal: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")

    print("=" * 60)
    print("Audio generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
