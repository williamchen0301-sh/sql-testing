#💼 AI Internship Skill Tracker
##What this app tracks and why
###This application tracks software engineering internship postings and uses an AI pipeline to extract specific technical skills from massive job descriptions. I built this to reverse-engineer the hiring market, allowing me to find exactly which skills and technologies are most in-demand so I can strategically build my resume.

Column Name,Data Type,Description
id,INTEGER PRIMARY KEY,Auto-incrementing unique identifier
company_name,TEXT NOT NULL,Name of the hiring company
role_title,TEXT NOT NULL,Specific title of the internship
posting_url,TEXT,Link to the original job posting
required_skills,TEXT,"AI-extracted, comma-separated list of required skills"
preferred_skills,TEXT,Comma-separated list of bonus skills
degree_reqs,TEXT,"Academic requirements (e.g., BS Computer Science)"
date_logged,DATE,Defaults to CURRENT_DATE when a row is created



Table Name: internship_postings
AI Internship Skill TrackerWhat this app tracks and whyThis application tracks software engineering internship postings and uses an AI pipeline to extract specific technical skills from massive job descriptions. I built this to reverse-engineer the hiring market, allowing me to find exactly which skills and technologies are most in-demand so I can strategically build my resume.🗄️ Database SchemaThe project uses a lightweight, highly portable SQLite database. It consists of a single, flat table designed for fast CRUD operations and easy Pandas integration.Table Name: internship_postingsColumn NameData TypeDescriptionidINTEGER PRIMARY KEYAuto-incrementing unique identifiercompany_nameTEXT NOT NULLName of the hiring companyrole_titleTEXT NOT NULLSpecific title of the internshipposting_urlTEXTLink to the original job postingrequired_skillsTEXTAI-extracted, comma-separated list of required skillspreferred_skillsTEXTComma-separated list of bonus skillsdegree_reqsTEXTAcademic requirements (e.g., BS Computer Science)date_loggedDATEDefaults to CURRENT_DATE when a row is created🚀 How to Run the App1. Clone the repository and navigate to the folder:Bashgit clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
2. Install the required Python libraries:Bashpip install streamlit pandas requests groq python-dotenv
3. Set up your Environment Variables:This project uses Groq (Llama 3.1) for AI keyword extraction.Create a file named .env in the root folder.Add your API key to the file like this:GROQ_API_KEY=your_api_key_here4. Run the Application:You can interact with the app in two ways:The Web Dashboard (Recommended):Run the Streamlit interface for an interactive, Excel-like data editor and analytics dashboard.Bashpython -m streamlit run app.py
The Automated AI Pipeline:Run the scraper to automatically fetch live jobs from the Remotive API, process the HTML using Llama 3.1, and save the clean skills to the database.Bashpython ai_scraper.py
⚙️ CRUD OperationsThis project fully supports Create, Read, Update, and Delete operations through both a Command-Line Interface (CLI) and a Streamlit Web UI.Create (Add Postings): * Web UI: Scroll to the bottom of the Streamlit data table and type directly into the empty row to add a new posting.CLI: Run python add_posting.py to use the interactive terminal prompt, or run python ai_scraper.py to let the AI automatically generate and insert rows from live API data.Read (View & Search):Web UI: The main dashboard displays the entire SQLite database as a Pandas DataFrame. You can click column headers to sort, use the built-in search bar to filter for specific skills, or use the "Skill Analytics" section to see charts of top skills.CLI: Run python search_postings.py to search the database by company name or specific required skills using SQL LIKE queries.Update (Modify Postings):Web UI: The app features an "Excel Mode." Simply double-click any cell in the Streamlit table, type your changes, and click "Save All Changes to Database" to execute a safe Pandas-to-SQL overwrite.CLI: Run python manage_postings.py, provide the specific id of the row, and enter the new values for the skills columns.Delete (Remove Postings):Web UI: Select the checkbox on the far left of any row(s) in the Streamlit table and press your Delete or Backspace key, then hit save.CLI: Run python manage_postings.py, select the delete option, enter the target id, and confirm the deletion to remove the record permanently.
