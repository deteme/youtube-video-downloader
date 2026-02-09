from tkinter import *
from tkinter import ttk
#from pytube import YouTube
from pytubefix import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import subprocess
import os

# Search for available video resolutions
def searchResolution():
    video_link = url_entry.get()
    if video_link == '':
        showerror(title='Error', message='Provide the video link please!')
    else:
        try:
            video = YouTube(video_link)
            resolutions = set()
            
            # Collect unique resolutions
            for stream in video.streams.filter(file_extension='mp4'):
                if stream.resolution and stream.resolution != 'None':
                    resolutions.add(stream.resolution)
            
            # Sort from highest to lowest
            resolutions = list(resolutions)
            resolutions.sort(key=lambda x: int(x.replace('p', '')) if x.replace('p', '').isdigit() else 0, reverse=True)
            
            # Update combobox
            video_resolution['values'] = resolutions
            video_resolution.set('')  # Clear selection
            
            showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
            
        except Exception as e:
            showerror(title='Error', message=f'An error occurred: {str(e)}')

# Download video with selected resolution
def download_video():
    try:
        video_link = url_entry.get()
        resolution = video_resolution.get()
        
        # Input validation
        if not video_link and not resolution:
            showerror(title='Error', message='Please enter both the video URL and resolution!!')
            return
        elif not video_link:
            showerror(title='Error', message='Please enter video URL!!')
            return
        elif not resolution:
            showerror(title='Error', message='Please select a video resolution!!')
            return
        elif resolution == 'None':
            showerror(title='Error', message='None is an invalid video resolution!!')
            return
        
        try:
            # Progress tracking
            def on_progress(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                percentage_completed = round(bytes_downloaded / total_size * 100)
                progress_bar['value'] = percentage_completed
                progress_label.config(text=f'{percentage_completed}%')
                window.update()
            
            video = YouTube(video_link, on_progress_callback=on_progress)
            
            # Get video stream
            video_stream = video.streams.filter(
                res=resolution, 
                file_extension="mp4",
                only_video=True
            ).first()
            
            if not video_stream:
                video_stream = video.streams.filter(
                    res=resolution, 
                    file_extension="mp4"
                ).first()
            
            if not video_stream:
                showerror(title='Error', message=f'No video stream found for {resolution}')
                progress_label.config(text='')
                progress_bar['value'] = 0
                return
            
            # Get audio stream
            audio_stream = video.streams.filter(
                only_audio=True,
                file_extension="mp4"
            ).order_by("abr").desc().first()
            
            if not audio_stream:
                showerror(title='Error', message='No audio stream found')
                progress_label.config(text='')
                progress_bar['value'] = 0
                return
            
            # Download video stream
            progress_label.config(text=f'Downloading video...')
            video_file = video_stream.download(filename_prefix="video_")
            
            # Download audio stream
            progress_label.config(text=f'Downloading audio...')
            audio_file = audio_stream.download(filename_prefix="audio_")
            
            # Merge with ffmpeg
            progress_label.config(text='Merging...')
            progress_bar['value'] = 75
            
            output_file = f"{video.title}.mp4"
            output_file = "".join(c for c in output_file if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
            
            result = subprocess.run([
                "ffmpeg", "-y",
                "-i", video_file,
                "-i", audio_file,
                "-c", "copy",
                output_file
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                os.remove(video_file)
                os.remove(audio_file)
                progress_bar['value'] = 100
                progress_label.config(text='Complete!')
                showinfo(title='Download Complete', message='Video has been downloaded successfully.')
            else:
                showerror(title='Merge Error', message='Failed to merge video and audio')
            
            # Reset UI
            progress_label.config(text='')
            progress_bar['value'] = 0
            
        except Exception as e:
            showerror(title='Download Error', message=f'Failed to download: {str(e)}')
            progress_label.config(text='')
            progress_bar['value'] = 0
            
    except Exception as e:
        showerror(title='Error', message=f'An error occurred: {str(e)}')
        progress_label.config(text='')
        progress_bar['value'] = 0

# Thread functions
def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()

def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()

# Create main window
window = Tk()
window.title('YouTube Video Downloader')
window.geometry('500x460+430+180')
window.resizable(height=FALSE, width=FALSE)

# Canvas for widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()

# Logo
logo = PhotoImage(file='youtubeLogo.png')
logo = logo.subsample(3, 3)
canvas.create_image(250, 80, image=logo)

# Widget styles
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))

entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('DotumChe', 12))

# URL entry
url_label = ttk.Label(window, text='Enter Video URL:', style='TLabel')
url_entry = ttk.Entry(window, width=76, style='TEntry')
canvas.create_window(114, 200, window=url_label)
canvas.create_window(250, 230, window=url_entry)

# Resolution selection
resolution_label = Label(window, text='Resolution:')
canvas.create_window(50, 260, window=resolution_label)

video_resolution = ttk.Combobox(window, width=10)
canvas.create_window(60, 280, window=video_resolution)

# Buttons
search_resolution = ttk.Button(window, text='Search Resolution', command=searchThread)
canvas.create_window(82, 315, window=search_resolution)

# Progress indicators
progress_label = Label(window, text='')
canvas.create_window(240, 360, window=progress_label)

progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
canvas.create_window(250, 380, window=progress_bar)

download_button = ttk.Button(window, text='Download Video', style='TButton', command=downloadThread)
canvas.create_window(240, 410, window=download_button)

# Run application
window.mainloop()