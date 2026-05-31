import csv
import os
import subprocess
import sys


_REQUIRED_PACKAGES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib.pyplot": "matplotlib",
}

_missing = []
for _mod, _pkg in _REQUIRED_PACKAGES.items():
    try:
        __import__(_mod)
    except ModuleNotFoundError:
        _missing.append(_pkg)

if _missing:
    print(f"Required packages missing: {', '.join(_missing)}")
    print("Attempting to install missing packages into the current Python interpreter...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", *_missing])
    except Exception as _err:
        print(f"Automatic installation failed: {_err}")
        print("Please install manually using:")
        print(f"  {sys.executable} -m pip install {' '.join(_missing)}")
        raise SystemExit(1)

# Safe imports after ensuring packages are present.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# GLOBAL DATA STORES (in-memory for the session)
# ---------------------------------------------------------------------

registered_students = []  # Module 1 - student records
course_enrollments = {}  # Module 2 - {student_name: [(course, credits)]}
student_records_db = []  # Module 3 - list of dicts
student_ids = []  # Module 4 - for sort/search
event_participants = {}  # Module 3 - sets per event


# ---------------------------------------------------------------------
# USER-DEFINED EXCEPTION (Module 7)
# ---------------------------------------------------------------------

class MissingFileOrFolderError(Exception):
    """Raised when a required file or folder is missing in the directory."""

    pass


# =============================================================
# MODULE 1 - Student Registration and Grade Evaluation
# =============================================================

def evaluate_grade(score):
    """Return (grade, remark) for a numeric score."""
    if 90 <= score <= 100:
        return "A", "Excellent"
    if score >= 75:
        return "B", "Very Good"
    if score >= 60:
        return "C", "Good"
    if score >= 40:
        return "D", "Average"
    return "F", "Needs Improvement"


def module1_register_student():
    """Collect student name + exam score, evaluate grade, store record."""
    print("\n--- Module 1 : Student Registration & Grade Evaluation ---")
    name = input("  Enter student name  : ").strip()
    if not name:
        print("  [!] Name cannot be empty.")
        return

    try:
        score = float(input("  Enter exam score (0-100) : "))
    except ValueError:
        print("  [!] Invalid score. Please enter a number.")
        return

    if not (0 <= score <= 100):
        print("  [!] Score must be between 0 and 100.")
        return

    grade, remark = evaluate_grade(score)
    student = {"name": name, "score": score, "grade": grade, "remark": remark}
    registered_students.append(student)

    # Also seed into student_ids (Module 4) using a simple auto-ID.
    new_id = 100 + len(registered_students)
    student["id"] = new_id
    student_ids.append(new_id)

    print("\n  -- Student Report ------------------")
    print(f"  Name    : {name}")
    print(f"  Score   : {score}")
    print(f"  Grade   : {grade}")
    print(f"  Remark  : {remark}")
    print(f"  Student ID assigned : {new_id}")


def module1_view_all():
    """Print all registered students."""
    print("\n  -- Registered Students ---------------------------------")
    if not registered_students:
        print("  (no students registered yet)")
        return

    for student in registered_students:
        print(
            f"  ID:{student.get('id', '?')}  {student['name']:<20}  "
            f"Score:{student['score']:6.1f}  Grade:{student['grade']}  "
            f"({student['remark']})"
        )


# =============================================================
# MODULE 2 - Course Enrollment Management
# =============================================================

def module2_enroll_courses():
    """Enroll courses for an existing student with loop + continue/break logic."""
    print("\n--- Module 2 : Course Enrollment Management ---")
    module1_view_all()
    if not registered_students:
        return

    name = input("  Enter student name to enroll courses : ").strip()
    if not any(s["name"].lower() == name.lower() for s in registered_students):
        print(f"  [!] Student '{name}' not found. Register them first.")
        return

    max_courses = 5
    courses = course_enrollments.get(name, [])

    print(f"\n  Enrolling courses for {name}  (max {max_courses})")
    while True:
        if len(courses) >= max_courses:
            print("  [!] Maximum course limit (5) reached!")
            break

        course_name = input("  Enter course name (or 'done' to finish) : ").strip()
        if course_name.lower() == "done":
            break
        if not course_name:
            print("  [!] Course name cannot be empty. Skipping...")
            continue

        credits_raw = input("  Enter credit value : ").strip()
        if not credits_raw.isdigit():
            print("  [!] Invalid credit value! Skipping entry...")
            continue

        credits = int(credits_raw)
        if credits <= 0:
            print("  [!] Credit must be positive! Skipping entry...")
            continue

        courses.append((course_name, credits))
        print(f"  Course '{course_name}' with {credits} credits added.\n")

    course_enrollments[name] = courses

    print("\n  -- Enrollment Report ----------------------------------")
    for course, credit in courses:
        print(f"  Course: {course:<30}  Credits: {credit}")
    print(f"  Total courses enrolled : {len(courses)}")


