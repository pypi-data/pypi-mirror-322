import os
from pydub import AudioSegment
import whisper

def audio_add(self):
    
    self.model = whisper.load_model("base")

    @self.bot.message_handler(content_types=['audio', 'voice']) #, 'document'
    def handle_audio(message):
        try:
            chat_id = message.chat.id
            file_info = None
            audio_path = None

            if message.content_type == 'audio':
                file_info = self.bot.get_file(message.audio.file_id)
                audio_path = f"/tmp/audio/{message.audio.file_id}.mp3"
            elif message.content_type == 'voice':
                file_info = self.bot.get_file(message.voice.file_id)
                audio_path = f"/tmp/audio/{message.voice.file_id}.ogg"

            if file_info:
                downloaded_file = self.bot.download_file(file_info.file_path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)

                # Save the audio file
                with open(audio_path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                #bot.send_message(chat_id, f"Audio received and saved successfully to {audio_path}.")
                print(f"Audio received and saved to {audio_path}")
                

                # Convert to WAV format if necessary
                wav_path = audio_path.replace('.mp3', '.wav').replace('.ogg', '.wav')
                if audio_path.endswith('.mp3') or audio_path.endswith('.ogg'):
                    audio = AudioSegment.from_file(audio_path)
                    audio.export(wav_path, format='wav')
                else:
                    wav_path = audio_path

                # Transcribe audio using Whisper
                result = self.model.transcribe(wav_path)
                transcription = result["text"]

                self.bot.send_message(chat_id, transcription, parse_mode='Markdown')
                print(f"Audio received and saved to {audio_path}")
                print(f"Transcription: {transcription}")     
                                
                text2 = self.text_process(self,transcription)
                
                print(f"Processed text {chat_id}: {text2}")      
                    
                if len(text2)>0:
                    self.bot.send_message(chat_id, text2)

                                            

        except Exception as e:
            error_message = {
                'app': 'Telegram Bot',
                'function': 'handle_audio',
                'msg': 'Failed to process audio file',
                'exception_type': type(e).__name__,
                'exception_message': str(e)
            }
            self.send_error_to_telegram(chat_id, error_message)
            print(f"Error processing audio file: {e}")

