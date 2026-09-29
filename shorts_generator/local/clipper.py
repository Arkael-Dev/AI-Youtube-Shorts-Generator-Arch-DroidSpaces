MAX_CLIP_DURATION = 180.0

"""Local clipping and subtitle rendering for vertical Shorts."""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..config import LOCAL_OUTPUT_DIR


def _ratio(aspect_ratio: str) -> float:
    try:
        w, h = aspect_ratio.split(":")
        return float(w) / float(h)
    except (ValueError, ZeroDivisionError):
        return 9.0 / 16.0


def _output_size() -> Tuple[int, int]:
    try:
        width = int(os.getenv("SHORTS_OUTPUT_WIDTH", "720"))
        height = int(os.getenv("SHORTS_OUTPUT_HEIGHT", "1280"))
    except ValueError:
        width, height = 720, 1280

    if width not in (720, 1080):
        width = 720
    if height not in (1280, 1920):
        height = 1280 if width == 720 else 1920

    return width, height


def _subtitle_color() -> str:
    color = os.getenv("SUBTITLE_COLOR", "FFFFFF").strip().lstrip("#")
    if len(color) != 6:
        return "FFFFFF"

    try:
        int(color, 16)
    except ValueError:
        return "FFFFFF"

    return color.upper()


def _ass_color(hex_color: str) -> str:
    """Convert RRGGBB to ASS AABBGGRR."""
    return "&H00{}{}{}".format(
        hex_color[4:6],
        hex_color[2:4],
        hex_color[0:2],
    )


def _cut_subclip(source_path: str, start: float, end: float, out_path: str) -> str:
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", source_path,
        "-ss", f"{start:.3f}",
        "-to", f"{end:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    return out_path


