import sqlite3

def update_posting(cursor, conn):
    print("\n--- ✏️ Update a Posting ---")
    record_id = input("Enter the ID of the posting you want to update: ").strip()
    
    # First, let's make sure the ID exists
    cursor.execute("SELECT company_name, role_title FROM internship_postings WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    
    if not record:
        print(f"❌ No posting found with ID {record_id}.")
        return
        
    print(f"Updating: [{record_id}] {record[0]} - {record[1]}")
    print("(Press Enter to keep current value)")
    
    # Ask for new values, but allow skipping
    new_req_skills = input("New Required Skills: ").strip()
    new_pref_skills = input("New Preferred Skills: ").strip()
    
    # Only update the fields the user actually typed something for
    if new_req_skills:
        cursor.execute("UPDATE internship_postings SET required_skills = ? WHERE id = ?", (new_req_skills, record_id))
    if new_pref_skills:
        cursor.execute("UPDATE internship_postings SET preferred_skills = ? WHERE id = ?", (new_pref_skills, record_id))
        
    conn.commit()
    print(f"✅ Posting {record_id} updated successfully!")

def delete_posting(cursor, conn):
    print("\n--- 🗑️ Delete a Posting ---")
    record_id = input("Enter the ID of the posting you want to delete: ").strip()
    
    # Verify the record exists before deleting
    cursor.execute("SELECT company_name, role_title FROM internship_postings WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    
    if not record:
        print(f"❌ No posting found with ID {record_id}.")
        return
        
    # Always ask for confirmation before a DELETE operation!
    confirm = input(f"Are you SURE you want to delete '{record[0]} - {record[1]}'? (y/n): ").strip().lower()
    
    if confirm == 'y':
        cursor.execute("DELETE FROM internship_postings WHERE id = ?", (record_id,))
        conn.commit()
        print(f"✅ Posting {record_id} has been deleted.")
    else:
        print("Phew! Deletion canceled.")

def main_menu():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    try:
        while True:
            print("\n--- ⚙️ Manage Postings ---")
            print("1. Update a posting's skills")
            print("2. Delete a posting")
            print("3. Exit")
            
            choice = input("Choose an option (1-3): ").strip()
            
            if choice == '1':
                update_posting(cursor, conn)
            elif choice == '2':
                delete_posting(cursor, conn)
            elif choice == '3':
                print("Exiting manager.")
                break
            else:
                print("Invalid choice.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main_menu()