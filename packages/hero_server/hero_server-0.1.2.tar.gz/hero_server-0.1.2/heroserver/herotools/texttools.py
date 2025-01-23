
import re
import unicodedata
import random


def description_fix(description):
    description = description.lower()
    description = unicodedata.normalize('NFKD', description).encode('ASCII', 'ignore').decode('ASCII')
    description = re.sub(r'[^a-z0-9\s]', '', description)    
    return description.strip()


# def name_fix(name: str) -> str:
#     """
#     Normalize the string to lowercase ASCII, replace spaces and specific punctuations with underscores,
#     and remove non-ASCII characters.
#     """
#     name = name.lower()
#     name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
#     name = re.sub(r'[ :;!]', '_', name)  # Replace spaces and specific punctuations with underscores
#     name = re.sub(r'\W+', '', name)  # Remove any other non-word characters
#     return name


def name_fix(name: str) -> str:
    """
    Normalize the string to lowercase ASCII, replace spaces and specific punctuations with underscores,
    maintain dots, and remove non-ASCII characters.
    """
    name = name.lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[ :;!]', '_', name)  # Replace spaces and specific punctuations with underscores
    name = re.sub(r'[^\w._]+', '', name)  # Remove any non-word characters except dots and underscores
    return name

def name_obfuscate(name):
    # Define a mapping of consonants to their obfuscated counterparts
    consonant_map = {
        'b': 'p', 'c': 'k', 'd': 't', 'f': 'v', 'g': 'j', 'h': 'x',
        'j': 'q', 'k': 'c', 'l': 'r', 'm': 'n', 'n': 'm', 'p': 'b',
        'q': 'g', 'r': 'l', 's': 'z', 't': 'd', 'v': 'f', 'w': 'y',
        'x': 'h', 'y': 'w', 'z': 's'
    }

    # Define a mapping of vowels to their obfuscated counterparts
    vowel_map = {
        'a': 'e', 'e': 'i', 'i': 'o', 'o': 'u', 'u': 'a'
    }

    # Convert the name to lowercase
    name = name.lower()

    # Split the name into words
    words = name.split()

    obfuscated_words = []
    for word in words:
        obfuscated_word = ''
        for char in word:
            if char in vowel_map:
                # Obfuscate vowels
                obfuscated_word += vowel_map[char]
            elif char in consonant_map:
                # Obfuscate consonants
                obfuscated_word += consonant_map[char]
            else:
                # Keep non-alphabetic characters unchanged
                obfuscated_word += char
        obfuscated_words.append(obfuscated_word)

    # Join the obfuscated words back into a single string
    obfuscated_name = ' '.join(obfuscated_words)

    # Capitalize the first letter of each word
    obfuscated_name = obfuscated_name.title()

    return obfuscated_name

def dedent(content: str) -> str:
    # Split the input content into lines
    lines = content.splitlines()
    
    # Remove leading and trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    
    if not lines:
        return ""
    
    # Find the minimum indentation (leading spaces) in all non-empty lines
    min_indent = None
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:  # Only consider non-empty lines
            leading_spaces = len(line) - len(stripped_line)
            if min_indent is None or leading_spaces < min_indent:
                min_indent = leading_spaces
    
    # Dedent each line by the minimum indentation found
    dedented_lines = [line[min_indent:] if len(line) > min_indent else line for line in lines]
    
    # Join the dedented lines back into a single string
    return "\n".join(dedented_lines)

if __name__ == "__main__":
    print("fixed name:", name_fix("John Doe"))
    print("obfuscated name:", name_obfuscate("John Doe"))