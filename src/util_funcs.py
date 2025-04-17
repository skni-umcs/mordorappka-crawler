from typing import Optional, List
import requests
from dacite import from_dict
import dacite
from util_types import *

# Function to fetch the API response
def fetch_activity_response(url: str, id: int) -> Optional[requests.Response]:
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
def parse_activity_response(response: requests.Response) -> Optional[List[Activity]]:
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


def fetch_students() -> Optional[requests.Response]:
    config = MoriaApiConfig()
    url = f"{config.api_url}{config.list_for_students_id}"
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
    
    
def parse_students_list(response: requests.Response) -> Optional[List[Students]]:
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
            if not student_data or not isinstance(student_data, dict) or len(student_data) == 0:
                # Pomijamy puste 
                continue

            try:
                student = from_dict(
                    data_class=Students,
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
