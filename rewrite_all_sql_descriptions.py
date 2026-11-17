import json

REWRITTEN_DESCRIPTIONS = {}

# ─────────────────────────────────────────────────────────────────────────────
# Group 1: Student Database (Q9 - Q13)
# ─────────────────────────────────────────────────────────────────────────────

REWRITTEN_DESCRIPTIONS[9] = """### **Problem Description**
Write an SQL query to retrieve students from the `student` table who satisfy specific demographic, score, and name pattern criteria.

### **Table Schema: `student`**
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Unique identifier (Primary Key) |
| `name` | VARCHAR(50) | Student's name |
| `age` | INT | Age in years |
| `gender` | CHAR(1) | `'M'` or `'F'` |
| `city` | VARCHAR(50) | City of residence |
| `email` | VARCHAR(100) | Unique email address |
| `marks` | INT | Marks scored (0–100) |
| `dob` | DATE | Date of birth (`YYYY-MM-DD`) |

---

### **Requirements**
1. **Score Filter:** `marks` must be between `60` and `95` (inclusive).
2. **City Filter:** `city` must be `'Delhi'`, `'Meerut'`, or `'Noida'`.
3. **City Exclusion:** `city` must **not** be `'Panipat'`.
4. **Name Pattern:** Student name must satisfy **at least one** of these patterns:
   - Starts with `'A'` (`name LIKE 'A%'`)
   - Starts with `'R'` (`name LIKE 'R%'`)
   - Ends with `'a'` (`name LIKE '%a'`)
   - Contains substring `'it'` (`name LIKE '%it%'`)
5. **Gender-City Exclusion:** Exclude female students from Meerut (`NOT (gender = 'F' AND city = 'Meerut')`).
6. **Sorting:** Sort results by `marks` in **descending** order. If marks are equal, sort alphabetically by `name` **ascending**.

---

### **Expected Output Columns**
| Column Name | Type | Description |
|---|---|---|
| `student_id` | INT | Student ID |
| `name` | VARCHAR | Student name |
| `city` | VARCHAR | Residence city |
| `age` | INT | Student age |
| `gender` | CHAR | Gender (`'M'`/`'F'`) |
| `marks` | INT | Marks scored |
| `dob` | DATE | Date of birth |
"""

REWRITTEN_DESCRIPTIONS[10] = """### **Problem Description**
Write an SQL query to find the **top 3 highest-scoring students** from the specified NCR cities.

### **Table Schema: `student`**
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Primary Key |
| `name` | VARCHAR(50) | Student's name |
| `age` | INT | Age in years |
| `gender` | CHAR(1) | `'M'` or `'F'` |
| `city` | VARCHAR(50) | City of residence |
| `marks` | INT | Marks scored (0–100) |
| `dob` | DATE | Date of birth |

---

### **Requirements**
1. **Score Filter:** `marks` must be between `75` and `100` (inclusive).
2. **City Filter:** `city` must be in `'Delhi'`, `'Meerut'`, `'Noida'`, or `'Panipat'`.
3. **Sorting:** Order by `marks` **descending**. If marks are tied, order by `age` **ascending**.
4. **Limit:** Return only the top **3** records (`LIMIT 3`).

---

### **Expected Output Columns**
| Column Name | Alias / Source | Description |
|---|---|---|
| `student_id` | `student_id` | Student ID |
| `student_name` | `name AS student_name` | Student's full name |
| `city` | `city` | City of residence |
| `student_marks` | `marks AS student_marks` | Score achieved |
| `age` | `age` | Age in years |
"""

REWRITTEN_DESCRIPTIONS[11] = """### **Problem Description**
Write an SQL query to generate an aggregate academic performance report for each qualifying city.

### **Table Schema: `student`**
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Primary Key |
| `name` | VARCHAR(50) | Student's name |
| `city` | VARCHAR(50) | City of residence |
| `marks` | INT | Marks scored (0–100) |

---

### **Requirements**
1. **Pre-aggregation Filter:** Consider only students with `marks` between `50` and `100` (inclusive).
2. **Grouping:** Group records by `city`.
3. **Aggregates:**
   - `total_students`: Total number of qualifying students in the city (`COUNT(*)`).
   - `total_marks`: Total sum of marks (`SUM(marks)`).
   - `average_marks`: Average score rounded to **2** decimal places (`ROUND(AVG(marks), 2)`).
   - `highest_marks`: Maximum score in the city (`MAX(marks)`).
   - `lowest_marks`: Minimum score in the city (`MIN(marks)`).
4. **Group Filter (`HAVING`):**
   - The city must have at least **2** students (`COUNT(*) >= 2`).
   - The city's average marks must be strictly greater than **75** (`AVG(marks) > 75`).
5. **Sorting:** Sort results by `average_marks` in **descending** order.

---

### **Expected Output Columns**
| Column Name | Calculation / Alias |
|---|---|
| `city` | City name |
| `total_students` | `COUNT(*)` |
| `total_marks` | `SUM(marks)` |
| `average_marks` | `ROUND(AVG(marks), 2)` |
| `highest_marks` | `MAX(marks)` |
| `lowest_marks` | `MIN(marks)` |
"""

