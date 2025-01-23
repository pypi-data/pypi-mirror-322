import os
from pydub import AudioSegment
import whisper
import moviepy.editor as mp
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

class Convertor:
    def __init__(self, max_chars_per_part=4000,context:str = "main"):
        self.max_chars_per_part = max_chars_per_part
        self.context = context

    @classmethod
    def new(cls, max_chars_per_part=4000):
        return cls(max_chars_per_part)

    def process(self, path: str):
        if path.lower().endswith(('.mp4', '.avi', '.mov')):  # Video files
            return self.process_video(path)
        elif path.lower().endswith(('.mp3', '.wav', '.ogg')):  # Audio files
            return self.process_audio(path)
        else:
            raise ValueError("Unsupported file format")

    def process_video(self, video_path: str):
        # Extract audio from video
        video = mp.VideoFileClip(video_path)
        audio_path = video_path.rsplit('.', 1)[0] + '.wav'
        video.audio.write_audiofile(audio_path)
        video.close()
        return audio_path

    def process_audio(self, audio_path: str):
        # Convert to WAV format if necessary
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        if not audio_path.lower().endswith('.wav'):
            audio = AudioSegment.from_file(audio_path)
            audio.export(wav_path, format='wav')
        else:
            wav_path = audio_path

    def split_text(self, text):
        parts = []
        current_part = ""
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            for sentence in sentences:
                if len(current_part) + len(sentence) < self.max_chars_per_part:
                    current_part += sentence + ' '
                else:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = sentence + ' '
            
            # Add a paragraph break if it doesn't exceed the limit
            if len(current_part) + 2 < self.max_chars_per_part:
                current_part += '\n\n'
            else:
                parts.append(current_part.strip())
                current_part = '\n\n'
        
        if current_part:
            parts.append(current_part.strip())
        
        return parts

    def find_natural_pause(self, text):
        words = word_tokenize(text)
        total_words = len(words)
        mid_point = total_words // 2

        # Look for punctuation near the middle
        for i in range(mid_point, total_words):
            if words[i] in '.!?':
                return ' '.join(words[:i+1]), ' '.join(words[i+1:])

        # If no punctuation found, split at the nearest space to the middle
        return ' '.join(words[:mid_point]), ' '.join(words[mid_point:])
    
    def write_to_file(self, parts, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, part in enumerate(parts, 1):
                f.write(f"Part {i}:\n\n")
                f.write(part)
                f.write("\n\n")
                if i < len(parts):
                    f.write("-" * 50 + "\n\n")
    

# Usage example:
if __name__ == "__main__":
    processor = Convertor.new() 
    item = "/Users/despiegk1/Documents/Zoom/2024-07-16 16.42.50 Kristof De Spiegeleer's Personal Meeting Room/video1720369800.mp4"
    transcription_parts = processor.process(item)
    
    processor.write_to_file(transcription_parts, output_file)    
    
    print(f"Transcription split into {len(transcription_parts)} parts:")
    for i, part in enumerate(transcription_parts, 1):
        print(f"Part {i}:")
        print(part)
        print("-" * 50)