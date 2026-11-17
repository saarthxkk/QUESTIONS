import json
import sqlite3
import calendar

# Setup runner to generate ground truth test cases
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

SCHEMA_SQL = """CREATE TABLE department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    location VARCHAR(50)
);

CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    age INT,
    gender CHAR(1),
    dept_id INT,
    city VARCHAR(50),
    salary INT,
    performance INT,
    joining_date DATE,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);"""

DEFAULT_DATA_SQL = """INSERT INTO department (dept_id, dept_name, location) VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Gurgaon');

INSERT INTO employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date) VALUES
(101, 'Aman', 28, 'M', 1, 'Delhi', 65000, 85, '2021-06-15'),
(102, 'Priya', 26, 'F', 1, 'Noida', 72000, 92, '2020-03-10'),
(103, 'Rohit', 31, 'M', 2, 'Delhi', 58000, 74, '2019-08-21'),
(104, 'Neha', 29, 'F', 2, 'Noida', 62000, 88, '2022-01-12'),
(105, 'Karan', 35, 'M', 3, 'Gurgaon', 85000, 91, '2018-05-17'),
(106, 'Riya', 27, 'F', 3, 'Delhi', 78000, 79, '2021-11-03'),
(107, 'Vikas', 30, 'M', 4, 'Noida', 68000, 83, '2020-07-19'),
(108, 'Anjali', 25, 'F', 4, 'Delhi', 71000, 95, '2023-02-14'),
(109, 'Mohit', 33, 'M', 5, 'Gurgaon', 55000, 68, '2019-12-01'),
(110, 'Simran', 28, 'F', 5, 'Delhi', 60000, 82, '2022-09-25'),
(111, 'Arjun', 24, 'M', 1, 'Gurgaon', 59000, 76, '2023-06-11'),
(112, 'Pooja', 32, 'F', 3, 'Noida', 88000, 94, '2017-04-20'),
(113, 'Nitin', 29, 'M', 4, 'Delhi', 64000, 72, '2021-01-05'),
(114, 'Kavita', 27, 'F', 5, 'Gurgaon', 63000, 89, '2020-10-16'),
(115, 'Deepak', 36, 'M', 2, 'Noida', 57000, 65, '2018-03-28');"""

# Edge test case dataset 2 (Modified values & boundaries)
DATA_SET_2 = """INSERT INTO department (dept_id, dept_name, location) VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Gurgaon');

INSERT INTO employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date) VALUES
(201, 'Aakash', 29, 'M', 1, 'Delhi', 75000, 88, '2021-08-10'),
(202, 'Anita', 27, 'F', 4, 'Noida', 74000, 93, '2022-04-18'),
(203, 'Rohan', 26, 'M', 1, 'Delhi', 68000, 89, '2020-11-20'),
(204, 'Sunita', 30, 'F', 3, 'Gurgaon', 82000, 92, '2019-02-14'),
(205, 'Manish', 34, 'M', 2, 'Noida', 61000, 77, '2020-05-22'),
(206, 'Divya', 28, 'F', 5, 'Delhi', 66000, 84, '2021-09-01'),
(207, 'Amit', 25, 'M', 4, 'Delhi', 62000, 87, '2023-01-15'),
(208, 'Reena', 31, 'F', 3, 'Noida', 89000, 96, '2018-07-19'),
(209, 'Varun', 32, 'M', 5, 'Gurgaon', 58000, 73, '2020-03-11'),
(210, 'Geeta', 29, 'F', 1, 'Noida', 70000, 91, '2022-10-05');"""

# Edge test case dataset 3 (Edge boundaries & single department testing)
DATA_SET_3 = """INSERT INTO department (dept_id, dept_name, location) VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Gurgaon');

INSERT INTO employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date) VALUES
(301, 'Aditi', 25, 'F', 1, 'Delhi', 60000, 90, '2020-01-01'),
(302, 'Alok', 32, 'M', 4, 'Noida', 80000, 89, '2021-03-15'),
(303, 'Savitri', 28, 'F', 3, 'Gurgaon', 85000, 95, '2019-06-20'),
(304, 'Rohit', 27, 'M', 2, 'Delhi', 59000, 78, '2022-08-10'),
(305, 'Kavita', 31, 'F', 5, 'Delhi', 62000, 83, '2020-12-25'),
(306, 'Naveen', 35, 'M', 3, 'Noida', 90000, 92, '2017-09-14'),
(307, 'Ankit', 26, 'M', 1, 'Noida', 67000, 86, '2023-04-05');"""

