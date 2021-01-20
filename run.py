import os
import argparse
from glob import glob

import pydub
from pydub import AudioSegment
from pydub.generators import Sine


parser = argparse.ArgumentParser()

parser.add_argument('path', help='Path to music file.')
parser.add_argument('freq', help='Frequency of binaural wave.')

args = parser.parse_args()

path = args.path
bias = args.freq.replace(',', '.')

if not os.path.exists(path):
    raise OSError('File not exists.')

try:
    bias = float(bias)
except Exception as ex:
    print(ex)

file_name = os.path.basename(path)
name, ext = os.path.splitext(file_name)
ext = ext.replace('.', '')
save_name = f'{name}_{bias}.{ext}'
# read audio file
track = AudioSegment.from_file(path, format=ext)
frame_rate = track.frame_rate
sample_width = track.sample_width
# generate two sine waves tracks
base_tone = Sine(freq=200).to_audio_segment(duration=len(track))
up_tone = Sine(freq=200 + bias).to_audio_segment(duration=len(track))
# merge two sine waves to stereo track
add_sounds = AudioSegment.from_mono_audiosegments(base_tone, up_tone)
# make a sine waves twice as quiet as a origin file 
add_sounds = add_sounds + track.dBFS - 6
# mixing all
combined = add_sounds.overlay(track)
combined = combined.set_frame_rate(frame_rate).set_sample_width(sample_width)
# save mix to file
combined.export(os.path.join('processed', save_name), format=ext)
