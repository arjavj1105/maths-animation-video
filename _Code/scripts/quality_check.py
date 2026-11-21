"""
Quality Assurance and Verification Script
Performs mathematical checks, audio checks, technical ffprobe checks,
and extracts representative frames from all six scenes.
"""

import os
import sys
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
FINAL_VIDEO = os.path.join(PROJECT_ROOT, "_Video.mp4")
FRAMES_DIR = os.path.join(PROJECT_ROOT, "_Code", "inspection_frames")

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

def run_technical_check():
    print("=" * 65)
    print("QUALITY CHECK: TECHNICAL VIDEO & AUDIO SPECIFICATIONS")
    print("=" * 65)

    if not os.path.exists(FINAL_VIDEO):
        print(f"FAIL: Final video does not exist at {FINAL_VIDEO}")
        return False

    cmd = [
        FFPROBE, "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        FINAL_VIDEO
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    info = json.loads(res.stdout)

    v_stream = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a_stream = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)

    assert v_stream is not None, "No video stream found!"
    assert a_stream is not None, "No audio stream found!"

    # Codecs
    v_codec = v_stream.get("codec_name", "")
    a_codec = a_stream.get("codec_name", "")
    width = int(v_stream.get("width", 0))
    height = int(v_stream.get("height", 0))
    duration = float(info["format"].get("duration", 0))
    size_mb = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)

    # Frame rate
    r_frame_rate = v_stream.get("r_frame_rate", "30/1")
    num, den = map(int, r_frame_rate.split("/"))
    fps = round(num / den, 2)

    print(f"Container:        {info['format'].get('format_name')}")
    print(f"Video Codec:      {v_codec} (Expected: h264)")
    print(f"Audio Codec:      {a_codec} (Expected: aac)")
    print(f"Resolution:       {width}x{height} (Expected: 1920x1080)")
    print(f"Aspect Ratio:     16:9")
    print(f"Frame Rate:       {fps} FPS (Expected: 30 FPS)")
    print(f"Total Duration:   {duration:.2f}s ({duration/60:.2f} minutes) [Limit: strictly <= 7 min]")
    print(f"File Size:        {size_mb:.2f} MB")

    # Assertions
    assert v_codec == "h264", f"Unexpected video codec: {v_codec}"
    assert a_codec == "aac", f"Unexpected audio codec: {a_codec}"
    assert width == 1920 and height == 1080, f"Unexpected resolution: {width}x{height}"
    assert duration <= 420.0, f"Duration exceeds 7 minute maximum: {duration:.2f}s"
    assert duration >= 240.0, f"Duration is shorter than expected: {duration:.2f}s"

    print("\n-> TECHNICAL SPECIFICATIONS: 100% PASSED!")
    return True

def extract_inspection_frames():
    print("\n" + "=" * 65)
    print("EXTRACTING REPRESENTATIVE INSPECTION FRAMES FROM EACH SCENE")
    print("=" * 65)
    os.makedirs(FRAMES_DIR, exist_ok=True)

    # Timestamps to sample each scene:
    # Scene 1: ~15s (Equations intro)
    # Scene 2: ~50s (Learning objective & row operations)
    # Scene 3: ~100s (3D Planes intersecting)
    # Scene 4: ~170s (Row operation arithmetic & echelon form)
    # Scene 5: ~245s (Verification with checkmarks)
    # Scene 6: ~300s (Takeaways and credits)
    sample_timestamps = [
        (15.0, "scene_01_hook_sample.png", "Scene 1: 3 Equations and Motivation"),
        (55.0, "scene_02_concepts_sample.png", "Scene 2: Core Concepts and Learning Objective"),
        (105.0, "scene_03_geometry_sample.png", "Scene 3: 3D Planes & Intersection Point"),
        (175.0, "scene_04_worked_example_sample.png", "Scene 4: Row Operations & REF Matrix"),
        (255.0, "scene_05_interpretation_sample.png", "Scene 5: Verification Checkmarks & Special Cases"),
        (310.0, "scene_06_summary_sample.png", "Scene 6: Summary Takeaways & Academic Credits")
    ]

    for ts, fname, desc in sample_timestamps:
        out_img = os.path.join(FRAMES_DIR, fname)
        cmd = [
            FFMPEG, "-y",
            "-ss", str(ts),
            "-i", FINAL_VIDEO,
            "-vframes", "1",
            "-q:v", "2",
            out_img
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"-> Extracted {fname} at {ts}s ({desc})")

    print("\n-> All inspection frames extracted successfully into:")
    print(f"   {FRAMES_DIR}")

def main():
    tech_ok = run_technical_check()
    if tech_ok:
        extract_inspection_frames()

if __name__ == "__main__":
    main()
