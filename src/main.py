from util_funcs import *
from util_types import *


def main():
    config = MoriaApiConfig()
    activity_id = 840  # Example ID, replace with actual ID
    activity_url = f"{config.api_url}{config.list_for_student}"

    costam = get_parsed_students()

    for a in costam:
        print(a)
        
main()