import sqlite3

def create_database():
    # Connect to SQLite. This creates 'internships.db' in your current folder if it doesn't exist.
    conn = sqlite3.connect('internships.db')
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Write the SQL command to create our MVP table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS internship_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        role_title TEXT NOT NULL,
        posting_url TEXT,
        required_skills TEXT,
        preferred_skills TEXT,
        degree_reqs TEXT,
        date_logged DATE DEFAULT CURRENT_DATE
    );
    """
    
    # Execute the SQL command
    cursor.execute(create_table_sql)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Success! The 'internships.db' database and 'internship_postings' table have been created.")

if __name__ == "__main__":
    create_database()