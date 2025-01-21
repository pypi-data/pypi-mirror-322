## Usage Example

Here's how you can use the `mydenoise` library:

```python
from mydenoise.denoise import dnoise

# Input and output paths
input_audio = "path_to_noisy_audio.wav"
output_audio = "denoised_output.wav"

# Denoise the audio
dnoise(input_audio, output_audio)
print(f"Denoised audio saved to {output_audio}")
