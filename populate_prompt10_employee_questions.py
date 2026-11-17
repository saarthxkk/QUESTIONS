import json
import sqlite3
import calendar

# ─── Database Schema & Datasets ──────────────────────────────────────────────

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
(5, 'Sales', 'Gurgaon'),
(6, 'Research', 'Mumbai');

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

# Edge test case dataset 2 (Modified boundaries & alternative hiring dates)
DATA_SET_2 = """INSERT INTO department (dept_id, dept_name, location) VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Gurgaon'),
(6, 'Research', 'Mumbai');

INSERT INTO employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date) VALUES
(201, 'Aditya', 27, 'M', 1, 'Delhi', 74000, 89, '2021-04-12'),
(202, 'Alka', 25, 'F', 4, 'Noida', 69000, 93, '2022-03-15'),
(203, 'Amitabh', 30, 'M', 1, 'Gurgaon', 78000, 91, '2020-11-20'),
(204, 'Sonia', 29, 'F', 3, 'Delhi', 84000, 92, '2019-02-14'),
(205, 'Manish', 34, 'M', 2, 'Noida', 61000, 77, '2020-05-22'),
(206, 'Divya', 28, 'F', 5, 'Delhi', 66000, 84, '2021-09-01'),
(207, 'Anita', 26, 'F', 4, 'Delhi', 73000, 96, '2023-01-15'),
(208, 'Reena', 31, 'F', 3, 'Noida', 89000, 94, '2018-07-19'),
(209, 'Varun', 32, 'M', 5, 'Gurgaon', 58000, 73, '2020-03-11'),
(210, 'Geeta', 29, 'F', 1, 'Noida', 70000, 89, '2022-10-05');"""

# Edge test case dataset 3 (Edge salaries, boundary performance values)
DATA_SET_3 = """INSERT INTO department (dept_id, dept_name, location) VALUES
(1, 'IT', 'Delhi'),
(2, 'HR', 'Noida'),
(3, 'Finance', 'Gurgaon'),
(4, 'Marketing', 'Delhi'),
(5, 'Sales', 'Gurgaon'),
(6, 'Research', 'Mumbai');

INSERT INTO employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date) VALUES
(301, 'Ananya', 25, 'F', 1, 'Delhi', 60000, 90, '2020-01-01'),
(302, 'Ashish', 32, 'M', 4, 'Noida', 80000, 88, '2021-03-15'),
(303, 'Savitri', 28, 'F', 3, 'Gurgaon', 85000, 95, '2019-06-20'),
(304, 'Rohit', 27, 'M', 2, 'Delhi', 59000, 78, '2022-08-10'),
(305, 'Kavita', 31, 'F', 5, 'Delhi', 62000, 83, '2020-12-25'),
(306, 'Priya', 26, 'F', 3, 'Delhi', 79000, 91, '2021-05-18'),
(307, 'Arun', 30, 'M', 1, 'Gurgaon', 68000, 89, '2020-09-09');"""


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


def format_table(columns, rows):
    if not columns and not rows:
        return "(Empty result)"
    col_names = [str(c) for c in columns]
    widths = [len(c) for c in col_names]
    for row in rows:
        for i, val in enumerate(row):
            s = "NULL" if val is None else str(val)
            if len(s) > widths[i]:
                widths[i] = len(s)
    sep = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    hdr = "|" + "|".join([f" {col_names[i].ljust(widths[i])} " for i in range(len(columns))]) + "|"
    out = [sep, hdr, sep]
    for row in rows:
        line = "|" + "|".join([f" {('NULL' if row[i] is None else str(row[i])).ljust(widths[i])} " for i in range(len(columns))]) + "|"
        out.append(line)
    out.append(sep)
    return "\n".join(out)


# ─── Exact SQL Solutions for Problems 1–8 (Prompt 10) ────────────────────────

