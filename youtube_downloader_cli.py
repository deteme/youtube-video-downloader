from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess
import os

def video_downloader(video_url):
    my_video = YouTube(
        video_url, 
        on_progress_callback=on_progress,
        use_oauth=True,
        allow_oauth_cache=True
    )
    
    print(f"Title: {my_video.title}")
    print(f"Duration: {my_video.length} seconds")
    
    # Get highest quality video stream
    video_stream = my_video.streams.filter(adaptive=True, only_video=True,file_extension="mp4").order_by("resolution").desc().first()
    
    # Get highest quality audio stream  
    audio_stream = my_video.streams.filter(adaptive=True,only_audio=True,file_extension="mp4"  ).order_by("abr").desc().first()
    
    print(f"Video Quality: {video_stream.resolution}")
    print(f"Audio Quality: {audio_stream.abr}")
    
    # Download both
    video_file = video_stream.download(filename_prefix="video_")
    audio_file = audio_stream.download(filename_prefix="audio_")
    
    # Merge with ffmpeg
    output_file = f"{my_video.title}.mp4"
    
    # Clean filename
    output_file = "".join(c for c in output_file if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
    
    # Merge video and audio
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", video_file, "-i", audio_file,  "-c", "copy", output_file ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        os.remove(video_file)
        os.remove(audio_file)
        print(f"Merged: {output_file}")
    else:
        print(f"FFmpeg error: {result.stderr}")
    
    return my_video.title

try:
    youtube_link = input('Enter the YouTube link: ')
    if youtube_link:
        print(f'Downloading your Video, please wait.......')
        video = video_downloader(youtube_link)
        print(f'"{video}" downloaded successfully!!')
except Exception as e:
    print(f'Error: {e}')