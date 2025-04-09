from typing import Optional, List
import requests
from dacite import from_dict
import dacite
from util_types import Activity

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
