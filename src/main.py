from util_funcs import *
from util_types import MoriaApiConfig, Activity


def main():
    config = MoriaApiConfig()
    activity_id = 841  # Example ID, replace with actual ID
    activity_url = f"{config.api_url}{config.list_for_student}"
    
    print("activity_url", activity_url)
    
    response = fetch_activity_response(activity_url, activity_id)
    activity = parse_activities(response)
    
    
    
    for a in activity:
        print(a.teacher_array)
        
        
main()