import sqlite3

def search_and_filter():
    print("\n--- 🔍 Search & Filter Internships ---")
    print("1. View all (Sorted by newest)")
    print("2. Filter by Company")
    print("3. Search for a specific Skill")
    
    choice = input("Choose an option (1-3): ").strip()
    
    # Connect to the database
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    try:
        if choice == '1':
            # Sort by ID descending (which effectively sorts by newest added)
            query = """
            SELECT company_name, role_title, required_skills, preferred_skills 
            FROM internship_postings 
            ORDER BY id DESC
            """
            cursor.execute(query)
            
        elif choice == '2':
            company = input("Enter company name to search: ").strip()
            # We use LIKE with % wildcards to catch partial matches (e.g., "Goog" finds "Google")
            query = """
            SELECT company_name, role_title, required_skills, preferred_skills 
            FROM internship_postings 
            WHERE company_name LIKE ? 
            ORDER BY id DESC
            """
            cursor.execute(query, (f"%{company}%",))
            
        elif choice == '3':
            skill = input("Enter a skill to search for (e.g., Python): ").strip()
            # Search both required and preferred skills for the keyword
            query = """
            SELECT company_name, role_title, required_skills, preferred_skills 
            FROM internship_postings 
            WHERE required_skills LIKE ? OR preferred_skills LIKE ? 
            ORDER BY company_name ASC
            """
            cursor.execute(query, (f"%{skill}%", f"%{skill}%"))
            
        else:
            print("Invalid choice. Please run the script again.")
            return

        # Fetch and display the results
        rows = cursor.fetchall()
        
        print(f"\n--- Results ({len(rows)} found) ---")
        if not rows:
            print("No matching postings found.")
        else:
            for row in rows:
                company, role, req_skills, pref_skills = row
                print(f"🏢 {company} | 💼 {role}")
                print(f"   Required:  {req_skills}")
                print(f"   Preferred: {pref_skills}\n")
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    search_and_filter()