REWRITTEN_DESCRIPTIONS[12] = """### **Problem Description**
Write an SQL query to analyze student birth demographics grouped by birth year and birth month.

### **Table Schema: `student`**
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Primary Key |
| `name` | VARCHAR(50) | Student's name |
| `dob` | DATE | Date of birth (`YYYY-MM-DD`) |

---

### **Requirements**
1. **Filtering:** Include students who meet **either** condition:
   - Born between `'2003-01-01'` and `'2005-12-31'` (inclusive), **OR**
   - Born in October (`MONTH(dob) = 10`).
2. **Date Extraction:**
   - `birth_year`: Extract 4-digit year (`YEAR(dob)`).
   - `birth_month_number`: Extract month number `1`–`12` (`MONTH(dob)`).
   - `birth_month_name`: Full month name, e.g. `'October'` (`MONTHNAME(dob)`).
   - `total_students`: Count of students in that cohort (`COUNT(*)`).
3. **Grouping:** Group by `birth_year`, `birth_month_number`, and `birth_month_name`.
4. **Filter:** Include groups with at least 1 student (`HAVING total_students >= 1`).
5. **Sorting:** Sort by `birth_year` **ascending**, then `birth_month_number` **ascending**.

---

### **Expected Output Columns**
| Column Name | Calculation / Alias | Description |
|---|---|---|
| `birth_year` | `YEAR(dob)` | Year of birth (e.g. `2004`) |
| `birth_month_number` | `MONTH(dob)` | Numeric month (`1`–`12`) |
| `birth_month_name` | `MONTHNAME(dob)` | Name of the month |
| `total_students` | `COUNT(*)` | Number of students |
"""

REWRITTEN_DESCRIPTIONS[13] = """### **Problem Description**
Write an SQL query to generate a complete statistical and demographic intelligence report grouped by student gender.

### **Table Schema: `student`**
| Column | Type | Description |
|---|---|---|
| `student_id` | INT | Primary Key |
| `gender` | CHAR(1) | `'M'` or `'F'` |
| `city` | VARCHAR(50) | Residence city |
| `age` | INT | Age in years |
| `marks` | INT | Score (0–100) |

---

### **Requirements**
1. **Grouping:** Group records by `gender`.
2. **Aggregates:**
   - `total_students`: Total students of that gender (`COUNT(*)`).
   - `total_marks`: Sum of marks (`SUM(marks)`).
   - `average_marks`: Average marks rounded to 2 decimals (`ROUND(AVG(marks), 2)`).
   - `highest_marks`: Maximum marks (`MAX(marks)`).
   - `lowest_marks`: Minimum marks (`MIN(marks)`).
   - `average_age`: Average age rounded to 2 decimals (`ROUND(AVG(age), 2)`).
   - `unique_cities`: Number of distinct cities (`COUNT(DISTINCT city)`).
   - `unique_ages`: Number of distinct ages (`COUNT(DISTINCT age)`).
   - `unique_marks`: Number of distinct mark values (`COUNT(DISTINCT marks)`).
3. **Sorting:** Sort results by `average_marks` in **descending** order.

---

### **Expected Output Columns**
| Column Name | Calculation |
|---|---|
| `gender` | Gender (`'M'` or `'F'`) |
| `total_students` | `COUNT(*)` |
| `total_marks` | `SUM(marks)` |
| `average_marks` | `ROUND(AVG(marks), 2)` |
| `highest_marks` | `MAX(marks)` |
| `lowest_marks` | `MIN(marks)` |
| `average_age` | `ROUND(AVG(age), 2)` |
| `unique_cities` | `COUNT(DISTINCT city)` |
| `unique_ages` | `COUNT(DISTINCT age)` |
| `unique_marks` | `COUNT(DISTINCT marks)` |
"""

# ─────────────────────────────────────────────────────────────────────────────
# Group 2: Employee & Department Database (Q14 - Q21)
# ─────────────────────────────────────────────────────────────────────────────

REWRITTEN_DESCRIPTIONS[14] = """### **Problem Description**
Write an SQL query to join `employee` and `department` tables and retrieve employees eligible for leadership and promotion consideration.

### **Table Schemas**
#### `employee`
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `age` | INT | Age in years |
| `gender` | CHAR(1) | `'M'` or `'F'` |
| `dept_id` | INT | Foreign key referencing `department.dept_id` |
| `city` | VARCHAR(50) | City of residence |
| `salary` | INT | Monthly salary |
| `performance` | INT | Performance rating (0–100) |
| `joining_date` | DATE | Date of joining |

#### `department`
| Column | Type | Description |
|---|---|---|
| `dept_id` | INT | Primary Key |
| `dept_name` | VARCHAR(50) | Department name |
| `location` | VARCHAR(50) | Department office location |

---

### **Requirements**
1. **Join:** Perform an `INNER JOIN` between `employee e` and `department d` ON `e.dept_id = d.dept_id`.
2. **Salary & Performance Filter:**
   - `salary` between `55000` and `80000` (inclusive).
   - `performance` score $\ge 75$.
3. **Department & Location Filter:**
   - Department must be `'IT'`, `'HR'`, `'Finance'`, or `'Marketing'`.
   - Employee `city` must be `'Delhi'` or `'Noida'`, and must **not** be `'Gurgaon'`.
4. **Name Pattern:** Employee name must start with `'A'` or `'R'`, end with `'a'`, or contain `'it'`.
5. **Exclusion:** Exclude male employees working in HR (`NOT (gender = 'M' AND dept_name = 'HR')`).
6. **Sorting:** Sort by `salary DESC`, then `performance DESC`, then `emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Alias |
|---|---|
| `emp_id` | `e.emp_id` |
| `employee_name` | `e.emp_name` |
| `department` | `d.dept_name` |
| `age` | `e.age` |
| `gender` | `e.gender` |
| `city` | `e.city` |
| `salary` | `e.salary` |
| `performance` | `e.performance` |
| `joining_date` | `e.joining_date` |
"""

REWRITTEN_DESCRIPTIONS[15] = """### **Problem Description**
Write an SQL query to select the **top 5 performers** across target departments for quarterly incentive awards.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `dept_id` | INT | Department ID |
| `salary` | INT | Monthly salary |
| `performance` | INT | Rating score (0–100) |
| `gender` | CHAR(1) | `'M'` or `'F'` |

---

### **Requirements**
1. **Performance Filter:** `performance` must be between `80` and `100` (inclusive).
2. **Salary Filter:** `salary` must be between `50000` and `85000` (inclusive).
3. **Department Filter:** `dept_id` must be in `(1, 2, 3, 4)`.
4. **Sorting:** Order by `performance_score` **descending**, then `employee_salary` **descending**, then `emp_id` **ascending**.
5. **Limit:** Return exactly the top **5** records (`LIMIT 5`).

---

### **Expected Output Columns**
| Column Name | Alias / Source | Description |
|---|---|---|
| `emp_id` | `emp_id` | Employee ID |
| `employee_name` | `emp_name AS employee_name` | Employee name |
| `dept_id` | `dept_id` | Department ID |
| `employee_salary` | `salary AS employee_salary` | Monthly salary |
| `performance_score` | `performance AS performance_score` | Rating score |
| `gender` | `gender` | Gender (`'M'`/`'F'`) |
"""

