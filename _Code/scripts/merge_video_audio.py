"""
Video & Human Narration Merge Pipeline
Combines 1080p scene video with Arjav Jain's recorded narration audio for all six scenes,
ensures audio-video sync, and concatenates all scenes into the final _Video.mp4.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
RENDERS_DIR = os.path.join(BASE_DIR, "renders")
PROCESSED_AUDIO_DIR = os.path.join(BASE_DIR, "audio", "processed")
COMBINED_DIR = os.path.join(BASE_DIR, "synced_scenes")
FINAL_VIDEO = os.path.join(PROJECT_ROOT, "_Video.mp4")

SCENE_IDS = [
    "scene_01",
    "scene_02",
    "scene_03",
    "scene_04",
    "scene_05",
    "scene_06"
]

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

def get_duration(file_path: str) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def sync_scene(scene_id: str):
    os.makedirs(COMBINED_DIR, exist_ok=True)
    video_path = os.path.join(RENDERS_DIR, f"{scene_id}.mp4")
    audio_path = os.path.join(PROCESSED_AUDIO_DIR, f"{scene_id}.wav")
    synced_path = os.path.join(COMBINED_DIR, f"{scene_id}_synced.mp4")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Missing rendered video: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Missing human voiceover audio: {audio_path}")

    v_dur = get_duration(video_path)
    a_dur = get_duration(audio_path)
    print(f"\nSyncing {scene_id}: Video = {v_dur:.2f}s, Audio = {a_dur:.2f}s")

    # If video is slightly longer or shorter, adjust video hold or pad audio
    # Typically video is crafted >= audio duration (+0.2-0.3s breathing buffer).
    if v_dur >= a_dur:
        # Pad audio with silence to match exact video duration
        pad_needed = v_dur - a_dur
        cmd = [
            FFMPEG, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", f"[1:a]apad=pad_dur={pad_needed:.3f}[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            synced_path
        ]
    else:
        # Video is shorter than audio: extend last frame of video to match audio duration
        pad_needed = a_dur - v_dur + 0.3
        cmd = [
            FFMPEG, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", f"[0:v]tpad=stop_mode=clone:stop_duration={pad_needed:.3f}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            synced_path
        ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    new_dur = get_duration(synced_path)
    print(f"-> Created {os.path.basename(synced_path)} (Duration: {new_dur:.2f}s)")
    return synced_path

def merge_all():
    print("=" * 65)
    print("MERGING ALL SCENES INTO FINAL VIDEO (ARJAV JAIN VOICEOVER)")
    print("Student: Arjav Jain | Student ID: E25B070861 | Batch: Ramanujan")
    print("=" * 65)

    synced_files = []
    for sid in SCENE_IDS:
        s_path = sync_scene(sid)
        synced_files.append(s_path)

    # Create concat list
    concat_txt = os.path.join(COMBINED_DIR, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in synced_files:
            f.write(f"file '{p}'\n")

    print(f"\nConcatenating {len(synced_files)} scenes into final MP4: {FINAL_VIDEO}")
    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-movflags", "+faststart",
        FINAL_VIDEO
    ]
    subprocess.run(cmd, check=True)

    final_dur = get_duration(FINAL_VIDEO)
    final_size_mb = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)
    print("\n" + "=" * 65)
    print(f"SUCCESS: Final Video Created at: {FINAL_VIDEO}")
    print(f"Duration: {final_dur:.2f}s ({final_dur/60:.2f} minutes)")
    print(f"File Size: {final_size_mb:.2f} MB")
    print("=" * 65)

if __name__ == "__main__":
    merge_all()