SOLUTIONS = {
    14: """SELECT e.emp_id, e.emp_name AS employee_name, d.dept_name AS department, e.age, e.gender, e.city, e.salary, e.performance, e.joining_date
FROM employee e
INNER JOIN department d ON e.dept_id = d.dept_id
WHERE e.age BETWEEN 25 AND 32
  AND e.salary BETWEEN 60000 AND 80000
  AND e.city IN ('Delhi', 'Noida', 'Gurgaon')
  AND e.joining_date BETWEEN '2020-01-01' AND '2023-12-31'
  AND (e.emp_name LIKE 'A%' OR e.emp_name LIKE '%a' OR e.emp_name LIKE '%it%')
  AND e.performance NOT BETWEEN 70 AND 85
  AND d.dept_name NOT IN ('HR', 'Sales')
ORDER BY e.salary DESC, employee_name ASC;""",

    15: """SELECT emp_id, emp_name AS employee_name, dept_id, salary AS employee_salary, performance AS performance_score, gender
FROM employee
WHERE performance >= 75 AND salary BETWEEN 60000 AND 90000
ORDER BY performance_score DESC, employee_salary DESC, employee_name ASC
LIMIT 5;""",

    16: """SELECT 
    COUNT(*) AS total_employees,
    SUM(salary) AS total_salary,
    ROUND(AVG(salary), 2) AS average_salary,
    MAX(salary) AS highest_salary,
    MIN(salary) AS lowest_salary,
    MAX(salary) - MIN(salary) AS salary_difference,
    COALESCE(SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END), 0) AS female_total_salary,
    ROUND(AVG(CASE WHEN performance > 80 THEN salary END), 2) AS high_performer_avg_salary,
    ROUND(AVG(performance), 2) AS average_performance
FROM employee;""",

    17: """SELECT 
    d.dept_id,
    d.dept_name AS department,
    COUNT(e.emp_id) AS total_employees,
    SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
    ROUND(AVG(e.salary), 2) AS average_salary,
    ROUND(AVG(e.performance), 2) AS average_performance,
    MAX(e.salary) AS highest_salary,
    MAX(e.performance) AS highest_performance,
    SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
    CASE 
        WHEN AVG(e.performance) >= 85 THEN 'Top Department'
        WHEN AVG(e.performance) >= 75 THEN 'Good Department'
        ELSE 'Needs Improvement'
    END AS department_category
FROM department d
INNER JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(e.emp_id) >= 3
   AND AVG(e.salary) > 60000
   AND AVG(e.performance) > 75
   AND MAX(e.performance) >= 90
ORDER BY average_salary DESC, average_performance DESC, d.dept_id ASC;""",

    18: """SELECT 
    d.dept_id,
    d.dept_name AS department,
    d.location AS department_location,
    e.emp_id,
    e.emp_name AS employee_name,
    e.salary AS employee_salary
FROM department d
LEFT JOIN employee e ON d.dept_id = e.dept_id
ORDER BY d.dept_id ASC, e.emp_id ASC;""",

    19: """SELECT 
    d.dept_id,
    d.dept_name AS department,
    d.location,
    COUNT(e.emp_id) AS total_employees,
    COALESCE(SUM(e.salary), 0) AS total_salary,
    ROUND(AVG(e.salary), 2) AS average_salary,
    MAX(e.performance) AS highest_performance,
    CASE WHEN COUNT(e.emp_id) >= 1 THEN 'Staffed' ELSE 'No Employees' END AS staffing_status
FROM employee e
RIGHT JOIN department d ON e.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name, d.location
ORDER BY d.dept_id ASC;""",

    20: """SELECT 
    d.dept_name AS department,
    COUNT(e.emp_id) AS total_employees,
    SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
    SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
    SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) AS high_performers,
    SUM(CASE WHEN e.performance < 80 THEN 1 ELSE 0 END) AS low_performers,
    SUM(CASE WHEN e.performance >= 90 THEN 1 ELSE 0 END) AS excellent_count,
    SUM(CASE WHEN e.performance >= 80 AND e.performance < 90 THEN 1 ELSE 0 END) AS good_count,
    SUM(CASE WHEN e.performance >= 70 AND e.performance < 80 THEN 1 ELSE 0 END) AS average_count,
    SUM(CASE WHEN e.performance < 70 THEN 1 ELSE 0 END) AS poor_count,
    SUM(CASE WHEN e.salary >= 70000 THEN 1 ELSE 0 END) AS high_salary_count,
    SUM(CASE WHEN e.salary < 70000 THEN 1 ELSE 0 END) AS low_salary_count,
    ROUND(100.0 * SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) / COUNT(e.emp_id), 2) AS high_performer_percentage,
    ROUND(100.0 * SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) / COUNT(e.emp_id), 2) AS female_percentage
FROM department d
INNER JOIN employee e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING SUM(CASE WHEN e.performance >= 80 THEN 1 ELSE 0 END) > SUM(CASE WHEN e.performance < 80 THEN 1 ELSE 0 END)
   AND (100.0 * SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END) / COUNT(e.emp_id)) > 50.0
ORDER BY department ASC;""",

    21: """SELECT 
    YEAR(e.joining_date) AS joining_year,
    COUNT(e.emp_id) AS total_employees,
    ROUND(AVG(e.performance), 2) AS average_performance,
    MIN(e.joining_date) AS earliest_joining_date,
    MAX(e.joining_date) AS latest_joining_date,
    COUNT(DISTINCT d.dept_id) AS departments_represented
FROM employee e
INNER JOIN department d ON e.dept_id = d.dept_id
WHERE e.joining_date BETWEEN '2019-01-01' AND '2023-12-31'
GROUP BY YEAR(e.joining_date)
HAVING COUNT(e.emp_id) > 2
ORDER BY total_employees DESC, joining_year ASC;"""
}