REWRITTEN_DESCRIPTIONS[16] = """### **Problem Description**
Write an SQL query to calculate overall corporate payroll and compensation statistics.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `salary` | INT | Monthly salary |
| `performance` | INT | Performance rating |
| `gender` | CHAR(1) | `'M'` or `'F'` |

---

### **Requirements**
Calculate the following single-row aggregate metrics across all employees:
1. `total_employees`: Total headcount (`COUNT(*)`).
2. `total_salary`: Total payroll expenditure (`SUM(salary)`).
3. `average_salary`: Mean salary rounded to 2 decimal places (`ROUND(AVG(salary), 2)`).
4. `highest_salary`: Maximum salary (`MAX(salary)`).
5. `lowest_salary`: Minimum salary (`MIN(salary)`).
6. `salary_difference`: Gap between highest and lowest salary (`MAX(salary) - MIN(salary)`).
7. `female_total_salary`: Total salary paid to female employees (`COALESCE(SUM(CASE WHEN gender = 'F' THEN salary ELSE 0 END), 0)`).
8. `high_performer_avg_salary`: Average salary of employees with `performance >= 85`, rounded to 2 decimals (`ROUND(AVG(CASE WHEN performance >= 85 THEN salary ELSE NULL END), 2)`).
9. `average_performance`: Mean performance rating rounded to 2 decimals (`ROUND(AVG(performance), 2)`).

---

### **Expected Output Columns**
| Column Name | Description |
|---|---|
| `total_employees` | Total employee count |
| `total_salary` | Total payroll sum |
| `average_salary` | Overall average salary |
| `highest_salary` | Peak salary |
| `lowest_salary` | Minimum salary |
| `salary_difference` | Max salary minus Min salary |
| `female_total_salary` | Total female payroll |
| `high_performer_avg_salary` | Avg salary of performance $\ge 85$ |
| `average_performance` | Overall mean performance |
"""

REWRITTEN_DESCRIPTIONS[17] = """### **Problem Description**
Write an SQL query to produce an executive department dashboard showing headcount, gender diversity, salary, performance metrics, and tier classification.

### **Table Schemas**
- `department (dept_id, dept_name, location)`
- `employee (emp_id, emp_name, dept_id, salary, performance, gender)`

---

### **Requirements**
1. **Join:** `department d INNER JOIN employee e ON d.dept_id = e.dept_id`.
2. **Grouping:** Group by `d.dept_id` and `d.dept_name`.
3. **Aggregates:**
   - `total_employees`: Count of employees (`COUNT(e.emp_id)`).
   - `male_count`: Count of male employees (`SUM(CASE WHEN e.gender = 'M' THEN 1 ELSE 0 END)`).
   - `female_count`: Count of female employees (`SUM(CASE WHEN e.gender = 'F' THEN 1 ELSE 0 END)`).
   - `average_salary`: `ROUND(AVG(e.salary), 2)`.
   - `average_performance`: `ROUND(AVG(e.performance), 2)`.
   - `highest_salary`: `MAX(e.salary)`.
   - `highest_performance`: `MAX(e.performance)`.
   - `high_performers`: Count of employees with `performance >= 85`.
   - `department_category`:
     - `'Tier 1'` if average performance $\ge 88$
     - `'Tier 2'` if average performance $\ge 80$ (and $< 88$)
     - `'Tier 3'` otherwise
4. **Group Filter (`HAVING`):** Include only departments having at least **2** employees and an average salary $\ge 60000$.
5. **Sorting:** Sort by `average_salary DESC`, then `d.dept_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Calculation |
|---|---|
| `dept_id` | `d.dept_id` |
| `department` | `d.dept_name` |
| `total_employees` | Headcount |
| `male_count` | Number of males |
| `female_count` | Number of females |
| `average_salary` | Department average salary |
| `average_performance` | Department average performance |
| `highest_salary` | Highest salary in department |
| `highest_performance` | Highest performance in department |
| `high_performers` | Count of performance $\ge 85$ |
| `department_category` | `'Tier 1'` / `'Tier 2'` / `'Tier 3'` |
"""

REWRITTEN_DESCRIPTIONS[18] = """### **Problem Description**
Write an SQL query using a `LEFT JOIN` to list all departments alongside their employees, ensuring that departments with **zero employees** are still included.

### **Table Schemas**
- `department (dept_id, dept_name, location)`
- `employee (emp_id, emp_name, dept_id, salary)`

---

### **Requirements**
1. **Join:** Perform a `LEFT JOIN` from `department d` to `employee e` ON `d.dept_id = e.dept_id`.
2. **Unstaffed Retention:** Any department without staff (e.g., `'Research'`) must appear with `NULL` for employee fields.
3. **Sorting:** Sort by `d.dept_id ASC`, then `e.salary DESC`, then `e.emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Alias / Source | Description |
|---|---|---|
| `dept_id` | `d.dept_id` | Department ID |
| `department` | `d.dept_name` | Department name |
| `department_location` | `d.location` | Office city |
| `emp_id` | `e.emp_id` | Employee ID (`NULL` if unstaffed) |
| `employee_name` | `e.emp_name` | Employee name (`NULL` if unstaffed) |
| `employee_salary` | `e.salary` | Monthly salary (`NULL` if unstaffed) |
"""

