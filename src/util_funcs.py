from typing import Optional, List
import requests
from dacite import from_dict
import dacite
from util_types import *

# Function to fetch the API response
def fetch_activities(url: str, id: int) -> Optional[requests.Response]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "id": id
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            return None

        return response
    except Exception as e:
        print(f"❌ Error during request execution: {str(e)}")
        return None

# Function to parse JSON response into a list of Activity objects
def parse_activities(response: requests.Response) -> Optional[List[Activity]]:
    try:
        data = response.json()

        # Check if the response structure is as expected
        if "result" not in data or "array" not in data["result"]:
            print("❌ Unexpected API response structure.")
            return None

        activities_data = data["result"]["array"]

        if not activities_data:
            print("❌ No activities found.")
            return None

        activities = []
        for activity_data in activities_data:
            try:
                # Convert JSON data to Activity object using dacite
                activity = from_dict(
                    data_class=Activity,
                    data=activity_data,
                    config=dacite.Config(check_types=False)
                )
                activities.append(activity)
            except Exception as e:
                print(f"❌ Error processing activity: {str(e)}")
                print(f"Problematic data: {activity_data}")
                continue

        if not activities:
            print("❌ Failed to process any activity.")
            return None

        return activities
    except Exception as e:
        print(f"❌ Error while processing response data: {str(e)}")
        return None

def get_parsed_activity_list(url: str, id: int) -> Optional[List[Activity]]:
    response = fetch_activities(url, id)
    if response is None:
        return None

    activities = parse_activities(response)
    if activities is None:
        return None

    return activities

def fetch(url: str) -> Optional[requests.Response]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
        )

        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            return None

        return response
    except Exception as e:
        print(f"❌ Error during request execution: {str(e)}")
        return None
    
    
def parse_students(response: requests.Response) -> Optional[List[Student]]:
    try:
        data = response.json()

        if "result" not in data or "array" not in data["result"]:
            print("❌ Unexpected API response structure.")
            return None

        students_data = data["result"]["array"]

        if not students_data:
            print("❌ No students found.")
            return None

        students = []
        for student_data in students_data:
            try:
                student = from_dict(
                    data_class=Student,
                    data=student_data,
                    config=dacite.Config(check_types=False)
                )
                students.append(student)
            except Exception as e:
                print(f"❌ Error processing student: {str(e)}")
                print(f"Problematic data: {student_data}")
                continue

        if not students:
            print("❌ All entries were empty or invalid.")
            return None

        return students
    except Exception as e:
        print(f"❌ Error while processing response data: {str(e)}")
        return None



def get_parsed_students() -> Optional[List[Student]]:
    config = MoriaApiConfig()
    activity_url = f"{config.api_url}{config.list_for_students_id}"
    response = fetch(activity_url)
    if response is None:
        return None

    students = parse_students(response)
    if students is None:
        return None

    filtered_students = [s for s in students if s.name and ("I st." in s.name or "II st." in s.name or "I stopnia" in s.name or "II stopnia" in s.name)]
    return filtered_students


def parse_rooms(response: requests.Response) -> Optional[List[Room]]:
    try:
        data = response.json()

        if "result" not in data or "array" not in data["result"]:
            print("❌ Unexpected API response structure.")
            return None

        rooms_data = data["result"]["array"]

        if not rooms_data:
            print("❌ No rooms found.")
            return None

        rooms = []
        for room_data in rooms_data:
            try:
                room = from_dict(
                    data_class=Room,
                    data=room_data,
                    config=dacite.Config(check_types=False)
                )
                rooms.append(room)
            except Exception as e:
                print(f"❌ Error processing room: {str(e)}")
                print(f"Problematic data: {room_data}")
                continue

        if not rooms:
            print("❌ All entries were empty or invalid.")
            return None

        return rooms
    except Exception as e:
        print(f"❌ Error while processing response data: {str(e)}")
        return None
    
def get_parsed_rooms() -> Optional[List[Room]]:
    config = MoriaApiConfig()
    activity_url = f"{config.api_url}{config.list_for_rooms_id}"
    response = fetch(activity_url)
    if response is None:
        return None

    rooms = parse_rooms(response)
    if rooms is None:
        return None

    return rooms


def parse_teachers(response: requests.Response) -> Optional[List[Teacher]]:
    try:
        data = response.json()

        if "result" not in data or "array" not in data["result"]:
            print("❌ Unexpected API response structure.")
            return None

        teachers_data = data["result"]["array"]

        if not teachers_data:
            print("❌ No teachers found.")
            return None

        teachers = []
        for teacher_data in teachers_data:
            try:
                teacher = from_dict(
                    data_class=Teacher,
                    data=teacher_data,
                    config=dacite.Config(check_types=False)
                )
                teachers.append(teacher)
            except Exception as e:
                print(f"❌ Error processing teacher: {str(e)}")
                print(f"Problematic data: {teacher_data}")
                continue

        if not teachers:
            print("❌ All entries were empty or invalid.")
            return None

        return teachers
    except Exception as e:
        print(f"❌ Error while processing response data: {str(e)}")
        return None
    
    
def get_parsed_teachers() -> Optional[List[Teacher]]:
    config = MoriaApiConfig()
    activity_url = f"{config.api_url}{config.list_for_teachers_id}"
    response = fetch(activity_url)
    if response is None:
        return None

    teachers = parse_teachers(response)
    if teachers is None:
        return None

    return teachers