# ─── Questions Specifications (Matching Prompt 10) ───────────────────────────

QUESTIONS_DEF = [
    {
        "id": 14,
        "title": "Employee Eligibility and Recruitment Search Engine",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "Filtering & INNER JOIN",
        "sql": SOLUTIONS[14],
        "description": """A large organization is upgrading its internal employee search platform to help the Human Resources (HR) team identify employees who may be eligible for special assignments, promotions and internal career opportunities.

The organization wants to create an eligibility search system that retrieves employee details along with their respective department information. However, employees must satisfy several conditions related to their salary, age, city, date of joining, name patterns and performance scores.

You are provided with two relational database tables:
- `employee`: Contains employee identification, personal details, salary, performance and joining date.
- `department`: Contains department names, department IDs and official office locations.

Both tables are connected through the `dept_id` column.

Write a single SQL query to retrieve employees who satisfy all the eligibility requirements listed below.

### Requirements
1. Retrieve `emp_id`, `employee_name` (`e.emp_name`), `department` (`d.dept_name`), `age`, `gender`, `city`, `salary`, `performance`, and `joining_date`.
2. Employee salary must be between ₹60,000 and ₹80,000, including both boundaries.
3. Employee age must be between 25 and 32, including both boundaries.
4. Employees must belong to Delhi, Noida or Gurgaon.
5. Joining date must fall between January 1, 2020 and December 31, 2023, including both dates.
6. Employee names must satisfy at least one of the following conditions:
   - Start with the letter 'A'
   - End with the letter 'a'
   - Contain the substring 'it'
7. Employees whose performance score is between 70 and 85, including both boundaries, must be excluded (`performance NOT BETWEEN 70 AND 85`).
8. Exclude employees belonging to the HR or Sales departments.
9. Sort the final results by salary in descending order. If salaries are equal, sort employee names alphabetically.
10. Use meaningful column aliases, such as `employee_name` and `department`.

### Acceptance Criteria (10 Checks)
- Employees from Panipat or outside Delhi/Noida/Gurgaon must never appear.
- Female employees from HR or Sales must never appear.
- Performance scores between 70 and 85 must be excluded.
- Age between 25 and 32 inclusive.
- Joining date from 2020 to 2023 inclusive.
- Exact column names: `emp_id`, `employee_name`, `department`, `age`, `gender`, `city`, `salary`, `performance`, `joining_date`."""
    },
    {
        "id": 15,
        "title": "Employee Performance Leaderboard and Incentive Selection",
        "difficulty": "Easy",
        "points": 25,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "ORDER BY & LIMIT",
        "sql": SOLUTIONS[15],
        "description": """A multinational organization conducts an annual employee performance evaluation to identify individuals who deserve special recognition, salary incentives and career advancement opportunities.

The HR department wants to build an employee leaderboard that displays the highest-performing employees across the organization.

However, the company has decided that only employees satisfying certain minimum performance and salary requirements should be eligible for the leaderboard.

An employee's performance score will be considered the primary ranking factor. In case multiple employees receive the same performance score, the employee earning a higher salary must be placed ahead. If both performance and salary are equal, names must be arranged alphabetically.

You are provided with an `employee` table containing employee information, including salary, performance, gender and department ID.

Write a single SQL query that generates the top five eligible employees.

### Requirements
1. Consider only employees whose performance score is greater than or equal to 75 (`performance >= 75`).
2. Consider only employees whose salary is between ₹60,000 and ₹90,000 inclusive (`salary BETWEEN 60000 AND 90000`).
3. Retrieve:
   - `emp_id`
   - `employee_name` (alias for `emp_name`)
   - `dept_id`
   - `employee_salary` (alias for `salary`)
   - `performance_score` (alias for `performance`)
   - `gender`
4. Arrange employees according to:
   - `performance_score` in descending order
   - `employee_salary` in descending order
   - `employee_name` in ascending alphabetical order
5. Return only the first five employees after applying the sorting conditions (`LIMIT 5`).
6. Use meaningful aliases such as `employee_name`, `employee_salary` and `performance_score`.

### Acceptance Criteria (10 Checks)
- Exactly 5 rows returned.
- Primary sort on performance DESC.
- Secondary sort on salary DESC.
- Tertiary sort on employee_name ASC.
- Performance strictly >= 75 and salary between 60,000 and 90,000."""
    },
    {
        "id": 16,
        "title": "Enterprise Payroll and Compensation Statistics Analyzer",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "Aggregate Functions & COALESCE",
        "sql": SOLUTIONS[16],
        "description": """The finance department of an organization is preparing its monthly payroll statement for senior management.

The company wants to understand its total employee strength, monthly salary expenditure, average compensation, salary distribution and the portion of its payroll allocated to female employees.

Additionally, management wants to analyze the average salary of employees who have achieved a performance score greater than 80 to understand the compensation associated with higher-performing employees.

You are provided with an `employee` table containing information about employee salaries, gender and performance scores.

Your task is to write a single SQL query that generates a consolidated payroll statistics report.

### Requirements
Calculate and display the following information in a single row:
1. `total_employees`: Total number of employees working in the organization.
2. `total_salary`: Total salary paid to all employees (`SUM(salary)`).
3. `average_salary`: Average salary of all employees, rounded to two decimal places (`ROUND(AVG(salary), 2)`).
4. `highest_salary`: Highest salary paid to any employee (`MAX(salary)`).
5. `lowest_salary`: Lowest salary paid to any employee (`MIN(salary)`).
6. `salary_difference`: Difference between the highest and lowest salaries (`MAX(salary) - MIN(salary)`).
7. `female_total_salary`: Total salary paid exclusively to female employees (`COALESCE(SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END), 0)`).
8. `high_performer_avg_salary`: Average salary of employees whose performance score is strictly greater than 80 (`ROUND(AVG(CASE WHEN performance > 80 THEN salary END), 2)`).
9. `average_performance`: Average performance score of all employees, rounded to two decimal places (`ROUND(AVG(performance), 2)`).
10. Give every calculated column the exact specified alias.

### Acceptance Criteria (10 Checks)
- Exactly one summary row returned.
- Female total salary sums only rows where gender = 'F'.
- High performer average includes only performance > 80.
- All averages rounded to 2 decimal places."""
    },
    {
        "id": 17,
        "title": "Department Performance and Executive Management Dashboard",
        "difficulty": "Hard",
        "points": 100,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "INNER JOIN, GROUP BY & HAVING",
        "sql": SOLUTIONS[17],
        "description": """The executive management team of a growing organization wants to develop a department-wise performance dashboard to identify departments that demonstrate strong financial performance and employee productivity.

The company wants to prioritize departments that maintain a sufficient employee workforce, offer competitive salaries and consistently achieve high employee performance scores.

The management team has decided that a department will be considered eligible for additional investment and performance incentives only when it satisfies multiple organizational requirements.

You are provided with two relational tables:
- `employee`: Stores employee details, including salary, gender, performance and department ID.
- `department`: Stores department identification, department names and official office locations.

The tables are connected through the common `dept_id` column.

Write a single SQL query using INNER JOIN, GROUP BY, aggregate functions, CASE and HAVING to generate the executive report.

### Requirements
For each department, calculate:
1. `dept_id` and `department` (`d.dept_name`).
2. `total_employees`: Total employee count (`COUNT(e.emp_id)`).
3. `male_count`: Total male employees (`SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END)`).
4. `female_count`: Total female employees (`SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END)`).
5. `average_salary`: Average employee salary, rounded to two decimal places (`ROUND(AVG(e.salary), 2)`).
6. `average_performance`: Average employee performance score, rounded to two decimal places (`ROUND(AVG(e.performance), 2)`).
7. `highest_salary`: Highest salary paid in the department (`MAX(e.salary)`).
8. `highest_performance`: Highest performance score achieved in the department (`MAX(e.performance)`).
9. `high_performers`: Number of employees with performance >= 80.
10. `department_category` using CASE:
    - Average performance >= 85: 'Top Department'
    - Average performance >= 75 and below 85: 'Good Department'
    - Below 75: 'Needs Improvement'

### Filtering Conditions (HAVING)
Only include departments satisfying all of the following requirements:
- At least 3 employees (`COUNT(e.emp_id) >= 3`)
- Average salary strictly greater than ₹60,000 (`AVG(e.salary) > 60000`)
- Average performance strictly greater than 75 (`AVG(e.performance) > 75`)
- At least one employee has a performance score of 90 or higher (`MAX(e.performance) >= 90`)

### Sorting Requirements
1. Sort by `average_salary` in descending order.
2. For equal average salaries, sort by `average_performance` in descending order.
3. Use `dept_id` ASC as a final tie-breaker."""
    },
    {
        "id": 18,
        "title": "Complete Department Directory Using LEFT JOIN",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "LEFT JOIN & NULL Handling",
        "sql": SOLUTIONS[18],
        "description": """An organization is developing a centralized department directory to maintain a complete record of all its registered departments and the employees assigned to each department.

The HR department wants to generate a report that displays every department along with the employees working in it. However, some departments may have recently been created and may not yet have any employees assigned to them.

The management team wants to ensure that such departments are not excluded from the final report.

You are provided with two relational tables:
- `department`: Contains department IDs, department names and official office locations.
- `employee`: Contains employee IDs, names, salaries and department IDs.

Write an SQL query using LEFT JOIN to generate a complete department directory.

The `department` table must be treated as the left-hand table so that every department appears in the output, regardless of whether it has matching employee records.

### Requirements
1. Display `dept_id` (Department ID).
2. Display `department` (Department name from `department.dept_name`).
3. Display `department_location` (Official department location from `department.location`).
4. Display `emp_id` (Employee ID).
5. Display `employee_name` (Employee name from `employee.emp_name`).
6. Display `employee_salary` (Employee salary from `employee.salary`).
7. Include all departments, including those without employees (such as Research).
8. For departments without employees, employee-related columns must display `NULL`.
9. Sort results by `dept_id` in ascending order.
10. For departments containing multiple employees, sort their employees by `emp_id` in ascending order.

### Acceptance Criteria (10 Checks)
- Exactly 16 rows returned (15 staffed employee rows + 1 unstaffed Research row).
- LEFT JOIN preserves all 6 departments.
- Research displays with emp_id = NULL, employee_name = NULL, employee_salary = NULL.
- Sorting is dept_id ASC, emp_id ASC."""
    },
    {
        "id": 19,
        "title": "Department Staffing and Vacancy Audit Using RIGHT JOIN",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "RIGHT JOIN & Vacancy Auditing",
        "sql": SOLUTIONS[19],
        "description": """The operations management team of a company wants to perform a staffing audit to understand the current workforce distribution across all registered departments.

The company maintains multiple departments, and management wants a report that identifies which departments have active employees and which departments are currently unstaffed.

In particular, newly created departments must remain visible in the report even when no employee has been assigned to them.

You are provided with two tables:
- `employee`: Contains employee details, including salary, performance and department ID.
- `department`: Contains all registered departments and their office locations.

Write a single SQL query using RIGHT JOIN, GROUP BY, aggregate functions and CASE to generate a department staffing report.

For this problem, use the `employee` table on the left side and the `department` table on the right side of the RIGHT JOIN.

### Requirements
For every department, calculate and display:
1. `dept_id`: Department ID (`d.dept_id`).
2. `department`: Department name (`d.dept_name`).
3. `location`: Office location (`d.location`).
4. `total_employees`: Employee count (`COUNT(e.emp_id)`).
5. `total_salary`: Total salary expenditure (`COALESCE(SUM(e.salary), 0)`).
6. `average_salary`: Average employee salary, rounded to two decimal places (`ROUND(AVG(e.salary), 2)`).
7. `highest_performance`: Maximum performance score (`MAX(e.performance)`).
8. `staffing_status` using CASE:
   - At least 1 employee: 'Staffed'
   - 0 employees: 'No Employees'

### Additional Requirements
- Use RIGHT JOIN: `FROM employee e RIGHT JOIN department d ON e.dept_id = d.dept_id`.
- Use `COUNT(e.emp_id)` instead of `COUNT(*)` so unstaffed departments return 0 employees.
- Use `COALESCE` so unstaffed departments show total_salary = 0.
- For departments with 0 employees, `average_salary` and `highest_performance` must remain NULL.
- Group records by `d.dept_id`, `d.dept_name`, `d.location`.
- Sort results by `d.dept_id` in ascending order."""
    },
    {
        "id": 20,
        "title": "Department Performance Classification and Workforce Diversity Audit",
        "difficulty": "Hard",
        "points": 100,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "CASE Aggregation, Diversity & Audit",
        "sql": SOLUTIONS[20],
        "description": """The Human Resources analytics team wants to perform a detailed analysis of workforce diversity, salary distribution and employee performance across different departments.

Senior management believes that departments should maintain a strong proportion of high-performing employees while also ensuring adequate female representation.

The company wants to identify departments that meet both requirements and generate a detailed report showing the composition of employees according to their performance and salary categories.

You are provided with two relational tables:
- `employee`: Stores employee information, including salary, gender, performance and department ID.
- `department`: Stores department names and department IDs.

Write a single SQL query using INNER JOIN, CASE, conditional aggregation, GROUP BY and HAVING to generate the department-wise audit report.

### Requirements
For each department, calculate:
1. `department`: Department name (`d.dept_name`).
2. `total_employees`: Total employees (`COUNT(e.emp_id)`).
3. `male_count`: Male employees (`SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END)`).
4. `female_count`: Female employees (`SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END)`).
5. `high_performers`: Employees with performance >= 80.
6. `low_performers`: Employees with performance < 80.
7. `excellent_count`: Performance >= 90.
8. `good_count`: Performance 80–89.
9. `average_count`: Performance 70–79.
10. `poor_count`: Performance below 70.
11. `high_salary_count`: Salary >= ₹70,000.
12. `low_salary_count`: Salary below ₹70,000.
13. `high_performer_percentage`: `ROUND(100.0 * high_performers / total_employees, 2)`.
14. `female_percentage`: `ROUND(100.0 * female_count / total_employees, 2)`.

### Filtering Conditions (HAVING)
Only return departments satisfying both conditions:
- The number of high-performing employees must be greater than low-performing employees (`high_performers > low_performers`).
- More than 50% of employees in the department must be female (`female_percentage > 50.0`).

Sort departments alphabetically by `department` in ascending order."""
    },
    {
        "id": 21,
        "title": "Annual Recruitment Trends and Hiring Cohort Analysis",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "Date Functions, Cohort & HAVING",
        "sql": SOLUTIONS[21],
        "description": """The Human Resources department wants to analyze the organization's recruitment history to identify its busiest hiring years.

The company has hired employees across several years, and management wants to understand how recruitment volume has changed over time. In addition to the number of employees hired, management wants to examine the average performance of employees recruited during each year.

The organization also wants to determine how many different departments participated in recruitment during each year.

You are provided with two relational tables:
- `employee`: Stores employee information, joining dates, performance scores and department IDs.
- `department`: Stores department identification and department names.

Both tables are connected through `dept_id`.

Write a SQL query using INNER JOIN, YEAR(), GROUP BY, aggregate functions and HAVING to generate an annual recruitment report.

### Requirements
1. Consider employees who joined between January 1, 2019 and December 31, 2023, inclusive (`joining_date BETWEEN '2019-01-01' AND '2023-12-31'`).
2. Extract the joining year using `YEAR(joining_date)`.
3. Group employee records according to their `joining_year`.
4. Calculate `total_employees`: Total employees hired in that year.
5. Calculate `average_performance`: Average employee performance, rounded to two decimal places.
6. Find `earliest_joining_date`: Earliest joining date recorded in each year (`MIN(joining_date)`).
7. Find `latest_joining_date`: Latest joining date recorded in each year (`MAX(joining_date)`).
8. Calculate `departments_represented`: Count of distinct departments represented (`COUNT(DISTINCT d.dept_id)`).
9. Display only years in which more than two employees were recruited (`HAVING COUNT(e.emp_id) > 2`).
10. Sort results by `total_employees` in descending order. If two years have the same employee count, sort by `joining_year` in ascending order."""
    }
]