REWRITTEN_DESCRIPTIONS[19] = """### **Problem Description**
Write an SQL query to perform a department staffing and vacancy audit, classifying every department as Vacant, Understaffed, or Properly Staffed.

### **Table Schemas**
- `department (dept_id, dept_name, location)`
- `employee (emp_id, emp_name, dept_id, salary, performance)`

---

### **Requirements**
1. **Join:** Use an outer join (`department d LEFT JOIN employee e ON d.dept_id = e.dept_id`) so all departments appear.
2. **Grouping:** Group by `d.dept_id`, `d.dept_name`, and `d.location`.
3. **Aggregates & NULL Handling:**
   - `total_employees`: `COUNT(e.emp_id)`.
   - `total_salary`: `COALESCE(SUM(e.salary), 0)`.
   - `average_salary`: `ROUND(COALESCE(AVG(e.salary), 0), 2)`.
   - `highest_performance`: `COALESCE(MAX(e.performance), 0)`.
   - `staffing_status`:
     - `'Vacant'` if `total_employees = 0`
     - `'Understaffed'` if `total_employees` is 1 or 2
     - `'Properly Staffed'` if `total_employees >= 3`
4. **Sorting:** Sort by `total_employees DESC`, then `d.dept_id ASC`.

---

### **Expected Output Columns**
| Column Name | Calculation / Description |
|---|---|
| `dept_id` | `d.dept_id` |
| `department` | `d.dept_name` |
| `location` | `d.location` |
| `total_employees` | Headcount |
| `total_salary` | Total payroll (`0` if vacant) |
| `average_salary` | Average salary (`0.00` if vacant) |
| `highest_performance` | Top performance score (`0` if vacant) |
| `staffing_status` | `'Vacant'` / `'Understaffed'` / `'Properly Staffed'` |
"""

REWRITTEN_DESCRIPTIONS[20] = """### **Problem Description**
Write an SQL query to audit departmental workforce diversity and performance distribution, returning departments that achieve high benchmarks in both areas.

### **Table Schemas**
- `department (dept_id, dept_name, location)`
- `employee (emp_id, emp_name, dept_id, gender, salary, performance)`

---

### **Requirements**
1. **Join:** `department d INNER JOIN employee e ON d.dept_id = e.dept_id`.
2. **Grouping:** Group by `d.dept_name`.
3. **Aggregates:**
   - `total_employees`: `COUNT(e.emp_id)`.
   - `male_count`: Males count (`gender = 'M'`).
   - `female_count`: Females count (`gender = 'F'`).
   - `high_performers`: `performance >= 85`.
   - `low_performers`: `performance < 75`.
   - `excellent_count`: `performance >= 90`.
   - `good_count`: `performance BETWEEN 80 AND 89`.
   - `average_count`: `performance BETWEEN 70 AND 79`.
   - `poor_count`: `performance < 70`.
   - `high_salary_count`: `salary >= 70000`.
   - `low_salary_count`: `salary < 60000`.
   - `high_performer_percentage`: `ROUND(high_performers * 100.0 / total_employees, 2)`.
   - `female_percentage`: `ROUND(female_count * 100.0 / total_employees, 2)`.
4. **Group Filter (`HAVING`):**
   - `high_performer_percentage >= 30.0`
   - `female_percentage >= 30.0`
5. **Sorting:** Sort by `high_performer_percentage DESC`, then `d.dept_name ASC`.

---

### **Expected Output Columns**
`department`, `total_employees`, `male_count`, `female_count`, `high_performers`, `low_performers`, `excellent_count`, `good_count`, `average_count`, `poor_count`, `high_salary_count`, `low_salary_count`, `high_performer_percentage`, `female_percentage`.
"""

REWRITTEN_DESCRIPTIONS[21] = """### **Problem Description**
Write an SQL query to analyze yearly employee recruitment trends and cohort statistics from 2019 onward.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `dept_id` | INT | Department ID |
| `performance` | INT | Rating score |
| `joining_date` | DATE | Date hired (`YYYY-MM-DD`) |

---

### **Requirements**
1. **Filter:** Consider only employees hired in or after 2019 (`YEAR(joining_date) >= 2019`).
2. **Grouping:** Group by `YEAR(joining_date)`.
3. **Aggregates:**
   - `joining_year`: 4-digit hiring year (`YEAR(joining_date)`).
   - `total_employees`: Total hired that year (`COUNT(*)`).
   - `average_performance`: Mean performance rounded to 2 decimals (`ROUND(AVG(performance), 2)`).
   - `earliest_joining_date`: First hire date of the year (`MIN(joining_date)`).
   - `latest_joining_date`: Last hire date of the year (`MAX(joining_date)`).
   - `departments_represented`: Distinct departments hired into (`COUNT(DISTINCT dept_id)`).
4. **Group Filter (`HAVING`):**
   - Total hired in year $\ge 2$ (`COUNT(*) >= 2`).
   - Average performance for the cohort $\ge 75$ (`AVG(performance) >= 75`).
5. **Sorting:** Sort chronologically by `joining_year ASC`.

---

### **Expected Output Columns**
| Column Name | Calculation |
|---|---|
| `joining_year` | `YEAR(joining_date)` |
| `total_employees` | `COUNT(*)` |
| `average_performance` | `ROUND(AVG(performance), 2)` |
| `earliest_joining_date` | `MIN(joining_date)` |
| `latest_joining_date` | `MAX(joining_date)` |
| `departments_represented` | `COUNT(DISTINCT dept_id)` |
"""

# ─────────────────────────────────────────────────────────────────────────────
# Group 3: Self JOIN & CROSS JOIN (Q22 - Q29)
# ─────────────────────────────────────────────────────────────────────────────

