from __future__ import unicode_literals
import yt_dlp
import os

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_clip(url, name, outdir):

    filename = os.path.join(outdir, url.split("?v=")[-1]+".mp3")

    ydl_opts = {
        'ffmpeg_location': '../ffmpeg/ffmpeg',
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return True
    except Exception:
        return False


def main(df, outdir):

    for k, row in df.iterrows():
        print("{:d} de {:d} - {} - {}".format(k, len(df), row["set_id"], row["ver_id"]))
        if row["status"]:
            name = "_".join((str(row["set_id"]), str(row["ver_id"])))
            download_clip(row["url"], name, outdir)


if __name__ == "__main__":
    
    import pandas as pd
    
    df_list = pd.read_csv('list.csv', sep='\t')
    df_list.columns = ["set_id", "ver_id", "title", "performer", "url", "status"]

    outdir = "data/"
    main(df_list, outdir)
