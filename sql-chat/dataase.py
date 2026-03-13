import sqlite3
import pandas as pd

def create_sample_database():
    """Creates a sample student database for testing"""
    
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    # ── Create Students table ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        grade TEXT,
        marks INTEGER,
        subject TEXT,
        city TEXT
    )
    """)

    # ── Create Teachers table ──
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        subject TEXT,
        experience INTEGER,
        salary INTEGER,
        city TEXT
    )
    """)

    # ── Sample Students data ──
    students = [
        (1, "Rahul Sharma", 15, "A", 92, "Math", "Mumbai"),
        (2, "Priya Patel", 16, "B", 78, "Science", "Delhi"),
        (3, "Amit Kumar", 15, "A", 95, "Math", "Bangalore"),
        (4, "Sneha Singh", 17, "C", 65, "English", "Mumbai"),
        (5, "Raj Verma", 16, "B", 82, "Science", "Pune"),
        (6, "Anita Desai", 15, "A", 88, "Math", "Delhi"),
        (7, "Vikram Nair", 17, "B", 75, "English", "Chennai"),
        (8, "Pooja Mehta", 16, "A", 91, "Science", "Mumbai"),
        (9, "Suresh Rao", 15, "C", 60, "Math", "Hyderabad"),
        (10, "Deepa Joshi", 17, "A", 94, "Science", "Pune"),
        (11, "Arjun Gupta", 16, "B", 80, "Math", "Delhi"),
        (12, "Kavya Reddy", 15, "A", 89, "English", "Bangalore"),
        (13, "Rohan Das", 17, "C", 58, "Science", "Mumbai"),
        (14, "Meera Pillai", 16, "B", 77, "Math", "Chennai"),
        (15, "Karan Malhotra", 15, "A", 96, "Science", "Delhi"),
    ]

    # ── Sample Teachers data ──
    teachers = [
        (1, "Mr. Sharma", "Math", 10, 55000, "Mumbai"),
        (2, "Mrs. Patel", "Science", 8, 48000, "Delhi"),
        (3, "Mr. Kumar", "English", 15, 62000, "Bangalore"),
        (4, "Mrs. Singh", "Math", 5, 42000, "Pune"),
        (5, "Mr. Verma", "Science", 12, 58000, "Mumbai"),
        (6, "Mrs. Desai", "English", 7, 45000, "Chennai"),
        (7, "Mr. Nair", "Math", 20, 75000, "Delhi"),
        (8, "Mrs. Mehta", "Science", 3, 38000, "Hyderabad"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO students VALUES (?,?,?,?,?,?,?)",
        students
    )
    cursor.executemany(
        "INSERT OR IGNORE INTO teachers VALUES (?,?,?,?,?,?)",
        teachers
    )

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_sample_database()