REWRITTEN_DESCRIPTIONS[22] = """### **Problem Description**
Write an SQL query using a `LEFT JOIN` to map each employee to their direct manager. Employees without a manager (e.g. CEO) must be included.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `manager_id` | INT | References `employee.emp_id` (`NULL` if no manager) |
| `department` | VARCHAR(50) | Department name |
| `salary` | INT | Monthly salary |
| `city` | VARCHAR(50) | Office city |

---

### **Requirements**
1. **Join:** `employee e LEFT JOIN employee m ON e.manager_id = m.emp_id`.
2. **NULL Handling:** If an employee has no manager (`manager_id IS NULL`), display `'No Manager'` for `manager_name`.
3. **Sorting:** Sort results by `e.emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Alias | Description |
|---|---|---|
| `emp_id` | `e.emp_id` | Employee ID |
| `employee_name` | `e.emp_name` | Employee name |
| `employee_salary` | `e.salary` | Employee salary |
| `department` | `e.department` | Department |
| `employee_city` | `e.city` | Employee city |
| `manager_id` | `e.manager_id` | Manager ID |
| `manager_name` | `COALESCE(m.emp_name, 'No Manager')` | Manager name |
| `manager_salary` | `m.salary` | Manager salary |
| `manager_city` | `m.city` | Manager city |
"""

REWRITTEN_DESCRIPTIONS[23] = """### **Problem Description**
Write an SQL query using a `SELF JOIN` to compare the salary of each employee against their direct manager's salary.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `manager_id` | INT | Manager's `emp_id` |
| `salary` | INT | Monthly salary |

---

### **Requirements**
1. **Join:** `employee e INNER JOIN employee m ON e.manager_id = m.emp_id` (only evaluate employees who have a manager).
2. **Calculations:**
   - `salary_difference`: `e.salary - m.salary`.
   - `salary_comparison`:
     - `'Higher than Manager'` if `e.salary > m.salary`
     - `'Equal to Manager'` if `e.salary = m.salary`
     - `'Lower than Manager'` if `e.salary < m.salary`
3. **Sorting:** Sort by `e.salary DESC`, then `e.emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Calculation / Source |
|---|---|
| `emp_id` | `e.emp_id` |
| `employee_name` | `e.emp_name` |
| `employee_salary` | `e.salary` |
| `manager_name` | `m.emp_name` |
| `manager_salary` | `m.salary` |
| `salary_difference` | `e.salary - m.salary` |
| `salary_comparison` | `'Higher than Manager'` / `'Equal to Manager'` / `'Lower than Manager'` |
"""

REWRITTEN_DESCRIPTIONS[24] = """### **Problem Description**
Write an SQL query to identify employees who either earn more than their direct manager OR are located in the exact same city as their manager.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `manager_id` | INT | Manager's `emp_id` |
| `salary` | INT | Monthly salary |
| `city` | VARCHAR(50) | City of residence |

---

### **Requirements**
1. **Join:** `employee e INNER JOIN employee m ON e.manager_id = m.emp_id`.
2. **Filter Condition (`OR` Logic):**
   - `e.salary > m.salary` **OR** `e.city = m.city`.
3. **Classification (`selection_reason`):**
   - `'Higher Salary & Same City'` if both conditions hold.
   - `'Higher Salary'` if only salary is greater.
   - `'Same City'` if only city is identical.
4. **Sorting:** Sort results by `e.emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Description |
|---|---|
| `emp_id` | `e.emp_id` |
| `employee_name` | `e.emp_name` |
| `manager_name` | `m.emp_name` |
| `employee_city` | `e.city` |
| `manager_city` | `m.city` |
| `selection_reason` | Reason classification flag |
"""

REWRITTEN_DESCRIPTIONS[25] = """### **Problem Description**
Write an SQL query to generate all unique pairs of employees working in the same department, preventing self-pairings and mirror duplicates.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `department` | VARCHAR(50) | Department |
| `salary` | INT | Monthly salary |

---

### **Requirements**
1. **Join Condition:** `employee e1 INNER JOIN employee e2 ON e1.department = e2.department AND e1.emp_id < e2.emp_id`.
   - `e1.emp_id < e2.emp_id` guarantees each pair appears exactly once and prevents self-matching.
2. **Sorting:** Sort by `e1.department ASC`, then `e1.emp_id ASC`, then `e2.emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source | Description |
|---|---|---|
| `employee1_id` | `e1.emp_id` | First employee ID |
| `employee1` | `e1.emp_name` | First employee name |
| `employee1_salary` | `e1.salary` | First employee salary |
| `employee2_id` | `e2.emp_id` | Second employee ID |
| `employee2` | `e2.emp_name` | Second employee name |
| `employee2_salary` | `e2.salary` | Second employee salary |
| `department` | `e1.department` | Shared department |
"""

REWRITTEN_DESCRIPTIONS[26] = """### **Problem Description**
Write an SQL query to identify employees who earn more than the average salary of all direct reports under their manager.

### **Table Schema: `employee`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `manager_id` | INT | Manager's `emp_id` |
| `salary` | INT | Monthly salary |

---

### **Requirements**
1. For every employee with a manager (`e.manager_id IS NOT NULL`), calculate the average salary of all employees reporting to that manager:
   $$\text{team\_avg} = \text{ROUND}(\text{AVG}(salary), 2) \quad \text{grouped by } manager\_id$$
2. **Filter:** Select employees whose salary is strictly greater than their team's average (`e.salary > team_avg`).
3. **Sorting:** Sort by `employee_salary DESC`, then `emp_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Description |
|---|---|
| `emp_id` | `e.emp_id` |
| `employee_name` | `e.emp_name` |
| `employee_salary` | `e.salary` |
| `manager_id` | `e.manager_id` |
| `manager_name` | `m.emp_name` |
| `manager_direct_reports_avg_salary` | Team average rounded to 2 decimals |
"""

