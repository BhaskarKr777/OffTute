# voice/speech_to_text.py

import subprocess
import tempfile
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from pathlib import Path


class SpeechToText:
    """
    Offline speech-to-text using whisper.cpp (CLI).
    """

    def __init__(
        self,
        whisper_exe: str = "whisper/whisper-cli.exe",
        model_path: str = "whisper/models/ggml-small.bin",
        sample_rate: int = 16000,
    ):
        self.whisper_exe = Path(whisper_exe)
        self.model_path = Path(model_path)
        self.sample_rate = sample_rate

        # Force correct microphone (Realtek Microphone Array)
        sd.default.device = 1

        if not self.whisper_exe.exists():
            raise FileNotFoundError(f"Whisper executable not found: {self.whisper_exe}")

        if not self.model_path.exists():
            raise FileNotFoundError(f"Whisper model not found: {self.model_path}")

    def listen(self, duration: int = 5) -> str:
        print(f"🎙️ Listening for {duration} seconds...")

        # Record audio
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()

        # Boost volume and convert to int16
        audio = (audio * 32767).astype(np.int16)

        # Save temporary wav file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav.write(tmp.name, self.sample_rate, audio)
            wav_path = tmp.name

        # Run whisper.cpp CLI
        result = subprocess.run(
            [
                str(self.whisper_exe),
                "-m", str(self.model_path),
                "-nt",
                wav_path,
            ],
            capture_output=True,
            text=True,
        )

        output = result.stdout.strip()
        if not output:
            output = result.stderr.strip()

        if not output:
            raise RuntimeError("Whisper returned no output.")

        return output
