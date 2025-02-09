import asyncio, os, yt_dlp


def cookiefile():
    cookie_dir = "cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]

    cookie_file = os.path.join(cookie_dir, cookies_files[0])
    return cookie_file



async def download_media_file(link: str, type: str):
    loop = asyncio.get_running_loop()
    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": cookiefile(),
        }

    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": cookiefile(),
        }
        
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    file = os.path.join(
        "downloads", f"{info['id']}.{info['ext']}"
    )
    if os.path.exists(file):
        return file
    await loop.run_in_executor(None, x.download, [link])
    return file
