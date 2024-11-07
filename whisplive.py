import pyaudio
import wave
import io
import requests
import time

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/octet-stream"
}

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Ensure sample rate is set to 16kHz for Whisper

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def transcribe_audio_chunk(audio_chunk):
    """Convert audio chunk to WAV format and send to API for transcription."""
    # Convert raw audio data to WAV format in memory
    with io.BytesIO() as wav_buffer:
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_chunk)
        
        wav_data = wav_buffer.getvalue()  # Get WAV data from buffer

    # Send WAV data to API
    response = requests.post(API_URL, headers=headers, data=wav_data)
    if response.status_code == 200:
        result = response.json()
        return result.get("text", "")
    else:
        print("Error:", response.status_code, response.json())
        return ""

print("Listening... Press Ctrl+C to stop.")

try:
    while True:
        frames = []
        
        # Capture audio for a short duration (e.g., 2 seconds)
        for _ in range(0, int(RATE / CHUNK * 2)):
            data = stream.read(CHUNK)
            frames.append(data)

        # Join frames to form audio chunk
        audio_data = b''.join(frames)
        transcription = transcribe_audio_chunk(audio_data)
        
        # Print real-time transcription
        if transcription:
            print("Transcription:", transcription)

        # Delay to manage request frequency
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping live transcription...")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
