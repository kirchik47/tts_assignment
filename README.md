# tts_assignment
TTS assignment for PARIMAL IIT Roorkee
Considered two models for TTS: Coqui-ai and SpeechT5. I've chosen Coqui-ai since it is more specialised on TTS, while SpeechT5 is more generalised, so the first model will perform better for the first task.
For the second task I've also decided to use Coqui-ai since I will fine-tune it for Ukrainian language, which there are few pretrained models for Ukrainian and Coqui provides flexibility.

TASK 1
Current plan for the first task:
1. Scrape through software engineering daily to get the podcasts audio files and transcripts.
2. Split the audio files into chunks so that each will correspond to the sentence in the transcript.
3. Adjust the dataset to make it suitable for fine-tuning.
4. Fine-tune the Coqui-ai model on the dataset.
5. Test it.

TASK 2
Current plan is basically the same as for the first, probably without scraping, just directly download dataset from github or other source.

TASK 3
Apply dynamic quantization to the model to reduce the size of the model and make it more efficient. This will be done
after the model is fine-tuned.