# Solutions
SOL_P1 = """SELECT e.emp_id, e.emp_name AS employee_name, d.dept_name AS department,
       e.age, e.gender, e.city, e.salary, e.performance, e.joining_date
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
WHERE e.salary BETWEEN 60000 AND 80000
  AND e.age BETWEEN 25 AND 32
  AND e.city IN ('Delhi', 'Noida')
  AND e.joining_date >= '2020-01-01'
  AND (e.emp_name LIKE 'A%' OR e.emp_name LIKE '%a' OR e.emp_name LIKE '%it%')
  AND (e.performance < 70 OR e.performance > 85)
  AND d.dept_name NOT IN ('HR', 'Sales')
  AND NOT (e.gender = 'F' AND e.performance < 90)
ORDER BY e.salary DESC, e.emp_name ASC;"""

SOL_P2 = """SELECT emp_id, emp_name AS employee_name, dept_id, salary AS employee_salary, performance AS performance_score, gender
FROM employee
WHERE performance >= 75
  AND salary BETWEEN 60000 AND 90000
ORDER BY performance DESC, salary DESC, emp_name ASC
LIMIT 5;"""

SOL_P3 = """SELECT COUNT(*) AS total_employees,
       SUM(salary) AS total_salary,
       ROUND(AVG(salary), 2) AS average_salary,
       MAX(salary) AS highest_salary,
       MIN(salary) AS lowest_salary,
       (MAX(salary) - MIN(salary)) AS salary_difference,
       SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END) AS female_total_salary,
       ROUND(AVG(CASE WHEN performance > 80 THEN salary ELSE NULL END), 2) AS high_performer_avg_salary,
       ROUND(AVG(performance), 2) AS average_performance
FROM employee;"""

SOL_P4 = """SELECT d.location,
       COUNT(e.emp_id) AS total_employees,
       SUM(e.salary) AS total_salary,
       ROUND(AVG(e.salary), 2) AS average_salary,
       MAX(e.performance) AS highest_performance,
       COUNT(DISTINCT d.dept_id) AS total_departments
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
GROUP BY d.location
HAVING COUNT(e.emp_id) >= 3 AND AVG(e.salary) > 65000
ORDER BY average_salary DESC, d.location ASC;"""

SOL_P5 = """SELECT e.emp_id,
       e.emp_name AS employee_name,
       d.dept_name AS department,
       e.age,
       e.salary,
       e.performance,
       CASE
           WHEN e.performance >= 90 THEN 'Excellent'
           WHEN e.performance >= 80 THEN 'Good'
           WHEN e.performance >= 70 THEN 'Average'
           ELSE 'Poor'
       END AS performance_category,
       CASE
           WHEN e.salary >= 80000 THEN 'High'
           WHEN e.salary >= 60000 THEN 'Medium'
           ELSE 'Low'
       END AS salary_category,
       CASE
           WHEN e.age < 28 THEN 'Young'
           WHEN e.age BETWEEN 28 AND 32 THEN 'Middle'
           ELSE 'Senior'
       END AS age_category,
       YEAR(e.joining_date) AS joining_year,
       MONTHNAME(e.joining_date) AS joining_month
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
ORDER BY e.performance DESC, e.emp_id ASC;"""

SOL_P6 = """SELECT d.dept_name AS department,
       COUNT(e.emp_id) AS total_employees,
       SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
       SUM(CASE WHEN e.performance < 80 THEN 1 ELSE 0 END) AS low_performers,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_employees,
       ROUND(SUM(CASE WHEN e.performance >= 80 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(e.emp_id), 2) AS high_performer_percentage,
       ROUND(SUM(CASE WHEN e.gender = 'F' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(e.emp_id), 2) AS female_percentage,
       SUM(CASE WHEN e.salary >= 70000 THEN 1 ELSE 0 END) AS high_salary_employees,
       SUM(CASE WHEN e.salary < 70000 THEN 1 ELSE 0 END) AS low_salary_employees
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) > SUM(CASE WHEN e.performance < 80 THEN 1 ELSE 0 END)
   AND (SUM(CASE WHEN e.gender = 'F' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(e.emp_id)) > 50.0
ORDER BY d.dept_name ASC;"""

