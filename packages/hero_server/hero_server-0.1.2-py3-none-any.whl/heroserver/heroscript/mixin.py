from pydantic import BaseModel, Field
from typing import Dict, Any, Type, TypeVar
import re
from colorama import Fore, Style
import hashlib
import json
import os
from types import List
from heroscript.heroaction import HeroAction
from heroscript.tools import format_multiline_text
    
class HeroScriptMixin:
    
    def heroscript(self) -> HeroAction:
        class_name = self.__class__.__name__.lower()
        prop_order = ["id", "oid", "name", "title", "description", "content"]
            
        # Get all the properties of the object
        props = list(self.__fields__.keys())
        
        # Separate properties into those in prop_order and the rest
        ordered_props = [prop for prop in prop_order if prop in props]
        remaining_props = [prop for prop in props if prop not in prop_order]
        
        # Sort the remaining properties
        sorted_remaining_props = sorted(remaining_props)
        
        # Combine the ordered properties and sorted remaining properties
        sorted_props = ordered_props + sorted_remaining_props
        
        lines = [f"!!{class_name}.define"]
        for prop in sorted_props:
            if prop in self.__fields__:
                val = getattr(self, prop)
            if isinstance(val, str):
                if "\n" in val:
                    val = format_multiline_text(text=val)
                elif any(c.isspace() for c in val):
                    val = f"'{val}'"
            lines.append(f"    {prop}:{val}")
        
        result = "\n".join(lines)
                
        return HeroAction(content=result)

    @classmethod
    def from_heroscript(cls, heroscript: str):
        lines = heroscript.strip().split("\n")
        class_name = lines[0].split("!!")[1].split(".")[0]
        
        props = {}
        multiline_prop = None
        multiline_value = List(str)
        
        for line in lines[1:]:
            if multiline_prop:
                if line.strip() == "'":
                    # End of multiline text
                    min_indent = min(len(ml) - len(ml.lstrip()) for ml in multiline_value if ml.strip())
                    unindented_lines = [ml[min_indent:] for ml in multiline_value]
                    props[multiline_prop] = "\n".join(unindented_lines)
                    multiline_prop = None
                    multiline_value = []
                else:
                    multiline_value.append(line)
            else:
                if ":" in line:
                    prop, value = line.split(":", 1)
                    prop = prop.strip()
                    value = value.strip()
                    
                    if value == "'":
                        # Start of multiline text
                        multiline_prop = prop
                    else:
                        if value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        props[prop] = value
        
        return cls(**props)
 

