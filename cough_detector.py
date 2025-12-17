"""Cough detection module using audio analysis."""
import numpy as np
from typing import Optional


class CoughDetector:
    """Detects coughs in audio data using simple heuristics."""
    
    def __init__(self, volume_threshold: int = 500, sample_rate: int = 48000):
        """
        Initialize the cough detector.
        
        Args:
            volume_threshold: Minimum volume level to consider as potential cough
            sample_rate: Audio sample rate in Hz
        """
        self.volume_threshold = volume_threshold
        self.sample_rate = sample_rate
        self.last_detection_time = 0
        self.cooldown_period = 3.0  # seconds between detections
        
    def analyze_audio(self, audio_data: bytes) -> bool:
        """
        Analyze audio data to detect if it contains a cough.
        
        Simple heuristic approach:
        - Checks for sudden volume spikes characteristic of coughs
        - Uses short duration and high energy as indicators
        
        Args:
            audio_data: Raw audio bytes (PCM format)
            
        Returns:
            True if a cough is detected, False otherwise
        """
        if not audio_data or len(audio_data) == 0:
            return False
            
        try:
            # Convert bytes to numpy array (16-bit PCM)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            if len(audio_array) == 0:
                return False
            
            # Calculate RMS (Root Mean Square) for volume
            rms = np.sqrt(np.mean(audio_array.astype(np.float64) ** 2))
            
            # Calculate peak amplitude
            peak = np.max(np.abs(audio_array))
            
            # Cough detection heuristics:
            # 1. Volume should exceed threshold
            # 2. Peak-to-RMS ratio indicates sudden burst
            # Use small epsilon to avoid division by zero without skewing the ratio
            epsilon = 1e-6
            peak_to_rms_ratio = peak / (rms + epsilon) if rms > epsilon else 0
            
            # Detect cough if:
            # - RMS volume is above threshold
            # - Peak-to-RMS ratio indicates a sudden burst (typical of coughs)
            is_cough = rms > self.volume_threshold and peak_to_rms_ratio > 3.0
            
            return is_cough
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return False
    
    def should_trigger(self, current_time: float) -> bool:
        """
        Check if enough time has passed since last detection to trigger again.
        
        Args:
            current_time: Current timestamp
            
        Returns:
            True if cooldown period has passed
        """
        if current_time - self.last_detection_time > self.cooldown_period:
            self.last_detection_time = current_time
            return True
        return False
