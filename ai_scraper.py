import requests
import sqlite3
import time
import os
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# 1. SETUP: Configure the Groq AI Securely
# ==========================================
# This line finds your .env file and loads the secrets into memory
load_dotenv()

# This pulls the specific key you named in the .env file
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("❌ ERROR: API key not found. Please check your .env file.")
    exit()

client = Groq(api_key=API_KEY)

def extract_skills_with_ai(raw_description):
    """The Inspector: Cleans the messy text using Meta's Llama 3 via Groq."""
    prompt = f"""
    You are an expert technical recruiter. Read the following job description. 
    Extract all technical skills, programming languages, and frameworks mentioned.
    Return ONLY a comma-separated list of the skills. 
    Do NOT include any conversational text. If none are found, return "None".
    
    JOB DESCRIPTION:
    {raw_description}
    """
    try:
        # We use Llama 3 8B because it is insanely fast and great at basic extraction
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        return "Extraction Error"

# ... The rest of your run_job_pipeline() code stays EXACTLY the same! ...

# ==========================================
# 2. THE MAIN PIPELINE
# ==========================================
def run_job_pipeline():
    print("🚀 Starting the AI Job Scraper...")
    
    # --- STEP 1: The Claw (Fetch Data from Remotive) ---
    print("📡 Fetching jobs from Remotive's Open API...")
    
    # We use a simple GET request. 
    # category=software-dev guarantees we get SWE jobs, and limit=5 keeps it fast for testing!
    api_url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=5"
    
    # Notice we don't even need headers/disguises because they welcome developers!
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"❌ Server error: {response.status_code}")
        return

    # Remotive stores their jobs list inside a 'jobs' key
    job_list = response.json().get('jobs', [])
    
    if not job_list:
        print("❌ No jobs found.")
        return

    # --- STEP 2: Connect to the Warehouse (Database) ---
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    inserted_count = 0
    
    # --- STEP 3: Process Each Job ---
    for job in job_list:
        title = job.get('title', 'Unknown Title')
        company = job.get('company_name', 'Unknown Company')
        url = job.get('url', '')
        
        # Remotive puts the massive HTML text block in the 'description' key
        messy_text = job.get('description', '') 
        
        # --- THE FIX: Chop the text to keep it under the token limit ---
        short_text = messy_text[:3000]

        # Prevent duplicates using both company and title
        cursor.execute("SELECT id FROM internship_postings WHERE company_name = ? AND role_title = ?", (company, title))
        if cursor.fetchone():
            print(f"⏭️ Skipping '{title}' at {company} (Already in database)")
            continue
            
        # The Magic Moment: Ask Groq/Llama3 to clean the text
        print(f"🤖 AI is analyzing: '{title}' at {company}...")
        clean_skills = extract_skills_with_ai(short_text)
        
        # Insert the completely clean data into SQLite!
        cursor.execute("""
            INSERT INTO internship_postings (company_name, role_title, posting_url, required_skills)
            VALUES (?, ?, ?, ?)
        """, (company, title, url, clean_skills))
        
        inserted_count += 1
        
        # Pause for 2 seconds so we don't overwhelm the free Groq API limits
        time.sleep(2) 
        
    # Save the database and close it
    conn.commit()
    conn.close()
    
    print(f"🎉 Pipeline Complete! Added {inserted_count} new jobs with AI-extracted skills.")

if __name__ == "__main__":
    run_job_pipeline()