REWRITTEN_DESCRIPTIONS[27] = """### **Problem Description**
Write an SQL query using a `CROSS JOIN` to generate the complete Cartesian product matrix between all employees and all projects.

### **Table Schemas**
- `employee (emp_id, emp_name, department)`
- `project (project_id, project_name, location)`

---

### **Requirements**
1. **Join:** Perform a `CROSS JOIN` between `employee e` and `project p`.
2. **Total Count:** Include a column `total_combinations` displaying the total number of combinations across the entire result set using `COUNT(*) OVER()`.
3. **Sorting:** Sort by `e.emp_id ASC`, then `p.project_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source / Alias | Description |
|---|---|---|
| `emp_id` | `e.emp_id` | Employee ID |
| `employee_name` | `e.emp_name` | Employee name |
| `department` | `e.department` | Department |
| `project_id` | `p.project_id` | Project ID |
| `project_name` | `p.project_name` | Project title |
| `project_location` | `p.location` | Project city |
| `total_combinations` | `COUNT(*) OVER()` | Total combinations count (e.g. 32) |
"""

REWRITTEN_DESCRIPTIONS[28] = """### **Problem Description**
Write an SQL query to generate the project allocation matrix for IT department employees, classifying whether each project assignment is Local or Remote.

### **Table Schemas**
- `employee (emp_id, emp_name, department, city)`
- `project (project_id, project_name, location)`

---

### **Requirements**
1. **Filter & Join:** Perform a `CROSS JOIN` between `employee e` and `project p`, filtered for `e.department = 'IT'`.
2. **Location Classification (`location_status`):**
   - `'Local'` if employee's city matches project location (`e.city = p.location`).
   - `'Remote'` otherwise.
3. **Sorting:** Sort by `e.emp_id ASC`, then `p.project_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source | Description |
|---|---|---|
| `emp_id` | `e.emp_id` | IT Employee ID |
| `employee_name` | `e.emp_name` | IT Employee name |
| `employee_city` | `e.city` | Employee residence city |
| `project_id` | `p.project_id` | Project ID |
| `project_name` | `p.project_name` | Project title |
| `project_location` | `p.location` | Project city |
| `location_status` | Classification | `'Local'` or `'Remote'` |
"""

REWRITTEN_DESCRIPTIONS[29] = """### **Problem Description**
Write an SQL query to find all valid employee–project pairings where the employee resides in the **exact same city** as the project location.

### **Table Schemas**
- `employee (emp_id, emp_name, city)`
- `project (project_id, project_name, location)`

---

### **Requirements**
1. **Join Condition:** Match employees and projects on location (`e.city = p.location`).
2. **Sorting:** Sort by `e.emp_id ASC`, then `p.project_id ASC`.

---

### **Expected Output Columns**
| Column Name | Source | Description |
|---|---|---|
| `emp_id` | `e.emp_id` | Employee ID |
| `employee_name` | `e.emp_name` | Employee name |
| `employee_city` | `e.city` | Employee city |
| `project_id` | `p.project_id` | Project ID |
| `project_name` | `p.project_name` | Project title |
| `project_location` | `p.location` | Project city (matches employee city) |
"""

# ─────────────────────────────────────────────────────────────────────────────
# Group 4: Window Functions (Q30 - Q37)
# ─────────────────────────────────────────────────────────────────────────────

REWRITTEN_DESCRIPTIONS[30] = """### **Problem Description**
Write an SQL query using ranking and distribution window functions to generate a comprehensive employee compensation and ranking report.

### **Table Schema: `employees`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `department` | VARCHAR(40) | Department |
| `city` | VARCHAR(40) | City |
| `salary` | DECIMAL(12,2) | Salary |
| `joining_date` | DATE | Date hired |

---

### **Requirements**
Calculate the following window metrics:
1. `salary_row_number`: Unique global row sequence ordered by `salary DESC, emp_id ASC`.
2. `salary_rank_global`: Global salary rank with gaps for ties using `RANK() OVER (ORDER BY salary DESC)`.
3. `department_dense_rank`: Rank within department without gaps using `DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)`.
4. `salary_quartile`: Divide all employees into 4 salary groups using `NTILE(4) OVER (ORDER BY salary DESC, emp_id ASC)`.
5. `joining_date_row_number`: Seniority sequence ordered by `joining_date ASC, emp_id ASC`.
6. `top_three_in_department`: `'Yes'` if `department_dense_rank <= 3`, else `'No'`.
7. `second_highest_in_department`: `'Yes'` if `department_dense_rank = 2`, else `'No'`.
8. `percent_rank_in_department`: `ROUND(PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary ASC), 2)`.
9. `cume_dist_in_department`: `ROUND(CUME_DIST() OVER (PARTITION BY department ORDER BY salary ASC), 2)`.
10. `third_highest_salary_in_department`: Value of the 3rd highest salary in the department using `NTH_VALUE(salary, 3)` across the full partition (`ORDER BY salary DESC, emp_id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`). Returns `NULL` if department has fewer than 3 employees.
11. **Sorting:** Sort final output by `salary_row_number ASC`.

---

### **Expected Output Columns**
`emp_id`, `emp_name`, `department`, `salary`, `salary_row_number`, `salary_rank_global`, `department_dense_rank`, `salary_quartile`, `joining_date_row_number`, `top_three_in_department`, `second_highest_in_department`, `percent_rank_in_department`, `cume_dist_in_department`, `third_highest_salary_in_department`.
"""