SOL_P7 = """SELECT YEAR(joining_date) AS joining_year,
       COUNT(emp_id) AS total_employees,
       ROUND(AVG(performance), 2) AS average_performance,
       MIN(joining_date) AS earliest_joining_date,
       MAX(joining_date) AS latest_joining_date
FROM employee
WHERE joining_date BETWEEN '2019-01-01' AND '2023-12-31'
GROUP BY YEAR(joining_date)
HAVING COUNT(emp_id) > 1
ORDER BY total_employees DESC, joining_year ASC;"""

SOL_P8 = """SELECT d.dept_id,
       d.dept_name AS department,
       COUNT(e.emp_id) AS total_employees,
       SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
       ROUND(AVG(e.salary), 2) AS average_salary,
       ROUND(AVG(e.performance), 2) AS average_performance,
       SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
       MAX(e.salary) AS highest_salary,
       MAX(e.performance) AS highest_performance,
       CASE
           WHEN AVG(e.performance) >= 85 THEN 'Top Department'
           WHEN AVG(e.performance) >= 75 THEN 'Good Department'
           ELSE 'Needs Improvement'
       END AS department_category
FROM department d
JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(e.emp_id) >= 3
   AND AVG(e.salary) > 60000
   AND AVG(e.performance) > 75
   AND MAX(e.performance) >= 90
ORDER BY average_salary DESC, average_performance DESC;"""

def build_test_cases(query):
    c1, r1 = run_query(SCHEMA_SQL, DEFAULT_DATA_SQL, query)
    c2, r2 = run_query(SCHEMA_SQL, DATA_SET_2, query)
    c3, r3 = run_query(SCHEMA_SQL, DATA_SET_3, query)
    return [
        {
            "id": 1,
            "description": "Standard corporate dataset (15 employees, 5 departments)",
            "isSample": True,
            "testData": DEFAULT_DATA_SQL,
            "expectedColumns": c1,
            "expectedRows": r1,
            "orderSensitive": True
        },
        {
            "id": 2,
            "description": "Diverse salary and demographic distribution test",
            "isSample": False,
            "testData": DATA_SET_2,
            "expectedColumns": c2,
            "expectedRows": r2,
            "orderSensitive": True
        },
        {
            "id": 3,
            "description": "Boundary conditions and date range validation test",
            "isSample": False,
            "testData": DATA_SET_3,
            "expectedColumns": c3,
            "expectedRows": r3,
            "orderSensitive": True
        }
    ]

SAMPLE_TABLES_VIEW = """-- department Table:
+---------+-----------+----------+
| dept_id | dept_name | location |
+---------+-----------+----------+
| 1       | IT        | Delhi    |
| 2       | HR        | Noida    |
| 3       | Finance   | Gurgaon  |
| 4       | Marketing | Delhi    |
| 5       | Sales     | Gurgaon  |
+---------+-----------+----------+

-- employee Table (15 records):
+--------+----------+-----+--------+---------+---------+--------+-------------+--------------+
| emp_id | emp_name | age | gender | dept_id | city    | salary | performance | joining_date |
+--------+----------+-----+--------+---------+---------+--------+-------------+--------------+
| 101    | Aman     | 28  | M      | 1       | Delhi   | 65000  | 85          | 2021-06-15   |
| 102    | Priya    | 26  | F      | 1       | Noida   | 72000  | 92          | 2020-03-10   |
| 103    | Rohit    | 31  | M      | 2       | Delhi   | 58000  | 74          | 2019-08-21   |
| 104    | Neha     | 29  | F      | 2       | Noida   | 62000  | 88          | 2022-01-12   |
| 105    | Karan    | 35  | M      | 3       | Gurgaon | 85000  | 91          | 2018-05-17   |
| 106    | Riya     | 27  | F      | 3       | Delhi   | 78000  | 79          | 2021-11-03   |
| 107    | Vikas    | 30  | M      | 4       | Noida   | 68000  | 83          | 2020-07-19   |
| 108    | Anjali   | 25  | F      | 4       | Delhi   | 71000  | 95          | 2023-02-14   |
| 109    | Mohit    | 33  | M      | 5       | Gurgaon | 55000  | 68          | 2019-12-01   |
| 110    | Simran   | 28  | F      | 5       | Delhi   | 60000  | 82          | 2022-09-25   |
| 111    | Arjun    | 24  | M      | 1       | Gurgaon | 59000  | 76          | 2023-06-11   |
| 112    | Pooja    | 32  | F      | 3       | Noida   | 88000  | 94          | 2017-04-20   |
| 113    | Nitin    | 29  | M      | 4       | Delhi   | 64000  | 72          | 2021-01-05   |
| 114    | Kavita   | 27  | F      | 5       | Gurgaon | 63000  | 89          | 2020-10-16   |
| 115    | Deepak   | 36  | M      | 2       | Noida   | 57000  | 65          | 2018-03-28   |
+--------+----------+-----+--------+---------+---------+--------+-------------+--------------+"""

