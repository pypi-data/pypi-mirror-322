import os
from ai.ask import ai_assistent

def text_add(self,reset:bool=False):
    
    self.ai_assistent = ai_assistent(reset=reset)
    self.text_process = text_process
    
    @self.bot.message_handler(content_types=['text'])
    def handle_text(message):
        try:
            chat_id = message.chat.id
            
            text = message.text

            # Here you can add your logic to process the text
            # For now, let's just echo the message back
            # response = f"You said: {text}"

            print(f"Received text from {chat_id}: {text}")                        
            
            text2 = self.text_process(self,text)
            
            print(f"Processed text {chat_id}: {text2}")      
                
            if len(text2)>0:
                self.bot.send_message(chat_id, text2)


        except Exception as e:
            error_message = {
                'app': 'Telegram Bot',
                'function': 'handle_text',
                'msg': 'Failed to process text',
                'exception_type': type(e).__name__,
                'exception_message': str(e)
            }
            self.send_error_to_telegram(chat_id, error_message)
            print(f"Error processing text file: {e}")


def text_process(self, txt) -> str:
    if "translate" not in txt.lower():            
        txt+='''\n\n
            only output the heroscript, no comments
            '''
    response = self.ai_assistent.ask(
        category='timemgmt',
        name='schedule',
        question=txt)
    return response