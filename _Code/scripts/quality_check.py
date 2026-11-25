"""
Quality Assurance and Verification Script
Performs technical ffprobe checks, audio checks,
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
    print(f"Total Duration:   {duration:.2f}s ({duration/60:.2f} minutes) [Limit: strictly < 7 min]")
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

    # Timestamps in the 316.63s video:
    # Scene 1: 0 - 34.5s => sample at 18.0s (Equations)
    # Scene 2: 34.5 - 81.0s => sample at 55.0s (Learning Objective) and 70.0s (Row Operations)
    # Scene 3: 81.0 - 122.3s => sample at 100.0s (3D Planes and Intersection Point)
    # Scene 4: 122.3 - 207.1s => sample at 150.0s (Row operation arithmetic) and 185.0s (REF Staircase)
    # Scene 5: 207.1 - 262.4s => sample at 235.0s (Checkmarks verification) and 250.0s (Special cases)
    # Scene 6: 262.4 - 316.6s => sample at 275.0s (Takeaways), 300.0s (Disclosure), 312.0s (Closing Card)
    sample_timestamps = [
        (18.0, "scene_01_hook_sample.png", "Scene 1: 3 Simultaneous Equations"),
        (55.0, "scene_02_concepts_sample.png", "Scene 2: Official Learning Objective"),
        (72.0, "scene_02_row_ops_sample.png", "Scene 2: Three Elementary Row Operations"),
        (100.0, "scene_03_geometry_sample.png", "Scene 3: 3D Planes & Intersection Point (1,2,3)"),
        (150.0, "scene_04_worked_example_sample.png", "Scene 4: Row Operation 1 Arithmetic"),
        (185.0, "scene_04_ref_staircase_sample.png", "Scene 4: Row Echelon Form & Pivots (1, 1, 3)"),
        (200.0, "scene_04_back_substitution.png", "Scene 4: Back Substitution & Final Solution"),
        (235.0, "scene_05_interpretation_sample.png", "Scene 5: Three Substitution Checks"),
        (250.0, "scene_05_special_cases.png", "Scene 5: Inconsistent vs Dependent Cases"),
        (275.0, "scene_06_takeaways.png", "Scene 6: Three Core Takeaways"),
        (300.0, "scene_06_summary_sample.png", "Scene 6: Academic References & Human Voiceover Disclosure"),
        (312.0, "scene_06_closing_card.png", "Scene 6: Arjav Jain Closing Academic Credentials")
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
        print(f"-> Extracted {fname} at {ts:.1f}s ({desc})")

    print("\n-> All inspection frames extracted successfully into:")
    print(f"   {FRAMES_DIR}")

def main():
    tech_ok = run_technical_check()
    if tech_ok:
        extract_inspection_frames()

if __name__ == "__main__":
    main()
