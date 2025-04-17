from util_funcs import *
from util_types import *


def main():
    config = MoriaApiConfig()
    activity_id = 841  # Example ID, replace with actual ID
    activity_url = f"{config.api_url}{config.list_for_student}"

    costam = get_parsed_teachers()
    if costam is None:
        print("❌ Failed to fetch students.")
        return
    for student in costam:
        print(student)

        
main()