# src/audio_analysis.py

import librosa
import numpy as np

def load_audio(filepath, sr=22050):
    """
    Load an audio file as a waveform (y) and sample rate (sr).
    Parameters:
        filepath (str): Path to audio file
        sr (int): Target sampling rate (default 22050 Hz)
    Returns:
        y (np.ndarray): Audio time series
        sr (int): Sampling rate
    """
    y, sr = librosa.load(filepath, sr=sr)
    return y, sr

def extract_tempo(y, sr):
    """
    Estimate tempo (beats per minute) from audio time series.
    Parameters:
        y (np.ndarray): Audio time series
        sr (int): Sampling rate
    Returns:
        tempo (float): Estimated tempo in BPM
    """
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def extract_key(y, sr):
    """
    Estimate musical key from audio.
    This is a simple heuristic using chroma features and pitch class profile.
    Parameters:
        y (np.ndarray): Audio time series
        sr (int): Sampling rate
    Returns:
        key (str): Estimated musical key (e.g., 'C', 'C#', 'D', etc.)
    """
    # Extract chroma features
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    
    # Pitch classes
    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Key is the pitch class with highest mean chroma energy
    key_index = np.argmax(chroma_mean)
    return pitch_classes[key_index]

def extract_mfcc(y, sr, n_mfcc=13):
    """
    Extract Mel-frequency cepstral coefficients (MFCCs).
    Parameters:
        y (np.ndarray): Audio time series
        sr (int): Sampling rate
        n_mfcc (int): Number of MFCCs to return
    Returns:
        mfccs (np.ndarray): MFCC feature matrix
    """
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfccs

# Example usage
if __name__ == "__main__":
    filepath = "data/sample_audio.mp3"  # Replace with your test file path
    y, sr = load_audio(filepath)
    print("Tempo (BPM):", extract_tempo(y, sr))
    print("Key:", extract_key(y, sr))
    mfccs = extract_mfcc(y, sr)
    print("MFCC shape:", mfccs.shape)
