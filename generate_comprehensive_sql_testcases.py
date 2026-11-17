import json
import sqlite3
import calendar

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_query(schema_sql, data_sql, query):
    conn = sqlite3.connect(":memory:")
    conn.create_function("YEAR", 1, lambda d: int(str(d).split("-")[0]) if d else None)
    conn.create_function("MONTH", 1, lambda d: int(str(d).split("-")[1]) if d else None)
    conn.create_function("MONTHNAME", 1, lambda d: calendar.month_name[int(str(d).split("-")[1])] if d else None)
    cur = conn.cursor()
    
    for stmt in (schema_sql + "\n" + data_sql).split(";"):
        s = stmt.strip()
        if s and not s.upper().startswith(("CREATE DATABASE", "USE ", "DROP TABLE")):
            cur.execute(s)
            
    cur.execute(query)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = [list(r) for r in cur.fetchall()]
    conn.close()
    return cols, rows

# ═══════════════════════════════════════════════════════════════════════════════
# GROUP 1: STUDENT DATABASE (Q9 - Q13)
# ═══════════════════════════════════════════════════════════════════════════════

STUDENT_SCHEMA = """CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender CHAR(1),
    city VARCHAR(50) DEFAULT 'Delhi',
    email VARCHAR(100) UNIQUE,
    marks INT,
    dob DATE
);"""

STUDENT_SOLUTIONS = {
    9: """SELECT student_id, name, city, age, gender, marks, dob
FROM student
WHERE marks BETWEEN 60 AND 95
  AND city IN ('Delhi', 'Meerut', 'Noida')
  AND city != 'Panipat'
  AND (name LIKE 'A%' OR name LIKE 'R%' OR name LIKE '%a' OR name LIKE '%it%')
  AND NOT (gender = 'F' AND city = 'Meerut')
ORDER BY marks DESC, name ASC;""",

    10: """SELECT student_id, name AS student_name, city, marks AS student_marks, age
FROM student
WHERE marks BETWEEN 75 AND 100
  AND city IN ('Delhi', 'Meerut', 'Noida', 'Panipat')
ORDER BY marks DESC, age ASC
LIMIT 3;""",

    11: """SELECT city, COUNT(*) AS total_students, SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks
FROM student
WHERE marks BETWEEN 50 AND 100
GROUP BY city
HAVING COUNT(*) >= 2 AND AVG(marks) > 75
ORDER BY average_marks DESC;""",

    12: """SELECT YEAR(dob) AS birth_year, MONTH(dob) AS birth_month_number,
       MONTHNAME(dob) AS birth_month_name, COUNT(*) AS total_students
FROM student
WHERE (dob BETWEEN '2003-01-01' AND '2005-12-31') OR MONTH(dob) = 10
GROUP BY birth_year, birth_month_number, birth_month_name
HAVING total_students >= 1
ORDER BY birth_year ASC, birth_month_number ASC;""",

    13: """SELECT gender, COUNT(*) AS total_students, SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks,
       ROUND(AVG(age), 2) AS average_age,
       COUNT(DISTINCT city) AS unique_cities,
       COUNT(DISTINCT age) AS unique_ages,
       COUNT(DISTINCT marks) AS unique_marks
FROM student
GROUP BY gender
ORDER BY average_marks DESC;"""
}

