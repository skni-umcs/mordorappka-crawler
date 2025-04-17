from util_funcs import *
from util_types import *


def main():
    config = MoriaApiConfig()
    activity_id = 841  # Example ID, replace with actual ID
    activity_url = f"{config.api_url}{config.list_for_student}"

    
    resp = fetch_activity_response(activity_url, activity_id)
    parsed = parse_activity_response(resp)
    
    for a in parsed:
        print(a)
     

        
main()