from pesq import pesq
from scipy.io import wavfile

# Load reference and synthesized audio
sr_ref, ref = wavfile.read('input.wav')
sr_deg, deg = wavfile.read('predicted.wav')

score = pesq(sr_ref, ref, deg, 'wb')  # 'wb' = wideband (16 kHz)

print(f'PESQ Score: {score}')