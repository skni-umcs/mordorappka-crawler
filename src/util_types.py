from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Event:
    id: int
    weekday: int
    start_time: str
    length: str
    break_length: str
    end_time: str
    room_id: int
    room: str

@dataclass
class Student:
    id: int
    name: str
    group: int
    groups: int

@dataclass
class Teacher:
    id: int
    name: str

@dataclass
class Type:
    id: int
    name: str
    shortcut: str

@dataclass
class Activity:
    id: int
    subject_id: int
    subject: str
    event_array: List[Event]
    students_count: int
    students_array: List[Student]
    teacher_array: List[Teacher]
    teacher_count: int
    type: Type


@dataclass
class MoriaApiConfig:
    url: str = "http://moria.umcs.lublin.pl/api/"
    
    