from util_funcs import *
from util_types import *
from database_handler import DBHandler
from crawler_utils import *


def main():
    
    url = MoriaApiConfig().api_url + MoriaApiConfig.list_for_student
    
    activites = get_parsed_activity_list(url, 841)

    for activity in activites:
        print(activity)    
    

    # update_subjects(DBHandler())
    
main()