# USAGE python3 frame_folder_sorter.py --input test_videos/ --output output_sorted_frames/
# output_sorted_frames is created automatically if the folder does not exist

import numpy as np
import argparse

import fnmatch
import cv2
import os


# function used to find files in the selected folder
def file_finder(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="path to folder with input videos and their annotations")
ap.add_argument("-o", "--output", required=True,
                help="path to folder with output labeled frames")
args = vars(ap.parse_args())

# find all videos and their annotations in argparse '--input' folder
video_names = sorted(file_finder('*.mkv', args['input']))
annotation_names = sorted(file_finder('*.txt', args['input']))
print(video_names, annotation_names)

# create argparse '--output' folder
if os.path.exists(args['output']) == False:
    os.mkdir(args['output'])
output_folder_name = args['output']
img_name = 1

# loop over all finded videos and their annotations
for video_label, (annotation_name, video_name) in enumerate(zip(annotation_names, video_names)):
    print(annotation_name, video_name)
    # read annotation file and write to 'new_lines' list annotation text
    with open(annotation_name, 'r') as f:
        new_lines = []
        for line in f:
            line = line.split('\n')[0].split(' ')
            line = list(map(int, line))
            new_lines.append(line)

    cap = cv2.VideoCapture(video_name)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_frame_counter = 1

    # loop over lines in annotation file
    for label, start_frame, end_frame in new_lines:
        if os.path.exists(output_folder_name + str(label)) == False:
            os.mkdir(output_folder_name + str(label))

        # loop over all frames in line
        for count in np.arange(start_frame, end_frame + 1):
            # find selected frame in video and read it
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            err, img = cap.read()

            # select output frame size
            img = cv2.resize(img, (500, 500))

            # save 'img' frame in output folder
            cv2.imwrite(output_folder_name + str(label) + '/' + '{}-frame.png'.format(img_name), img)
            video_frame_counter += 1
            img_name += 1
            print('{}/{}'.format(video_frame_counter, length), end='\r')

    cap.release()