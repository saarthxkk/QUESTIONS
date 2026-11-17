import json
import sqlite3
import calendar

# Setup DB runner to generate ground truth test cases
def run_query(schema_sql, data_sql, query):
    conn = sqlite3.connect(":memory:")
    conn.create_function("YEAR", 1, lambda d: int(str(d).split("-")[0]) if d else None)
    conn.create_function("MONTH", 1, lambda d: int(str(d).split("-")[1]) if d else None)
    conn.create_function("MONTHNAME", 1, lambda d: calendar.month_name[int(str(d).split("-")[1])] if d else None)
    cur = conn.cursor()
    
    for stmt in (schema_sql + "\n" + data_sql).split(";"):
        s = stmt.strip()
        if s and not s.upper().startswith(("CREATE DATABASE", "USE ")):
            cur.execute(s)
            
    cur.execute(query)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = [list(r) for r in cur.fetchall()]
    conn.close()
    return cols, rows

SCHEMA_SQL = """CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender CHAR(1),
    city VARCHAR(50) DEFAULT 'Delhi',
    email VARCHAR(100) UNIQUE,
    marks INT,
    dob DATE
);"""

DEFAULT_DATA_SQL = """INSERT INTO student (student_id, name, age, gender, city, email, marks, dob) VALUES
(101, 'Aditya', 29, 'M', 'Meerut', 'aditya@gmail.com', 85, '1996-10-25'),
(102, 'Rahul', 21, 'M', 'Delhi', 'rahul@gmail.com', 72, '2005-03-12'),
(103, 'Priya', 22, 'F', 'Noida', 'priya@gmail.com', 91, '2004-07-18'),
(104, 'Amit', 20, 'M', 'Meerut', 'amit@gmail.com', 65, '2006-01-25'),
(105, 'Neha', 23, 'F', 'Delhi', 'neha@gmail.com', 78, '2003-11-09'),
(106, 'Riya', 21, 'F', 'Panipat', 'riya@gmail.com', 88, '2005-05-22'),
(107, 'Rohit', 24, 'M', 'Noida', 'rohit@gmail.com', 55, '2002-09-14'),
(108, 'Anjali', 22, 'F', 'Meerut', 'anjali@gmail.com', 95, '2004-12-03'),
(109, 'Karan', 25, 'M', 'Delhi', 'karan@gmail.com', 67, '2001-06-28'),
(110, 'Ankit', 20, 'M', 'Panipat', 'ankit@gmail.com', 81, '2006-02-17');"""

# Edge case dataset 1 (different cities, names, marks)
DATA_SET_2 = """INSERT INTO student (student_id, name, age, gender, city, email, marks, dob) VALUES
(201, 'Aakash', 22, 'M', 'Delhi', 'aakash@gmail.com', 94, '2004-10-10'),
(202, 'Ritika', 21, 'F', 'Noida', 'ritika@gmail.com', 82, '2005-04-15'),
(203, 'Rohan', 20, 'M', 'Meerut', 'rohan@gmail.com', 62, '2006-08-20'),
(204, 'Simran', 23, 'F', 'Meerut', 'simran@gmail.com', 89, '2003-01-05'),
(205, 'Mohit', 25, 'M', 'Delhi', 'mohit@gmail.com', 76, '2001-10-30'),
(206, 'Deepak', 24, 'M', 'Panipat', 'deepak@gmail.com', 90, '2002-12-12'),
(207, 'Anita', 22, 'F', 'Delhi', 'anita@gmail.com', 88, '2004-03-25');"""

# Edge case dataset 3 (boundaries)
DATA_SET_3 = """INSERT INTO student (student_id, name, age, gender, city, email, marks, dob) VALUES
(301, 'Ramesh', 20, 'M', 'Delhi', 'ramesh@gmail.com', 60, '2006-05-10'),
(302, 'Radha', 21, 'F', 'Noida', 'radha@gmail.com', 95, '2005-10-01'),
(303, 'Asha', 22, 'F', 'Meerut', 'asha@gmail.com', 92, '2004-09-18'),
(304, 'Kavita', 24, 'F', 'Panipat', 'kavita@gmail.com', 79, '2002-10-15');"""

