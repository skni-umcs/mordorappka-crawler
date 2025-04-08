from util_funcs import get_activity
from util_types import MoriaApiConfig, Activity


def main():
    config = MoriaApiConfig()
    activity_id = 841  # Example ID, replace with actual ID
    activity_url = f"{config.api_url}{config.list_for_student}"
    
    print("activity_url", activity_url)
    
    activity = get_activity(activity_url, activity_id)
    
    
    for a in activity:
        print(a.subject)
        
        
main()