# 8 Datasets for Student DB
STUDENT_DATASETS = [
    ("Standard college student dataset (10 records)", """INSERT INTO student VALUES
(101, 'Aditya', 29, 'M', 'Meerut', 'aditya@gmail.com', 85, '1996-10-25'),
(102, 'Rahul', 21, 'M', 'Delhi', 'rahul@gmail.com', 72, '2005-03-12'),
(103, 'Priya', 22, 'F', 'Noida', 'priya@gmail.com', 91, '2004-07-18'),
(104, 'Amit', 20, 'M', 'Meerut', 'amit@gmail.com', 65, '2006-01-25'),
(105, 'Neha', 23, 'F', 'Delhi', 'neha@gmail.com', 78, '2003-11-09'),
(106, 'Riya', 21, 'F', 'Panipat', 'riya@gmail.com', 88, '2005-05-22'),
(107, 'Rohit', 24, 'M', 'Noida', 'rohit@gmail.com', 55, '2002-09-14'),
(108, 'Anjali', 22, 'F', 'Meerut', 'anjali@gmail.com', 95, '2004-12-03'),
(109, 'Karan', 25, 'M', 'Delhi', 'karan@gmail.com', 67, '2001-06-28'),
(110, 'Ankit', 20, 'M', 'Panipat', 'ankit@gmail.com', 81, '2006-02-17');""", True),

    ("High marks & tie-breaker scenario", """INSERT INTO student VALUES
(201, 'Aakash', 22, 'M', 'Delhi', 'aakash@gmail.com', 95, '2004-10-10'),
(202, 'Radha', 21, 'F', 'Delhi', 'radha@gmail.com', 95, '2005-04-15'),
(203, 'Rohan', 20, 'M', 'Meerut', 'rohan@gmail.com', 85, '2006-08-20'),
(204, 'Simran', 23, 'F', 'Noida', 'simran@gmail.com', 85, '2003-10-05'),
(205, 'Mohit', 25, 'M', 'Delhi', 'mohit@gmail.com', 76, '2001-10-30'),
(206, 'Deepak', 24, 'M', 'Panipat', 'deepak@gmail.com', 92, '2002-12-12'),
(207, 'Anita', 22, 'F', 'Noida', 'anita@gmail.com', 95, '2004-03-25');""", False),

    ("Boundary marks & threshold evaluation", """INSERT INTO student VALUES
(301, 'Ramesh', 20, 'M', 'Delhi', 'ramesh@gmail.com', 60, '2006-05-10'),
(302, 'Radha', 21, 'F', 'Noida', 'radha@gmail.com', 95, '2005-10-01'),
(303, 'Asha', 22, 'F', 'Meerut', 'asha@gmail.com', 92, '2004-09-18'),
(304, 'Kavita', 24, 'F', 'Panipat', 'kavita@gmail.com', 79, '2002-10-15'),
(305, 'Rohit', 23, 'M', 'Delhi', 'rohit305@gmail.com', 75, '2003-08-12');""", False),

    ("Female students Meerut exclusion testing", """INSERT INTO student VALUES
(401, 'Pooja', 22, 'F', 'Meerut', 'pooja@gmail.com', 92, '2004-06-12'),
(402, 'Shweta', 23, 'F', 'Meerut', 'shweta@gmail.com', 88, '2003-10-20'),
(403, 'Ankit', 21, 'M', 'Meerut', 'ankit403@gmail.com', 85, '2005-02-14'),
(404, 'Ritu', 20, 'F', 'Delhi', 'ritu@gmail.com', 90, '2006-07-07'),
(405, 'Arun', 22, 'M', 'Delhi', 'arun@gmail.com', 80, '2004-10-04');""", False),

    ("Panipat and Out-of-NCR exclusion testing", """INSERT INTO student VALUES
(501, 'Riya', 21, 'F', 'Panipat', 'riya501@gmail.com', 94, '2005-03-03'),
(502, 'Anil', 24, 'M', 'Panipat', 'anil@gmail.com', 90, '2002-11-11'),
(503, 'Aman', 22, 'M', 'Delhi', 'aman503@gmail.com', 88, '2004-05-19'),
(504, 'Rita', 23, 'F', 'Noida', 'rita@gmail.com', 82, '2003-10-18'),
(505, 'Gaurav', 25, 'M', 'Jaipur', 'gaurav@gmail.com', 95, '2001-08-25');""", False),

    ("Name pattern edge cases (A%, R%, %a, %it%)", """INSERT INTO student VALUES
(601, 'Anurag', 21, 'M', 'Delhi', 'anurag@gmail.com', 90, '2005-01-10'),
(602, 'Ravina', 22, 'F', 'Noida', 'ravina@gmail.com', 86, '2004-10-12'),
(603, 'Sumit', 23, 'M', 'Meerut', 'sumit@gmail.com', 80, '2003-04-15'),
(604, 'Tina', 20, 'F', 'Delhi', 'tina@gmail.com', 84, '2006-09-09'),
(605, 'Suresh', 24, 'M', 'Delhi', 'suresh@gmail.com', 85, '2002-12-01');""", False),

    ("October birthdates & date ranges", """INSERT INTO student VALUES
(701, 'Aditi', 22, 'F', 'Noida', 'aditi701@gmail.com', 92, '2004-10-15'),
(702, 'Rohan', 21, 'M', 'Delhi', 'rohan702@gmail.com', 78, '2005-10-22'),
(703, 'Aman', 25, 'M', 'Delhi', 'aman703@gmail.com', 74, '2001-10-05'),
(704, 'Neha', 23, 'F', 'Delhi', 'neha704@gmail.com', 88, '2003-04-11'),
(705, 'Ajay', 20, 'M', 'Meerut', 'ajay@gmail.com', 70, '2006-10-31');""", False),

    ("City-level threshold testing (<2 students vs >=2 students)", """INSERT INTO student VALUES
(801, 'Archana', 22, 'F', 'Delhi', 'archana@gmail.com', 90, '2004-03-15'),
(802, 'Rupesh', 23, 'M', 'Delhi', 'rupesh@gmail.com', 85, '2003-10-10'),
(803, 'Anand', 21, 'M', 'Meerut', 'anand@gmail.com', 60, '2005-08-20'),
(804, 'Rohit', 24, 'M', 'Noida', 'rohit804@gmail.com', 92, '2002-05-12'),
(805, 'Pooja', 20, 'F', 'Noida', 'pooja805@gmail.com', 88, '2006-10-01');""", False)
]

