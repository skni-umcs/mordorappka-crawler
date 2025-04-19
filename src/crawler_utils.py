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
    if is_winter_term:
        academic_year = f"{current_year }/{current_year + 1}"
    else:
        academic_year = f"{current_year - 1}/{current_year}"
    
    periods = [
        {"id": 1, "winter_term": is_winter_term, "academic_year": academic_year},
    ]
    
    for period in periods:
        db.insert_period(period["id"], period["winter_term"], period["academic_year"])
    db.connection.commit()
    

import re


# counter zrobiony na odwal sie, powinno brać z bazy danych
def update_majors(db: DBHandler):
    StudentsInformation = get_parsed_students()
    if StudentsInformation is None:
        print("❌ Failed to fetch students information.")
        return
    
    majors = []
    seen_names = set()


    for student in StudentsInformation:
        counter = 1

        # Wywalamy "UWAGA! PLAN MOŻE ULEC ZMIANIE" i numerek z przodu
        name = re.sub(r'^\d+\s*', '', student.name)
        name = re.sub(r'UWAGA!?\s*PLAN MOŻE ULEC ZMIANIE', '', name, flags=re.IGNORECASE).strip()

        # Deduplikacja po oczyszczonej nazwie
        if name in seen_names:
            continue
        seen_names.add(name)
        
        id = counter
        counter += 1

        # Określenie stopnia
        if "I st." in name or "I stopnia" in name:
            degree = "Lic."
            duration = 3
        elif "II st." in name or "II stopnia" in name:
            degree = "Mgr."
            duration = 2
        else:
            degree = "Dr."
            duration = 3  # zgaduję że 3 lata, zmień jak trzeba

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

    
# I Tu sie robią zależności czyli musze czytać z bazy danych jakie id ma jakis tam major i tak dalej