employee_questions = [
    {
        "id": 14,
        "title": "Employee Eligibility and Recruitment Search System",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Employee Recruitment Search (JOIN)",
        "type": "sql",
        "tags": ["SQL", "INNER JOIN", "WHERE", "BETWEEN", "LIKE", "Filtering"],
        "description": """## Employee Eligibility and Recruitment Search System

A large organization is developing an internal employee search and recruitment management system. The HR department wants to identify employees who satisfy a specific combination of salary, age, location, performance, and recruitment-related requirements.

Write a single SQL query that retrieves all eligible employees.

### Requirements:
1. Retrieve `emp_id`, `employee_name` (`emp_name AS employee_name`), `department` (`dept_name AS department`), `age`, `gender`, `city`, `salary`, `performance`, and `joining_date`.
2. Salary must be **between ₹60,000 and ₹80,000** (inclusive).
3. Age must be **between 25 and 32 years old** (inclusive).
4. Employee must belong to either **Delhi** or **Noida**.
5. Must have joined on or after **January 1, 2020** (`joining_date >= '2020-01-01'`).
6. Employee name must satisfy at least one of:
   - Starts with 'A'
   - Ends with 'a'
   - Contains substring 'it'
7. **Exclude** employees whose performance scores are **between 70 and 85** (inclusive).
8. **Exclude** employees belonging to **HR** or **Sales** departments.
9. **Exclude female employees whose performance is below 90**.
10. Sort by **`salary` in descending order**, then alphabetically by name.

### Output Columns:
`emp_id`, `employee_name`, `department`, `age`, `gender`, `city`, `salary`, `performance`, `joining_date`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """emp_id | employee_name | department | age | gender | city  | salary | performance | joining_date
-------+---------------+------------+-----+--------+-------+--------+-------------+-------------
102    | Priya         | IT         | 26  | F      | Noida | 72000  | 92          | 2020-03-10  
108    | Anjali        | Marketing  | 25  | F      | Delhi | 71000  | 95          | 2023-02-14  

(2 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT e.emp_id, e.emp_name AS employee_name, d.dept_name AS department,
       e.age, e.gender, e.city, e.salary, e.performance, e.joining_date
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
WHERE 
ORDER BY ;""",
        "testCases": build_test_cases(SOL_P1)
    },
    {
        "id": 15,
        "title": "Employee Performance Leaderboard and Reward Selection",
        "difficulty": "Easy",
        "points": 25,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Employee Performance Leaderboard",
        "type": "sql",
        "tags": ["SQL", "ORDER BY", "LIMIT", "Aliases", "Filtering"],
        "description": """## Employee Performance Leaderboard and Reward Selection

A multinational organization conducts an annual performance evaluation. The HR department wants to generate an employee leaderboard prioritizing top performers who meet compensation and performance thresholds.

### Requirements:
1. Consider employees whose performance score is **at least 75**.
2. Consider employees whose salaries are **between ₹60,000 and ₹90,000** (inclusive).
3. Retrieve: `emp_id`, `employee_name` (`emp_name AS employee_name`), `dept_id`, `employee_salary` (`salary AS employee_salary`), `performance_score` (`performance AS performance_score`), and `gender`.
4. Sort using the following priority:
   - `performance_score` in descending order
   - `employee_salary` in descending order
   - `employee_name` in ascending alphabetical order
5. Display **only the top 5 employees** (`LIMIT 5`).

### Output Columns:
`emp_id`, `employee_name`, `dept_id`, `employee_salary`, `performance_score`, `gender`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """emp_id | employee_name | dept_id | employee_salary | performance_score | gender
-------+---------------+---------+-----------------+-------------------+-------
108    | Anjali        | 4       | 71000           | 95                | F     
112    | Pooja         | 3       | 88000           | 94                | F     
102    | Priya         | 1       | 72000           | 92                | F     
105    | Karan         | 3       | 85000           | 91                | M     
114    | Kavita        | 5       | 63000           | 89                | F     

(5 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT emp_id, emp_name AS employee_name, dept_id, salary AS employee_salary, performance AS performance_score, gender
FROM employee
WHERE 
ORDER BY 
LIMIT 5;""",
        "testCases": build_test_cases(SOL_P2)
    },
    {
        "id": 16,
        "title": "Company Payroll and Financial Statistics Analyzer",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Company Payroll Statistics",
        "type": "sql",
        "tags": ["SQL", "Aggregate Functions", "COUNT", "SUM", "AVG", "CASE", "ROUND"],
        "description": """## Company Payroll and Financial Statistics Analyzer

The finance department requires a consolidated executive financial summary report regarding overall payroll expenditure, salary distributions, and female/high-performer metrics.

Write a query returning a **single-row summary**:
1. `total_employees`: Total number of employees (`COUNT(*)`).
2. `total_salary`: Total salary expenditure (`SUM(salary)`).
3. `average_salary`: Average employee salary rounded to 2 decimal places (`ROUND(AVG(salary), 2)`).
4. `highest_salary`: Maximum salary paid (`MAX(salary)`).
5. `lowest_salary`: Minimum salary paid (`MIN(salary)`).
6. `salary_difference`: Difference between highest and lowest salary (`MAX(salary) - MIN(salary)`).
7. `female_total_salary`: Total salary paid to female employees (`SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END)`).
8. `high_performer_avg_salary`: Average salary of employees whose performance score is **strictly greater than 80** rounded to 2 decimals.
9. `average_performance`: Average performance score of the organization rounded to 2 decimal places.

### Output Columns:
`total_employees`, `total_salary`, `average_salary`, `highest_salary`, `lowest_salary`, `salary_difference`, `female_total_salary`, `high_performer_avg_salary`, `average_performance`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """total_employees | total_salary | average_salary | highest_salary | lowest_salary | salary_difference | female_total_salary | high_performer_avg_salary | average_performance
----------------+--------------+----------------+----------------+---------------+-------------------+---------------------+---------------------------+--------------------
15              | 1005000      | 67000.0        | 88000          | 55000         | 33000             | 494000              | 70444.44                  | 82.2               

(1 row)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT COUNT(*) AS total_employees,
       SUM(salary) AS total_salary,
       ROUND(AVG(salary), 2) AS average_salary,
       MAX(salary) AS highest_salary,
       MIN(salary) AS lowest_salary,
       (MAX(salary) - MIN(salary)) AS salary_difference,
       SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END) AS female_total_salary,
       ROUND(AVG(CASE WHEN performance > 80 THEN salary ELSE NULL END), 2) AS high_performer_avg_salary,
       ROUND(AVG(performance), 2) AS average_performance
FROM employee;""",
        "testCases": build_test_cases(SOL_P3)
    },
    {
        "id": 17,
        "title": "Department Location and Workforce Distribution Analysis",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Department Location & Workforce",
        "type": "sql",
        "tags": ["SQL", "INNER JOIN", "GROUP BY", "HAVING", "COUNT", "AVG", "DISTINCT"],
        "description": """## Department Location and Workforce Distribution Analysis

Management wants to evaluate workforce and payroll distribution across the **department's official office locations** (`department.location`), not the employee's personal city.

### Requirements:
1. Join `employee` and `department` on `dept_id`.
2. Group by `d.location`.
3. Calculate:
   - `total_employees`: Total employees working in departments at that location.
   - `total_salary`: Combined salary expenditure for that location.
   - `average_salary`: Average employee salary rounded to 2 decimal places.
   - `highest_performance`: Highest individual performance score at that location.
   - `total_departments`: Number of distinct departments operating at that location (`COUNT(DISTINCT d.dept_id)`).
4. Include only locations having **at least 3 employees** (`COUNT >= 3`).
5. Include only locations where `average_salary` is **strictly greater than ₹65,000**.
6. Sort by `average_salary` in descending order, then alphabetically by location.

### Output Columns:
`location`, `total_employees`, `total_salary`, `average_salary`, `highest_performance`, `total_departments`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """location | total_employees | total_salary | average_salary | highest_performance | total_departments
---------+-----------------+--------------+----------------+---------------------+------------------
Gurgaon  | 6               | 429000       | 71500.0        | 94                  | 2                
Delhi    | 6               | 399000       | 66500.0        | 95                  | 2                

(2 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT d.location,
       COUNT(e.emp_id) AS total_employees,
       SUM(e.salary) AS total_salary,
       ROUND(AVG(e.salary), 2) AS average_salary,
       MAX(e.performance) AS highest_performance,
       COUNT(DISTINCT d.dept_id) AS total_departments
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
GROUP BY d.location
HAVING 
ORDER BY ;""",
        "testCases": build_test_cases(SOL_P4)
    },
    {
        "id": 18,
        "title": "Employee Classification and HR Information Directory",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Employee HR Classification (CASE)",
        "type": "sql",
        "tags": ["SQL", "CASE Statements", "Date Functions", "YEAR", "MONTHNAME", "INNER JOIN"],
        "description": """## Employee Classification and HR Information Directory

The HR department requires a dynamic employee directory classifying employees according to salary, age, and performance using CASE statements.

### Retrieve for every employee:
`emp_id`, `employee_name` (`e.emp_name`), `department` (`d.dept_name`), `age`, `salary`, `performance`.

### Create Three Classification Columns:
1. **`performance_category`**:
   - `Performance >= 90` -> `'Excellent'`
   - `Performance >= 80` -> `'Good'`
   - `Performance >= 70` -> `'Average'`
   - `Performance < 70` -> `'Poor'`
2. **`salary_category`**:
   - `Salary >= 80000` -> `'High'`
   - `Salary >= 60000` -> `'Medium'`
   - `Salary < 60000` -> `'Low'`
3. **`age_category`**:
   - `Age < 28` -> `'Young'`
   - `Age BETWEEN 28 AND 32` -> `'Middle'`
   - `Age > 32` -> `'Senior'`
4. **`joining_year`**: `YEAR(joining_date)`.
5. **`joining_month`**: `MONTHNAME(joining_date)`.

### Sorting:
Sort by `performance` in descending order, then by `emp_id` in ascending order.

### Output Columns:
`emp_id`, `employee_name`, `department`, `age`, `salary`, `performance`, `performance_category`, `salary_category`, `age_category`, `joining_year`, `joining_month`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """emp_id | employee_name | department | age | salary | performance | performance_category | salary_category | age_category | joining_year | joining_month
-------+---------------+------------+-----+--------+-------------+----------------------+-----------------+--------------+--------------+--------------
108    | Anjali        | Marketing  | 25  | 71000  | 95          | Excellent            | Medium          | Young        | 2023         | February     
112    | Pooja         | Finance    | 32  | 88000  | 94          | Excellent            | High            | Middle       | 2017         | April        
102    | Priya         | IT         | 26  | 72000  | 92          | Excellent            | Medium          | Young        | 2020         | March        
105    | Karan         | Finance    | 35  | 85000  | 91          | Excellent            | High            | Senior       | 2018         | May          
114    | Kavita        | Sales      | 27  | 63000  | 89          | Good                 | Medium          | Young        | 2020         | October      
104    | Neha          | HR         | 29  | 62000  | 88          | Good                 | Medium          | Middle       | 2022         | January      

(Total 15 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT e.emp_id,
       e.emp_name AS employee_name,
       d.dept_name AS department,
       e.age,
       e.salary,
       e.performance,
       CASE 
           WHEN e.performance >= 90 THEN 'Excellent'
           WHEN e.performance >= 80 THEN 'Good'
           WHEN e.performance >= 70 THEN 'Average'
           ELSE 'Poor'
       END AS performance_category,
       CASE 
           WHEN e.salary >= 80000 THEN 'High'
           WHEN e.salary >= 60000 THEN 'Medium'
           ELSE 'Low'
       END AS salary_category,
       CASE 
           WHEN e.age < 28 THEN 'Young'
           WHEN e.age BETWEEN 28 AND 32 THEN 'Middle'
           ELSE 'Senior'
       END AS age_category,
       YEAR(e.joining_date) AS joining_year,
       MONTHNAME(e.joining_date) AS joining_month
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
ORDER BY e.performance DESC, e.emp_id ASC;""",
        "testCases": build_test_cases(SOL_P5)
    },
    {
        "id": 19,
        "title": "Department Performance and Gender Diversity Audit",
        "difficulty": "Hard",
        "points": 100,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Department Diversity Audit",
        "type": "sql",
        "tags": ["SQL", "CASE + GROUP BY", "HAVING", "Conditional Aggregates", "ROUND"],
        "description": """## Department Performance and Gender Diversity Audit

A company wants to identify departments that have both a high proportion of top performers and balanced female representation.

### For every department, calculate:
1. `department`: Department name (`d.dept_name`).
2. `total_employees`: Total employee count (`COUNT(e.emp_id)`).
3. `high_performers`: Count of employees with `performance >= 80`.
4. `low_performers`: Count of employees with `performance < 80`.
5. `female_employees`: Total female employees (`gender = 'F'`).
6. `high_performer_percentage`: `ROUND(high_performers * 100.0 / total_employees, 2)`.
7. `female_percentage`: `ROUND(female_employees * 100.0 / total_employees, 2)`.
8. `high_salary_employees`: Count of employees earning `salary >= 70000`.
9. `low_salary_employees`: Count of employees earning `salary < 70000`.

### Filtering Conditions (HAVING):
- The number of `high_performers` must be strictly greater than `low_performers`.
- More than 50% of employees in the department must be female (`female_percentage > 50.0`).

### Sorting:
Sort alphabetically by department name.

### Output Columns:
`department`, `total_employees`, `high_performers`, `low_performers`, `female_employees`, `high_performer_percentage`, `female_percentage`, `high_salary_employees`, `low_salary_employees`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """department | total_employees | high_performers | low_performers | female_employees | high_performer_percentage | female_percentage | high_salary_employees | low_salary_employees
-----------+-----------------+-----------------+----------------+------------------+---------------------------+-------------------+-----------------------+---------------------
Finance    | 3               | 2               | 1              | 2                | 66.67                     | 66.67             | 3                     | 0                   
Sales      | 3               | 2               | 1              | 2                | 66.67                     | 66.67             | 0                     | 3                   

(2 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT d.dept_name AS department,
       COUNT(e.emp_id) AS total_employees,
       SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
       SUM(CASE WHEN e.performance < 80 THEN 1 ELSE 0 END) AS low_performers,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_employees,
       ROUND(SUM(CASE WHEN e.performance >= 80 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(e.emp_id), 2) AS high_performer_percentage,
       ROUND(SUM(CASE WHEN e.gender = 'F' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(e.emp_id), 2) AS female_percentage,
       SUM(CASE WHEN e.salary >= 70000 THEN 1 ELSE 0 END) AS high_salary_employees,
       SUM(CASE WHEN e.salary < 70000 THEN 1 ELSE 0 END) AS low_salary_employees
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING 
ORDER BY d.dept_name ASC;""",
        "testCases": build_test_cases(SOL_P6)
    },
    {
        "id": 20,
        "title": "Annual Employee Recruitment and Hiring Trend Analysis",
        "difficulty": "Medium",
        "points": 50,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Annual Recruitment Trends",
        "type": "sql",
        "tags": ["SQL", "Date Functions", "YEAR", "GROUP BY", "HAVING", "ROUND"],
        "description": """## Annual Employee Recruitment and Hiring Trend Analysis

Analyze company hiring history between **2019 and 2023** to observe recruitment volume and candidate performance by cohort year.

### Requirements:
1. Consider employees who joined between **January 1, 2019 and December 31, 2023** (inclusive).
2. Extract the joining year using `YEAR(joining_date) AS joining_year`.
3. Group by `joining_year`.
4. Calculate:
   - `total_employees`: `COUNT(emp_id)`.
   - `average_performance`: `ROUND(AVG(performance), 2)`.
   - `earliest_joining_date`: `MIN(joining_date)`.
   - `latest_joining_date`: `MAX(joining_date)`.
5. Only display years in which **more than one employee was recruited** (`COUNT > 1`).
6. Sort by `total_employees` in descending order, then by `joining_year` in ascending order.

### Output Columns:
`joining_year`, `total_employees`, `average_performance`, `earliest_joining_date`, `latest_joining_date`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """joining_year | total_employees | average_performance | earliest_joining_date | latest_joining_date
-------------+-----------------+---------------------+-----------------------+--------------------
2020         | 3               | 88.0                | 2020-03-10            | 2020-10-16         
2021         | 3               | 78.67               | 2021-01-05            | 2021-11-03         
2019         | 2               | 71.0                | 2019-08-21            | 2019-12-01         
2022         | 2               | 85.0                | 2022-01-12            | 2022-09-25         
2023         | 2               | 85.5                | 2023-02-14            | 2023-06-11         

(5 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT YEAR(joining_date) AS joining_year,
       COUNT(emp_id) AS total_employees,
       ROUND(AVG(performance), 2) AS average_performance,
       MIN(joining_date) AS earliest_joining_date,
       MAX(joining_date) AS latest_joining_date
FROM employee
WHERE joining_date BETWEEN '2019-01-01' AND '2023-12-31'
GROUP BY YEAR(joining_date)
HAVING COUNT(emp_id) > 1
ORDER BY total_employees DESC, joining_year ASC;""",
        "testCases": build_test_cases(SOL_P7)
    },
    {
        "id": 21,
        "title": "Executive Department Performance and Workforce Intelligence Dashboard",
        "difficulty": "Hard",
        "points": 100,
        "category": "SQL",
        "track": "SQL",
        "subtopic": "Executive Dashboard (Hard)",
        "type": "sql",
        "tags": ["SQL", "Multiple SQL Concepts", "CASE", "GROUP BY", "HAVING", "ROUND", "MAX"],
        "description": """## Executive Department Performance and Workforce Intelligence Dashboard

Develop a comprehensive centralized executive dashboard comparing department headcount, diversity, salary, and quality.

### For each department, calculate:
1. `dept_id`, `department` (`d.dept_name`).
2. `total_employees`: `COUNT(e.emp_id)`.
3. `male_count`: Total male employees.
4. `female_count`: Total female employees.
5. `average_salary`: `ROUND(AVG(e.salary), 2)`.
6. `average_performance`: `ROUND(AVG(e.performance), 2)`.
7. `high_performers`: Count of employees with `performance >= 80`.
8. `highest_salary`: `MAX(e.salary)`.
9. `highest_performance`: `MAX(e.performance)`.
10. `department_category` (CASE expression):
    - `Average performance >= 85` -> `'Top Department'`
    - `Average performance >= 75` -> `'Good Department'`
    - `Average performance < 75` -> `'Needs Improvement'`

### Filtering Conditions (HAVING):
- Department must have **at least 3 employees**.
- Average salary must be **greater than ₹60,000**.
- Average performance score must be **greater than 75**.
- At least one employee in the department must have a performance score of **90 or higher** (`MAX(performance) >= 90`).

### Sorting:
Sort by `average_salary` in descending order, then by `average_performance` in descending order.

### Output Columns:
`dept_id`, `department`, `total_employees`, `male_count`, `female_count`, `average_salary`, `average_performance`, `high_performers`, `highest_salary`, `highest_performance`, `department_category`""",
        "sampleInput": SAMPLE_TABLES_VIEW,
        "sampleOutput": """dept_id | department | total_employees | male_count | female_count | average_salary | average_performance | high_performers | highest_salary | highest_performance | department_category
--------+------------+-----------------+------------+--------------+----------------+---------------------+-----------------+----------------+---------------------+--------------------
3       | Finance    | 3               | 1          | 2            | 83666.67       | 88.0                | 2               | 88000          | 94                  | Top Department     
4       | Marketing  | 3               | 2          | 1            | 67666.67       | 83.33               | 2               | 71000          | 95                  | Good Department    
1       | IT         | 3               | 2          | 1            | 65333.33       | 84.33               | 2               | 72000          | 92                  | Good Department    

(3 rows)""",
        "tableSchema": SCHEMA_SQL,
        "testData": DEFAULT_DATA_SQL,
        "boilerplate": """-- Write your SQL query below
SELECT d.dept_id,
       d.dept_name AS department,
       COUNT(e.emp_id) AS total_employees,
       SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
       SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
       ROUND(AVG(e.salary), 2) AS average_salary,
       ROUND(AVG(e.performance), 2) AS average_performance,
       SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
       MAX(e.salary) AS highest_salary,
       MAX(e.performance) AS highest_performance,
       CASE
           WHEN AVG(e.performance) >= 85 THEN 'Top Department'
           WHEN AVG(e.performance) >= 75 THEN 'Good Department'
           ELSE 'Needs Improvement'
       END AS department_category
FROM department d
JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(e.emp_id) >= 3
   AND AVG(e.salary) > 60000
   AND AVG(e.performance) > 75
   AND MAX(e.performance) >= 90
ORDER BY average_salary DESC, average_performance DESC;""",
        "testCases": build_test_cases(SOL_P8)
    }
]

if __name__ == '__main__':
    with open("data/questions.json", "r") as f:
        existing = json.load(f)

    # Retain Q1..Q13, remove any >=14 if previously inserted
    existing = [q for q in existing if q["id"] <= 13]
    existing.extend(employee_questions)

    with open("data/questions.json", "w") as f:
        json.dump(existing, f, indent=2)

    print(f"Successfully added all 8 Employee SQL questions! Total questions now: {len(existing)}")
    for q in employee_questions:
        print(f"  Added Q{q['id']}: [{q['subtopic']}] {q['title']} ({q['difficulty']} - {q['points']} pts)")
