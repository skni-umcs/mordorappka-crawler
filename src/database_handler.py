from database_connection import *



db = DatabaseConnection()

db.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)

print(db.fetchall())