REWRITTEN_DESCRIPTIONS[31] = """### **Problem Description**
Write an SQL query using aggregate window functions to compare individual employee salaries against departmental benchmarks and running payroll totals.

### **Table Schema: `employees`**
| Column | Type | Description |
|---|---|---|
| `emp_id` | INT | Primary Key |
| `emp_name` | VARCHAR(50) | Employee name |
| `department` | VARCHAR(40) | Department name |
| `salary` | DECIMAL(12,2) | Monthly salary |
| `joining_date` | DATE | Date of joining |

---

### **Requirements**
Calculate the following window metrics partitioned by `department`:
1. `department_avg_salary`: `ROUND(AVG(salary) OVER (PARTITION BY department), 2)`.
2. `department_total_salary`: `SUM(salary) OVER (PARTITION BY department)`.
3. `department_min_salary`: `MIN(salary) OVER (PARTITION BY department)`.
4. `department_max_salary`: `MAX(salary) OVER (PARTITION BY department)`.
5. `salary_difference_from_department_avg`: `ROUND(salary - department_avg, 2)`.
6. `salary_contribution_percentage`: `ROUND(salary * 100.0 / department_total, 2)`.
7. `running_salary_by_joining_date`: Running payroll total ordered by `joining_date ASC, emp_id ASC` (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).
8. `cumulative_salary_percentage_desc`: Running cumulative salary percentage ordered by `salary DESC, emp_id ASC` (`running_sum * 100.0 / department_total`), rounded to 2 decimals.
9. `above_department_average`: `'Yes'` if `salary > department_avg`, else `'No'`.
10. **Sorting:** Sort by `department ASC`, then `salary DESC`, then `emp_id ASC`.

---

### **Expected Output Columns**
`emp_id`, `emp_name`, `department`, `salary`, `department_avg_salary`, `department_total_salary`, `department_min_salary`, `department_max_salary`, `salary_difference_from_department_avg`, `salary_contribution_percentage`, `running_salary_by_joining_date`, `cumulative_salary_percentage_desc`, `above_department_average`.
"""

REWRITTEN_DESCRIPTIONS[32] = """### **Problem Description**
Write an SQL query using navigation window functions (`LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`) to analyze customer purchasing behavior over time.

### **Table Schemas**
- `customers (customer_id, customer_name, city, registration_date)`
- `orders (order_id, customer_id, emp_id, order_date, amount, status)`

---

### **Requirements**
Partition all window calculations by customer (`o.customer_id`) and order chronologically by `o.order_date ASC, o.order_id ASC`. Include all order statuses:
1. `previous_order_amount`: Previous order amount using `LAG(amount)`.
2. `next_order_amount`: Next order amount using `LEAD(amount)`.
3. `amount_difference_from_previous`: `amount - previous_amount` (display `0` if first order).
4. `percentage_change_from_previous`: `ROUND((amount - previous) * 100.0 / previous, 2)` (`NULL` if first order).
5. `amount_increased_vs_previous`: `'Yes'` if `amount > previous_amount`, else `'No'`.
6. `first_order_amount`: Amount of the customer's very first order using `FIRST_VALUE()`.
7. `last_order_amount`: Amount of the customer's latest order using `LAST_VALUE()` with `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
8. `minimum_order_amount`, `maximum_order_amount`, `average_order_amount`: Customer overall min, max, and avg (rounded to 2 decimals).
9. `second_order_amount`: Amount of the customer's 2nd chronological order using `NTH_VALUE(amount, 2)` across the full partition.
10. `first_order_date` & `latest_order_date`: First and latest order dates for the customer.
11. **Sorting:** Sort by `o.customer_id ASC`, `o.order_date ASC`, `o.order_id ASC`.

---

### **Expected Output Columns**
`order_id`, `customer_id`, `customer_name`, `order_date`, `amount`, `status`, `previous_order_amount`, `next_order_amount`, `amount_difference_from_previous`, `percentage_change_from_previous`, `amount_increased_vs_previous`, `first_order_amount`, `last_order_amount`, `minimum_order_amount`, `maximum_order_amount`, `average_order_amount`, `second_order_amount`, `first_order_date`, `latest_order_date`.
"""

REWRITTEN_DESCRIPTIONS[33] = """### **Problem Description**
Write an SQL query using explicit window frames (`ROWS BETWEEN`) to compute customer running totals and rolling 3-transaction moving windows.

### **Table Schemas**
- `customers (customer_id, customer_name)`
- `orders (order_id, customer_id, emp_id, order_date, amount, status)`

---

### **Requirements**
Partition by `o.customer_id` and order chronologically by `o.order_date ASC, o.order_id ASC`. Include all order statuses:
1. `running_total_amount`: Cumulative sum of spending from the first order up to the current order (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).
2. `rolling_three_order_total`: Sum of amounts for current order and up to 2 preceding orders (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`).
3. `rolling_three_order_average`: Moving average over the same 3-order window, rounded to 2 decimals.
4. `running_minimum_order_amount`: Lowest order amount observed so far for that customer.
5. `running_order_count`: Cumulative order counter (`1, 2, 3...`).
6. **Sorting:** Sort by `o.customer_id ASC`, `o.order_date ASC`, `o.order_id ASC`.

---

### **Expected Output Columns**
| Column Name | Calculation |
|---|---|
| `order_id` | `o.order_id` |
| `customer_id` | `o.customer_id` |
| `customer_name` | `c.customer_name` |
| `order_date` | `o.order_date` |
| `amount` | `o.amount` |
| `running_total_amount` | Cumulative spending |
| `rolling_three_order_total` | Sum of current + up to 2 preceding |
| `rolling_three_order_average` | Avg of current + up to 2 preceding |
| `running_minimum_order_amount` | Running minimum |
| `running_order_count` | Sequential order count |
"""

REWRITTEN_DESCRIPTIONS[34] = """### **Problem Description**
Write an SQL query to track the company-wide sales timeline while analyzing employee-level running performance and peak completed sales.

### **Table Schemas**
- `employees (emp_id, emp_name)`
- `orders (order_id, customer_id, emp_id, order_date, amount, status)`

---

### **Requirements**
1. `company_running_order_amount`: Global running sum of all orders ordered by `order_date ASC, order_id ASC`. Include all statuses.
2. `previous_order_amount_by_employee`: `LAG(amount)` partitioned by `o.emp_id` and ordered chronologically.
3. `employee_running_max_order_amount`: Running maximum order amount handled by that employee up to current transaction.
4. `employee_highest_completed_order_amount`: Maximum amount among `Completed` orders handled by that employee across their entire history.
5. `is_employee_highest_completed_order`: `'Yes'` if the order is `Completed` and its amount equals `employee_highest_completed_order_amount`, else `'No'`.
6. **Sorting:** Sort chronologically by `order_date ASC`, then `order_id ASC`.

---

### **Expected Output Columns**
`order_id`, `order_date`, `customer_id`, `emp_id`, `employee_name`, `amount`, `status`, `company_running_order_amount`, `previous_order_amount_by_employee`, `employee_running_max_order_amount`, `employee_highest_completed_order_amount`, `is_employee_highest_completed_order`.
"""

