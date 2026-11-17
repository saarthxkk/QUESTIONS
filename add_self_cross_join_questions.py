import json
import sqlite3

# ─── Database Schema & Test Datasets ──────────────────────────────────────────

SCHEMA_SQL = """CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    manager_id INT,
    department VARCHAR(50),
    salary INT,
    city VARCHAR(50),
    FOREIGN KEY (manager_id) REFERENCES employee(emp_id)
);

CREATE TABLE project (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(50),
    location VARCHAR(50)
);"""

DEFAULT_DATA_SQL = """INSERT INTO employee (emp_id, emp_name, manager_id, department, salary, city) VALUES
(101, 'Aman', NULL, 'IT', 90000, 'Delhi'),
(102, 'Priya', 101, 'IT', 70000, 'Noida'),
(103, 'Rohit', 101, 'IT', 65000, 'Delhi'),
(104, 'Neha', 102, 'HR', 60000, 'Noida'),
(105, 'Karan', 102, 'HR', 55000, 'Delhi'),
(106, 'Simran', 103, 'Finance', 75000, 'Gurgaon'),
(107, 'Arjun', 103, 'Finance', 50000, 'Delhi'),
(108, 'Pooja', 106, 'IT', 58000, 'Gurgaon');

INSERT INTO project (project_id, project_name, location) VALUES
(1, 'Banking System', 'Delhi'),
(2, 'E-Commerce', 'Noida'),
(3, 'Hospital Management', 'Gurgaon'),
(4, 'AI Chatbot', 'Delhi');"""

# Edge test dataset 2: Alternative reporting hierarchy, different cities and project counts
DATA_SET_2 = """INSERT INTO employee (emp_id, emp_name, manager_id, department, salary, city) VALUES
(201, 'Vikram', NULL, 'IT', 95000, 'Delhi'),
(202, 'Sunita', 201, 'IT', 80000, 'Delhi'),
(203, 'Rahul', 201, 'HR', 65000, 'Noida'),
(204, 'Ananya', 202, 'IT', 85000, 'Delhi'),
(205, 'Deepak', 202, 'IT', 72000, 'Gurgaon'),
(206, 'Meera', 203, 'HR', 60000, 'Noida');

INSERT INTO project (project_id, project_name, location) VALUES
(10, 'Cloud Gateway', 'Delhi'),
(20, 'Payment Hub', 'Noida'),
(30, 'Telehealth App', 'Gurgaon');"""

# Edge test dataset 3: Boundary salary comparison, multiple projects per city
DATA_SET_3 = """INSERT INTO employee (emp_id, emp_name, manager_id, department, salary, city) VALUES
(301, 'Aditi', NULL, 'IT', 88000, 'Delhi'),
(302, 'Kunal', 301, 'IT', 88000, 'Noida'),
(303, 'Tanvi', 301, 'IT', 92000, 'Delhi'),
(304, 'Gaurav', 302, 'Finance', 60000, 'Gurgaon'),
(305, 'Ritu', 302, 'Finance', 58000, 'Gurgaon');

INSERT INTO project (project_id, project_name, location) VALUES
(101, 'AI Platform', 'Delhi'),
(102, 'Analytics Suite', 'Delhi'),
(103, 'Logistics Engine', 'Noida');"""


def run_query(schema_sql, data_sql, query):
    conn = sqlite3.connect(":memory:")
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


# ─── Exact SQL Solutions for Problems 1–8 ─────────────────────────────────────