# ═══════════════════════════════════════════════════════════════════════════════
# GROUP 2: EMPLOYEE & DEPARTMENT DATABASE (Q14 - Q21)
# ═══════════════════════════════════════════════════════════════════════════════

from populate_prompt10_employee_questions import (
    SCHEMA_SQL as EMP_DEPT_SCHEMA,
    SOLUTIONS as EMP_DEPT_SOLUTIONS,
    DEFAULT_DATA_SQL as EMP_DEPT_DATA_1
)

EMP_DEPT_DATASETS = [
    ("Standard Company Dataset (15 Employees, 6 Departments)", EMP_DEPT_DATA_1, True),

    ("Dataset 2: Alternative Hiring Cohorts & Location Diversity", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(201, 'Aditya', 27, 'M', 1, 'Delhi', 74000, 89, '2021-04-12'),
(202, 'Alka', 25, 'F', 4, 'Noida', 69000, 93, '2022-03-15'),
(203, 'Amitabh', 30, 'M', 1, 'Gurgaon', 78000, 91, '2020-11-20'),
(204, 'Sonia', 29, 'F', 3, 'Delhi', 84000, 92, '2019-02-14'),
(205, 'Manish', 34, 'M', 2, 'Noida', 61000, 77, '2020-05-22'),
(206, 'Divya', 28, 'F', 5, 'Delhi', 66000, 84, '2021-09-01'),
(207, 'Anita', 26, 'F', 4, 'Delhi', 73000, 96, '2023-01-15'),
(208, 'Reena', 31, 'F', 3, 'Noida', 89000, 94, '2018-07-19'),
(209, 'Varun', 32, 'M', 5, 'Gurgaon', 58000, 73, '2020-03-11'),
(210, 'Geeta', 29, 'F', 1, 'Noida', 70000, 89, '2022-10-05');""", False),

    ("Dataset 3: Boundary Salaries & Distinct Department Sizes", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(301, 'Ananya', 25, 'F', 1, 'Delhi', 60000, 90, '2020-01-01'),
(302, 'Ashish', 32, 'M', 4, 'Noida', 80000, 88, '2021-03-15'),
(303, 'Savitri', 28, 'F', 3, 'Gurgaon', 85000, 95, '2019-06-20'),
(304, 'Rohit', 27, 'M', 2, 'Delhi', 59000, 78, '2022-08-10'),
(305, 'Kavita', 31, 'F', 5, 'Delhi', 62000, 83, '2020-12-25'),
(306, 'Priya', 26, 'F', 3, 'Delhi', 79000, 91, '2021-05-18'),
(307, 'Arun', 30, 'M', 1, 'Gurgaon', 68000, 89, '2020-09-09');""", False),

    ("Dataset 4: High Performance & Strict Department Filters", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(401, 'Amit', 28, 'M', 1, 'Delhi', 75000, 92, '2021-07-01'),
(402, 'Pooja', 29, 'F', 1, 'Noida', 76000, 94, '2022-02-15'),
(403, 'Ankit', 30, 'M', 1, 'Gurgaon', 77000, 91, '2020-06-10'),
(404, 'Ritu', 27, 'F', 3, 'Delhi', 86000, 95, '2019-11-20'),
(405, 'Kunal', 35, 'M', 3, 'Gurgaon', 88000, 93, '2018-04-12'),
(406, 'Sneha', 31, 'F', 3, 'Noida', 82000, 89, '2021-08-05'),
(407, 'Deepak', 36, 'M', 2, 'Delhi', 55000, 68, '2019-01-15');""", False),

    ("Dataset 5: Female Dominance & Gender Diversity Audit", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(501, 'Renu', 26, 'F', 3, 'Delhi', 81000, 92, '2021-03-10'),
(502, 'Meenakshi', 28, 'F', 3, 'Gurgaon', 83000, 91, '2020-05-15'),
(503, 'Tarun', 32, 'M', 3, 'Noida', 79000, 78, '2019-09-22'),
(504, 'Shalini', 27, 'F', 5, 'Delhi', 65000, 88, '2022-04-11'),
(505, 'Vandana', 29, 'F', 5, 'Gurgaon', 64000, 85, '2021-12-01'),
(506, 'Pramod', 33, 'M', 5, 'Noida', 62000, 66, '2020-07-19');""", False),

    ("Dataset 6: Multiple Unstaffed Departments (Testing LEFT & RIGHT JOIN)", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(601, 'Aman', 29, 'M', 1, 'Delhi', 72000, 89, '2021-06-15'),
(602, 'Priya', 27, 'F', 1, 'Noida', 74000, 92, '2020-08-20'),
(603, 'Karan', 34, 'M', 3, 'Gurgaon', 86000, 90, '2019-03-12'),
(604, 'Anjali', 26, 'F', 4, 'Delhi', 71000, 94, '2022-10-05');""", False),

    ("Dataset 7: Edge Joining Dates (2018 vs 2019-2023 Cohorts)", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(701, 'OldHire', 38, 'M', 1, 'Delhi', 90000, 95, '2018-05-10'),
(702, 'Hire2019A', 31, 'F', 2, 'Delhi', 60000, 80, '2019-04-12'),
(703, 'Hire2019B', 30, 'M', 3, 'Gurgaon', 75000, 82, '2019-09-18'),
(704, 'Hire2019C', 29, 'F', 4, 'Noida', 68000, 85, '2019-11-25'),
(705, 'Hire2023A', 24, 'M', 1, 'Gurgaon', 62000, 88, '2023-02-14'),
(706, 'Hire2023B', 25, 'F', 5, 'Delhi', 61000, 90, '2023-06-20'),
(707, 'Hire2023C', 26, 'M', 4, 'Delhi', 70000, 92, '2023-10-15');""", False),

    ("Dataset 8: Salary Range Boundaries & Exclusion Patterns", """INSERT INTO department VALUES
(1, 'IT', 'Delhi'), (2, 'HR', 'Noida'), (3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'), (5, 'Sales', 'Gurgaon'), (6, 'Research', 'Mumbai');

INSERT INTO employee VALUES
(801, 'Aakash', 25, 'M', 1, 'Delhi', 60000, 89, '2020-02-01'),
(802, 'Anuradha', 32, 'F', 4, 'Noida', 80000, 96, '2023-11-30'),
(803, 'Rohit', 28, 'M', 2, 'Delhi', 65000, 72, '2021-04-10'),
(804, 'Mohit', 30, 'M', 5, 'Gurgaon', 70000, 80, '2022-07-15'),
(805, 'Arun', 29, 'M', 3, 'Gurgaon', 75000, 90, '2021-09-09');""", False)
]