def _reframe_vertical(in_path: str, out_path: str, aspect_ratio: str) -> str:
    try:
        import cv2  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "opencv-python is required for --mode local. Install it with:\n"
            "    pip install -r requirements-local.txt"
        ) from e

    target_ratio = _ratio(aspect_ratio)
    target_w, target_h = _output_size()

    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        raise RuntimeError(f"could not open {in_path}")

    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    if target_ratio < src_w / src_h:
        crop_h = src_h
        crop_w = int(crop_h * target_ratio)
    else:
        crop_w = src_w
        crop_h = int(crop_w / target_ratio)

    crop_w = max(2, crop_w - (crop_w % 2))
    crop_h = max(2, crop_h - (crop_h % 2))

    silent_path = out_path + ".silent.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(silent_path, fourcc, fps, (crop_w, crop_h))

    last_center: Tuple[int, int] = (src_w // 2, src_h // 2)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cx, cy = last_center
        x0 = max(0, min(src_w - crop_w, cx - crop_w // 2))
        y0 = max(0, min(src_h - crop_h, cy - crop_h // 2))

        cropped = frame[y0:y0 + crop_h, x0:x0 + crop_w]
        writer.write(cropped)

    cap.release()
    writer.release()

    # Scale the cropped vertical frame to the exact selected Shorts size.
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", silent_path,
        "-i", in_path,
        "-vf", f"scale={target_w}:{target_h}:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-shortest",
        "-movflags", "+faststart",
        out_path,
    ]

    subprocess.run(cmd, check=True)
    os.remove(silent_path)
    return out_path


def _snap_to_transcript_boundaries(
    start_time: float,
    end_time: float,
    transcript: Optional[Dict],
) -> Tuple[float, float]:
    if not transcript:
        return start_time, end_time

    segments = transcript.get("segments", [])
    if not segments:
        return start_time, end_time

    start_candidates = [
        float(s["start"])
        for s in segments
        if float(s["start"]) <= start_time
    ]
    end_candidates = [
        float(s["end"])
        for s in segments
        if float(s["end"]) >= end_time
    ]

    if start_candidates:
        start_time = max(start_candidates)

    if end_candidates:
        end_time = min(end_candidates)

    if end_time <= start_time:
        return start_time, end_time

    return start_time, end_time


def _write_clip_srt(
    transcript: Optional[Dict],
    clip_start: float,
    clip_end: float,
    srt_path: str,
) -> Optional[str]:
    """Create synchronized ASS subtitles with selectable font color."""

    ass_path = Path(srt_path).with_suffix(".ass")
    color = _ass_color(_subtitle_color())

    def ts(seconds: float) -> str:
        seconds = max(0.0, float(seconds))
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        sec = seconds % 60
        return f"{h}:{m:02d}:{sec:05.2f}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        f"Style: Caption,DejaVu Sans,64,{color},{color},&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,180,1",
        "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]

    segments = (transcript or {}).get("segments", [])

    for seg in segments:
        seg_start = float(seg.get("start", 0))
        seg_end = float(seg.get("end", 0))

        if seg_end <= clip_start or seg_start >= clip_end:
            continue

        start = max(seg_start, clip_start) - clip_start
        end = min(seg_end, clip_end) - clip_start

        text = str(seg.get("text", "")).strip()
        if not text or end <= start:
            continue

        text = (
            text.replace("\\", "")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("\n", " ")
        )

        words = text.split()
        if len(words) > 8:
            mid = len(words) // 2
            text = " ".join(words[:mid]) + r"\N" + " ".join(words[mid:])

        text = (
            r"{\fad(120,120)\fscx90\fscy90"
            r"\t(0,120,\fscx100\fscy100)}"
            + text
        )

        lines.append(
            f"Dialogue: 0,{ts(start)},{ts(end)},Caption,,0,0,0,,{text}"
        )

    ass_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(ass_path)


def _burn_subtitles(video_path: str, ass_path: Optional[str], out_path: str) -> str:
    """Blur subtitle background first, then render sharp ASS text above it."""

    if not ass_path or not os.path.exists(ass_path):
        if video_path != out_path:
            os.replace(video_path, out_path)
        return out_path

    target_w, target_h = _output_size()

    # Subtitle area is blurred independently from the subtitle layer.
    # 720p: 230px band, 1080p: 320px band.
    band_h = 230 if target_h == 1280 else 320
    band_y = max(0, target_h - band_h - 90)

    subtitle_path = str(ass_path).replace("\\", "/")
    if ":" in subtitle_path:
        subtitle_path = subtitle_path.replace(":", r"\:")

    filter_complex = (
        f"[0:v]split=2[base][blur];"
        f"[blur]crop=iw:{band_h}:0:{band_y},"
        f"boxblur=luma_radius=14:luma_power=2[blurband];"
        f"[base][blurband]overlay=0:{band_y}[bg];"
        f"[bg]ass={subtitle_path}[v]"
    )

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", video_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a:0?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        out_path,
    ]

    subprocess.run(cmd, check=True)
    return out_path


def crop_clip_local(
    source_path: str,
    start_time: float,
    end_time: float,
    aspect_ratio: str,
    out_path: str,
    transcript: Optional[Dict] = None,
) -> str:
    """Cut, reframe, blur subtitle background and burn synchronized captions."""

    start_time = max(0.0, float(start_time))
    end_time = min(float(end_time), start_time + MAX_CLIP_DURATION)

    start_time, end_time = _snap_to_transcript_boundaries(
        start_time,
        end_time,
        transcript,
    )

    if end_time <= start_time:
        raise ValueError("invalid clip boundaries after transcript alignment")

    cut_path = out_path + ".cut.mp4"
    reframed_path = out_path + ".reframed.mp4"
    srt_path = out_path + ".srt"
    ass_path = out_path + ".ass"

    try:
        _cut_subclip(source_path, start_time, end_time, cut_path)
        _reframe_vertical(cut_path, reframed_path, aspect_ratio)

        subtitle_file = _write_clip_srt(
            transcript,
            start_time,
            end_time,
            srt_path,
        )

        _burn_subtitles(reframed_path, subtitle_file, out_path)
    finally:
        for path in (cut_path, reframed_path, srt_path, ass_path):
            if os.path.exists(path):
                os.remove(path)

    return out_path


def crop_highlights_local(
    source_path: str,
    highlights: List[Dict],
    aspect_ratio: str = "9:16",
    out_dir: Optional[str] = None,
    transcript: Optional[Dict] = None,
) -> List[Dict]:
    out_dir = out_dir or LOCAL_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    results: List[Dict] = []

    for i, h in enumerate(highlights, 1):
        out_path = os.path.join(out_dir, f"short_{i:02d}.mp4")
        print(
            f"[clip/local] {i}/{len(highlights)}: "
            f"{h.get('title', '(untitled)')}",
            flush=True,
        )

        try:
            crop_clip_local(
                source_path,
                float(h["start_time"]),
                float(h["end_time"]),
                aspect_ratio,
                out_path,
                transcript=transcript,
            )
            results.append({**h, "clip_url": out_path})
        except Exception as e:
            print(f"[clip/local] {i} failed: {e}", flush=True)
            results.append({
                **h,
                "clip_url": None,
                "error": str(e),
            })

    return results
