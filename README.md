# COMP 3004 - PostgreSQL & Python CRUD Application

## Video Demonstration
- **Demo Video Link:** [https://youtu.be/6oIm84MA8Q4]

## Project Structure
- `db/schema.sql` — SQL script to create the `students` table and insert initial records.
- `app/main.py` — Python app that shows CRUD operations via CLI and `psycopg2`.
- `requirements.txt` — Python dependencies.

## Prerequisites
- PostgreSQL (14+)
- Python (3.9+)

## Database Setup
1. Open `psql` or pgAdmin and create a database:

   ```sql
   CREATE DATABASE comp3004_a3;
## Running Instructions
1. First run db/schema.sql against comp3004_a3 to create the students and fill the table with data

    ```Bash
    psql -U postgres -d comp3004_a3 -f db/schema.sql
2. Then install the required Python dependencies:
    ```Bash
    pip install -r requirements.txt

3. IMPORTANT:
    Make sure to setup your environmental variable for the password of your database correctly:
    (Assuming Windows):
    ```Powershell
    $env:DB_PASSWORD="password"
4. Lastly run it:
    ```Bash
    python app/main.py

