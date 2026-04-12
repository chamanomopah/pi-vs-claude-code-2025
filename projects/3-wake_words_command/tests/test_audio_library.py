# -*- coding: utf-8 -*-
"""
Test automated audio files.
Verifies that all generated audio files are valid and can be loaded.
"""

import sys
import io
from pathlib import Path

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import numpy as np
import soundfile as sf


def test_audio_files():
    """Test all generated audio files."""
    
    print("\n" + "=" * 80)
    print(" 🎵 TESTING AUDIO FILES")
    print("=" * 80)
    
    audio_dir = Path("tests/audio")
    
    # Find all wav files
    wav_files = list(audio_dir.rglob("*.wav"))
    
    if not wav_files:
        print("❌ No audio files found!")
        return 1
    
    print(f"\nFound {len(wav_files)} audio files")
    
    all_valid = True
    total_duration = 0.0
    
    for wav_path in sorted(wav_files):
        try:
            # Load audio file
            audio, sr = sf.read(str(wav_path))
            
            # Get info
            duration = len(audio) / sr
            total_duration += duration
            channels = 1 if len(audio.shape) == 1 else audio.shape[1]
            
            # Calculate stats
            rms = np.sqrt(np.mean(audio ** 2))
            peak = np.abs(audio).max()
            
            # Determine category
            category = wav_path.parent.name
            
            # Display
            status = "✅" if rms > 0.001 else "⚠️ "
            print(f"{status} {category:15s} {wav_path.stem:30s} | {duration:5.2f}s | {sr:5d}Hz | Ch:{channels} | RMS:{rms:.4f}")
            
            # Warn if too quiet
            if rms < 0.001:
                print(f"    ⚠️  Very quiet audio file")
                all_valid = False
                
        except Exception as e:
            print(f"❌ ERROR: {wav_path}: {e}")
            all_valid = False
    
    # Summary
    print("\n" + "=" * 80)
    print(" 📊 SUMMARY")
    print("=" * 80)
    print(f"Total files tested: {len(wav_files)}")
    print(f"Total duration: {total_duration:.1f} seconds")
    print(f"Average duration: {total_duration/len(wav_files):.2f} seconds")
    
    if all_valid:
        print("\n✅ All audio files are valid!")
        return 0
    else:
        print("\n⚠️  Some audio files may have issues")
        return 1


def list_audio_library():
    """List all audio files in the library."""
    
    print("\n" + "=" * 80)
    print(" 📂 AUDIO LIBRARY")
    print("=" * 80)
    
    audio_dir = Path("tests/audio")
    
    for category_dir in sorted(audio_dir.iterdir()):
        if category_dir.is_dir():
            print(f"\n{category_dir.name.upper()}:")
            print("-" * 80)
            
            wav_files = sorted(category_dir.glob("*.wav"))
            for wav_file in wav_files:
                size_kb = wav_file.stat().st_size / 1024
                print(f"  📄 {wav_file.stem:40s} ({size_kb:6.1f} KB)")


if __name__ == "__main__":
    
    # List library
    list_audio_library()
    
    # Test files
    exit_code = test_audio_files()
    
    print("\n" + "=" * 80)
    
    sys.exit(exit_code)
