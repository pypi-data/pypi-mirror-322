# Audio Optimizer

[![PyPI version](https://badge.fury.io/py/audio-optimizer.svg)](https://badge.fury.io/py/audio-optimizer)  
A Python library for optimizing audio processing parameters using differential evolution. This library is particularly useful for improving audio processing pipelines by fine-tuning parameters of noise reduction techniques.

---

## Features

- Automatically optimize audio processing parameters with **Differential Evolution**.
- Seamlessly integrates with the `noisereduce` library for noise reduction.
- Handles audio file loading, processing, and evaluation with **librosa**.
- Computes **Mean Squared Error (MSE)** as the optimization loss function.
- Easily customizable bounds for optimization parameters.

---

## Usage

from audio_optimizer.core import optimize_parameters

# Input audio paths
input_audio_path = "input_audio.wav"
target_audio_path = "target_audio.wav"

# Optimize parameters
best_params, loss = optimize_parameters(input_audio_path, target_audio_path, epochs=50, popsize=15)

print("Best Parameters:", best_params)
print("Final Loss:", loss)

---

## Installation

Install the library using pip:

```bash
pip install audio-optimizer


