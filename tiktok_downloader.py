import yt_dlp
import tempfile
import os
import shutil

def download_tiktok_video_temp(url):
    """
    Download video TikTok ke file sementara, return (path, filename)
    """
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'noplaylist': True,
        'geo_bypass': True,
        'retries': 5,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename, os.path.basename(filename)
    except Exception as e:
        shutil.rmtree(temp_dir)
        return None, None