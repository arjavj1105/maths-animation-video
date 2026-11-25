"""
Full Production Scene Renderer
Renders all six Manim scenes in 1080p (1920x1080) at 30 FPS.
Synchronized to Arjav Jain's Human Voiceover.
"""

import os
import sys
import subprocess
import time
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders")

SCENES = [
    ("scene_01_hook.py", "Scene01Hook", "scene_01.mp4"),
    ("scene_02_concepts.py", "Scene02Concepts", "scene_02.mp4"),
    ("scene_03_geometry.py", "Scene03Geometry", "scene_03.mp4"),
    ("scene_04_worked_example.py", "Scene04WorkedExample", "scene_04.mp4"),
    ("scene_05_interpretation.py", "Scene05Interpretation", "scene_05.mp4"),
    ("scene_06_summary.py", "Scene06Summary", "scene_06.mp4")
]

MANIM = "/opt/homebrew/bin/manim"

def render_scene(py_file, class_name, out_name, quality="h"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_path = os.path.join(SCENES_DIR, py_file)
    print(f"\nRendering {class_name} ({py_file}) at 1080p30...")
    start_t = time.time()

    cmd = [
        MANIM,
        f"-q{quality}",
        "--fps", "30",
        full_path,
        class_name
    ]
    res = subprocess.run(cmd, check=True)
    elapsed = time.time() - start_t
    print(f"-> Finished {class_name} in {elapsed:.1f}s")

    # Locate generated file in media/videos/<stem>/1080p30/<class_name>.mp4
    stem = os.path.splitext(py_file)[0]
    expected_path = os.path.join(PROJECT_ROOT, "media", "videos", stem, "1080p30", f"{class_name}.mp4")
    dest_path = os.path.join(OUTPUT_DIR, out_name)

    if os.path.exists(expected_path):
        shutil.copy2(expected_path, dest_path)
        print(f"-> Successfully copied to {dest_path}")
    else:
        print(f"ERROR: Expected output not found at {expected_path}")
        sys.exit(1)

def main():
    print("=" * 65)
    print("M3 ANIMATION PROJECT: 1080p30 FULL PRODUCTION RENDER")
    print("Student: Arjav Jain | Student ID: E25B070861 | Batch: Ramanujan")
    print("=" * 65)
    total_start = time.time()

    for py_file, class_name, out_name in SCENES:
        render_scene(py_file, class_name, out_name, quality="h")

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 65)
    print(f"All 6 scenes rendered successfully in {total_elapsed/60:.2f} minutes!")
    print("=" * 65)

if __name__ == "__main__":
    main()
