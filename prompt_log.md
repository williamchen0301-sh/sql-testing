
# 📝 AI Development Prompt Log

### 🛠️ AI Models & Tools Used

* **Assistant/Co-pilot:** Gemini (Used for architectural planning, debugging, and generating the Python/SQL code).
* **Application AI Engine:** Groq API running Meta's `llama-3.1-8b-instant` model (Used within the Python script to extract skills from raw HTML).
* **Core Tech Stack:** Python, SQLite3, Streamlit, Pandas, Requests.

---

### 🚀 Development Process & Key Prompts

#### Phase 1: Database Architecture & CLI MVP

The project started by defining a realistic, 3-hour Minimum Viable Product (MVP). Instead of overengineering a complex relational database, I opted for a flat SQLite table that would be fast to build and easy to query.

* **Prompt 1 (The Idea):** *"I am thinking of building a small app that uses a SQLite database to help with recording the hiring posts of companies on internships so that people can get a better understanding of what kind of abilities they are looking at... what are the pieces of information that we should track"*
* **Prompt 2 (Security):** *"now can you help me write a Python function that asks the user for info and inserts a new row into my table using sqlite3. Use parameterized queries to avoid SQL injection."*

#### Phase 2: Upgrading to a Visual UI (Streamlit)

After successfully building the CRUD operations in the terminal, it became obvious that a Command-Line Interface is too slow for actual data entry.

* **Prompt 3 (The Pivot):** *"I am thinking of maybe making an interface for this program, the current works well in python but is too tedious for usage"*
* **Prompt 4 (UX Improvement):** *"is there a better way for the users to update and delete the data without entering the specific id number, we would like to be able to update a specific data while viewing it by just clicking on it rather than having to find out its specific id and changing it, couldn't it be as simple as editing a excel spreadsheet"*
* *Result:* Transitioned to Streamlit's `st.data_editor` for an interactive, Pandas-backed "Excel Mode" grid.



#### Phase 3: Data Analytics & Automation Limitations

Once the UI was working, I realized manual entry wouldn't scale for companies with hundreds of open roles, and flat comma-separated strings were hard to count.

* **Prompt 5 (Analytics Concept):** *"when i think about this, it doesn't really make sense that for a company there's only 1 required skill right? it should have multiple... asking how many times the skill python appears on google in the database"*
* *Result:* Leveraged Pandas `.explode()` to virtually unpack the strings for analytics without changing the database schema.


* **Prompt 6 (Scaling via Scraping):** *"when actually doing the research, it appears that on the web page of many companies, there are hundreds and even thousands of results, which makes it unreasonable for human recording of data into the current database, is there any possible way to solve this problem?"*
* *Result:* Attempted to scrape ByteDance but hit a 405 bot-protection error. Pivoted to the developer-friendly **Remotive Open API**.



#### Phase 4: AI Pipeline Integration & Debugging

The API returned massive, messy HTML blocks. Instead of writing fragile regex or BeautifulSoup scrapers, I decided to use an LLM as a data-cleaning pipeline.

* **Prompt 7 (The AI Solution):** *"maybe we can let AI extract the key words, then we can get over the hardest part of the job? there are just too many tech_skills possible on the webpage so defining the skills one is looking for is ok but doesn't work that well when unfamiliar words appear"*
* **Prompt 8 (Connecting the Pipeline):** *"can you give the code showing how this connects with the scraping, i am a little bit confused in how the program works"*

---

### ⚠️ Known Flaws & Technical Trade-offs

During the final testing of the AI extraction pipeline, the application crashed with a **413 Rate Limit Exceeded** error from the Groq API.

**The Problem:** Job descriptions downloaded via API contain heavy HTML/CSS boilerplate. Some postings were exceeding 24,000 tokens, completely blowing past the free-tier limit of 6,000 tokens per minute.

**The Workaround/Flaw:** To fix this, I implemented a strict character cutoff in `ai_scraper.py`:

```python
short_text = messy_text[:3000] 

```

* *Why this is a flaw:* The scraper currently truncates the job description after the first 3,000 characters to keep the payload lightweight. If a company lists their technical requirements at the very bottom of a massive job posting, the AI will not see them, and it will return "None".
* *Future Fix:* A better long-term solution would be to run the text through a lightweight HTML stripper (like BeautifulSoup's `get_text()`) to remove all the code tags *before* sending it to the AI, rather than just blindly chopping the string.
