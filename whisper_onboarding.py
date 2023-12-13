import whisper
import json 
import openai
from openai import OpenAI

def transcribe_audio(model, audio_path):
    """
    This function takes a Whisper model instance and an audio file path,
    loads the audio, and performs transcription.
    """
    # Load audio file
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    result = model.transcribe(audio)

    return result

def transcribe_audio_native(model, audio_path):
    client = OpenAI()

    audio_file = open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
        model=model, 
        file=audio_file, 
        response_format="text"
    )

    with open('transcription_results_whisper_native.json', 'w') as json_file:
        json.dump(transcription, json_file, indent=4)
    
    print(transcription["text"])

def main():
    # Download and load the Whisper model
    model = whisper.load_model("base")
    # The path to audio file
    audio_path ='sample_audio.mp3'

    # Transcribing audio
    transcription = transcribe_audio(model, audio_path)
     # Write transcription results to JSON file
    with open('transcription_results_whisper.json', 'w') as json_file:
        json.dump(transcription, json_file, indent=4)

    print("Transcription:")
    print(transcription)

if __name__ == "__main__":
    main()