# Solutions
SOL_Q1 = """SELECT student_id, name, city, age, gender, marks, dob
FROM student
WHERE marks BETWEEN 60 AND 95
  AND city IN ('Delhi', 'Meerut', 'Noida')
  AND city != 'Panipat'
  AND (name LIKE 'A%' OR name LIKE 'R%' OR name LIKE '%a' OR name LIKE '%it%')
  AND NOT (gender = 'F' AND city = 'Meerut')
ORDER BY marks DESC, name ASC;"""

SOL_Q2 = """SELECT student_id, name AS student_name, city, marks AS student_marks, age
FROM student
WHERE marks BETWEEN 75 AND 100
  AND city IN ('Delhi', 'Meerut', 'Noida', 'Panipat')
ORDER BY marks DESC, age ASC
LIMIT 3;"""

SOL_Q3 = """SELECT city, COUNT(*) AS total_students, SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks
FROM student
WHERE marks BETWEEN 50 AND 100
GROUP BY city
HAVING COUNT(*) >= 2 AND AVG(marks) > 75
ORDER BY average_marks DESC;"""

SOL_Q4 = """SELECT YEAR(dob) AS birth_year, MONTH(dob) AS birth_month_number,
       MONTHNAME(dob) AS birth_month_name, COUNT(*) AS total_students
FROM student
WHERE (dob BETWEEN '2003-01-01' AND '2005-12-31') OR MONTH(dob) = 10
GROUP BY birth_year, birth_month_number, birth_month_name
HAVING total_students >= 1
ORDER BY birth_year ASC, birth_month_number ASC;"""

SOL_Q5 = """SELECT gender, COUNT(*) AS total_students, SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks,
       ROUND(AVG(age), 2) AS average_age,
       COUNT(DISTINCT city) AS unique_cities,
       COUNT(DISTINCT age) AS unique_ages,
       COUNT(DISTINCT marks) AS unique_marks
FROM student
GROUP BY gender
ORDER BY average_marks DESC;"""

def build_test_cases(query):
    # TC 1: Default dataset (Sample)
    c1, r1 = run_query(SCHEMA_SQL, DEFAULT_DATA_SQL, query)
    # TC 2: Dataset 2
    c2, r2 = run_query(SCHEMA_SQL, DATA_SET_2, query)
    # TC 3: Dataset 3
    c3, r3 = run_query(SCHEMA_SQL, DATA_SET_3, query)

    return [
        {
            "id": 1,
            "description": "Standard college student dataset (10 records)",
            "isSample": True,
            "testData": DEFAULT_DATA_SQL,
            "expectedColumns": c1,
            "expectedRows": r1,
            "orderSensitive": True
        },
        {
            "id": 2,
            "description": "Diverse demographics & city distribution dataset",
            "isSample": False,
            "testData": DATA_SET_2,
            "expectedColumns": c2,
            "expectedRows": r2,
            "orderSensitive": True
        },
        {
            "id": 3,
            "description": "Boundary marks (60, 95) & edge cases dataset",
            "isSample": False,
            "testData": DATA_SET_3,
            "expectedColumns": c3,
            "expectedRows": r3,
            "orderSensitive": True
        }
    ]