# ═══════════════════════════════════════════════════════════════════════════════
# GROUP 3: SELF JOIN & CROSS JOIN DATABASE (Q22 - Q29)
# ═══════════════════════════════════════════════════════════════════════════════

from add_self_cross_join_questions import (
    SCHEMA_SQL as SELF_CROSS_SCHEMA,
    SOLUTIONS as SELF_CROSS_SOLUTIONS,
    DEFAULT_DATA_SQL as SELF_CROSS_DATA_1
)

SELF_CROSS_DATASETS = [
    ("Standard Employee-Project Dataset (8 Employees, 4 Projects)", SELF_CROSS_DATA_1, True),

    ("Dataset 2: Alternative Hierarchy & Project Count", """INSERT INTO employee VALUES
(201, 'Vikram', NULL, 'IT', 95000, 'Delhi'),
(202, 'Sunita', 201, 'IT', 80000, 'Delhi'),
(203, 'Rahul', 201, 'HR', 65000, 'Noida'),
(204, 'Ananya', 202, 'IT', 85000, 'Delhi'),
(205, 'Deepak', 202, 'IT', 72000, 'Gurgaon'),
(206, 'Meera', 203, 'HR', 60000, 'Noida');

INSERT INTO project VALUES
(10, 'Cloud Gateway', 'Delhi'),
(20, 'Payment Hub', 'Noida'),
(30, 'Telehealth App', 'Gurgaon');""", False),

    ("Dataset 3: Boundary Hierarchy & Multiple Projects per City", """INSERT INTO employee VALUES
(301, 'Aditi', NULL, 'IT', 88000, 'Delhi'),
(302, 'Kunal', 301, 'IT', 88000, 'Noida'),
(303, 'Tanvi', 301, 'IT', 92000, 'Delhi'),
(304, 'Gaurav', 302, 'Finance', 60000, 'Gurgaon'),
(305, 'Ritu', 302, 'Finance', 58000, 'Gurgaon');

INSERT INTO project VALUES
(101, 'AI Platform', 'Delhi'),
(102, 'Analytics Suite', 'Delhi'),
(103, 'Logistics Engine', 'Noida');""", False),

    ("Dataset 4: Manager-Employee Salary Equal and Inverted", """INSERT INTO employee VALUES
(401, 'Aman', NULL, 'IT', 80000, 'Delhi'),
(402, 'Priya', 401, 'IT', 80000, 'Noida'),
(403, 'Rohit', 401, 'IT', 85000, 'Delhi'),
(404, 'Neha', 402, 'HR', 75000, 'Noida'),
(405, 'Karan', 402, 'HR', 82000, 'Delhi');

INSERT INTO project VALUES
(1, 'Project Alpha', 'Delhi'),
(2, 'Project Beta', 'Noida');""", False),

    ("Dataset 5: Department Pairing Variations (Large single dept)", """INSERT INTO employee VALUES
(501, 'E1', NULL, 'IT', 90000, 'Delhi'),
(502, 'E2', 501, 'IT', 80000, 'Delhi'),
(503, 'E3', 501, 'IT', 70000, 'Delhi'),
(504, 'E4', 501, 'IT', 60000, 'Delhi'),
(505, 'E5', 501, 'HR', 65000, 'Noida');

INSERT INTO project VALUES
(1, 'P1', 'Delhi'), (2, 'P2', 'Noida');""", False),

    ("Dataset 6: All Remote & Different Cities for Employees and Managers", """INSERT INTO employee VALUES
(601, 'Aman', NULL, 'IT', 92000, 'Delhi'),
(602, 'Priya', 601, 'IT', 72000, 'Mumbai'),
(603, 'Rohit', 601, 'Finance', 68000, 'Bangalore'),
(604, 'Neha', 602, 'HR', 61000, 'Pune');

INSERT INTO project VALUES
(1, 'Banking Core', 'Delhi'),
(2, 'Cloud Sync', 'Gurgaon');""", False),

    ("Dataset 7: Multiple IT Employees Matching Single Project Location", """INSERT INTO employee VALUES
(701, 'Aman', NULL, 'IT', 90000, 'Delhi'),
(702, 'Priya', 701, 'IT', 75000, 'Delhi'),
(703, 'Rohit', 701, 'IT', 70000, 'Delhi'),
(704, 'Simran', 701, 'HR', 65000, 'Noida');

INSERT INTO project VALUES
(1, 'Central Portal', 'Delhi'),
(2, 'Regional Portal', 'Delhi');""", False),

    ("Dataset 8: Comprehensive 8-Employee Hierarchy Verification", """INSERT INTO employee VALUES
(801, 'Boss', NULL, 'IT', 100000, 'Delhi'),
(802, 'Lead1', 801, 'IT', 85000, 'Noida'),
(803, 'Lead2', 801, 'Finance', 80000, 'Delhi'),
(804, 'Dev1', 802, 'IT', 75000, 'Noida'),
(805, 'Dev2', 802, 'IT', 70000, 'Delhi'),
(806, 'Fin1', 803, 'Finance', 65000, 'Gurgaon'),
(807, 'Fin2', 803, 'Finance', 60000, 'Delhi');

INSERT INTO project VALUES
(1, 'Govt System', 'Delhi'),
(2, 'Tax Engine', 'Noida'),
(3, 'FinApp', 'Gurgaon');""", False)
]

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATION ROUTINE
# ═══════════════════════════════════════════════════════════════════════════════

