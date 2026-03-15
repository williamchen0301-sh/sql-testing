import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Internship Tracker", page_icon="💼", layout="wide")
st.title("💼 Internship Tracker (Excel Mode - Bug Fixed!)")

def get_connection():
    return sqlite3.connect('internships.db')

conn = get_connection()
# FIX #1: ALWAYS use ORDER BY so the rows never shuffle randomly when Streamlit reruns
df = pd.read_sql_query("SELECT * FROM internship_postings ORDER BY id", conn)
conn.close()

# FIX #2: Set the 'id' as the index. 
# This acts as a permanent anchor so Streamlit knows EXACTLY which row you are editing.
df.set_index('id', inplace=True)

st.write("Edit the table below just like a spreadsheet! Double-click a cell to edit, or select a row and press Delete/Backspace to remove it.")

# 3. The Magic Interactive Table
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

if st.button("💾 Save All Changes to Database", type="primary"):
    try:
        # FIX #3: Bring the 'id' anchor back as a regular column before saving
        edited_df.reset_index(inplace=True)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # FIX #4: The Safe Save. 
        # Delete the old rows, but KEEP the actual table structure (and rules) intact.
        cursor.execute("DELETE FROM internship_postings")
        
        # Append the edited data back in. This protects your database schema!
        edited_df.to_sql('internship_postings', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        st.success("✅ Database successfully updated! No more ghost edits.")
    except Exception as e:
        st.error(f"An error occurred while saving: {e}")

st.divider() # Adds a nice visual line break
st.subheader("📈 Skill Analytics Engine")
st.write("Find out exactly what skills a specific company is asking for.")

# 1. Ask the user which company they want to analyze
target_company = st.text_input("Enter a company to analyze (e.g., Google, Amazon):").strip()

if target_company:
    # 2. Filter the dataframe to only include that company
    # case=False means "google" and "Google" will both match
    company_df = df[df['company_name'].str.contains(target_company, case=False, na=False)]
    
    if company_df.empty:
        st.warning(f"No postings found for {target_company}.")
    else:
        st.success(f"Found {len(company_df)} postings for {target_company}!")
        
        # 3. The Pandas Magic: Split, Explode, and Count
        # - .str.split(',') turns "Python, SQL" into a list: ['Python', ' SQL']
        # - .explode() turns that list into individual rows
        # - .str.strip() removes the accidental spaces around the words
        all_skills = company_df['required_skills'].dropna().str.split(',').explode().str.strip()
        
        # 4. Count the occurrences and format it as a nice table
        skill_counts = all_skills.value_counts().reset_index()
        skill_counts.columns = ['Skill', 'Times Requested']
        
        # 5. Display the results!
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Most requested skills at {target_company}:**")
            st.dataframe(skill_counts, hide_index=True)
        with col2:
            # Let's add a quick bar chart because Streamlit makes it easy!
            st.write("**Visual Breakdown:**")
            st.bar_chart(skill_counts.set_index('Skill'))