SOLUTIONS = {
    22: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.salary AS employee_salary,
    e.department,
    e.city AS employee_city,
    m.emp_id AS manager_id,
    m.emp_name AS manager_name,
    m.salary AS manager_salary,
    m.city AS manager_city
FROM employee e
LEFT JOIN employee m ON e.manager_id = m.emp_id
ORDER BY e.emp_id ASC;""",

    23: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.salary AS employee_salary,
    m.emp_name AS manager_name,
    m.salary AS manager_salary,
    e.salary - m.salary AS salary_difference,
    CASE 
        WHEN e.salary > m.salary THEN 'Higher than manager'
        WHEN e.salary < m.salary THEN 'Lower than manager'
        ELSE 'Equal to manager'
    END AS salary_comparison
FROM employee e
INNER JOIN employee m ON e.manager_id = m.emp_id
ORDER BY e.emp_id ASC;""",

    24: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    m.emp_name AS manager_name,
    e.city AS employee_city,
    m.city AS manager_city,
    CASE 
        WHEN (m.manager_id IS NULL OR m.emp_name = 'Aman') AND e.city = m.city THEN 'Direct report to Aman and same city as manager'
        WHEN (m.manager_id IS NULL OR m.emp_name = 'Aman') THEN 'Direct report to Aman'
        WHEN e.city = m.city THEN 'Same city as manager'
    END AS selection_reason
FROM employee e
INNER JOIN employee m ON e.manager_id = m.emp_id
WHERE (m.manager_id IS NULL OR m.emp_name = 'Aman') OR e.city = m.city
ORDER BY e.emp_id ASC;""",

    25: """SELECT 
    e1.emp_id AS employee1_id,
    e1.emp_name AS employee1,
    e1.salary AS employee1_salary,
    e2.emp_id AS employee2_id,
    e2.emp_name AS employee2,
    e2.salary AS employee2_salary,
    e1.department
FROM employee e1
INNER JOIN employee e2 ON e1.department = e2.department AND e1.emp_id < e2.emp_id
ORDER BY e1.department ASC, e1.emp_id ASC, e2.emp_id ASC;""",

    26: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.salary AS employee_salary,
    m.emp_id AS manager_id,
    m.emp_name AS manager_name,
    ROUND((SELECT AVG(sub.salary) FROM employee sub WHERE sub.manager_id = e.manager_id), 2) AS manager_direct_reports_avg_salary
FROM employee e
INNER JOIN employee m ON e.manager_id = m.emp_id
WHERE e.salary > (SELECT AVG(sub.salary) FROM employee sub WHERE sub.manager_id = e.manager_id)
ORDER BY e.emp_id ASC;""",

    27: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.department,
    p.project_id,
    p.project_name,
    p.location AS project_location,
    (SELECT COUNT(*) FROM employee) * (SELECT COUNT(*) FROM project) AS total_combinations
FROM employee e
CROSS JOIN project p
ORDER BY e.emp_id ASC, p.project_id ASC;""",

    28: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.city AS employee_city,
    p.project_id,
    p.project_name,
    p.location AS project_location,
    CASE 
        WHEN e.city = p.location THEN 'Location Match'
        ELSE 'Different Location'
    END AS location_status
FROM employee e
CROSS JOIN project p
WHERE e.department = 'IT'
ORDER BY e.emp_id ASC, p.project_id ASC;""",

    29: """SELECT 
    e.emp_id,
    e.emp_name AS employee_name,
    e.city AS employee_city,
    p.project_id,
    p.project_name,
    p.location AS project_location
FROM employee e
CROSS JOIN project p
WHERE e.city = p.location
ORDER BY e.emp_id ASC, p.project_id ASC;"""
}

# ─── Questions Metadata ───────────────────────────────────────────────────────

