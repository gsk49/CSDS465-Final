import os
import json
import subprocess
import multiprocessing
from multiprocessing import freeze_support
import csv

def get_youtube_video_title(url):
    command = ["yt-dlp", "--get-title", url]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        title = result.stdout.strip()
        return title
    else:
        print("Failed to retrieve video title")
        return None
    

def local_clip(filename, start_time, duration, output_filename, output_directory):
    end_time = start_time + duration
    command = ['ffmpeg',
               '-ss', str(start_time),
               '-i', '"%s"' % filename,
               '-t', str(end_time - start_time),
               '-c:v', 'copy', '-an',
               '-threads', '1',
               '-loglevel', 'panic',
               os.path.join(output_directory,output_filename)]
    command = ' '.join(command)

    try:
        output = subprocess.check_output(command, shell=True,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        #print (err.output)
        return err.output


def wrapper(clip):

    input_directory = './full_videos'

    output_directory = './segmented_videos/balls000'

    duration = clip['end']-clip['start']
    video_title = get_youtube_video_title(clip['url'])
    local_clip(os.path.join(input_directory, video_title+'.mp4'),
               clip['start'], duration, str(clip['end'])+'.mp4',
               output_directory)
    return 0
    

if __name__ == '__main__':
    freeze_support()
    with open('data/mlb-youtube-segmented.json', 'r') as f:
        data = json.load(f)
        
        # desired_labels = {'ball'}
        # undesired_label = 'swing'
        
        # video_titles = []

        # filtered_segments = [
        #     data[k] for k in data.values()
        #     if any(label in desired_labels for label in data[k]["labels"]) and
        #        all(label != undesired_label for label in data[k]['labels'])
        # ]

        #pool = multiprocessing.Pool(processes=8)
        #pool.map(wrapper, filtered_segments)

        #####
        #####   Choose pitch types, we may want to consider knucklecurves
        #####   as curves, etc. (2 seam and 4 seam equivalent, etc.)
        #####
        desired_types = {'sinker'}
        
        # List to store video titles
        video_titles = []

        input_directory = './full_videos'
        # Filter segments based on type and collect video titles
        for segment in data.values():
            if "type" in segment and segment["type"] in desired_types:
                filename = str(segment['end']) + '.avi'  # Generate filename using end time
                video_titles.append(filename)

        # Write video titles to a CSV file
        #####
        #####   Output to whichever CSV you want (corresponding to pitch type)
        #####
        with open('./pitch_types/sinkers.csv', 'w', newline='') as csvfile:
            fieldnames = ['Title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for title in video_titles:
                writer.writerow({'Title': title})

        print('Video titles saved to segmented_video_titles.csv')

        print('Download Completed')