SAMPLE_TABLE_VIEW = """+------------+--------+-----+--------+---------+--------------------+-------+------------+
| student_id | name   | age | gender | city    | email              | marks | dob        |
+------------+--------+-----+--------+---------+--------------------+-------+------------+
| 101        | Aditya | 29  | M      | Meerut  | aditya@gmail.com   | 85    | 1996-10-25 |
| 102        | Rahul  | 21  | M      | Delhi   | rahul@gmail.com    | 72    | 2005-03-12 |
| 103        | Priya  | 22  | F      | Noida   | priya@gmail.com    | 91    | 2004-07-18 |
| 104        | Amit   | 20  | M      | Meerut  | amit@gmail.com     | 65    | 2006-01-25 |
| 105        | Neha   | 23  | F      | Delhi   | neha@gmail.com     | 78    | 2003-11-09 |
| 106        | Riya   | 21  | F      | Panipat | riya@gmail.com     | 88    | 2005-05-22 |
| 107        | Rohit  | 24  | M      | Noida   | rohit@gmail.com    | 55    | 2002-09-14 |
| 108        | Anjali | 22  | F      | Meerut  | anjali@gmail.com   | 95    | 2004-12-03 |
| 109        | Karan  | 25  | M      | Delhi   | karan@gmail.com    | 67    | 2001-06-28 |
| 110        | Ankit  | 20  | M      | Panipat | ankit@gmail.com    | 81    | 2006-02-17 |
+------------+--------+-----+--------+---------+--------------------+-------+------------+"""