def generate_questions():
    with open("data/questions.json", "r") as f:
        existing_questions = json.load(f)

    # Keep questions 1 to 13
    base_questions = [q for q in existing_questions if q["id"] < 14]

    new_questions = []
    datasets = [
        ("Standard Company Dataset (15 Employees, 6 Departments)", DEFAULT_DATA_SQL, True),
        ("Dataset 2: Edge Boundaries & Alternative Cohorts", DATA_SET_2, False),
        ("Dataset 3: Boundary Salaries & Distinct Department Sizes", DATA_SET_3, False)
    ]

    for qdef in QUESTIONS_DEF:
        qid = qdef["id"]
        sql = qdef["sql"]

        # Run query on standard dataset to generate sample output
        sample_cols, sample_rows = run_query(SCHEMA_SQL, DEFAULT_DATA_SQL, sql)
        sample_output_ascii = format_table(sample_cols, sample_rows)

        # Generate test cases
        test_cases = []
        for tc_id, (desc, data_sql, is_sample) in enumerate(datasets, 1):
            cols, rows = run_query(SCHEMA_SQL, data_sql, sql)
            test_cases.append({
                "id": tc_id,
                "description": desc,
                "isSample": is_sample,
                "testData": data_sql,
                "expectedColumns": cols,
                "expectedRows": rows,
                "orderSensitive": True
            })

        q_obj = {
            "id": qid,
            "title": qdef["title"],
            "difficulty": qdef["difficulty"],
            "points": qdef["points"],
            "track": qdef["track"],
            "category": qdef["category"],
            "subtopic": qdef["subtopic"],
            "tags": [qdef["subtopic"], "SQL", "MySQL"],
            "description": qdef["description"],
            "type": "sql",
            "tableSchema": SCHEMA_SQL,
            "testData": DEFAULT_DATA_SQL,
            "sampleInput": "SELECT * FROM department;\nSELECT * FROM employee;",
            "sampleOutput": sample_output_ascii,
            "boilerplate": f"-- Write your MySQL query below\n-- Schema: department (dept_id, dept_name, location)\n--         employee (emp_id, emp_name, age, gender, dept_id, city, salary, performance, joining_date)\n\n",
            "testCases": test_cases
        }
        new_questions.append(q_obj)

    final_questions = base_questions + new_questions

    with open("data/questions.json", "w") as f:
        json.dump(final_questions, f, indent=2)

    print(f"✅ Successfully wrote {len(final_questions)} questions to data/questions.json!")
    print(f"Added {len(new_questions)} Employee SQL Questions (Q14-Q21) from Prompt 10.")


if __name__ == "__main__":
    generate_questions()
