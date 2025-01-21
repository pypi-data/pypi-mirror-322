import numpy as np
from scipy.optimize import differential_evolution
from librosa import load
from noisereduce.noisereduce import SpectralGateStationary


def load_audio(file_path):
    data, rate = load(file_path, sr=None)
    return data, rate


def audio_loss(params, data, rate, target_actual):
    prop_decrease, time_constant_s, freq_mask_smooth_hz, time_mask_smooth_ms, n_std_thresh_stationary = params

    sg = SpectralGateStationary(
        y=data,
        sr=rate,
        y_noise=None,
        prop_decrease=prop_decrease,
        time_constant_s=time_constant_s,
        freq_mask_smooth_hz=freq_mask_smooth_hz,
        time_mask_smooth_ms=time_mask_smooth_ms,
        n_std_thresh_stationary=n_std_thresh_stationary,
        tmp_folder=None,
        chunk_size=6000000,
        padding=30000,
        n_fft=1024,
        win_length=None,
        hop_length=None,
        clip_noise_stationary=False,
        use_tqdm=False,
        n_jobs=1,
    )

    processed = sg.get_traces(start_frame=0, end_frame=len(data))

    min_length = min(len(processed), len(target_actual))
    processed = processed[:min_length]
    target = target_actual[:min_length]

    loss = np.mean((processed - target) ** 2)
    return loss


def optimize_parameters(input_audio_path, target_audio_path, epochs=50, popsize=15):
    data, rate = load_audio(input_audio_path)
    target_actual, target_rate = load_audio(target_audio_path)

    if rate != target_rate:
        raise ValueError("Input and target audio must have the same sample rate.")

    bounds = [
        (0.1, 1.0),
        (0.1, 5.0),
        (100, 1000),
        (10, 200),
        (0.5, 5.0),
    ]

    result = differential_evolution(
        func=audio_loss,
        bounds=bounds,
        args=(data, rate, target_actual),
        strategy="best1bin",
        maxiter=epochs,
        popsize=popsize,
        tol=1e-6,
    )

    return result.x, result.fun
