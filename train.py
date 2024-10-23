import os
import torch

torch.backends.cudnn.enabled = False
os.environ["OMP_NUM_THREADS"] = "1" 
# BaseDatasetConfig: defines name, formatter and path of the dataset.
from TTS.TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.TTS.tts.configs.vits_config import VitsConfig
from TTS.TTS.utils.audio import AudioProcessor
from TTS.TTS.tts.datasets import load_tts_samples
from TTS.TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.TTS.tts.models.vits import Vits
from trainer import Trainer, TrainerArgs


output_path = "tts_train_dir"
if not os.path.exists(output_path):
    os.makedirs(output_path)

dataset_config = BaseDatasetConfig(
    formatter="ljspeech", 
    meta_file_train="C:/Users/kirch/pythonProject/tts_assignment/tts_assignment/data/task1/metadata_3.csv", 
    path="C:/Users/kirch/pythonProject/tts_assignment/tts_assignment/data/task1/"
)

config = VitsConfig(
    batch_size=32,
    eval_batch_size=16,
    num_loader_workers=1,
    num_eval_loader_workers=1,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=20,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    print_step=250,
    print_eval=False,
    mixed_precision=False,
    output_path=output_path,
    datasets=[dataset_config],
    save_step=10000,
    distributed_backend='gloo',
    precision='fp32',
    cudnn_enable=False,
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

model = Vits(config, ap, tokenizer, speaker_manager=None)

trainer = Trainer(
    TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples,
)
trainer.fit()