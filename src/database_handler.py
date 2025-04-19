from database_connection import *
from util_types import *
from datetime import datetime, timezone

class DBHandler:
    connection: None
    
    def __init__(self, host, port):
        self.connection = DatabaseConnection()
        
        
    
    def insert_faculty(self, id: int, name: str) -> None:
         
        query = """
            INSERT INTO faculties (faculty_id, faculty_name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        
        self.connection.execute(query, (id, name))
        
    
    def insert_period(self, id: int, winter_term: bool, academic_year: str):
        
        query = """
            INSERT INTO periods (period_id, winter_term, academic_year)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        self.connection.execute(query, (id, winter_term, academic_year))
        
        
        
    def insert_major(self, id: int, name: str, degree: str, duration: int, faculty_id: int, active: bool):
        
        query = """
            INSERT INTO majors (major_id, major_name, major_degree, duration_in_sems, faculty_id, active)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        self.connection.execute(query, (id, name, degree, duration, faculty_id, active))
        
        
    def insert_term_groups(self, id: int, year: int, major_id: int, period_id: int):
        
        query = """
            INSERT INTO term_groups (term_group_id, year, major_id, period_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        self.connection.execute(query, (id, year, major_id, period_id))
        
    def insert_subjects(self, id: int, term_group_id: int, name: str, period_id: int): 
            
            query = """
                INSERT INTO subjects (subject_id, term_group_id, subject_name, period_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """
            
            self.connection.execute(query, (id, term_group_id, name, period_id))
    
    
    def insert_room(self, room_id: int, room_number: int, faculty_id: int, room_address: str, room_capacity: int):
        
        query = """
            INSERT INTO rooms (room_id, room_number, faculty_id, room_address, room_capacity)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """
        
        self.connection.execute(query, (room_id, room_number, faculty_id, room_address, room_capacity))
        
    def insert_teacher(self, teacher_id: int, teacher_name: str, teacher_degree: str, faculty_id: int, active: bool):
            
            query = """
                INSERT INTO teachers (teacher_id, teacher_name, teacher_degree, faculty_id, active)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """
            
            self.connection.execute(query, (teacher_id, teacher_name, teacher_degree, faculty_id, active))
            
    def insert_class(self, class_id: int, class_type: str, subject_id: int, group_id: int, teacher_id: int, start_time: datetime, end_time: datetime, break_duration: int, weekday: int, every_two_weeks: bool, room_id: int, term_group_id: int):
            
            query = """
                INSERT INTO classes (class_id, class_type, subject_id, group_id, teacher_id, start_time, end_time, break_duration, weekday, every_two_weeks, room_id, term_group_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """
            
            self.connection.execute(query, (class_id, class_type, subject_id, group_id, teacher_id, start_time, end_time, break_duration, weekday, every_two_weeks, room_id, term_group_id))
