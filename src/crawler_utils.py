from util_types import *
from util_funcs import *
from database_handler import DBHandler
from typing import List, Optional
from datetime import datetime, timezone

is_winter_term = datetime.now(timezone.utc).month in [1, 2, 10, 11, 12]
current_year = datetime.now(timezone.utc).year



def update_faculties(db: DBHandler):
    faculties = [
        {"id": 1, "name": "Nieznany Wydział"},
        {"id": 2, "name": "Wydział Matematyki, Fizyki i Informatyki"},
        {"id": 3, "name": "Wydział Nauk o Ziemi i Gospodarki Przestrzennej"},
    ]
    
    for faculty in faculties:
        db.insert_faculty(faculty["id"], faculty["name"])
    db.connection.commit()
    
# Obecnie to zadziała beznadziejnie ale nie wiem jak to zrobić i mi szkoda czasu
def update_periods(db: DBHandler):

    current_year = datetime.now(timezone.utc).year
    is_winter_term = datetime.now(timezone.utc).month in [1, 2, 10, 11, 12]
    academic_year = f"{current_year}/{current_year + 1}" if is_winter_term else f"{current_year - 1}/{current_year}"
    
    id = db.fetch_from("periods", "MAX(period_id)")[0][0] if db.fetch_from("periods", "MAX(period_id)") else 0
    
    periods = [
        {"id": id + 1, "winter_term": is_winter_term, "academic_year": academic_year},
    ]
    
    for period in periods:
        db.insert_period(period["id"], period["winter_term"], period["academic_year"])
    db.connection.commit()
    

import re


def update_majors(db: DBHandler):
    StudentsInformation = get_parsed_students()
    if StudentsInformation is None:
        print("❌ Failed to fetch students information.")
        return
    
    majors = []
    seen_names = set()

    counter = 1
    id = db.fetch_from("majors", "MAX(major_id)")[0][0] if db.fetch_from("majors", "MAX(major_id)") else 0
    for student in StudentsInformation:

        # Wywalamy "UWAGA! PLAN MOŻE ULEC ZMIANIE" i numerek z przodu
        name = re.sub(r'^\d+\s*', '', student.name)
        name = re.sub(r'UWAGA!?\s*PLAN MOŻE ULEC ZMIANIE', '', name, flags=re.IGNORECASE).strip()

        # Deduplikacja po oczyszczonej nazwie
        if name in seen_names:
            continue
        seen_names.add(name)
        
        id = id + 1

        # Określenie stopnia
        if "II st." in name or "II stopnia" in name:
            degree = "Mgr."
            duration = 2
        elif "I st." in name or "I stopnia" in name:
            degree = "Lic."
            duration = 3
        else:
            degree = "Dr."
            duration = 3

        duration = duration * 2

        # Faculty ID – tu trzeba by to kiedyś robić lepiej niż ifami
        if any(x in name for x in ["Matematyka", "Fizyka", "Informatyka"]):
            faculty_id = 2
        elif "Geoinformatyka" in name:
            faculty_id = 3
        else:
            faculty_id = 1

        active = True

        majors.append({
            "id": id,
            "name": name,
            "degree": degree,
            "duration": duration,
            "faculty_id": faculty_id,
            "active": active
        })

    for major in majors:
        db.insert_major(
            major["id"],
            major["name"],
            major["degree"],
            major["duration"],
            major["faculty_id"],
            major["active"]
        )
        
    db.connection.commit()

    