def update_all_sql_testcases():
    with open("data/questions.json", "r") as f:
        questions = json.load(f)

    updated_count = 0

    for q in questions:
        qid = q["id"]

        # ── Group 1: Student DB (Q9 - Q13) ──
        if 9 <= qid <= 13:
            sql = STUDENT_SOLUTIONS[qid]
            schema = STUDENT_SCHEMA
            datasets = STUDENT_DATASETS
        # ── Group 2: Employee-Dept DB (Q14 - Q21) ──
        elif 14 <= qid <= 21:
            sql = EMP_DEPT_SOLUTIONS[qid]
            schema = EMP_DEPT_SCHEMA
            datasets = EMP_DEPT_DATASETS
        # ── Group 3: Self-Cross Join DB (Q22 - Q29) ──
        elif 22 <= qid <= 29:
            sql = SELF_CROSS_SOLUTIONS[qid]
            schema = SELF_CROSS_SCHEMA
            datasets = SELF_CROSS_DATASETS
        else:
            continue

        test_cases = []
        for tc_id, (desc, data_sql, is_sample) in enumerate(datasets, 1):
            cols, rows = run_query(schema, data_sql, sql)
            test_cases.append({
                "id": tc_id,
                "description": desc,
                "isSample": is_sample,
                "testData": data_sql,
                "expectedColumns": cols,
                "expectedRows": rows,
                "orderSensitive": True
            })

        q["testCases"] = test_cases
        updated_count += 1
        print(f"Updated Q{qid} ({q['title'][:35]}...) -> {len(test_cases)} test cases.")

    with open("data/questions.json", "w") as f:
        json.dump(questions, f, indent=2)

    print(f"\n🎉 Successfully updated all {updated_count} SQL questions with 8 comprehensive test cases each!")


if __name__ == "__main__":
    update_all_sql_testcases()
