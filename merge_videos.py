#!/usr/bin/env python3
"""
Merge all .mov files in output/video/ directory chronologically.
Sorts by timestamp in Korean filename format.
"""

import os
import re
import subprocess
import unicodedata
from pathlib import Path
from datetime import datetime


def parse_korean_timestamp(filename):
    """
    Parse Korean timestamp from filename format:
    "화면 기록 YYYY-MM-DD 오전/오후 H.MM.SS.mov"
    Returns datetime object for sorting.
    """
    filename = unicodedata.normalize('NFC', filename)
    pattern = r'화면 기록 (\d{4})-(\d{2})-(\d{2}) (오전|오후) (\d{1,2})\.(\d{2})\.(\d{2})\.mov'
    match = re.match(pattern, filename)

    if not match:
        raise ValueError(f"Filename does not match expected format: {filename}")

    year, month, day, am_pm, hour, minute, second = match.groups()

    # Convert to 24-hour format
    hour = int(hour)
    if am_pm == "오후" and hour != 12:
        hour += 12
    elif am_pm == "오전" and hour == 12:
        hour = 0

    return datetime(int(year), int(month), int(day), hour, int(minute), int(second))


def main():
    # Define directories
    video_dir = Path("/Users/dreamondal/workspace/blog-poster/output/video")
    output_file = video_dir / "merged_output.mov"
    filelist_path = video_dir / "filelist.txt"

    print(f"📁 Scanning directory: {video_dir}")

    # Find all .mov files (excluding output if it exists)
    mov_files = [
        f for f in video_dir.glob("*.mov")
        if f.name != "merged_output.mov"
    ]

    if not mov_files:
        print("❌ No .mov files found in directory")
        return

    print(f"📹 Found {len(mov_files)} video files")

    # Sort files by timestamp
    try:
        sorted_files = sorted(mov_files, key=lambda f: parse_korean_timestamp(f.name))
    except ValueError as e:
        print(f"❌ Error parsing filenames: {e}")
        return

    print("\n📋 Files in chronological order:")
    for i, f in enumerate(sorted_files, 1):
        timestamp = parse_korean_timestamp(f.name)
        print(f"  {i}. {f.name} ({timestamp.strftime('%Y-%m-%d %I:%M:%S %p')})")

    # Create filelist.txt for ffmpeg concat demuxer
    print(f"\n📝 Creating filelist: {filelist_path}")
    with open(filelist_path, 'w', encoding='utf-8') as f:
        for mov_file in sorted_files:
            # Escape single quotes and use absolute paths
            escaped_path = str(mov_file.absolute()).replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")

    # Build ffmpeg command
    # Re-encode with H.264 video and AAC audio for compatibility
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(filelist_path),
        '-c:v', 'libx264',      # H.264 video codec
        '-preset', 'medium',     # Encoding speed vs compression
        '-crf', '23',            # Quality (lower = better, 23 is default)
        '-c:a', 'aac',           # AAC audio codec
        '-b:a', '192k',          # Audio bitrate
        '-movflags', '+faststart',  # Enable web streaming
        '-y',                    # Overwrite output file
        str(output_file)
    ]

    print(f"\n🎬 Merging videos with ffmpeg...")
    print(f"   Output: {output_file}")
    print(f"   Command: {' '.join(ffmpeg_cmd)}\n")

    # Run ffmpeg
    try:
        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            capture_output=False,  # Let ffmpeg output go to terminal
            encoding='utf-8'
        )
        print(f"\n✅ Successfully merged {len(sorted_files)} videos!")
        print(f"   Output file: {output_file}")

        # Print output file size
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ ffmpeg failed with error code {e.returncode}")
        return
    except FileNotFoundError:
        print("\n❌ ffmpeg not found. Please install ffmpeg:")
        print("   brew install ffmpeg")
        return
    finally:
        # Clean up filelist
        if filelist_path.exists():
            filelist_path.unlink()
            print(f"🧹 Cleaned up temporary filelist")


if __name__ == "__main__":
    main()
