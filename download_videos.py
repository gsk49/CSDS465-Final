import os
import json
import subprocess

save_dir = './'

def download_video(url):
    command = ["yt-dlp", "-o",
               f"{save_dir}/%(title)s.%(ext)s", "-f", "bestvideo[ext=mp4]/best[ext=mp4]/best", url]
    subprocess.call(command)

    
# with open('data/mlb-youtube-segmented.json', 'r') as f:
#     data = json.load(f)
#     for key, entry in data.items():
#         yturl = entry['url']
#         download_video(yturl)
        
#         print('Download Completed')

# testing with just 20 entries for the time being
with open('data/mlb-youtube-segmented.json', 'r') as f:
    data = json.load(f)
    count = 0
    for key, entry in data.items():
        if count>5:
            yturl = entry['url']
            download_video(yturl)

        count += 1
        print('Download Completed')
        if count >= 8:
            break