sql_questions = [
    {
        "id": 9,
        "title": "Student Performance Search Engine",
        "difficulty": "Easy",
        "points": 25,
        "category": "SQL",
        "type": "sql",
        "tags": ["SQL", "SELECT", "WHERE", "ORDER BY", "LIKE", "Filtering"],
        "description": """## Student Performance Search Engine

The college administration wants to develop a student search system to identify students who meet specific academic and demographic requirements.

Write an SQL query to retrieve the `student_id`, `name`, `city`, `age`, `gender`, `marks`, and `dob` of students who satisfy the following conditions:

1. Students must have marks **between 60 and 95** (inclusive).
2. Students must belong to **Delhi, Meerut, or Noida**.
3. Students must **not** belong to **Panipat**.
4. Their names must either **start with 'A' or 'R'**, **end with 'a'**, or **contain the substring 'it'**.
5. **Exclude female students from Meerut**.
6. Display the results in **descending order of marks**.
7. If two students have equal marks, sort them **alphabetically by name**.

### Table Schema: `student`
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Primary key |
| `name` | VARCHAR(50) | Student's name |
| `age` | INT | Age in years |
| `gender` | CHAR(1) | 'M' or 'F' |
| `city` | VARCHAR(50) | City of residence |
| `email` | VARCHAR(100) | Unique email address |
| `marks` | INT | Marks scored (0-100) |
| `dob` | DATE | Date of birth (YYYY-MM-DD) |

### Validation Highlights
- Students from Panipat must never appear.
- Female students from Meerut must never appear.
- Students with marks below 60 must never appear.
- All 7 columns must be present in the output.""",
        "sampleInput": SAMPLE_TABLE_VIEW,
        "sampleOutput": """student_id | name   | city   | age | gender | marks | dob       
-----------+--------+--------+-----+--------+-------+-----------
103        | Priya  | Noida  | 22  | F      | 91    | 2004-07-18
101        | Aditya | Meerut | 29  | M      | 85    | 1996-10-25
105        | Neha   | Delhi  | 23  | F      | 78    | 2003-11-09
102        | Rahul  | Delhi  | 21  | M      | 72    | 2005-03-12
104        | Amit   | Meerut | 20  | M      | 65    | 2006-01-25

(5 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT student_id, name, city, age, gender, marks, dob
FROM student
WHERE 
ORDER BY ;""",
        "testCases": build_test_cases(SOL_Q1)
    },
    {
        "id": 10,
        "title": "Top Performing Students Leaderboard",
        "difficulty": "Easy",
        "points": 25,
        "category": "SQL",
        "type": "sql",
        "tags": ["SQL", "ORDER BY", "LIMIT", "Aliases", "Filtering"],
        "description": """## Top Performing Students Leaderboard

A college is preparing a merit list based on students' academic performance.

Write an SQL query to generate a leaderboard containing the top-performing students.

Your query must:
1. Retrieve `student_id`, `name`, `city`, `marks`, and `age`.
2. Consider only students whose marks are between 70 and 100.
3. Consider students belonging to **Delhi, Meerut, Noida, or Panipat**.
4. Exclude students whose marks are below 75.
5. Sort students by **marks in descending order**.
6. If marks are equal, prioritize **younger students** (ascending order of age).
7. Display **only the top 3 students**.
8. Give the output columns meaningful aliases:
   - `name` as **`student_name`**
   - `marks` as **`student_marks`**

### Output Columns
`student_id`, `student_name`, `city`, `student_marks`, `age`""",
        "sampleInput": SAMPLE_TABLE_VIEW,
        "sampleOutput": """student_id | student_name | city    | student_marks | age
-----------+--------------+---------+---------------+----
108        | Anjali       | Meerut  | 95            | 22 
103        | Priya        | Noida   | 91            | 22 
106        | Riya         | Panipat | 88            | 21 

(3 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT student_id, name AS student_name, city, marks AS student_marks, age
FROM student
WHERE 
ORDER BY 
LIMIT 3;""",
        "testCases": build_test_cases(SOL_Q2)
    },
    {
        "id": 11,
        "title": "City-Wise Academic Performance Report",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "type": "sql",
        "tags": ["SQL", "GROUP BY", "HAVING", "Aggregate Functions", "ROUND"],
        "description": """## City-Wise Academic Performance Report

The college management wants to compare academic performance across different cities.

Write an SQL query that displays:
1. The name of each `city`.
2. Total students belonging to that city (alias: **`total_students`**).
3. Total marks obtained by students in that city (alias: **`total_marks`**).
4. Average marks of students rounded to 2 decimal places (alias: **`average_marks`**).
5. Highest marks obtained in that city (alias: **`highest_marks`**).
6. Lowest marks obtained in that city (alias: **`lowest_marks`**).

### Apply the following conditions:
- Consider only students whose marks are between 50 and 100.
- Include **only cities having at least 2 students**.
- Display **only cities where the average marks are strictly greater than 75**.
- Sort cities by **`average_marks` in descending order**.

### Output Columns
`city`, `total_students`, `total_marks`, `average_marks`, `highest_marks`, `lowest_marks`""",
        "sampleInput": SAMPLE_TABLE_VIEW,
        "sampleOutput": """city    | total_students | total_marks | average_marks | highest_marks | lowest_marks
--------+----------------+-------------+---------------+---------------+-------------
Panipat | 2              | 169         | 84.5          | 88            | 81          
Meerut  | 3              | 245         | 81.67         | 95            | 65          

(2 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT city,
       COUNT(*) AS total_students,
       SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks,
       MIN(marks) AS lowest_marks
FROM student
WHERE 
GROUP BY city
HAVING 
ORDER BY ;""",
        "testCases": build_test_cases(SOL_Q3)
    },
    {
        "id": 12,
        "title": "Student Birthdate Analytics System",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "type": "sql",
        "tags": ["SQL", "Date Functions", "YEAR", "MONTH", "MONTHNAME", "GROUP BY"],
        "description": """## Student Birthdate Analytics System

The college administration wants to analyze student birth records to organize birthday events and generate demographic reports.

Write an SQL query to generate a birthdate report.

Your query must:
1. Retrieve the birth year using the `YEAR()` function (alias: **`birth_year`**).
2. Retrieve the birth month number using `MONTH()` (alias: **`birth_month_number`**).
3. Retrieve the birth month name using `MONTHNAME()` (alias: **`birth_month_name`**).
4. Count the number of students born in each year and month combination (alias: **`total_students`**).
5. Consider students whose DOB falls **between '2003-01-01' and '2005-12-31'**, along with students **born in October** regardless of their birth year.
6. Group the results by birth year and birth month.
7. Display only groups containing at least one student.
8. Sort the output by **`birth_year` in ascending order**, then **`birth_month_number` in ascending order**.

### Output Columns
`birth_year`, `birth_month_number`, `birth_month_name`, `total_students`""",
        "sampleInput": SAMPLE_TABLE_VIEW,
        "sampleOutput": """birth_year | birth_month_number | birth_month_name | total_students
-----------+--------------------+------------------+---------------
1996       | 10                 | October          | 1             
2003       | 11                 | November         | 1             
2004       | 7                  | July             | 1             
2004       | 12                 | December         | 1             
2005       | 3                  | March            | 1             
2005       | 5                  | May              | 1             

(6 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT YEAR(dob) AS birth_year,
       MONTH(dob) AS birth_month_number,
       MONTHNAME(dob) AS birth_month_name,
       COUNT(*) AS total_students
FROM student
WHERE 
GROUP BY birth_year, birth_month_number, birth_month_name
HAVING total_students >= 1
ORDER BY birth_year ASC, birth_month_number ASC;""",
        "testCases": build_test_cases(SOL_Q4)
    },
    {
        "id": 13,
        "title": "Complete Student Database Intelligence Report",
        "difficulty": "Hard",
        "points": 100,
        "category": "SQL",
        "type": "sql",
        "tags": ["SQL", "DISTINCT", "Aggregate Functions", "GROUP BY", "Intelligence"],
        "description": """## Complete Student Database Intelligence Report

The college wants to build a comprehensive student analytics dashboard to understand academic performance and demographic distribution.

Write an SQL query to generate a **gender-wise academic performance report**.

For each gender, calculate:
1. Gender (`gender`).
2. Total number of students: `COUNT(*)` as **`total_students`**.
3. Sum of marks obtained: `SUM(marks)` as **`total_marks`**.
4. Average marks rounded to 2 decimal places: `ROUND(AVG(marks), 2)` as **`average_marks`**.
5. Highest marks: `MAX(marks)` as **`highest_marks`**.
6. Lowest marks: `MIN(marks)` as **`lowest_marks`**.
7. Average age rounded to 2 decimal places: `ROUND(AVG(age), 2)` as **`average_age`**.
8. Number of unique cities represented: `COUNT(DISTINCT city)` as **`unique_cities`**.
9. Number of unique ages: `COUNT(DISTINCT age)` as **`unique_ages`**.
10. Number of unique marks: `COUNT(DISTINCT marks)` as **`unique_marks`**.

### Additional Requirements:
- Group the results by `gender`.
- Sort the results by **`average_marks` in descending order**.

### Output Columns
`gender`, `total_students`, `total_marks`, `average_marks`, `highest_marks`, `lowest_marks`, `average_age`, `unique_cities`, `unique_ages`, `unique_marks`""",
        "sampleInput": SAMPLE_TABLE_VIEW,
        "sampleOutput": """gender | total_students | total_marks | average_marks | highest_marks | lowest_marks | average_age | unique_cities | unique_ages | unique_marks
-------+----------------+-------------+---------------+---------------+--------------+-------------+---------------+-------------+-------------
F      | 4              | 352         | 88.0          | 95            | 78           | 22.0        | 4             | 3           | 4           
M      | 6              | 425         | 70.83         | 85            | 55           | 23.17       | 4             | 5           | 6           

(2 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT gender,
       COUNT(*) AS total_students,
       SUM(marks) AS total_marks,
       ROUND(AVG(marks), 2) AS average_marks,
       MAX(marks) AS highest_marks,
       MIN(marks) AS lowest_marks,
       ROUND(AVG(age), 2) AS average_age,
       COUNT(DISTINCT city) AS unique_cities,
       COUNT(DISTINCT age) AS unique_ages,
       COUNT(DISTINCT marks) AS unique_marks
FROM student
GROUP BY gender
ORDER BY average_marks DESC;""",
        "testCases": build_test_cases(SOL_Q5)
    }
]

if __name__ == '__main__':
    # Load existing questions and update / append
    with open("/Users/saar.thxkk/Desktop/COMPILER/data/questions.json", "r") as f:
        questions = json.load(f)

    # Keep questions 1-8, remove any existing >=9 if rerun
    questions = [q for q in questions if q["id"] <= 8]
    questions.extend(sql_questions)

    with open("/Users/saar.thxkk/Desktop/COMPILER/data/questions.json", "w") as f:
        json.dump(questions, f, indent=2)

    print(f"Successfully updated questions.json! Total questions now: {len(questions)}")
    for q in sql_questions:
        print(f"Added Q{q['id']}: {q['title']} ({q['difficulty']} - {q['points']} pts, {len(q['testCases'])} test cases)")
