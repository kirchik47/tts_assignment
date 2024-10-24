import torch
from torch.quantization import quantize_dynamic


model = torch.load('tts-train-dir/run-October-24-2024_09+52PM-39d4123/checkpoint_50.pth')
# Apply dynamic quantization
quantized_model = quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8  # Linear layers quantized to INT8
)

torch.save(quantized_model, 'quantized_model.pth')