# =============================================================
# MODULE 3 - Student Record Data Management (Lists, Dicts, Sets)
# =============================================================

def module3_manage_records():
    """Add student records to DB and perform set-based event analysis."""
    print("\n--- Module 3 : Student Record Data Management ---")

    add = input("  Add a new student record? (y/n) : ").strip().lower()
    if add == "y":
        name = input("  Name  : ").strip()
        try:
            age = int(input("  Age   : "))
            grades_raw = input("  Enter grades separated by spaces : ")
            grades = [float(g) for g in grades_raw.split()]
        except ValueError:
            print("  [!] Invalid input. Skipping record.")
        else:
            student_records_db.append({"name": name, "age": age, "grades": grades})
            print(f"  Record added for {name}.")

    print("\n  -- Student Records ------------------------------------")
    if not student_records_db:
        print("  (no records yet)")
    else:
        for student in student_records_db:
            avg = sum(student["grades"]) / len(student["grades"]) if student["grades"] else 0
            print(
                f"  Name: {student['name']:<20}  Age: {student['age']}  "
                f"Grades: {student['grades']}  Avg: {avg:.1f}"
            )

    print("\n  -- Event Participation Analysis (Sets) ----------------")
    event_a = {"Priya", "Rahul", "Anita", "Kiran"}
    event_b = {"Rahul", "Anita", "Sneha"}

    event_participants["Event A"] = event_a
    event_participants["Event B"] = event_b

    print(f"  Event A participants : {event_a}")
    print(f"  Event B participants : {event_b}")
    print(f"  Common (A and B)     : {event_a & event_b}")
    print(f"  All (A or B)         : {event_a | event_b}")
    print(f"  Only A (A - B)       : {event_a - event_b}")


# =============================================================
# MODULE 4 - Sorting and Searching Student IDs
# =============================================================

def _bubble_sort(lst):
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def _selection_sort(lst):
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def _linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def _binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def module4_sort_search():
    """Sort student IDs with Bubble / Selection Sort; search with Linear / Binary."""
    print("\n--- Module 4 : Sorting & Searching Student IDs ---")

    if not student_ids:
        print("  [!] No student IDs available. Register students first (Module 1).")
        return

    print(f"  Original IDs          : {student_ids}")
    bubble = _bubble_sort(student_ids)
    select = _selection_sort(student_ids)
    print(f"  Sorted (Bubble Sort) : {bubble}")
    print(f"  Sorted (Selection)   : {select}")

    try:
        target = int(input("  Enter Student ID to search : "))
    except ValueError:
        print("  [!] Invalid ID.")
        return

    li = _linear_search(bubble, target)
    bi = _binary_search(bubble, target)

    if li != -1:
        print(f"  Linear Search : ID {target} found at index {li}")
    else:
        print(f"  Linear Search : ID {target} not found.")

    if bi != -1:
        print(f"  Binary Search : ID {target} found at index {bi}")
    else:
        print(f"  Binary Search : ID {target} not found.")


# =============================================================
# MODULE 5 - Student Fee Calculation using Functions
# =============================================================

def calculate_fee(
    tuition_fee: float,
    hostel_fee: float = 0.0,
    transportation_fee: float = 0.0,
) -> float:
    """Return total fee from components."""
    return float(tuition_fee) + float(hostel_fee) + float(transportation_fee)


