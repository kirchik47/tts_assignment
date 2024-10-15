# tts_assignment
TTS assignment for PARIMAL IIT Roorkee
Considered two models for TTS: Coqui-ai and SpeechT5. I've chosen Coqui-ai since it is more specialised on TTS, while SpeechT5 is more generalised, so the first model will perform better.
Current plan for the first task:
1. Scrape through software engineering daily to get the podcasts audio files and transcripts.
2. Split the audio files into chunks so that each will correspond to the sentence in the transcript.
3. Probably adjust the dataset to make it suitable for fine-tuning.
4. Fine-tune the Coqui-ai model on the dataset.
5. Test it.