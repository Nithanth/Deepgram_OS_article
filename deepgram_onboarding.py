from deepgram import Deepgram
import asyncio, json, sys, os

# Your Deepgram API Key
DEEPGRAM_API_KEY = 'YOUR_API_KEY_HERE'

# Location of the file you want to transcribe
FILE = 'sample_audio.mp3'

# Mimetype for the file you want to transcribe
MIMETYPE = 'mp3'

async def main():
    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # Check whether requested file is local or remote, and prepare source
    if FILE.startswith('http'):
        source = {'url': FILE}
    else:
        # Open the audio file and keep it open
        audio = open(FILE, 'rb')
        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }

    # Send the audio to Deepgram and get the response
    try:
        response = await asyncio.create_task(
            deepgram.transcription.prerecorded(
                source,
                {
                    'smart_format': True,
                    'model': 'nova-2',
                }
            )
        )

        # Write the response to the console
        print(json.dumps(response, indent=4))

        # Write the response to JSON file
        with open('transcription_results_deepgram.json', 'w') as file:
            json.dump(response, file, indent=4)
    finally:
        # Close the file manually after the task is completed
        if not FILE.startswith('http'):
            audio.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        print(f'line {line_number}: {exception_type} - {e}')
