"""Setup script for the Discord cough detection bot."""
import os
import sys


def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True


def check_env_file():
    """Check if .env file exists."""
    if os.path.exists('.env'):
        print("✓ .env file found")
        return True
    else:
        print("✗ .env file not found")
        print("  Please copy .env.example to .env and fill in your values")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    required = ['discord', 'dotenv', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} not installed")
    
    if missing:
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return False
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    import shutil
    if shutil.which('ffmpeg'):
        print("✓ FFmpeg installed")
        return True
    else:
        print("✗ FFmpeg not found")
        print("  FFmpeg is required for audio processing")
        print("  Install instructions: https://ffmpeg.org/download.html")
        return False


def check_audio_file():
    """Check if audio file exists."""
    audio_path = 'assets/stop_coughing.mp3'
    if os.path.exists(audio_path):
        print(f"✓ Audio file found at {audio_path}")
        return True
    else:
        print(f"⚠ Audio file not found at {audio_path}")
        print("  The bot will work but won't play sounds")
        print("  See assets/README.md for instructions")
        return True  # Not critical


def main():
    """Run all setup checks."""
    print("Discord Cough Detection Bot - Setup Check")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_env_file(),
        check_dependencies(),
        check_ffmpeg(),
        check_audio_file()
    ]
    
    print("\n" + "=" * 50)
    if all(checks[:4]):  # First 4 are critical
        print("✓ All critical checks passed!")
        print("\nYou can now run the bot with:")
        print("  python bot.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