def module5_fee_calculator():
    """Interactive fee calculator using keyword / default arguments."""
    print("\n--- Module 5 : Student Fee Calculation ---")

    def get_amount(prompt):
        try:
            val = float(input(f"  {prompt} (press Enter to skip / default 0) : ").strip() or 0)
            return max(val, 0.0)
        except ValueError:
            print("  [!] Invalid input. Using 0.")
            return 0.0

    tuition = get_amount("Tuition Fee   (Rs.)")
    hostel = get_amount("Hostel Fee     (Rs.)")
    transport = get_amount("Transport Fee  (Rs.)")

    total = calculate_fee(
        tuition,
        hostel_fee=hostel,
        transportation_fee=transport,
    )

    print("\n  -- Fee Breakdown --------------------------------------")
    print(f"  Tuition Fee      : Rs. {tuition:,.2f}")
    print(f"  Hostel Fee       : Rs. {hostel:,.2f}")
    print(f"  Transportation   : Rs. {transport:,.2f}")
    print("  -------------------------------------------------------")
    print(f"  Total Fee        : Rs. {total:,.2f}")


# =============================================================
# MODULE 6 - File Handling for Student Academic Records
# =============================================================

FILE_PATH = "student_records.txt"


def module6_file_handling():
    """Write student records to file, read back, generate a simple report."""
    print("\n--- Module 6 : File Handling - Academic Records ---")

    # Use currently registered students; fall back to demo data.
    if registered_students:
        records_to_write = registered_students
    else:
        records_to_write = [
            {"id": 101, "name": "Arjun", "score": 85},
            {"id": 102, "name": "Meera", "score": 92},
            {"id": 103, "name": "Ravi", "score": 76},
            {"id": 104, "name": "Anita", "score": 89},
        ]

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write("ID,Name,Marks\n")
        for student in records_to_write:
            file.write(f"{student.get('id', '?')},{student['name']},{int(student['score'])}\n")
    print(f"  Records written to '{FILE_PATH}'")

    print("\n  -- Stored Records -------------------------------------")
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        print(f"  {line.strip()}")

    total = 0
    total_marks = 0
    highest = -1
    top_student = ""

    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) < 3:
            continue

        marks = int(parts[2])
        total += 1
        total_marks += marks
        if marks > highest:
            highest = marks
            top_student = parts[1]

    if total:
        avg = total_marks / total
        print(f"\n  Total Students : {total}")
        print(f"  Average Marks  : {avg:.2f}")
        print(f"  Top Student    : {top_student} ({highest} marks)")


# =============================================================
# MODULE 7 - Directory Scanning with Exception Handling
# =============================================================

