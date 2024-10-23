from pydub import AudioSegment
import re
import os
import pandas as pd


time_pattern = r"\[(\d{1,2}:\d{2}:\d{2})\]"
time_pattern_stripped = r"(\d{1,2}:\d{2}:\d{2})"
episode_pattern = r".*EPISODE\s\d+.*"
end_intro_pattern = r"\[[A-Z]+\]"
speaker_pattern = r"[A-Z]+:"
def get_timestamps(transcript):
    timestamps = re.findall(time_pattern, transcript)
    timestamps_ms = [int(timestamp.split(':')[0]) * 60 * 60 * 1000 +  
                     int(timestamp.split(':')[1]) * 60 * 1000 +
                     int(timestamp.split(':')[2]) * 1000 for timestamp in timestamps]
    return timestamps_ms

def split_transcripts(transcript):
    cleaned_transcript = re.sub(speaker_pattern, "", transcript).replace('\n\n', '').replace('\n', ' ')
    cleaned_transcript = re.sub(end_intro_pattern, "", cleaned_transcript)
    splitted_transcript = re.split(time_pattern, cleaned_transcript)
    splitted_transcript =  [s.strip().strip('"') for s in splitted_transcript 
                            if not re.match(time_pattern_stripped, s) and not re.match(episode_pattern, s) and s != '']
    return splitted_transcript


file_path = "data/audios"
segment_idx = 0
segments = []
transcripts = []
for i, file in enumerate(os.listdir(file_path)):
    filename = os.path.join(file_path, file)
    if file.endswith(".mp3"):
        # audio = AudioSegment.from_file(filename)
        pass
    else:
        with open(filename, 'r') as f:
            try:
                transcript = f.read()
            except UnicodeDecodeError as e:
                print(e)
                continue
            timestamps_ms = get_timestamps(transcript)
            splitted_transcript = split_transcripts(transcript)
            for j, stamp in enumerate(timestamps_ms):
                # start_time = stamp
                # if j < len(timestamps_ms) - 1:
                #     end_time = timestamps_ms[j + 1]
                #     segment = audio[start_time:end_time]
                # else:
                #     segment = audio[start_time:]
                # segment.export(f"data/segments/segment_{segment_idx}.mp3", format='mp3')
                segments.append(f'segment_{segment_idx}')
                transcripts.append(splitted_transcript[j])
                segment_idx += 1
    print(i)
metadata = pd.DataFrame({0: segments, 1: transcripts})
metadata.to_csv('data/metadata.csv', sep='|', index=False)
    