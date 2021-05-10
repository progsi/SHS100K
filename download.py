from __future__ import unicode_literals
import youtube_dl
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

    filename = os.path.join(outdir, name+".wav")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return True
    except Exception:
        return False


def main(list, outdir):

    for k, row in enumerate(list):
        print("{:d} de {:d} - {} - {}".format(k, len(list), row["set_id"], row["ver_id"]))
        if row["status"]:
            name = "_".join(row["set_id"], row["ver_id"])
            download_clip(row["url"], name, outdir)


if __name__ == "__main__":

    outdir = ""
    main(list, outdir)
