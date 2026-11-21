"""
Audio measurement and timing synchronization helpers.
"""

import os
import subprocess

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio")

def get_scene_audio_path(scene_id: str) -> str:
    return os.path.join(AUDIO_DIR, f"{scene_id}.mp3")

def get_scene_duration(scene_id: str, default_duration: float = 30.0) -> float:
    """
    Returns the exact measured duration of the scene's narration mp3.
    Falls back to default_duration if the file is missing or ffprobe is unavailable.
    """
    audio_path = get_scene_audio_path(scene_id)
    if not os.path.exists(audio_path):
        return default_duration

    for probe_bin in ["/opt/homebrew/bin/ffprobe", "ffprobe"]:
        try:
            cmd = [
                probe_bin, "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            continue

    # Fallback to file size estimation if ffprobe not available
    # edge-tts generates 48kbps or 64kbps CBR/VBR mp3
    try:
        size_bytes = os.path.getsize(audio_path)
        # Average bitrate ~64 kbps = 8000 bytes/sec
        return max(default_duration, size_bytes / 6000.0)
    except Exception:
        return default_duration
