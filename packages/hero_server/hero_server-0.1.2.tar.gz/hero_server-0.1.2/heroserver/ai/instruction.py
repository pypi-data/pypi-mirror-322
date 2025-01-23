import os
import json
import redis
from typing import List,Dict,Optional

redis_client = redis.Redis(host='localhost', port=6379, db=0)

#loads instructions from filesystem and stores in redis for further usage
class MessageManager:
    def __init__(self, name = '', category = '', path: str = "", load: bool = True):
        self.name = name
        self.category = category
        self.messages : List[Dict[str, str]] = []
        if self.category=="":        
            return
        if path:
            self.add(path)
        else:
            if load:
                self.load()

    def add(self, dir_path: str, filter: Optional[List[str]] = None, save: bool = True):
        dir_path = os.path.expanduser(dir_path)
        def process_files(current_dir: str):
            files_to_process = []
            for root, _, files in os.walk(current_dir):
                for file in files:
                    if file.startswith(('sys_', 'user_')):
                        try:
                            priority = int(file.split('_')[1])
                            descr = '_'.join(file.split('_')[2:])
                            if not filter or any(f in descr for f in filter):
                                files_to_process.append((os.path.join(root, file), priority))
                        except (IndexError, ValueError):
                            print(f"Skipping file with invalid format: {file}")
            
            for file_path, _ in sorted(files_to_process, key=lambda x: x[1]):
                file_name = os.path.basename(file_path)
                role = "system" if file_name.startswith('sys_') else "user"
                self.add_file(file_path, role)

        process_files(dir_path)
        
        if save:
            self.save()


    def add_file(self, file_path, role):
        file_path = os.path.expanduser(file_path)
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if role == "system":
                self.add_message(role, content)
            elif role == "user":
                content_parts = content.split('--------', 1)
                if len(content_parts) == 2:
                    content1, content2 = content_parts[0].strip(), content_parts[1].strip()
                    self.add_message("user", content1)
                    self.add_message("assistant", content2)
                else:
                    raise Exception(f"File {file_path} does not contain the expected separator '--------'")
            else:
                raise Exception("Wrong role")

    def add_message(self, role, content):
        if not self.__validate_message(role, content):
            raise ValueError(f"Invalid message format. Role: {role}, Content: {content}")
        self.messages.append({"role": role, "content": content})

    def __validate_message(self, role, content):
        valid_roles = ["system", "user", "assistant"]
        return (
            isinstance(role, str) and
            role in valid_roles and
            isinstance(content, str) and
            len(content.strip()) > 0
        )

    def print_messages(self):
        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]
            print(f"\n{role}:\n{'-' * len(role)}")
            print(content)
            print("-" * 40)

    def get_messages(self):
        return self.messages

    def save(self):
        key = f"llm:instructions:{self.category}:{self.name}"
        value = json.dumps(self.messages)
        redis_client.set(key, value)

    #return true if there where instructions
    def load(self):
        key = f"llm:instructions:{self.category}:{self.name}"
        value = redis_client.get(key)
        if value:
            self.messages = json.loads(value)
            return True
        return False

    def delete(self):
        key = f"llm:instructions:{self.category}:{self.name}"
        return redis_client.delete(key)
    
def instructions_reset():
    pattern = "llm:instructions*"
    keys_to_delete = redis_client.scan_iter(match=pattern)
    for key in keys_to_delete:
        redis_client.delete(key)

#get message manager and get from redis
def instructions_get( name:str, category:str) -> MessageManager:
    m= MessageManager(name, category)
    return m
    
def instructions_load(path: str) -> List[MessageManager]:
    path = os.path.expanduser(path)
    message_managers = []
    #print(f"load {path}")        
    for item in os.listdir(path):
        cat_path = os.path.join(path, item)
        if os.path.isdir(cat_path):        
            category = os.path.basename(cat_path)
            #print(f"  load category: {cat_path}")
            # Process files in the category directory, these will be re=used in each messagemanager
            category_manager = MessageManager(name="", category=category)
            for item in os.listdir(cat_path):
                item_path = os.path.join(cat_path, item)                
                if os.path.isfile(item_path):                    
                    if item.startswith('sys_') or item.startswith('user_'):
                        #print(f"     load cat base: {item_path}")
                        role = "system" if item.startswith('sys_') else "user"
                        category_manager.add_file(item_path, role)
                elif os.path.isdir(item_path):
                    #print(f"     load cat: {item_path}")
                    manager = MessageManager(name=item, category=category)
                    manager.messages = category_manager.messages
                    manager.add(item_path)
                    message_managers.append(manager)

    return message_managers


# Usage example:
if __name__ == "__main__":
    
    # mypath="/Users/despiegk1/code/git.ourworld.tf/projectmycelium/hero_server/lib/ai/instructions/timemgmt"
    # #mypath=""
    # manager = MessageManager(name="schedule", category="timemgmt",path=mypath)
    # manager.print_messages()    
    
    mypath="/Users/despiegk1/code/git.ourworld.tf/projectmycelium/hero_server/lib/ai/instructions"
    instructions_reset()
    instructions_load(mypath)

