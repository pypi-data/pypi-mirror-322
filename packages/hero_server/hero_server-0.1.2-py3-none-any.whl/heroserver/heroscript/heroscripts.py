from pydantic import BaseModel, Field
from typing import Any, Type, TypeVar
import re
import hashlib
import json
import os
from types import List,Dict


T = TypeVar("T", bound=BaseModel)

class HeroScripts:
    def __init__(self, class_types: dict, path:str = "", content:str = "", indexpath: str = ""):
        self.class_types = class_types
        self.heroscripts = List(HeroScript)
        self.path = os.path.expanduser(path) 
        self.indexpath = os.path.expanduser(indexpath)
        self.done = Dict[str,str] = {}
        
        # self.done_load()
        
        if self.path:
            try:
                # self.done_load()
                self.load(self.path)
                self.done_save()
            except FileNotFoundError as e:
                print(f"Directory not found: {self.path}")
                print(f"Error: {str(e)}")

        self.create_indexes()
        self.index_objects()                
                            
        if content:
            blocks = extract_heroscript_blocks(content)
            self.heroscripts.extend(HeroScript(block) for block in blocks)

    def done_load(self):
        if self.path:
            done_file = os.path.join(self.path, "done.json")
            if os.path.exists(done_file):
                with open(done_file, "r") as f:
                    self.done = json.load(f)
        
    def done_save(self):
        if self.path:
            done_file = os.path.join(self.path, "done.json")
            with open(done_file, "w") as f:
                json.dump(self.done, f)
    
    def load(self, path):
        for root, _, files in os.walk(path):
            for filename in files:
                print(f" - load {path}/{filename}")
                path=f"{path}/{filename}"
                if filename.endswith(".md"):
                    filepath = os.path.join(root, filename)
                    with open(filepath, "r") as file:
                        content = file.read()
                        md5hash = hashlib.md5(content.encode()).hexdigest()
                        if filepath not in self.done or self.done[filepath] != md5hash:
                            blocks = self.extract_heroscript_blocks(content)
                            self.heroscripts.extend(HeroScript(block,path) for block in blocks)
                            self.done[filepath] = md5hash       
       
    @staticmethod

            
    def get_objects(self):
        objects = []
        for heroscript in self.heroscripts:
            if heroscript.content:
                try:
                    class_name = heroscript.content.split("\n")[0].split("!!")[1].split(".")[0].lower()
                    if class_name in self.class_types:
                        class_type = self.class_types[class_name]
                        try:
                            obj = class_type.from_heroscript(heroscript.content)
                            objects.append(obj)
                        except Exception as e:
                            print(f"Error parsing HeroScript: {e}")
                except (IndexError, ValueError):
                    print(f"Invalid HeroScript format: {heroscript.content}")
        return objects
    

    def create_indexes(self):
        for class_type in self.class_types.values():
            schema = self.create_schema(class_type)
            index_dir = os.path.join(self.indexpath, class_type.__name__.lower())
            if not os.path.exists(index_dir):
                os.makedirs(index_dir)
                index.create_in(index_dir, schema)
    
    def create_schema(self, class_type):
        schema_fields = {"path": STORED()}
        for field_name, field in class_type.__fields__.items():
            json_schema_extra = getattr(field, "json_schema_extra", None)
            if json_schema_extra is not None:
                metadata = json_schema_extra.get("metadata", {})
                if isinstance(metadata, list):
                    metadata = {item: True for item in metadata}
                if metadata.get("unique") or metadata.get("indexed"):
                    if field.annotation == str :
                        schema_fields[field_name] = ID(stored=True, unique=metadata.get("unique", False))
                    elif field.annotation == int or field.annotation == float :
                        schema_fields[field_name] = NUMERIC(stored=True, unique=metadata.get("unique", False))
                    else:
                        schema_fields[field_name] = TEXT(stored=True,lowercase=True)
        return Schema(**schema_fields)

    def index_objects(self):
        for heroscript in self.heroscripts:
            for obj in self.get_objects():
                index_dir = os.path.join(self.indexpath, type(obj).__name__.lower())
                ix = index.open_dir(index_dir)
                writer = ix.writer()
                writer.add_document(path=heroscript.path, **{k: str(v).lower() for k, v in obj.dict().items() if k in ix.schema.names()})
                writer.commit()
        
    def search(self, class_type, query):
        index_dir = os.path.join(self.indexpath, class_type.__name__.lower())
        ix = index.open_dir(index_dir)
        qp = QueryParser("name", schema=ix.schema)
        q = qp.parse(query)
        with ix.searcher() as searcher:
            results = searcher.search(q)
            # return results
            return [result["path"] for result in results]
