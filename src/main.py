from util_funcs import *
from util_types import *
from database_handler import DBHandler
from crawler_utils import *


def main():
    
    db = DBHandler()
    
    update_all(db)
    
    #TODO: Update indexing on subject_id in update_subjects and update_classes because moria indexing sucks
main()