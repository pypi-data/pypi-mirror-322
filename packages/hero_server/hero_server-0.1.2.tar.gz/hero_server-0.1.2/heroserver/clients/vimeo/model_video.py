from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from dataclasses_json import dataclass_json
import json
import yaml

def json_to_yaml(json_data):
    # If the input is a JSON string, parse it into a Python dictionary
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    # Convert the dictionary to a YAML formatted string
    yaml_data = yaml.dump(json_data, sort_keys=False, default_flow_style=False)
    
    return yaml_data


@dataclass_json
@dataclass
class Size:
    width: int
    height: int
    link: str
    link_with_play_button: Optional[str] = None

@dataclass_json
@dataclass
class Pictures:
    uri: str
    active: bool
    type: str
    base_link: str
    sizes: List[Size]
    resource_key: str
    default_picture: bool

@dataclass_json
@dataclass
class Embed:
    html: str
    badges: Dict[str, Any]
    interactive: bool
    buttons: Dict[str, bool]
    logos: Dict[str, Any]
    play_button: Dict[str, Any]
    title: Dict[str, Any]
    end_screen: List[Any]
    playbar: bool
    quality_selector: Optional[str]
    pip: bool
    autopip: bool
    volume: bool
    color: str
    colors: Dict[str, str]
    event_schedule: bool
    has_cards: bool
    outro_type: str
    show_timezone: bool
    cards: List[Any]
    airplay: bool
    audio_tracks: bool
    chapters: bool
    chromecast: bool
    closed_captions: bool
    transcript: bool
    ask_ai: bool
    uri: Optional[str]
    email_capture_form: Optional[str]
    speed: bool

@dataclass_json
@dataclass
class Uploader:
    pictures: Pictures

@dataclass_json
@dataclass
class User:
    uri: str
    name: str
    link: str
    capabilities: Dict[str, bool]
    location: str
    gender: str
    bio: str
    short_bio: str
    created_time: str
    pictures: Pictures
    websites: List[Dict[str, Optional[str]]]
    #metadata: Dict[str, Any]
    location_details: Dict[str, Optional[Any]]
    skills: List[Any]
    available_for_hire: bool
    can_work_remotely: bool
    preferences: Dict[str, Any]
    content_filter: List[str]
    upload_quota: Dict[str, Any]
    resource_key: str
    account: str

@dataclass_json
@dataclass
class VideoInfo:
    uri: str
    name: str
    description: Optional[str]
    type: str
    link: str
    player_embed_url: str
    duration: int
    width: int
    height: int
    #embed: Embed
    created_time: str
    modified_time: str
    release_time: str
    content_rating: List[str]
    content_rating_class: str
    rating_mod_locked: bool
    license: Optional[str]
    privacy: Dict[str, Any]
    pictures: Pictures
    tags: List[Any]
    stats: Dict[str, int]
    categories: List[Any]
    uploader: Uploader
    #metadata: Dict[str, Any]
    manage_link: str
    #user: Optional[User]
    last_user_action_event_date: Optional[str]
    parent_folder: Optional[Dict[str, Any]]
    review_page: Optional[Dict[str, Any]]
    files: Optional[List[Dict[str, Any]]]
    download: Optional[List[Dict[str, Any]]]
    app: Optional[Dict[str, str]]
    play: Optional[Dict[str, Any]]
    status: str
    resource_key: str
    upload: Optional[Dict[str, Optional[str]]]
    transcode: Dict[str, str]
    is_playable: bool
    has_audio: bool
    

def video_model_load(json_data:str,dojsonload:bool=True) -> VideoInfo:
    
    if dojsonload:
        json_dict = json.loads(json_data)
    else:
        json_dict = json_data
    
    json_dict.pop('metadata', {})
    json_dict.pop('embed', {})
    json_dict.pop('user', {})
    json_dict.pop('websites', {})
    # if 'user' in json_dict:
    #     json_dict['user'].pop('metadata', None)
    # if 'websites' in json_dict:
    #     json_dict['websites'].pop('metadata', None)
            
    
    json_data_cleaned = json.dumps(json_dict)
        
    video_object = VideoInfo.from_json(json_data_cleaned)
         
    return video_object


def videos_model_load(json_data:str) -> List[VideoInfo]:
    json_list = json.loads(json_data)
    json_list2= list()
    
    for item in json_list["data"]:        
        d=video_model_load(item,dojsonload=False)
        json_list2.append(d)
         
    return json_list2