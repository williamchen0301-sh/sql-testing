import sqlite3

def add_job_posting():
    print("\n--- Add a New Internship Posting ---")
    
    # 1. Gather input from the user
    company_name = input("Company Name (e.g., Google, Acme Corp): ").strip()
    role_title = input("Role Title (e.g., Software Engineering Intern): ").strip()
    posting_url = input("Posting URL (optional, press Enter to skip): ").strip()
    required_skills = input("Required Skills (comma-separated, e.g., Python, SQL): ").strip()
    preferred_skills = input("Preferred Skills (comma-separated, e.g., Docker, AWS): ").strip()
    degree_reqs = input("Degree Requirements (e.g., BS CS, Junior): ").strip()
    
    # 2. Connect to the database
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    # 3. The parameterized SQL query using '?' placeholders
    insert_sql = """
    INSERT INTO internship_postings (
        company_name, 
        role_title, 
        posting_url, 
        required_skills, 
        preferred_skills, 
        degree_reqs
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    
    # 4. The tuple containing our sanitized user inputs
    data_tuple = (company_name, role_title, posting_url, required_skills, preferred_skills, degree_reqs)
    
    try:
        # 5. Execute the query with the data tuple
        cursor.execute(insert_sql, data_tuple)
        conn.commit()
        print(f"\n✅ Success! Added '{role_title}' at '{company_name}' to the database.")
    except sqlite3.Error as e:
        print(f"\n❌ An error occurred with the database: {e}")
    finally:
        # 6. Always close the connection
        conn.close()

if __name__ == "__main__":
    # A simple loop to let you enter multiple postings without restarting the script
    while True:
        add_job_posting()
        
        # Ask if the user wants to keep going
        cont = input("\nDo you want to add another posting? (y/n): ").strip().lower()
        if cont != 'y':
            print("\nExiting tracker. Happy hunting!")
            break