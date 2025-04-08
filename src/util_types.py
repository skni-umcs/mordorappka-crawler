from dataclasses import dataclass, field
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
    
    def __str__(self):
        return (
            f"🎓 Activity #{self.id} — {self.subject} (type: {self.type.name})\n"
            f"📅 Events: {len(self.event_array)} | 👨‍🎓 Students: {self.students_count} | 👨‍🏫 Teachers: {self.teacher_count}\n"
            f"🧑‍🏫 {[t.name for t in self.teacher_array]}\n"
            f"📆 {', '.join([f'Day {e.weekday} @ {e.start_time}' for e in self.event_array])}"
        )


@dataclass
class MoriaApiConfig:
    api_url: str = field(init=False, default = "http://moria.umcs.lublin.pl/api/")
    # For Activity
    list_for_room: str = field(init=False, default = "activity_list_for_room")
    list_for_student: str = field(init=False, default = "activity_list_for_students")
    list_for_teacher: str = field(init=False, default = "activity_list_for_teacher")

    
    
    