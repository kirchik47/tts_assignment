import os
import torch
from phonemizer import phonemize
import pandas as pd

# os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = "C:\\Users\\kirch\\eSpeak NG\\libespeak-ng.dll"
# os.environ["PHONEMIZER_ESPEAK_PATH"] = "C:\\Users\\kirch\\eSpeak NG"
torch.backends.cudnn.enabled = False 

from TTS.TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.TTS.tts.configs.vits_config import VitsConfig
from TTS.TTS.utils.audio import AudioProcessor
from TTS.TTS.tts.datasets import load_tts_samples
from TTS.TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.TTS.tts.models.vits import Vits
from trainer import Trainer, TrainerArgs

def phonemize_dataset(filepath):
    dataset = pd.read_csv(filepath, sep='|')
    for index, row in dataset.iterrows():
        print(f"Processing row {index}")
        dataset.loc[index, 'phonemized'] = phonemize(row['sentence'], 'pl', backend='espeak', strip=True)
    return dataset

# This condition is for preventing creation of processes recursevily
if __name__ == '__main__':
    output_path = "tts_train_dir"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dataset_config = BaseDatasetConfig(
        formatter="ljspeech", 
        meta_file_train="C:/Users/kirch/pythonProject/tts_assignment/tts_assignment/data/task1/metadata_3.csv", 
        path="C:/Users/kirch/pythonProject/tts_assignment/tts_assignment/data/task1/"
    )
    # The Vits config does not have phonemizer for polish, so I'm doing this using phonemizer lib

    # phonemes_dataset = phonemize_dataset('data/task2/metadata_pl.csv')
    # print(phonemes_dataset)
    # phonemes_dataset = pd.read_csv('data/task2/metadata_pl_phonemes.csv')
    # phonemes_dataset = phonemes_dataset['phonemized']  
    # phonemes_dataset.to_csv('data/task2/metadata_pl_phonemes_only.csv', index=False)

    config = VitsConfig(
        batch_size=8,
        eval_batch_size=16,
        num_loader_workers=1,
        num_eval_loader_workers=1,
        run_eval=True,
        test_delay_epochs=-1,
        epochs=20,
        text_cleaner="phoneme_cleaners",
        use_phonemes=True,
        phoneme_language="en-us",
        phoneme_cache_path=os.path.join(output_path, os.path.join(output_path, "phoneme_cache")),
        print_step=10,
        print_eval=False,
        mixed_precision=False,
        output_path=output_path,
        datasets=[dataset_config],
        save_step=50,
        distributed_backend='gloo',
        precision='fp32',
        cudnn_enable=False,
        save_n_checkpoints=100,
        lr_disc=0.00005,
        lr_gen=0.00005
    )

    ap = AudioProcessor.init_from_config(config)
    # Modify sample rate if for a custom audio dataset:
    # ap.sample_rate = 22050

    tokenizer, config = TTSTokenizer.init_from_config(config)

    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )

    # checkpoint_path = 'C:/Users/kirch/pythonProject/tts_assignment/tts_assignment/tts_train_dir/run-October-24-2024_11+10AM-39d4123/checkpoint_50.pth'
    model = Vits(config, ap, tokenizer, speaker_manager=None)
    # model.load_checkpoint(config=config, checkpoint_path=checkpoint_path)
    trainer = Trainer(
        TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples,
    )
    trainer.fit()