def update_term_groups(db: DBHandler):
    StudentsInformation = get_parsed_students()
    if StudentsInformation is None:
        print("❌ Failed to fetch students information.")
        return
    
    term_groups = []
    
    for student in StudentsInformation:
        name = re.sub(r'^\d+\s*', '', student.name)
        name = re.sub(r'UWAGA!?\s*PLAN MOŻE ULEC ZMIANIE', '', name, flags=re.IGNORECASE).strip()
        digit = re.search(r'\d+', student.name).group()
        year = int(digit)

        
        major = db.fetch_from("majors", "major_id", "major_name = %s", (name,))
        major_id = major[0][0] if major else None
    
        current_year = datetime.now(timezone.utc).year
        is_winter_term = datetime.now(timezone.utc).month in [1, 2, 10, 11, 12]
        academic_year = f"{current_year}/{current_year + 1}" if is_winter_term else f"{current_year - 1}/{current_year}"
    
        period = db.fetch_from("periods", "period_id", "academic_year = %s AND winter_term = %s", (academic_year, is_winter_term))
        period_id = period[0][0] if period else None
        
        
        term_groups.append({
            "id": student.id,
            "year": year if year else None,
            "major_id": major_id,
            "period_id": period_id
        })
        
        
    for term_group in term_groups:
        db.insert_term_groups(
            term_group["id"],
            term_group["year"],
            term_group["major_id"],
            term_group["period_id"]
        )
    db.connection.commit()
    
    
def update_subjects(db: DBHandler):
    StudentsInformation = get_parsed_students()
    if StudentsInformation is None:
        print("❌ Failed to fetch students information.")
        return
    for s in StudentsInformation:
        url = MoriaApiConfig().api_url + MoriaApiConfig.list_for_student
        activites = get_parsed_activity_list(url, s.id)
        print("URL:", url)
        print("Student ID:", s.id)
        if activites is None:
            print("❌ Failed to fetch activity list.")
            continue
        
        subjects = []
        seen_names = set()
        id = db.fetch_from("subjects", "MAX(subject_id)")[0][0] if db.fetch_from("subjects", "MAX(subject_id)") else 0
        for activity in activites:
            
            name = activity.subject
            if name in seen_names:
                continue
            seen_names.add(name)
         
            id = id + 1
            term_group_id = s.id
            
            
            current_year = datetime.now(timezone.utc).year
            is_winter_term = datetime.now(timezone.utc).month in [1, 2, 10, 11, 12]
            academic_year = f"{current_year}/{current_year + 1}" if is_winter_term else f"{current_year - 1}/{current_year}"
    
            period = db.fetch_from("periods", "period_id", "academic_year = %s AND winter_term = %s", (academic_year, is_winter_term))
            period_id = period[0][0] if period else None
            
            
            
            subjects.append({
                "id": id,
                "term_group_id": term_group_id,
                "name": name,
                "period_id": period_id
            })
            
        for subject in subjects:
            db.insert_subjects(
                subject["id"],
                subject["term_group_id"],
                subject["name"],
                subject["period_id"]
            )
            
        db.connection.commit()
            

# update_rooms() jest niemożliwe do zrobienia za duzo wyjątków albo 3 miliony ifów albo zmiana bazy danych

def update_teachers(db: DBHandler):
    TeachersInformation = get_parsed_teachers()
    if TeachersInformation is None:
        print("❌ Failed to fetch teachers information.")
        return
    
    for teacher in TeachersInformation:
        name = teacher.first_name + " " + teacher.last_name
        id = teacher.id
    
        degree = teacher.degree
        
        # Zero jakichkolwiek informacji o wydziale to jest bez sensu xD
        faculty_id = 1
        active = True
        
        db.insert_teacher(
            id,
            name,
            degree,
            faculty_id,
            active
        )
    
    db.connection.commit()
    
    
    
def update_classes(db: DBHandler):
    StudentsInformation = get_parsed_students()
    url = MoriaApiConfig().api_url + MoriaApiConfig.list_for_student
    if StudentsInformation is None:
        print("❌ Failed to fetch students information.")
        return
    
    for student in StudentsInformation:
        activities = get_parsed_activity_list(url, student.id)
        if activities is None:
            print("❌ Failed to fetch activity list.")
            continue
        
        
        for activity in activities:
            
            for event in activity.event_array:
                start_time = event.start_time
                end_time = event.end_time
                break_duration = event.break_duration
                weekday = event.weekday
                every_two_weeks = event.every_two_weeks
                
                
            class_id = activity.id
            
            class_type = activity.type.name
            
            subject_id = db.fetch_from("subjects", "subject_id", "subject_name = %s AND term_group_id = %s", (activity.subject, student.id))
            
            group_id = 
            
            
            