def scan_directory(path):
    """Walk a directory, print structure, handle errors + user-defined exception."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Invalid directory path: '{path}'")

        print(f"\n  Scanning: {path}\n")
        for root, dirs, files in os.walk(path):
            level = root.replace(path, "").count(os.sep)
            indent = "    " * level
            print(f"  {indent}{os.path.basename(root)}/")

            sub = "    " * (level + 1)
            for fname in files:
                print(f"  {sub}{fname}")

            if not files and not dirs:
                raise MissingFileOrFolderError(f"Empty folder detected: {root}")

    except FileNotFoundError as exc:
        print(f"  [Error] {exc}")
    except MissingFileOrFolderError as exc:
        print(f"  [Custom Error] {exc}")
    except Exception as exc:
        print(f"  [Unexpected Error] {exc}")


def module7_directory_scan():
    print("\n--- Module 7 : Directory Scanning with Exception Handling ---")
    path = input("  Enter directory path to scan (press Enter to scan current dir) : ").strip()
    if not path:
        path = "."
    scan_directory(path)


# =============================================================
# MODULE 8 - Performance Analytics (NumPy, Pandas, Matplotlib)
# =============================================================

PERF_CSV = "student_performance.csv"


def _generate_demo_csv():
    """Create a demo CSV if none exists."""
    rows = [
        ["Name", "Math", "Science", "English"],
        ["Priya", 88, 92, 85],
        ["Rahul", 75, 80, 70],
        ["Anita", 95, 89, 93],
        ["Kiran", 60, 72, 68],
        ["Sneha", 82, 78, 88],
    ]

    with open(PERF_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"  Demo CSV '{PERF_CSV}' created.")


def module8_performance_analytics():
    """Load CSV, compute stats with NumPy/Pandas, plot with Matplotlib."""
    print("\n--- Module 8 : Student Performance Analytics ---")

    if not os.path.exists(PERF_CSV):
        print(f"  '{PERF_CSV}' not found. Generating demo data...")
        _generate_demo_csv()

    try:
        df = pd.read_csv(PERF_CSV)

        print("\n  -- Raw Data --------------------------------------------")
        print(df.to_string(index=False))

        print("\n  -- Statistical Summary (Pandas) ------------------------")
        print(df.describe().to_string())

        scores = df[["Math", "Science", "English"]].to_numpy()
        mean_s = np.mean(scores, axis=0)
        median_s = np.median(scores, axis=0)
        std_s = np.std(scores, axis=0)

        print("\n  -- NumPy Analysis --------------------------------------")
        subjects = ["Math", "Science", "English"]
        for i, subject in enumerate(subjects):
            print(
                f"  {subject:<10}  Mean:{mean_s[i]:6.2f}  "
                f"Median:{median_s[i]:6.2f}  StdDev:{std_s[i]:5.2f}"
            )

        print("\n  -- Top Performers --------------------------------------")
        for subject in subjects:
            top = df.loc[df[subject].idxmax(), "Name"]
            print(f"  {subject:<10} : {top}")

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(
            "Smart Campus - Student Performance Analytics",
            fontsize=14,
            fontweight="bold",
        )

        axes[0].bar(subjects, mean_s, color=["steelblue", "seagreen", "darkorange"])
        axes[0].set_title("Average Scores per Subject")
        axes[0].set_xlabel("Subject")
        axes[0].set_ylabel("Average Score")
        axes[0].set_ylim(0, 100)
        for i, value in enumerate(mean_s):
            axes[0].text(i, value + 1, f"{value:.1f}", ha="center", fontsize=9)

        x = range(len(df))
        width = 0.25
        colors = ["steelblue", "seagreen", "darkorange"]
        for i, subject in enumerate(subjects):
            offset = [xi + i * width for xi in x]
            axes[1].bar(offset, df[subject], width, label=subject, color=colors[i])

        axes[1].set_xticks([xi + width for xi in x])
        axes[1].set_xticklabels(df["Name"], rotation=15)
        axes[1].set_title("Student-wise Performance Comparison")
        axes[1].set_ylabel("Score")
        axes[1].set_ylim(0, 110)
        axes[1].legend()

        plt.tight_layout()
        chart_path = "performance_chart.png"
        plt.savefig(chart_path, dpi=120)
        plt.show()
        print(f"\n  Chart saved as '{chart_path}'")

    except FileNotFoundError:
        print("  [Error] CSV file not found.")
    except Exception as exc:
        print(f"  [Unexpected Error] {exc}")


# =============================================================
# MAIN DASHBOARD
# =============================================================

MENU = """
+============================================================+
|      SMART CAMPUS INFORMATION SYSTEM - DASHBOARD           |
+============================================================+
|  1. Student Registration & Grade Evaluation  (Lab 1)        |
|  2. Course Enrollment Management             (Lab 2)        |
|  3. Student Record Data Management           (Lab 3)        |
|  4. Sorting & Searching Student IDs          (Lab 4)        |
|  5. Student Fee Calculation                  (Lab 5)        |
|  6. File Handling - Academic Records         (Lab 6)        |
|  7. Directory Scanning & Exception Handling  (Lab 7)        |
|  8. Performance Analytics (NumPy/Pandas/MPL) (Lab 8)        |
|  9. View All Registered Students                            |
|  0. Exit                                                    |
+============================================================+
"""

DISPATCH = {
    "1": module1_register_student,
    "2": module2_enroll_courses,
    "3": module3_manage_records,
    "4": module4_sort_search,
    "5": module5_fee_calculator,
    "6": module6_file_handling,
    "7": module7_directory_scan,
    "8": module8_performance_analytics,
    "9": module1_view_all,
}


def main():
    print("\n" + "=" * 60)
    print("  Welcome to the Smart Campus Information System")
    print("  Dayananda Sagar College of Engineering")
    print("=" * 60)

    while True:
        print(MENU)
        choice = input("  Enter your choice : ").strip()

        if choice == "0":
            print("\n  Thank you for using Smart Campus Information System. Goodbye!\n")
            break
        if choice in DISPATCH:
            DISPATCH[choice]()
        else:
            print("  [!] Invalid choice. Please enter a number from 0 to 9.")

        input("\n  [Press Enter to return to the menu...]")


if __name__ == "__main__":
    main()