QUESTIONS_DEF = [
    {
        "id": 22,
        "title": "Employee Manager Directory and Reporting Hierarchy",
        "difficulty": "Easy",
        "points": 25,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "SELF JOIN & LEFT JOIN",
        "sql": SOLUTIONS[22],
        "description": """A large organization wants to develop an internal employee directory that provides information about every employee and their respective reporting manager.

The organization maintains employee information in a single relational table. Each employee is assigned a unique employee ID, and the `manager_id` column identifies the employee ID of their direct manager.

Since managers are also employees of the organization, their information is stored in the same table.

The organization has one top-level manager, Aman, who does not report to any other employee. Therefore, his `manager_id` is `NULL`.

The HR department wants to generate a complete reporting hierarchy in which every employee is displayed alongside their manager's information. Employees without a manager must also appear in the report.

You are required to write a single SQL query using SELF JOIN to generate this employee reporting directory.

### Requirements
1. Display `emp_id`, `employee_name` (`e.emp_name`), `employee_salary` (`e.salary`), `department` (`e.department`), and `employee_city` (`e.city`).
2. Display `manager_id` (`m.emp_id`), `manager_name` (`m.emp_name`), `manager_salary` (`m.salary`), and `manager_city` (`m.city`).
3. Join the `employee` table with itself using appropriate table aliases (`FROM employee e LEFT JOIN employee m ON e.manager_id = m.emp_id`).
4. Use `LEFT JOIN` to ensure that every employee appears in the result, including top-level managers without managers.
5. Employees without managers must have `NULL` values in their manager-related columns.
6. Sort records by `emp_id` in ascending order (`ORDER BY e.emp_id ASC`).

### Acceptance Criteria (10 Checks)
- Exactly 8 employees must appear.
- Aman must appear in the result with manager-related columns as `NULL`.
- Priya and Rohit must show Aman as their manager.
- Neha and Karan must show Priya as their manager.
- Simran and Arjun must show Rohit as their manager.
- Pooja must show Simran as her manager.
- Results must be sorted by `emp_id` ascending."""
    },
    {
        "id": 23,
        "title": "Employee and Manager Salary Comparison System",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "SELF JOIN & CASE",
        "sql": SOLUTIONS[23],
        "description": """The HR department of an organization wants to conduct a salary analysis to understand the compensation difference between employees and their direct managers.

Management wants to identify employees who earn less than their managers, employees who earn more than their managers, and employees who receive exactly the same salary as their managers.

The organization stores both employee and manager information in a single table. Therefore, a SELF JOIN is required to compare the salary of an employee with the salary of another employee who manages them.

In addition to comparing salaries, management wants to calculate the exact salary difference between each employee and their manager.

Write a single SQL query to generate this salary comparison report.

### Requirements
1. Retrieve `emp_id` and `employee_name` (`e.emp_name`).
2. Display the employee's salary (`e.salary AS employee_salary`).
3. Display the direct manager's name (`m.emp_name AS manager_name`) and salary (`m.salary AS manager_salary`).
4. Calculate the salary difference using: `e.salary - m.salary AS salary_difference`.
5. Use `CASE` to classify employees into the following categories:
   - `employee_salary > manager_salary`: `'Higher than manager'`
   - `employee_salary < manager_salary`: `'Lower than manager'`
   - `employee_salary = manager_salary`: `'Equal to manager'`
   Alias as `salary_comparison`.
6. Use `INNER JOIN` because employees without a manager (e.g. Aman) cannot be compared.
7. Sort the result using `emp_id` in ascending order (`ORDER BY e.emp_id ASC`).

### Acceptance Criteria (10 Checks)
- Exactly 7 employees must be returned (Aman excluded).
- Priya has a salary difference of -20000 ('Lower than manager').
- Simran has a salary difference of +10000 ('Higher than manager').
- Correct CASE classification for all employees.
- Results sorted by `emp_id` ascending."""
    },
    {
        "id": 24,
        "title": "Direct Reporting and Same-City Manager Relationship Analysis",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "SELF JOIN & OR Logic",
        "sql": SOLUTIONS[24],
        "description": """The management team wants to analyze reporting relationships within the organization to understand how employees are distributed across different cities.

The company wants to identify two specific groups of employees:
- Employees who directly report to the top-level manager, Aman.
- Employees who work in the same city as their respective manager.

Some employees may satisfy both conditions. For example, an employee might report directly to Aman and also work in the same city as him.

Write a single SQL query using SELF JOIN to identify employees who satisfy at least one of these conditions.

### Requirements
1. Display `emp_id`, `employee_name` (`e.emp_name`), `manager_name` (`m.emp_name`), `employee_city` (`e.city`), and `manager_city` (`m.city`).
2. Include employees who directly report to Aman OR live in the same city as their manager (`m.emp_name = 'Aman' OR e.city = m.city`).
3. Use `CASE` to classify the reason for selection (`selection_reason`):
   - Reports to Aman and lives in the same city: `'Direct report to Aman and same city as manager'`
   - Reports directly to Aman only: `'Direct report to Aman'`
   - Lives in the same city as manager only: `'Same city as manager'`
4. Employees satisfying both conditions must appear only once.
5. Employees without managers must be excluded.
6. Sort records by `emp_id` in ascending order.

### Acceptance Criteria (10 Checks)
- Exactly 5 employees returned (Priya, Rohit, Neha, Arjun, Pooja).
- Rohit receives 'Direct report to Aman and same city as manager'.
- Priya receives 'Direct report to Aman'.
- Neha, Arjun, Pooja receive 'Same city as manager'.
- Aman must not appear."""
    },
    {
        "id": 25,
        "title": "Find Unique Employee Pairs Working in the Same Department",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "SELF JOIN & Pair Combinations",
        "sql": SOLUTIONS[25],
        "description": """A company wants to organize department-wise collaboration sessions to encourage employees to work together on common activities.

The HR department wants to identify every possible pair of employees belonging to the same department.

However, the report must avoid duplicate combinations. For example, if Aman and Priya belong to the same department, the pair should appear only once as Aman–Priya. The reverse combination, Priya–Aman, must not appear. Additionally, no employee should be paired with themselves.

Write a single SQL query using SELF JOIN to generate all unique employee pairs working in the same department.

### Requirements
1. Display `employee1_id` (`e1.emp_id`) and `employee1` (`e1.emp_name`).
2. Display `employee1_salary` (`e1.salary`).
3. Display `employee2_id` (`e2.emp_id`) and `employee2` (`e2.emp_name`).
4. Display `employee2_salary` (`e2.salary`).
5. Display `department` (`e1.department`).
6. Match employees whose department values are equal (`e1.department = e2.department`).
7. Use the condition `e1.emp_id < e2.emp_id` to prevent duplicate reverse pairs and self-pairing.
8. Sort final output by `department` ASC, followed by `employee1_id` ASC, and `employee2_id` ASC.

### Acceptance Criteria (10 Checks)
- Exactly 8 unique pairs returned.
- IT produces exactly 6 pairs.
- HR produces exactly 1 pair (Neha and Karan).
- Finance produces exactly 1 pair (Simran and Arjun).
- No self-pairs or reverse duplicates."""
    },
    {
        "id": 26,
        "title": "Employees Earning More Than Their Manager's Team Average",
        "difficulty": "Hard",
        "points": 100,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "Correlated Subquery & Team Benchmarks",
        "sql": SOLUTIONS[26],
        "description": """The compensation analytics department of an organization wants to identify employees who earn more than the average salary of employees reporting to the same manager.

Management wants to evaluate salary distribution within each manager's team rather than comparing salaries across the entire organization.

For every employee who has a manager, the system must calculate the average salary of all employees who report directly to that same manager. The current employee is included in that manager's direct-report group.

An employee should appear in the final result only when their salary is strictly greater than the calculated team average.

Write a single SQL query using a correlated subquery to generate this report.

### Requirements
1. Display `emp_id`, `employee_name` (`e.emp_name`), and `employee_salary` (`e.salary`).
2. Display `manager_id` (`m.emp_id`) and `manager_name` (`m.emp_name`).
3. Calculate `manager_direct_reports_avg_salary` using a correlated subquery that averages salaries of employees sharing `e.manager_id`. Round to 2 decimal places.
4. Compare `e.salary > (SELECT AVG(sub.salary) FROM employee sub WHERE sub.manager_id = e.manager_id)`.
5. Return only employees whose salaries are strictly greater than their manager's team average.
6. Exclude top-level managers with `manager_id IS NULL`.
7. Sort output by `emp_id` in ascending order.

### Acceptance Criteria (10 Checks)
- Exactly 3 employees returned: Priya (₹70,000 vs ₹67,500), Neha (₹60,000 vs ₹57,500), Simran (₹75,000 vs ₹62,500).
- Employees earning less than or equal to team average (Rohit, Karan, Arjun, Pooja) excluded.
- Top-level manager Aman excluded."""
    },
    {
        "id": 27,
        "title": "Generate the Complete Employee–Project Combination Matrix",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "CROSS JOIN & Cartesian Product",
        "sql": SOLUTIONS[27],
        "description": """A software development company has several employees and multiple ongoing projects. The project management department wants to create a project planning matrix to examine every possible employee-project assignment.

At the initial planning stage, the company does not want to apply any restrictions based on department, city, salary or employee experience. Every employee must therefore be paired with every available project.

You are provided with two tables:
- `employee`: Contains employee information (ID, name, department, city).
- `project`: Contains project identification, name and location.

Write a single SQL query using CROSS JOIN to generate every possible employee-project combination.

In addition to generating the complete matrix, the total number of possible combinations must be displayed alongside every result row.

### Requirements
1. Display `emp_id`, `employee_name` (`e.emp_name`), and `department`.
2. Display `project_id`, `project_name`, and `project_location` (`p.location`).
3. Generate all combinations using `CROSS JOIN`.
4. Calculate total combinations (e.g. `(SELECT COUNT(*) FROM employee) * (SELECT COUNT(*) FROM project) AS total_combinations`).
5. Every result row must contain the total combination count (32).
6. Sort results by `emp_id` ASC and `project_id` ASC.

### Acceptance Criteria (10 Checks)
- Exactly 32 records returned (8 employees × 4 projects = 32).
- Every row contains total_combinations = 32.
- Every employee paired with all 4 projects.
- Results sorted by emp_id and project_id ascending."""
    },
    {
        "id": 28,
        "title": "IT Department Project Allocation and Location Compatibility Matrix",
        "difficulty": "Medium",
        "points": 50,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "CROSS JOIN & Location Matching",
        "sql": SOLUTIONS[28],
        "description": """A software development organization has decided to create a centralized project allocation planning system specifically for its Information Technology (IT) department.

The project management team wants to examine how every IT employee can potentially be assigned to the organization's available projects.

However, the team also wants to understand whether an employee's current city matches the location of a particular project.

The organization does not want to remove projects located in different cities. Instead, it wants to display every possible employee-project combination and classify each combination according to its location compatibility.

### Requirements
1. Consider only employees belonging to the IT department (`e.department = 'IT'`).
2. Display `emp_id`, `employee_name` (`e.emp_name`), and `employee_city` (`e.city`).
3. Display `project_id`, `project_name`, and `project_location` (`p.location`).
4. Use `CROSS JOIN` to generate every possible combination between IT employees and projects.
5. Use `CASE` to create `location_status`:
   - `e.city = p.location`: `'Location Match'`
   - Different cities: `'Different Location'`
6. Do not exclude mismatched combinations.
7. Sort by `emp_id` ASC and `project_id` ASC.

### Acceptance Criteria (10 Checks)
- Exactly 16 records returned (4 IT employees × 4 projects = 16).
- 6 records classified as 'Location Match'.
- 10 records classified as 'Different Location'.
- Non-IT employees must not appear."""
    },
    {
        "id": 29,
        "title": "Find Projects Located in the Same City as Each Employee",
        "difficulty": "Hard",
        "points": 100,
        "track": "SQL",
        "category": "SQL",
        "subtopic": "CROSS JOIN & City Filtering",
        "sql": SOLUTIONS[29],
        "description": """A company wants to develop a location-based project recommendation system that identifies projects suitable for employees based on their current city.

The organization wants to identify employees who can potentially be associated with projects located in their own city.

Unlike the previous problem, this time the company does not want to display mismatched combinations. Only employee-project combinations where the employee's city exactly matches the project's location should be included.

Since one city may contain multiple projects, an employee may be matched with more than one project.

Write a single SQL query using CROSS JOIN and WHERE to generate the location-based project recommendation report.

### Requirements
1. Display `emp_id`, `employee_name` (`e.emp_name`), and `employee_city` (`e.city`).
2. Display `project_id`, `project_name`, and `project_location` (`p.location`).
3. Generate candidate combinations using `CROSS JOIN`.
4. Filter combinations where employee city equals project location (`e.city = p.location`).
5. Employees in Delhi match both Delhi projects (Banking System & AI Chatbot).
6. Employees in Noida match Noida projects (E-Commerce).
7. Employees in Gurgaon match Gurgaon projects (Hospital Management).
8. Sort final result by `emp_id` ASC and `project_id` ASC.

### Acceptance Criteria (10 Checks)
- Exactly 12 matching combinations returned.
- Delhi employees (4) × 2 projects = 8 matches.
- Noida employees (2) × 1 project = 2 matches.
- Gurgaon employees (2) × 1 project = 2 matches.
- No mismatched city combinations."""
    }
]


