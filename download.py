from __future__ import unicode_literals
import yt_dlp
import os
import pandas as pd


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

    filename = os.path.join(outdir, url.split("?v=")[-1])
    
    if not os.path.isfile(filename):

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

def filter_df(df, mode='TEST'):
    
    df_mode = pd.read_csv('SHS100K-' + mode, sep='\t')
    
    all_ids = df.set_id.astype("str") + '_' + df.ver_id.astype("str")
    relevant_ids = df_mode.iloc[:, 0].astype("str") + '_' + df_mode.iloc[:, 1].astype("str")
    
    filtered_df = df[all_ids.isin(relevant_ids)]
    print(f"Filtering from {len(all_ids)} to {len(filtered_df)}")
    
    return filtered_df


if __name__ == "__main__":
        
    df_list = pd.read_csv('list.csv', sep='\t')
    df_list.columns = ["set_id", "ver_id", "title", "performer", "url", "status"]

    # ugly but too lazy for argparse
    df_list = filter_df(df_list)
    
    outdir = "data/"
    main(df_list, outdir)
