import os
import psycopg2
from psycopg2 import Error

def get_connection():
    # Establishing and returning a connection to the PostgreSQL database
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME", "comp3004_a3"),
        user = os.getenv("DB_USER", "postgres"),
        password = os.getenv("DB_PASSWORD", "postgres"),
        host = os.getenv("DB_HOST", "localhost"),
        port = os.getenv("DB_PORT", "5432"), #Port 5432 is the official default port that PostgreSQL listens on for incoming database connections.
    )

def getAllStudents():
    # Retrieving and displaying all records from table
    # the three """ let's write multi-line strings which is easier for SQL queries
    query = """ 
        SELECT student_id, first_name, last_name, email, enrollment_date
        FROM students
        ORDER BY student_id ASC;
    """

    try: 
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

                print("\n-- Current Students --")
                if not rows:
                    print("No student records found")
                else:
                    print(f"{'ID':<4} | {'First Name':<12} | {'Last_name':<12} | {'Email':<26} | {'Enrollment Date'}")
                    print("-" * 76)
                    for row in rows:
                        student_id, first_name, last_name, email, enrollment_date = row
                        print(f"{student_id:<4} | {first_name:<12} | {last_name:<12} | {email:<26} | {enrollment_date}")
                print()
                return rows
    except Error as e:
        print(f"Db error: could not retrieve students: {e}")
        return []

def addStudent(first_name, last_name, email, enrollment_date):
    #Inserting a new student record
    query = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """
    #Basically %s is a query placeholder which is used by psycopg2 for parametrized sql statements. 
    #passing a tuple to cur.execute(query, (val1, val2, val3,val4)), psycopg2 will safely substitute the values put into those spots respectively. 
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (first_name, last_name, email, enrollment_date))
                new_id = cur.fetchone()[0]
                conn.commit()
                print(f"Success: Added student '{first_name} {last_name}' with student_id = {new_id} ")
                return new_id
    except Error as e:
        print(f"Db Error: Could not add student: {e}")
        return None

def updateStudentEmail(student_id, new_email):
    #Updates student email address with specified student_id
    query = """
        UPDATE students
        SET email = %s
        WHERE student_id = %s;
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (new_email, student_id))
                conn.commit()
                if cur.rowcount == 0:
                    print(f"Warning: no student found with student_id = {student_id}")
                    return False
                print(f"Success: updated email for student_id = {student_id} to '{new_email}'")
                return True
    except Error as e:
        print(f"Db Error: could not update student email: {e}")
        return False

def deleteStudent(student_id):
    #Deleting the record of student with specified student_id
    query = """
        DELETE FROM students
        WHERE student_id = %s;
    """
    try: 
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (student_id,)) #trailing comma so python constructs a ONE ELEMENT TUPLES
                conn.commit()
                if cur.rowcount == 0:
                    print(f"Warning: no student found with student_id = {student_id}")
                    return False
                print(f"Success: deleted student with student_id = {student_id}")
                return True
    except Error as e:
        print(f"db error: could not delete student: {e}")
        return False

def main():
    #an interactive command line interface to demonstrace each Copy, Read,Update, Delete operation

    while True:
        print("Student db menu")
        print("1. getAllStudents() - View all students")
        print("2. addStudent() - add a student")
        print("3. updateStudentemail() - update a student's email")
        print("4. deleteStudent() - delete a student")
        print("0. Exit")

        choice = input("Select an option (0-4): ").strip()
        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == "3":
            try:
                student_id = int(input("Student ID to update: ").strip())
                new_email = input("New email: ").strip()
                updateStudentEmail(student_id, new_email)
            except ValueError:
                print("Input error: student_id must be an integer")
        elif choice == "4":
            try:  
                student_id = int(input("Student ID to delete: ").strip())
                deleteStudent(student_id)
            except ValueError:
                print("Input error: student_id must be an integer")
        elif choice == "0":
            print("Exiting application")
            break
        else:
            print("Input error: Please choose a valid option (0-4).\n")
if __name__ == "__main__":
    main()