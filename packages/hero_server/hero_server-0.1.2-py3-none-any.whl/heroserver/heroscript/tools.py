
from typing import List
import os
from colorama import Fore, Style
from herotools.texttools import dedent
import textwrap

#load the heroscripts from filesystem
def heroscript_blocks(path: str) ->  List[str]:
    
    heroscript_blocks = list()
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    blocks = _extract_heroscript_blocks(content)
                    heroscript_blocks.extend(blocks)
    
    return heroscript_blocks


def _extract_heroscript_blocks(content: str):
    content=dedent(content)
    blocks = []
    lines = content.split("\n")
    
    in_block = False
    block_lines : List[str] = list()
    
    for line in lines:
        if line.startswith("```hero"):
            in_block = True
            block_lines = []
        elif line.startswith("```") and in_block:
            in_block = False
            block = "\n".join(block_lines)
            blocks.append(block)
        elif in_block:
            block_lines.append(line)
    return blocks     


def action_blocks(path: str = "", content:str = "") ->  List[str]:
    if content!="":
        return __action_blocks_get(content)
    res : List[str] = list()
    for hscript in heroscript_blocks(path):
        for actionscript in __action_blocks_get(hscript):
            res.append(actionscript)
    return res
    
def __action_blocks_get(content: str) ->  List[str]:
    content=dedent(content)
    blocks = list()
    lines = content.split("\n")
    
    block_lines : List[str] = list()
    herofound=False
    
    for line in lines:
        # print(line)
        if line.startswith("!!"):
            herofound=True
            if block_lines: #means we found before
                block = "\n".join(block_lines)
                blocks.append(block)
                block_lines = []
                # print("f1")
            block_lines.append(line)
        elif line.strip() and not line.startswith(" ") and not line.startswith("\t") and block_lines:
            block = "\n".join(block_lines)
            blocks.append(block)
            block_lines = []
            herofound=False
        elif herofound:
            block_lines.append(line)
            # print("append")
        
    if block_lines:
        block = "\n".join(block_lines)
        blocks.append(block)
    
    return blocks

def myprint(obj):
    class_name = f"{Fore.YELLOW}{obj.__class__.__name__}{Style.RESET_ALL}"
    fields = [field for field in obj.__fields__ if field in obj.__dict__]
    attributes = ', '.join(f"{Fore.LIGHTBLACK_EX}{field}{Style.RESET_ALL}={Fore.GREEN}'{getattr(obj, field)}'{Style.RESET_ALL}" for field in fields)
    print( f"{class_name}({attributes})" )


#format text to be ready to be set in heroscript
def format_multiline_text(text: str) -> str:
    
    text = dedent(text)
    text = textwrap.indent(text, "    ")
    
    # Join the formatted lines with newline characters and add the required indentation
    formatted_text = "'\n" + text + "\n    '"
    
    return formatted_text    



#representation with colors of heroscript
def heroscript_repr(content:str) ->str:
    lines = content.split("\n")
    formatted_lines = []
    
    for line in lines:
        if line.startswith("!!"):
            formatted_line = f"{Fore.RED}{line}{Style.RESET_ALL}"
        elif ":" in line:
            prop, value = line.split(":", 1)
            prop = prop.strip()
            value = value.strip()
            
            if value.startswith("'") and value.endswith("'"):
                value = f" {Fore.GREEN}{value}{Style.RESET_ALL}"
            else:
                value = f" {Fore.YELLOW}{value}{Style.RESET_ALL}"
            
            formatted_line = f"    {Fore.CYAN}{prop}{Style.RESET_ALL}:{value}"
        else:
            formatted_line = line
        
        formatted_lines.append(formatted_line)
    
    return "\n".join(formatted_lines)

def heroscript_print(content:str):
    o=heroscript_repr(content)
    print(o)
    
    
if __name__ == "__main__":
    
    t="  something\n  a\n\n  bbbb"
    
    print(dedent(t))
    
    print(format_multiline_text(t))