REWRITTEN_DESCRIPTIONS[35] = """### **Problem Description**
Write an SQL query using CTEs and window ranking functions to identify the top 2 revenue-generating customers in each city, and display their top 3 completed transactions.

### **Table Schemas**
- `customers (customer_id, customer_name, city)`
- `orders (order_id, customer_id, emp_id, order_date, amount, status)`
- `employees (emp_id, emp_name)`

---

### **Requirements**
1. **Customer Revenue & Rank:**
   - Calculate total completed revenue per customer (`status = 'Completed'`).
   - Rank customers within their city using `RANK() OVER (PARTITION BY c.city ORDER BY completed_total DESC)` (`customer_rank_in_city`).
   - Retain customers with `customer_rank_in_city <= 2` (preserves ties at rank 2).
2. **Order Rank:**
   - For eligible customers, rank their individual Completed orders using `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC, order_date ASC, order_id ASC)` (`order_rank_for_customer`).
   - Retain only the top 3 completed orders (`order_rank_for_customer <= 3`).
3. **Sorting:** Sort by `city ASC`, `customer_rank_in_city ASC`, `customer_id ASC`, `order_rank_for_customer ASC`.

---

### **Expected Output Columns**
`customer_id`, `customer_name`, `city`, `completed_order_total`, `customer_rank_in_city`, `order_rank_for_customer`, `order_id`, `order_date`, `order_amount`, `handled_by_employee`.
"""

REWRITTEN_DESCRIPTIONS[36] = """### **Problem Description**
Write an SQL query to return exactly **one record per customer** summarizing their earliest order, latest overall order, and latest completed order with previous completed amount.

### **Table Schemas**
- `customers (customer_id, customer_name, city)`
- `orders (order_id, customer_id, order_date, amount, status)`

---

### **Requirements**
1. Return exactly one row for every customer in `customers`.
2. **Overall Order Metrics:**
   - `first_order_date`: Earliest order date across all orders for that customer.
   - `latest_order_date`: Latest order date across all orders for that customer.
   - `latest_order_id`, `latest_order_amount`, `latest_order_status`: Details of the customer's most recent order (any status), determined by `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) = 1`.
3. **Completed Order Metrics:**
   - Filter `status = 'Completed'`.
   - `latest_completed_order_id`, `latest_completed_order_date`, `latest_completed_order_amount`: Details of the most recent Completed order.
   - `previous_completed_order_amount`: Amount of the Completed order immediately preceding the latest completed order, using `LAG(amount)`.
   - If customer has no completed orders, completed fields must be `NULL`.
4. **Sorting:** Sort final output by `customer_id ASC`.

---

### **Expected Output Columns**
`customer_id`, `customer_name`, `city`, `first_order_date`, `latest_order_date`, `latest_order_id`, `latest_order_amount`, `latest_order_status`, `latest_completed_order_id`, `latest_completed_order_date`, `latest_completed_order_amount`, `previous_completed_order_amount`.
"""

REWRITTEN_DESCRIPTIONS[37] = """### **Problem Description**
Write an SQL query using a `LEFT JOIN` to evaluate employee sales contributions, department rankings, and cumulative department revenue percentages.

### **Table Schemas**
- `employees (emp_id, emp_name, department)`
- `orders (order_id, emp_id, amount, status)`

---

### **Requirements**
1. **Join:** Start with `employees e LEFT JOIN orders o ON e.emp_id = o.emp_id`. All 12 employees must appear.
2. **Completed Aggregates:**
   - `completed_order_count`: Count of orders with `status = 'Completed'` (`0` if none).
   - `completed_revenue`: Sum of completed order amounts (`COALESCE(..., 0)`).
   - `average_completed_order_amount`: `ROUND(AVG(...), 2)` (`NULL` if no completed orders).
   - `highest_completed_order_amount`: `MAX(...)` (`NULL` if no completed orders).
3. **Department Ranks:**
   - `department_sales_rank`: `RANK() OVER (PARTITION BY department ORDER BY completed_revenue DESC)`.
   - `department_sales_dense_rank`: `DENSE_RANK() OVER (PARTITION BY department ORDER BY completed_revenue DESC)`.
4. **Cumulative Revenue Percentage:**
   - Cumulative sum of employee completed revenue within department divided by total departmental completed revenue (`running_sum * 100.0 / dept_total_revenue`), rounded to 2 decimals.
   - Break ties deterministically with `emp_id ASC`.
   - If a department has 0 total completed revenue, display `100.00`.
5. **Sorting:** Sort by `department ASC`, then `completed_revenue DESC`, then `emp_id ASC`.

---

### **Expected Output Columns**
`emp_id`, `employee_name`, `department`, `completed_order_count`, `completed_revenue`, `average_completed_order_amount`, `highest_completed_order_amount`, `department_sales_rank`, `department_sales_dense_rank`, `cumulative_department_revenue_percentage`.
"""

def update_all_descriptions():
    with open("data/questions.json", "r") as f:
        questions = json.load(f)

    updated_count = 0
    for q in questions:
        qid = q["id"]
        if qid in REWRITTEN_DESCRIPTIONS:
            q["description"] = REWRITTEN_DESCRIPTIONS[qid].strip()
            updated_count += 1

    with open("data/questions.json", "w") as f:
        json.dump(questions, f, indent=2)

    print(f"Successfully updated clean, clear descriptions for all {updated_count} SQL questions!")

if __name__ == "__main__":
    update_all_descriptions()
