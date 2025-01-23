import os

from pydub import AudioSegment
import assemblyai as aai


class Client:
    def __init__(self):
        api_key = os.getenv("ASSEMBLYAI")

        if not api_key:
            raise EnvironmentError(
                "Please set the ASSEMBLYAI environment variable with your AssemblyAI API key."
            )

        self.api_key = api_key
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()

    def convert_to_ogg_mono(self, input_path: str, output_path: str):
        """Converts an audio file from .mp4 to .ogg (mono)."""
        audio = AudioSegment.from_file(input_path, format="mp4")
        # Convert to mono if needed by uncommenting the line below
        # audio = audio.set_channels(1)
        audio.export(output_path, format="ogg")
        print(f"Converted to .ogg in {output_path}")

    def transcribe_audio(self, audio_path: str, output_path: str):
        """Transcribes the audio file and saves the transcription to a Markdown file."""
        config = aai.TranscriptionConfig(
            speaker_labels=True,
        )

        transcript = self.transcriber.transcribe(audio_path, config)

        with open(output_path, "w", encoding="utf-8") as f:
            for utterance in transcript.utterances:
                f.write(
                    f"** Speaker {utterance.speaker}:\n{utterance.text}\n-------------\n"
                )

        print(f"Transcription saved to {output_path}")

    def transcribe_audio_file(self, input_path: str, output_transcription_path: str):
        """Handles the entire process from conversion to transcription and cleanup."""
        converted_audio_path = input_path.replace(".mp4", ".ogg")

        # Convert .mp4 to .ogg
        self.convert_to_ogg_mono(input_path, converted_audio_path)

        # Perform the transcription
        self.transcribe_audio(converted_audio_path, output_transcription_path)

        # Optionally, clean up the converted file
        os.remove(converted_audio_path)
        print(f"Removed temporary file {converted_audio_path}")


# Example usage:
if __name__ == "__main__":
    # Retrieve API key from environment variable

    # Define the paths for the input audio and output transcription
    input_audio_path = "/tmp/475353425.mp4"
    output_transcription_path = "/tmp/transcribe_475353425.md"

    # Perform the transcription process
    client = Client()
    client.transcribe_audio_file(input_audio_path, output_transcription_path)
