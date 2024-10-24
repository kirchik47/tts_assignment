import librosa
import soundfile as sf
import os


def convert_to_mono(input_file, output_file, sr=44100):
    # Load the audio file with librosa and convert to mono 
    audio, _ = librosa.load(input_file, sr=sr, mono=True)
    print(audio)
    # Save the mono audio to a new file using soundfile
    sf.write(output_file, audio, sr)

filepath = 'data/task1/wavs/'
for i, file in enumerate(os.listdir(filepath)):
    convert_to_mono(os.path.join(filepath, file), os.path.join(filepath, file))