def append_questions():
    with open("data/questions.json", "r") as f:
        existing_questions = json.load(f)

    # Filter out existing 22-29 if any
    base_questions = [q for q in existing_questions if q["id"] < 22]

    new_questions = []
    datasets = [
        ("Standard Employee-Project Dataset (8 Employees, 4 Projects)", DEFAULT_DATA_SQL, True),
        ("Dataset 2: Alternative Hierarchy & Project Count", DATA_SET_2, False),
        ("Dataset 3: Boundary Hierarchy & Multiple Projects per City", DATA_SET_3, False)
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
            "tags": [qdef["subtopic"], "SELF JOIN", "CROSS JOIN", "SQL", "MySQL"],
            "description": qdef["description"],
            "type": "sql",
            "tableSchema": SCHEMA_SQL,
            "testData": DEFAULT_DATA_SQL,
            "sampleInput": "SELECT * FROM employee;\nSELECT * FROM project;",
            "sampleOutput": sample_output_ascii,
            "boilerplate": f"-- Write your MySQL query below\n-- Schema: employee (emp_id, emp_name, manager_id, department, salary, city)\n--         project (project_id, project_name, location)\n\n",
            "testCases": test_cases
        }
        new_questions.append(q_obj)

    final_questions = base_questions + new_questions

    with open("data/questions.json", "w") as f:
        json.dump(final_questions, f, indent=2)

    print(f"✅ Successfully wrote {len(final_questions)} questions to data/questions.json!")
    print(f"Added {len(new_questions)} SELF JOIN & CROSS JOIN SQL Questions (Q22-Q29).")


if __name__ == "__main__":
    append_questions()
