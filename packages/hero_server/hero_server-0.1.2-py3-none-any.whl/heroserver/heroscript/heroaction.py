
from herotools.texttools import dedent
from typing import List, Dict, Tuple
import re
from heroscript.tools import action_blocks,format_multiline_text,heroscript_repr
import textwrap

class HeroActions:
    def __init__(self, path: str = "", content:str = ""):
        blocks=action_blocks(path=path,content=content)
        self.actions : List[HeroAction] = []
        for block in blocks:
            self.actions.append(HeroAction(block))

    def __repr__(self):
        out=""
        for item in self.actions:            
            out+=item.__repr__()+"\n"
        return out
            

class HeroAction:
    def __init__(self, content: str):
        blocks=action_blocks(content=content)
        if len(blocks)==0:
            raise ValueError(f"don't find actions in {content}")
        elif len(blocks)>1:
            raise ValueError(f"Found more than one action in {content}")
        content=blocks[0]
        self.name, content = _name_paramstr(content)
        self.params = Params(content)
    
    def __str__(self):
        param_str=textwrap.indent(self.params.__str__(),"    ")
        return f"!!{self.name}\n{param_str}"
    
    def __repr__(self):
        #return self.__str__()
        return heroscript_repr(self.__str__())


class Params:
    def __init__(self, content: str):
        self.__params = params_parse(content)
    
    def __str__(self):
        sorted_params = sorted(self.__params.items())
        param_str=""
        for key,value in sorted_params:
            if "'" in value:
                param_str+=f"{key}: {value}\n"
            elif "\n" in value:
                v=format_multiline_text(value)
                param_str+=f"{key}: {v}\n"
            elif " " in value:
                param_str+=f"{key}: '{value}'\n"                
            else:
                param_str+=f"{key}: {value}\n"
        return param_str

    
    def get_int(self, key: str, defval: int = 99999999) -> int:
        if key not in self.__params:
            if defval == 99999999:
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return int(self.__params[key])
        
    def get_float(self, key: str, defval: float = 99999999.0) -> float:
        if key not in self.__params:
            if defval == 99999999.0:
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return float(self.__params[key])
    
    def get(self, key: str, defval: str = "99999999") -> str:
        if key not in self.__params:
            if defval == "99999999":
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return self.__params[key]
    
    def get_list(self, key: str, defval: List[str] = [], needtoexist: bool = True) -> List[str]:
        if defval is None:
            defval = []
        if key not in self.__params:
            if needtoexist:
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return [item.strip().strip("'").strip() for item in self.__params[key].split(",")]
    
    def get_list_int(self, key: str, defval: List[int] = [], needtoexist: bool = True) -> List[int]:
        if defval is None:
            defval = []
        if key not in self.__params:
            if needtoexist:
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return [int(item.strip()) for item in self.__params[key].split(",")]
    
    def get_list_float(self, key: str, defval: List[float] = [], needtoexist: bool = True) -> List[float]:
        if defval is None:
            defval = []
        if key not in self.__params:
            if needtoexist:
                raise KeyError(f"Key '{key}' must exist in parameters")
            return defval
        return [float(item.strip()) for item in self.__params[key].split(",")]
    
    def get_all(self) -> Dict[str, str]:
        return self.__params


def _name_paramstr(heroscript: str) -> Tuple[str, str]:
    if not isinstance(heroscript, str):
        raise ValueError("Input must be a string")

    heroscript = dedent(heroscript)
    lines = heroscript.strip().split("\n")
    if not lines or "!!" not in lines[0]:
        raise ValueError("The first line must contain '!!' to indicate the class name")

    try:
        class_name = lines[0].split("!!")[1].lower().strip()
    except IndexError:
        raise ValueError("Invalid format for class name extraction")

    rest_of_text = dedent("\n".join(lines[1:]))
    return class_name, rest_of_text


def params_parse(content: str) -> Dict[str, str]:
    lines = dedent(content).strip().split("\n")
    props = {}
    multiline_prop = None
    multiline_value : List[str] = list()

    for line in lines:
        if multiline_prop:
            if line.strip() == "'":
                props[prop] = dedent("\n".join(multiline_value))    
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
                    multiline_prop = prop
                else:
                    if value.startswith("'") and value.endswith("'"):
                        value1 = value[1:-1]
                        if not "'" in value1:
                            value=value1
                    props[prop] = value
    return props



if __name__ == "__main__":

    # Example usage
    text = """
        
        !!obj1.define
            myname:    'mymama'
            mylist: '20,200'
            mylist2: 20,'a bbb'
            mylist3: 20,200
            myint:2                   

        !!obj2.color
            mother: 'mymama'
            name:'aurelie'
            length:60
            description:'
                multiline is supported 
                now for aurelie
                '
            color:green
    """


    hero_actions = HeroActions(content=text)
    print(hero_actions)
    
    a2=hero_actions.actions[1]
    
    
    assert a2.params.get_list(key="color")==["green"]
    assert a2.params.get_list(key="mother")==["mymama"]
    assert a2.params.get(key="color")=="green"
    assert a2.params.get_int(key="length")==60
    assert a2.params.get_list_int(key="length")==[60]
    
    #now some non existing ones
    assert a2.params.get_int(key="lengtha",defval=3)==3
    assert a2.params.get(key="lengtha",defval="3")=="3"
    
    a1=hero_actions.actions[0]
    #print(a1.params.get_list(key="mylist2"))
    assert a1.params.get_list(key="mylist")==["20","200"]
    assert a1.params.get_list_int(key="mylist")==[20,200]
    assert a1.params.get_list(key="mylist2")==["20","a bbb"]