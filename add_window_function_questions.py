import json
import sqlite3
from sql_engine import create_connection, execute_query, compare_sql_results, format_table

SCHEMA_SQL = """
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    department VARCHAR(40) NOT NULL,
    city VARCHAR(40),
    salary DECIMAL(12,2) NOT NULL,
    joining_date DATE NOT NULL
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    city VARCHAR(40),
    registration_date DATE NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    emp_id INT NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
"""

BASE_DATA_SQL = """
INSERT INTO employees (emp_id, emp_name, department, city, salary, joining_date) VALUES
(1, 'Aarav', 'IT', 'Delhi', 75000, '2021-01-15'),
(2, 'Diya', 'HR', 'Noida', 52000, '2020-03-10'),
(3, 'Kabir', 'Sales', 'Delhi', 61000, '2022-06-01'),
(4, 'Meera', 'IT', 'Gurugram', 90000, '2019-11-20'),
(5, 'Ishaan', 'Finance', 'Noida', 68000, '2021-08-12'),
(6, 'Anaya', 'Sales', 'Delhi', 58000, '2023-02-05'),
(7, 'Reyansh', 'HR', 'Gurugram', 56000, '2022-09-18'),
(8, 'Sara', 'IT', 'Noida', 82000, '2020-07-25'),
(9, 'Vivaan', 'Finance', 'Delhi', 72000, '2018-04-30'),
(10, 'Myra', 'Sales', 'Gurugram', 65000, '2021-12-01'),
(11, 'Arjun', 'IT', 'Delhi', 75000, '2022-01-10'),
(12, 'Kiara', 'Finance', 'Noida', 68000, '2023-05-15');

INSERT INTO customers (customer_id, customer_name, city, registration_date) VALUES
(101, 'Rohan', 'Delhi', '2022-01-10'),
(102, 'Tanya', 'Noida', '2022-02-14'),
(103, 'Dev', 'Delhi', '2022-03-20'),
(104, 'Ira', 'Gurugram', '2022-04-05'),
(105, 'Neel', 'Noida', '2022-05-12'),
(106, 'Sia', 'Delhi', '2022-06-18'),
(107, 'Manav', 'Gurugram', '2022-07-22'),
(108, 'Aditi', 'Noida', '2022-08-30');

INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
(1001, 101, 1, '2024-01-02', 1200, 'Completed'),
(1002, 102, 3, '2024-01-03', 2500, 'Completed'),
(1003, 101, 4, '2024-01-05', 1800, 'Completed'),
(1004, 103, 6, '2024-01-06', 3200, 'Pending'),
(1005, 104, 10, '2024-01-08', 1500, 'Completed'),
(1006, 102, 3, '2024-01-10', 3000, 'Completed'),
(1007, 105, 5, '2024-01-11', 4200, 'Completed'),
(1008, 101, 1, '2024-01-12', 2200, 'Completed'),
(1009, 106, 6, '2024-01-14', 2800, 'Cancelled'),
(1010, 103, 10, '2024-01-15', 3500, 'Completed'),
(1011, 104, 10, '2024-01-18', 2700, 'Completed'),
(1012, 107, 7, '2024-01-20', 1900, 'Completed'),
(1013, 105, 5, '2024-01-22', 3900, 'Pending'),
(1014, 102, 3, '2024-01-25', 1800, 'Completed'),
(1015, 108, 8, '2024-01-27', 5100, 'Completed'),
(1016, 106, 6, '2024-02-01', 3300, 'Completed'),
(1017, 107, 7, '2024-02-03', 2100, 'Completed'),
(1018, 101, 4, '2024-02-05', 2600, 'Pending'),
(1019, 108, 8, '2024-02-08', 4700, 'Completed'),
(1020, 104, 10, '2024-02-10', 3100, 'Completed'),
(1021, 103, 6, '2024-02-12', 2900, 'Completed'),
(1022, 105, 5, '2024-02-15', 4500, 'Completed'),
(1023, 102, 3, '2024-02-18', 2200, 'Cancelled'),
(1024, 106, 6, '2024-02-20', 3600, 'Completed'),
(1025, 107, 7, '2024-02-22', 2400, 'Completed'),
(1026, 108, 8, '2024-02-25', 5300, 'Completed'),
(1027, 101, 1, '2024-03-01', 3100, 'Completed'),
(1028, 103, 10, '2024-03-03', 4100, 'Completed'),
(1029, 104, 10, '2024-03-05', 2900, 'Pending'),
(1030, 105, 5, '2024-03-08', 4800, 'Completed');
"""

def run_query(query, data_sql=BASE_DATA_SQL):
    conn = create_connection(SCHEMA_SQL, data_sql)
    res = execute_query(conn, query)
    conn.close()
    if not res["success"]:
        raise Exception(f"Query error: {res['error']}")
    return res["columns"], res["rows"]

def build_test_cases(query, test_variants):
    cases = []
    for idx, (desc, data_override, is_sample) in enumerate(test_variants, start=1):
        cols, rows = run_query(query, data_override)
        cases.append({
            "id": idx,
            "description": desc,
            "isSample": is_sample,
            "testData": data_override,
            "expectedColumns": cols,
            "expectedRows": rows,
            "orderSensitive": True
        })
    return cases

def get_emp_override(emp_rows):
    vals = ",\n".join(f"({r[0]}, '{r[1]}', '{r[2]}', '{r[3]}', {r[4]}, '{r[5]}')" for r in emp_rows)
    return f"INSERT INTO employees (emp_id, emp_name, department, city, salary, joining_date) VALUES\n{vals};\n"

# Canonical Queries
QUERY_30 = """
SELECT 
    emp_id,
    emp_name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id ASC) AS salary_row_number,
    RANK() OVER (ORDER BY salary DESC) AS salary_rank_global,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS department_dense_rank,
    NTILE(4) OVER (ORDER BY salary DESC, emp_id ASC) AS salary_quartile,
    ROW_NUMBER() OVER (ORDER BY joining_date ASC, emp_id ASC) AS joining_date_row_number,
    CASE 
        WHEN DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) <= 3 THEN 'Yes' 
        ELSE 'No' 
    END AS top_three_in_department,
    CASE 
        WHEN DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) = 2 THEN 'Yes' 
        ELSE 'No' 
    END AS second_highest_in_department,
    ROUND(PERCENT_RANK() OVER (PARTITION BY department ORDER BY salary ASC), 2) AS percent_rank_in_department,
    ROUND(CUME_DIST() OVER (PARTITION BY department ORDER BY salary ASC), 2) AS cume_dist_in_department,
    NTH_VALUE(salary, 3) OVER (
        PARTITION BY department 
        ORDER BY salary DESC, emp_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS third_highest_salary_in_department
FROM employees
ORDER BY salary_row_number;
"""

QUERY_31 = """
SELECT 
    emp_id,
    emp_name,
    department,
    salary,
    ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS department_avg_salary,
    SUM(salary) OVER (PARTITION BY department) AS department_total_salary,
    MIN(salary) OVER (PARTITION BY department) AS department_min_salary,
    MAX(salary) OVER (PARTITION BY department) AS department_max_salary,
    ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS salary_difference_from_department_avg,
    ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY department), 2) AS salary_contribution_percentage,
    SUM(salary) OVER (
        PARTITION BY department 
        ORDER BY joining_date ASC, emp_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_salary_by_joining_date,
    ROUND(
        SUM(salary) OVER (
            PARTITION BY department 
            ORDER BY salary DESC, emp_id ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) * 100.0 / SUM(salary) OVER (PARTITION BY department), 
        2
    ) AS cumulative_salary_percentage_desc,
    CASE 
        WHEN salary > AVG(salary) OVER (PARTITION BY department) THEN 'Yes' 
        ELSE 'No' 
    END AS above_department_average
FROM employees
ORDER BY department ASC, salary DESC, emp_id ASC;
"""

QUERY_32 = """
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_name,
    o.order_date,
    o.amount,
    o.status,
    LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC) AS previous_order_amount,
    LEAD(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC) AS next_order_amount,
    COALESCE(o.amount - LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC), 0) AS amount_difference_from_previous,
    CASE 
        WHEN LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC) IS NULL THEN NULL
        ELSE ROUND((o.amount - LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC)) * 100.0 / 
                   LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC), 2)
    END AS percentage_change_from_previous,
    CASE 
        WHEN o.amount > LAG(o.amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC, o.order_id ASC) THEN 'Yes'
        ELSE 'No'
    END AS amount_increased_vs_previous,
    FIRST_VALUE(o.amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_order_amount,
    LAST_VALUE(o.amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order_amount,
    MIN(o.amount) OVER (PARTITION BY o.customer_id) AS minimum_order_amount,
    MAX(o.amount) OVER (PARTITION BY o.customer_id) AS maximum_order_amount,
    ROUND(AVG(o.amount) OVER (PARTITION BY o.customer_id), 2) AS average_order_amount,
    NTH_VALUE(o.amount, 2) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS second_order_amount,
    FIRST_VALUE(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_order_date,
    LAST_VALUE(o.order_date) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS latest_order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.customer_id ASC, o.order_date ASC, o.order_id ASC;
"""

QUERY_33 = """
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_name,
    o.order_date,
    o.amount,
    SUM(o.amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_amount,
    SUM(o.amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_three_order_total,
    ROUND(
        AVG(o.amount) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date ASC, o.order_id ASC 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_three_order_average,
    MIN(o.amount) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_minimum_order_amount,
    COUNT(o.order_id) OVER (
        PARTITION BY o.customer_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.customer_id ASC, o.order_date ASC, o.order_id ASC;
"""

QUERY_34 = """
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    o.emp_id,
    e.emp_name AS employee_name,
    o.amount,
    o.status,
    SUM(o.amount) OVER (
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS company_running_order_amount,
    LAG(o.amount) OVER (
        PARTITION BY o.emp_id 
        ORDER BY o.order_date ASC, o.order_id ASC
    ) AS previous_order_amount_by_employee,
    MAX(o.amount) OVER (
        PARTITION BY o.emp_id 
        ORDER BY o.order_date ASC, o.order_id ASC 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS employee_running_max_order_amount,
    MAX(CASE WHEN o.status = 'Completed' THEN o.amount ELSE NULL END) OVER (
        PARTITION BY o.emp_id
    ) AS employee_highest_completed_order_amount,
    CASE 
        WHEN o.status = 'Completed' AND o.amount = MAX(CASE WHEN o.status = 'Completed' THEN o.amount ELSE NULL END) OVER (PARTITION BY o.emp_id)
        THEN 'Yes'
        ELSE 'No'
    END AS is_employee_highest_completed_order
FROM orders o
JOIN employees e ON o.emp_id = e.emp_id
ORDER BY o.order_date ASC, o.order_id ASC;
"""

QUERY_35 = """
WITH CustomerRevenue AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        SUM(o.amount) AS completed_order_total,
        RANK() OVER (PARTITION BY c.city ORDER BY SUM(o.amount) DESC) AS customer_rank_in_city
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'Completed'
    GROUP BY c.customer_id, c.customer_name, c.city
),
EligibleCustomers AS (
    SELECT * FROM CustomerRevenue WHERE customer_rank_in_city <= 2
),
RankedOrders AS (
    SELECT 
        ec.customer_id,
        ec.customer_name,
        ec.city,
        ec.completed_order_total,
        ec.customer_rank_in_city,
        ROW_NUMBER() OVER (
            PARTITION BY ec.customer_id 
            ORDER BY o.amount DESC, o.order_date ASC, o.order_id ASC
        ) AS order_rank_for_customer,
        o.order_id,
        o.order_date,
        o.amount AS order_amount,
        e.emp_name AS handled_by_employee
    FROM EligibleCustomers ec
    JOIN orders o ON ec.customer_id = o.customer_id
    JOIN employees e ON o.emp_id = e.emp_id
    WHERE o.status = 'Completed'
)
SELECT 
    customer_id,
    customer_name,
    city,
    completed_order_total,
    customer_rank_in_city,
    order_rank_for_customer,
    order_id,
    order_date,
    order_amount,
    handled_by_employee
FROM RankedOrders
WHERE order_rank_for_customer <= 3
ORDER BY city ASC, customer_rank_in_city ASC, customer_id ASC, order_rank_for_customer ASC;
"""

QUERY_36 = """
WITH AllOrdersRanked AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        amount,
        status,
        MIN(order_date) OVER (PARTITION BY customer_id) AS first_order_date,
        MAX(order_date) OVER (PARTITION BY customer_id) AS latest_order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn_all
    FROM orders
),
LatestOverall AS (
    SELECT 
        customer_id,
        first_order_date,
        latest_order_date,
        order_id AS latest_order_id,
        amount AS latest_order_amount,
        status AS latest_order_status
    FROM AllOrdersRanked
    WHERE rn_all = 1
),
CompletedOrdersRanked AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        amount,
        LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date ASC, order_id ASC) AS previous_completed_order_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) AS rn_comp
    FROM orders
    WHERE status = 'Completed'
),
LatestCompleted AS (
    SELECT 
        customer_id,
        order_id AS latest_completed_order_id,
        order_date AS latest_completed_order_date,
        amount AS latest_completed_order_amount,
        previous_completed_order_amount
    FROM CompletedOrdersRanked
    WHERE rn_comp = 1
)
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    lo.first_order_date,
    lo.latest_order_date,
    lo.latest_order_id,
    lo.latest_order_amount,
    lo.latest_order_status,
    lc.latest_completed_order_id,
    lc.latest_completed_order_date,
    lc.latest_completed_order_amount,
    lc.previous_completed_order_amount
FROM customers c
LEFT JOIN LatestOverall lo ON c.customer_id = lo.customer_id
LEFT JOIN LatestCompleted lc ON c.customer_id = lc.customer_id
ORDER BY c.customer_id ASC;
"""

QUERY_37 = """
WITH EmpAgg AS (
    SELECT 
        e.emp_id,
        e.emp_name AS employee_name,
        e.department,
        COUNT(CASE WHEN o.status = 'Completed' THEN o.order_id ELSE NULL END) AS completed_order_count,
        COALESCE(SUM(CASE WHEN o.status = 'Completed' THEN o.amount ELSE 0 END), 0) AS completed_revenue,
        ROUND(AVG(CASE WHEN o.status = 'Completed' THEN o.amount ELSE NULL END), 2) AS average_completed_order_amount,
        MAX(CASE WHEN o.status = 'Completed' THEN o.amount ELSE NULL END) AS highest_completed_order_amount
    FROM employees e
    LEFT JOIN orders o ON e.emp_id = o.emp_id
    GROUP BY e.emp_id, e.emp_name, e.department
),
DeptTotals AS (
    SELECT 
        emp_id,
        employee_name,
        department,
        completed_order_count,
        completed_revenue,
        average_completed_order_amount,
        highest_completed_order_amount,
        RANK() OVER (PARTITION BY department ORDER BY completed_revenue DESC) AS department_sales_rank,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY completed_revenue DESC) AS department_sales_dense_rank,
        SUM(completed_revenue) OVER (PARTITION BY department) AS dept_total_revenue,
        SUM(completed_revenue) OVER (
            PARTITION BY department 
            ORDER BY completed_revenue DESC, emp_id ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS running_dept_revenue
    FROM EmpAgg
)
SELECT 
    emp_id,
    employee_name,
    department,
    completed_order_count,
    completed_revenue,
    average_completed_order_amount,
    highest_completed_order_amount,
    department_sales_rank,
    department_sales_dense_rank,
    CASE 
        WHEN dept_total_revenue = 0 THEN 100.00
        ELSE ROUND(running_dept_revenue * 100.0 / dept_total_revenue, 2)
    END AS cumulative_department_revenue_percentage
FROM DeptTotals
ORDER BY department ASC, completed_revenue DESC, emp_id ASC;
"""

# ─────────────────────────────────────────────────────────────────────────────
# 10 Test Variants for each of the 8 Problems
# ─────────────────────────────────────────────────────────────────────────────

def get_p1_ten_variants():
    c1 = ("Primary comprehensive dataset (all 12 employees across 4 departments)", BASE_DATA_SQL, True)
    d2 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 75000, '2021-01-15'), (2, 'Diya', 'HR', 'Noida', 55000, '2020-03-10'),
        (3, 'Kabir', 'Sales', 'Delhi', 61000, '2022-06-01'), (4, 'Meera', 'IT', 'Gurugram', 90000, '2019-11-20'),
        (5, 'Ishaan', 'Finance', 'Noida', 70000, '2021-08-12'), (6, 'Anaya', 'Sales', 'Delhi', 61000, '2023-02-05'),
        (7, 'Reyansh', 'HR', 'Gurugram', 55000, '2022-09-18'), (8, 'Sara', 'IT', 'Noida', 82000, '2020-07-25'),
        (9, 'Vivaan', 'Finance', 'Delhi', 70000, '2018-04-30'), (10, 'Myra', 'Sales', 'Gurugram', 65000, '2021-12-01'),
        (11, 'Arjun', 'IT', 'Delhi', 75000, '2022-01-10'), (12, 'Kiara', 'Finance', 'Noida', 70000, '2023-05-15')
    ])
    c2 = ("Triple salary tie in Finance and double tie in HR to test DENSE_RANK without gaps", d2, False)
    d3 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 75000, '2021-01-15'), (2, 'Diya', 'HR', 'Noida', 52000, '2020-03-10'),
        (3, 'Kabir', 'Sales', 'Delhi', 61000, '2022-06-01'), (4, 'Meera', 'IT', 'Gurugram', 90000, '2019-11-20'),
        (5, 'Ishaan', 'Finance', 'Noida', 68000, '2021-08-12'), (6, 'Anaya', 'Sales', 'Delhi', 58000, '2023-02-05'),
        (7, 'Zara', 'Legal', 'Delhi', 95000, '2020-01-01'), (8, 'Sara', 'IT', 'Noida', 82000, '2020-07-25')
    ])
    c3 = ("Departments with fewer than 3 employees (verifying NTH_VALUE produces NULL)", d3, False)
    d4 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 80000, '2021-01-15'), (2, 'Sara', 'IT', 'Noida', 80000, '2020-07-25'),
        (3, 'Meera', 'IT', 'Gurugram', 80000, '2019-11-20'), (4, 'Arjun', 'IT', 'Delhi', 80000, '2022-01-10'),
        (5, 'Ishaan', 'Finance', 'Noida', 70000, '2021-08-12'), (6, 'Vivaan', 'Finance', 'Delhi', 70000, '2018-04-30')
    ])
    c4 = ("All equal salaries within IT department (testing RANK 1 with tie and NTILE splitting)", d4, False)
    d5 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 75000, '2023-12-31'), (2, 'Diya', 'HR', 'Noida', 52000, '2023-11-30'),
        (3, 'Kabir', 'Sales', 'Delhi', 61000, '2023-10-31'), (4, 'Meera', 'IT', 'Gurugram', 90000, '2023-09-30'),
        (5, 'Ishaan', 'Finance', 'Noida', 68000, '2023-08-31'), (6, 'Anaya', 'Sales', 'Delhi', 58000, '2023-07-31'),
        (7, 'Reyansh', 'HR', 'Gurugram', 56000, '2023-06-30'), (8, 'Sara', 'IT', 'Noida', 82000, '2023-05-31'),
        (9, 'Vivaan', 'Finance', 'Delhi', 72000, '2023-04-30'), (10, 'Myra', 'Sales', 'Gurugram', 65000, '2023-03-31'),
        (11, 'Arjun', 'IT', 'Delhi', 75000, '2023-02-28'), (12, 'Kiara', 'Finance', 'Noida', 68000, '2023-01-31')
    ])
    c5 = ("Reverse joining date distribution (verifying joining_date_row_number sequence)", d5, False)
    d6 = get_emp_override([
        (1, 'Emp1', 'D1', 'City', 100000, '2020-01-01'), (2, 'Emp2', 'D1', 'City', 90000, '2020-01-02'),
        (3, 'Emp3', 'D1', 'City', 80000, '2020-01-03'), (4, 'Emp4', 'D1', 'City', 70000, '2020-01-04'),
        (5, 'Emp5', 'D2', 'City', 60000, '2020-01-05'), (6, 'Emp6', 'D2', 'City', 50000, '2020-01-06'),
        (7, 'Emp7', 'D2', 'City', 40000, '2020-01-07'), (8, 'Emp8', 'D2', 'City', 30000, '2020-01-08')
    ])
    c6 = ("Uniform 8-employee distribution (NTILE(4) exactly 2 employees per quartile)", d6, False)
    d7 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 150000, '2021-01-15'), (2, 'Diya', 'IT', 'Noida', 120000, '2020-03-10'),
        (3, 'Kabir', 'IT', 'Delhi', 90000, '2022-06-01'), (4, 'Meera', 'IT', 'Gurugram', 60000, '2019-11-20'),
        (5, 'Ishaan', 'IT', 'Noida', 30000, '2021-08-12')
    ])
    c7 = ("Single large department with 5 salary levels (testing CUME_DIST and PERCENT_RANK steps)", d7, False)
    d8 = get_emp_override([
        (10, 'Aarav', 'IT', 'Delhi', 80000, '2021-01-15'), (20, 'Arjun', 'IT', 'Delhi', 80000, '2021-01-15'),
        (30, 'Diya', 'HR', 'Noida', 60000, '2021-01-15'), (40, 'Reyansh', 'HR', 'Gurugram', 60000, '2021-01-15')
    ])
    c8 = ("Simultaneous tie in salary and joining date (deterministic ordering via emp_id)", d8, False)
    d9 = get_emp_override([
        (100, 'Solo', 'Executive', 'Delhi', 250000, '2018-01-01')
    ])
    c9 = ("Single employee organization (global rank 1, NTILE 1, NTH_VALUE NULL)", d9, False)
    d10 = get_emp_override([
        (1, 'E1', 'IT', 'Delhi', 10000, '2020-01-01'), (2, 'E2', 'IT', 'Delhi', 20000, '2020-01-02'),
        (3, 'E3', 'IT', 'Delhi', 30000, '2020-01-03'), (4, 'E4', 'IT', 'Delhi', 40000, '2020-01-04')
    ])
    c10 = ("Ascending salary order in IT (verifying salary DESC reverses order correctly)", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p2_ten_variants():
    c1 = ("Standard 12 employees departmental payroll baseline", BASE_DATA_SQL, True)
    d2 = get_emp_override([
        (1, 'Meera', 'IT', 'Delhi', 90000, '2020-01-01'), (2, 'Ishaan', 'Finance', 'Noida', 70000, '2020-01-01'),
        (3, 'Reyansh', 'HR', 'Gurugram', 50000, '2020-01-01'), (4, 'Myra', 'Sales', 'Delhi', 60000, '2020-01-01')
    ])
    c2 = ("Solo employee departments (verifying 100% payroll contribution and 0 diff from avg)", d2, False)
    d3 = get_emp_override([
        (1, 'Aarav', 'IT', 'Delhi', 80000, '2021-01-01'), (2, 'Sara', 'IT', 'Noida', 80000, '2022-01-01'),
        (3, 'Ishaan', 'Finance', 'Noida', 70000, '2020-01-01'), (4, 'Vivaan', 'Finance', 'Delhi', 70000, '2021-01-01')
    ])
    c3 = ("Equal salary cohorts (verifying 50.00% exact contribution and cumulative 100.00%)", d3, False)
    d4 = get_emp_override([
        (1, 'First', 'IT', 'Delhi', 10000, '2019-01-01'), (2, 'Second', 'IT', 'Noida', 20000, '2020-01-01'),
        (3, 'Third', 'IT', 'Delhi', 30000, '2021-01-01'), (4, 'Fourth', 'IT', 'Noida', 40000, '2022-01-01')
    ])
    c4 = ("Strict 4-stage chronological onboarding (running salary 10k -> 30k -> 60k -> 100k)", d4, False)
    d5 = get_emp_override([
        (1, 'CFO', 'Finance', 'Delhi', 300000, '2018-01-01'), (2, 'Analyst', 'Finance', 'Noida', 50000, '2022-01-01'),
        (3, 'Clerk', 'Finance', 'Noida', 30000, '2023-01-01')
    ])
    c5 = ("Significant salary disparity in Finance (above_department_average flag only on top earner)", d5, False)
    d6 = get_emp_override([
        (1, 'S1', 'Sales', 'Delhi', 50000, '2020-01-01'), (2, 'S2', 'Sales', 'Delhi', 60000, '2020-06-01'),
        (3, 'S3', 'Sales', 'Delhi', 70000, '2021-01-01'), (4, 'S4', 'Sales', 'Delhi', 80000, '2021-06-01'),
        (5, 'S5', 'Sales', 'Delhi', 90000, '2022-01-01')
    ])
    c6 = ("5-tier Sales workforce (verifying stepwise cumulative percentage descent)", d6, False)
    d7 = get_emp_override([
        (10, 'Aarav', 'IT', 'Delhi', 90000, '2021-01-15'), (20, 'Sara', 'IT', 'Noida', 80000, '2021-01-15'),
        (30, 'Arjun', 'IT', 'Delhi', 70000, '2021-01-15')
    ])
    c7 = ("Identical joining dates with emp_id tie-breaking for running total", d7, False)
    d8 = get_emp_override([
        (1, 'E1', 'D1', 'City', 100000, '2020-01-01'), (2, 'E2', 'D1', 'City', 50000, '2021-01-01'),
        (3, 'E3', 'D2', 'City', 200000, '2020-01-01'), (4, 'E4', 'D2', 'City', 100000, '2021-01-01')
    ])
    c8 = ("Two 2-employee departments verifying partition isolation", d8, False)
    d9 = get_emp_override([
        (1, 'E1', 'DeptA', 'City', 50000, '2020-01-01'), (2, 'E2', 'DeptB', 'City', 60000, '2020-01-01'),
        (3, 'E3', 'DeptC', 'City', 70000, '2020-01-01'), (4, 'E4', 'DeptD', 'City', 80000, '2020-01-01'),
        (5, 'E5', 'DeptE', 'City', 90000, '2020-01-01')
    ])
    c9 = ("Five single-employee departments verifying aggregate stability across wide partitions", d9, False)
    d10 = get_emp_override([
        (1, 'E1', 'IT', 'Delhi', 50000, '2020-01-01'), (2, 'E2', 'IT', 'Delhi', 50000, '2020-01-02')
    ])
    c10 = ("All equal salaries (above_department_average flag must be 'No' for both)", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p3_ten_variants():
    c1 = ("Complete 30 orders baseline across all 8 customers", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 102, 3, '2024-01-02', 3000, 'Completed'),
    (1003, 102, 3, '2024-01-05', 4500, 'Completed');
    """
    c2 = ("Single order customer (verifying LAG/LEAD are NULL, diff is 0, % change is NULL)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 10000, 'Completed'), (1002, 101, 1, '2024-01-05', 8000, 'Completed'),
    (1003, 101, 1, '2024-01-10', 6000, 'Completed'), (1004, 101, 1, '2024-01-15', 4000, 'Completed');
    """
    c3 = ("Monotonically decreasing customer purchases (negative differences and 'No' increase flag)", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2000, 'Completed'), (1002, 101, 1, '2024-01-02', 4000, 'Completed'),
    (1003, 101, 1, '2024-01-03', 2000, 'Completed'), (1004, 101, 1, '2024-01-04', 5000, 'Completed');
    """
    c4 = ("Alternating surge and drop (verifying exact 100.00% gain and -50.00% drop calculations)", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 3000, 'Completed'), (1002, 101, 1, '2024-01-05', 3000, 'Completed'),
    (1003, 101, 1, '2024-01-10', 3000, 'Completed');
    """
    c5 = ("Identical order amounts (verifying difference 0, percentage change 0.00%, increase 'No')", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1500, 'Completed'), (1002, 101, 1, '2024-01-10', 3000, 'Completed'),
    (1003, 102, 2, '2024-01-05', 2000, 'Completed'), (1004, 102, 2, '2024-01-15', 1000, 'Completed');
    """
    c6 = ("Two customers with 2 orders (FIRST_VALUE and second_order_amount exact boundary checks)", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Cancelled'), (1002, 101, 1, '2024-01-05', 2000, 'Pending'),
    (1003, 101, 1, '2024-01-10', 3000, 'Completed');
    """
    c7 = ("Status diversity in chronological order (verifying all statuses are retained in chain)", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 1500, 'Completed'),
    (1003, 101, 1, '2024-01-03', 2000, 'Completed'), (1004, 101, 1, '2024-01-04', 2500, 'Completed'),
    (1005, 101, 1, '2024-01-05', 3000, 'Completed'), (1006, 101, 1, '2024-01-06', 3500, 'Completed');
    """
    c8 = ("6-order customer trajectory (verifying LAST_VALUE and latest_order_date across deep frame)", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2000, 'Completed'), (1002, 101, 1, '2024-01-01', 3000, 'Completed'),
    (1003, 101, 1, '2024-01-01', 4000, 'Completed');
    """
    c9 = ("Same day transactions broken deterministically by order_id", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 100, 'Completed'), (1002, 101, 1, '2024-01-02', 200, 'Completed'),
    (1003, 101, 1, '2024-01-03', 400, 'Completed'), (1004, 101, 1, '2024-01-04', 800, 'Completed');
    """
    c10 = ("Exponential growth 100% constant percentage change progression", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p4_ten_variants():
    c1 = ("30 orders customer running & rolling analytics baseline", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed');
    """
    c2 = ("Single order boundary (running total = rolling total = amount, count = 1)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed');
    """
    c3 = ("Two orders only (rolling total uses 2 available rows without error)", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 101, 1, '2024-01-03', 3000, 'Completed'), (1004, 101, 1, '2024-01-04', 4000, 'Completed'),
    (1005, 101, 1, '2024-01-05', 5000, 'Completed');
    """
    c4 = ("5 consecutive transactions (rolling 3-order window sliding from [1,2,3] to [3,4,5])", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 101, 1, '2024-01-02', 3000, 'Completed'),
    (1003, 101, 1, '2024-01-03', 4000, 'Completed'), (1004, 101, 1, '2024-01-04', 2000, 'Completed'),
    (1005, 101, 1, '2024-01-05', 1000, 'Completed');
    """
    c5 = ("Strictly decreasing orders (running minimum correctly tracking down to 1000)", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 102, 2, '2024-01-01', 5000, 'Completed'), (1004, 102, 2, '2024-01-02', 6000, 'Completed');
    """
    c6 = ("Two distinct customers (running total and count resetting per customer)", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 3000, 'Cancelled'), (1002, 101, 1, '2024-01-02', 4000, 'Pending'),
    (1003, 101, 1, '2024-01-03', 5000, 'Completed');
    """
    c7 = ("Cancelled and Pending inclusion in cumulative window metrics", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1234.56, 'Completed'), (1002, 101, 1, '2024-01-02', 2345.67, 'Completed'),
    (1003, 101, 1, '2024-01-03', 3456.78, 'Completed');
    """
    c8 = ("Decimal precision rounding validation for rolling averages", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 100, 'Completed'), (1002, 101, 1, '2024-01-02', 100, 'Completed'),
    (1003, 101, 1, '2024-01-03', 100, 'Completed'), (1004, 101, 1, '2024-01-04', 100, 'Completed');
    """
    c9 = ("Constant order amount sequence (rolling average exactly equals amount)", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1004, 101, 1, '2024-01-04', 4000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed'),
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1003, 101, 1, '2024-01-03', 3000, 'Completed');
    """
    c10 = ("Unordered physical rows sorted properly by order_date ASC", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p5_ten_variants():
    c1 = ("Complete 30 orders company-wide timeline baseline", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2000, 'Completed'), (1002, 102, 2, '2024-01-02', 3000, 'Completed'),
    (1003, 103, 3, '2024-01-03', 4000, 'Completed');
    """
    c2 = ("Each order handled by distinct employee (previous employee order all NULL)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Pending'), (1002, 102, 1, '2024-01-02', 2000, 'Cancelled'),
    (1003, 103, 1, '2024-01-03', 1500, 'Pending');
    """
    c3 = ("Employee with zero Completed orders (highest completed amount is NULL, flag 'No')", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Pending'), (1002, 102, 1, '2024-01-02', 3000, 'Completed'),
    (1003, 103, 1, '2024-01-03', 2000, 'Completed');
    """
    c4 = ("Pending order amount higher than completed (running max is 5000, highest completed is 3000)", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 102, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 103, 1, '2024-01-03', 3000, 'Completed');
    """
    c5 = ("Single employee linear increase (highest completed flag only on order 1003)", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 4000, 'Completed'), (1002, 102, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 103, 1, '2024-01-03', 1000, 'Completed');
    """
    c6 = ("Highest completed order is the first transaction (order 1001 flagged 'Yes')", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 102, 2, '2024-01-02', 1000, 'Completed'),
    (1003, 103, 1, '2024-01-03', 2000, 'Completed'), (1004, 104, 2, '2024-01-04', 2000, 'Completed');
    """
    c7 = ("Interleaved employee assignments (verifying global running sum vs employee partition)", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 10000, 'Completed'), (1002, 102, 1, '2024-01-02', 20000, 'Completed'),
    (1003, 103, 1, '2024-01-03', 30000, 'Completed'), (1004, 104, 1, '2024-01-04', 40000, 'Completed');
    """
    c8 = ("High-value cumulative trajectory reaching 100,000", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 102, 1, '2024-01-01', 1000, 'Completed');
    """
    c9 = ("Equal amount orders for same employee (both flagged if tied at highest)", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 500, 'Completed'), (1002, 102, 2, '2024-01-02', 600, 'Pending'),
    (1003, 103, 3, '2024-01-03', 700, 'Cancelled');
    """
    c10 = ("One completed, one pending, one cancelled company-wide sequence", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p6_ten_variants():
    c1 = ("Complete baseline revenue leaderboard across Delhi, Noida, and Gurugram (18 rows)", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 103, 6, '2024-01-02', 5000, 'Completed'),
    (1003, 106, 6, '2024-01-03', 3000, 'Completed');
    """
    c2 = ("Revenue tie at rank 1 in Delhi (both customers must receive rank 1 and be included)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 101, 1, '2024-01-03', 3000, 'Completed'), (1004, 101, 1, '2024-01-04', 4000, 'Completed'),
    (1005, 101, 1, '2024-01-05', 5000, 'Completed');
    """
    c3 = ("Customer with 5 completed orders (verifying exact top-3 cutoff by amount DESC)", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 4000, 'Completed'), (1002, 102, 3, '2024-01-02', 3000, 'Completed'),
    (1003, 103, 6, '2024-01-03', 2000, 'Completed'), (1004, 106, 6, '2024-01-04', 1000, 'Completed');
    """
    c4 = ("Delhi with 3 customers (Dev at rank 2, Sia at rank 3 excluded)", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Pending'), (1002, 101, 1, '2024-01-02', 3000, 'Completed'),
    (1003, 103, 6, '2024-01-03', 4000, 'Completed');
    """
    c5 = ("Pending orders excluded from both customer revenue ranking and top order list", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed'),
    (1003, 101, 1, '2024-01-03', 2000, 'Completed');
    """
    c6 = ("Equal amount orders for customer (tie-breaking by order_date ASC and order_id ASC)", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 104, 10, '2024-01-01', 6000, 'Completed'), (1002, 107, 7, '2024-01-02', 4000, 'Completed');
    """
    c7 = ("Gurugram city isolation test (Ira rank 1, Manav rank 2)", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 108, 8, '2024-01-01', 10000, 'Completed'), (1002, 105, 5, '2024-01-02', 8000, 'Completed'),
    (1003, 102, 3, '2024-01-03', 6000, 'Completed');
    """
    c8 = ("Noida city 3 customers (Aditi rank 1, Neel rank 2, Tanya rank 3 excluded)", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 2000, 'Completed');
    """
    c9 = ("Customer with fewer than 3 orders (returns all available 2 orders cleanly)", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 3000, 'Completed'), (1002, 103, 6, '2024-01-02', 3000, 'Completed'),
    (1003, 106, 6, '2024-01-03', 3000, 'Completed');
    """
    c10 = ("Three-way revenue tie at rank 1 in city (all 3 customers must be included with rank 1)", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p7_ten_variants():
    c1 = ("Complete 8 customer transaction timeline and latest completed status baseline", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2000, 'Completed'), (1002, 101, 1, '2024-01-10', 3000, 'Cancelled');
    """
    c2 = ("Latest order is Cancelled (latest_order_status 'Cancelled' vs latest_completed 1001)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1500, 'Pending');
    """
    c3 = ("Customer with no Completed orders (latest_completed columns are NULL)", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 2500, 'Completed');
    """
    c4 = ("Single Completed order (previous_completed_order_amount is NULL)", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-05', 2000, 'Completed'),
    (1003, 101, 1, '2024-01-10', 3000, 'Completed');
    """
    c5 = ("Three completed orders (latest is 3000, previous completed is 2000)", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-05', 5000, 'Pending'),
    (1003, 101, 1, '2024-01-10', 2000, 'Completed'), (1004, 101, 1, '2024-01-15', 8000, 'Pending');
    """
    c6 = ("Interspersed Pending orders (LAG correctly skipping Pending records)", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 102, 3, '2024-01-02', 2000, 'Completed');
    """
    c7 = ("Two customers each having 1 Completed order", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 101, 1, '2024-01-02', 1500, 'Cancelled'),
    (1003, 101, 1, '2024-01-03', 2000, 'Completed'), (1004, 101, 1, '2024-01-04', 2500, 'Cancelled'),
    (1005, 101, 1, '2024-01-05', 3000, 'Completed');
    """
    c8 = ("Alternating Completed/Cancelled sequence (previous completed is 2000)", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 101, 1, '2024-01-01', 6000, 'Completed');
    """
    c9 = ("Same day orders for single customer (latest order deterministically chosen by order_id)", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0]
    c10 = ("Empty orders table (all 8 customers appear with NULL order history)", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

def get_p8_ten_variants():
    c1 = ("Complete 12 employee sales contribution and departmental revenue baseline", BASE_DATA_SQL, True)
    d2 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed');
    """
    c2 = ("Only one employee with orders (all 11 other employees retain 0 revenue and NULL avg/max)", d2, False)
    d3 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 102, 8, '2024-01-02', 5000, 'Completed');
    """
    c3 = ("Tied Completed revenue in IT (Aarav and Sara share department sales rank 1)", d3, False)
    d4 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 3000, 'Pending'), (1002, 102, 1, '2024-01-02', 4000, 'Cancelled');
    """
    c4 = ("Orders present but zero Completed (verifying count 0, revenue 0, avg NULL, max NULL)", d4, False)
    d5 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 3, '2024-01-01', 2000, 'Completed'), (1002, 102, 6, '2024-01-02', 4000, 'Completed'),
    (1003, 103, 10, '2024-01-03', 6000, 'Completed');
    """
    c5 = ("Sales team 3-tier performance (Myra rank 1, Anaya rank 2, Kabir rank 3)", d5, False)
    d6 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 7, '2024-01-01', 8000, 'Completed');
    """
    c6 = ("HR department solo performer (Reyansh 100% cumulative revenue, Diya 100%)", d6, False)
    d7 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 5, '2024-01-01', 10000, 'Completed');
    """
    c7 = ("Finance department single earner (Ishaan 100%, Vivaan and Kiara tied rank 2)", d7, False)
    d8 = BASE_DATA_SQL.split("INSERT INTO orders")[0]
    c8 = ("Completely empty orders table (all 12 employees must appear with 0 orders and 100% cumulative)", d8, False)
    d9 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 1000, 'Completed'), (1002, 102, 4, '2024-01-02', 2000, 'Completed'),
    (1003, 103, 8, '2024-01-03', 3000, 'Completed'), (1004, 104, 11, '2024-01-04', 4000, 'Completed');
    """
    c9 = ("All 4 IT employees having completed orders (verifying 4-tier cumulative progression)", d9, False)
    d10 = BASE_DATA_SQL.split("INSERT INTO orders")[0] + """
    INSERT INTO orders (order_id, customer_id, emp_id, order_date, amount, status) VALUES
    (1001, 101, 1, '2024-01-01', 5000, 'Completed'), (1002, 102, 3, '2024-01-02', 5000, 'Completed');
    """
    c10 = ("Balanced inter-departmental completed orders (IT and Sales each have active orders)", d10, False)
    return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

# ─────────────────────────────────────────────────────────────────────────────
# Markdown Descriptions
# ─────────────────────────────────────────────────────────────────────────────

DESC_30 = """# **Problem 1. Employee Salary Ranking and Distribution Report**

**Difficulty:** Hard  
**Concepts:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`, `PERCENT_RANK()`, `CUME_DIST()`, `NTH_VALUE()`

---

### **Problem Statement**
The Human Resources analytics team of a multinational organization wants to develop a comprehensive employee salary ranking system.

The organization employs individuals across several departments, and management wants to evaluate employee compensation both at the organizational level and within individual departments.

The HR team wants to identify the highest-paid employees, determine salary rankings, divide employees into salary groups and calculate the relative salary distribution within each department.

Management also wants to identify the second-highest-paid employees in every department. In departments where multiple employees receive the same salary, all employees sharing the second-highest salary rank must be included.

Additionally, the company wants to compare employees based on their joining dates and identify the third-highest salary within each department.

---

### **Requirements**
1. Display employee ID, employee name, department, and salary.
2. Assign a unique global row number to every employee using `ROW_NUMBER()`, ordered by salary in descending order. In case of equal salaries, use employee ID in ascending order as a tie-breaker.
3. Calculate the global salary rank using `RANK()`. Employees earning equal salaries must receive the same rank, and subsequent ranks must contain gaps.
4. Calculate salary rank within each department using `DENSE_RANK()`, without leaving gaps after tied salaries.
5. Identify employees whose salary rank within their department is among the top three. Display a descriptive flag (`'Yes'` or `'No'`).
6. Identify employees whose department-wise dense rank equals 2 (`'Yes'` or `'No'`). Include all employees tied at the second-highest salary.
7. Divide all employees into four salary groups using `NTILE(4)`, ordered by salary in descending order and employee ID ascending.
8. Assign a separate row number to employees according to joining date in ascending order (`joining_date_row_number`), breaking ties with `emp_id`.
9. Calculate `PERCENT_RANK()` for every employee based on salary in ascending order within their department, rounded to 2 decimal places.
10. Calculate `CUME_DIST()` for employees based on salary in ascending order within their department, rounded to 2 decimal places.
11. Use `NTH_VALUE()` to display the third-highest salary within each department on every employee row (`ORDER BY salary DESC, emp_id ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`). If the department contains fewer than three employees, display NULL.
12. Sort the final result by `salary_row_number` ascending.

---

### **Output Format**
| Column | Description |
|---|---|
| `emp_id` | Employee ID |
| `emp_name` | Employee name |
| `department` | Employee department |
| `salary` | Employee salary |
| `salary_row_number` | Global unique salary sequence |
| `salary_rank_global` | Global salary rank |
| `department_dense_rank` | Salary rank within department |
| `salary_quartile` | Salary group from 1 to 4 |
| `joining_date_row_number` | Joining date sequence |
| `top_three_in_department` | Whether employee is in top 3 ranks (`'Yes'` / `'No'`) |
| `second_highest_in_department` | Whether employee has rank 2 (`'Yes'` / `'No'`) |
| `percent_rank_in_department` | Relative salary ranking within department |
| `cume_dist_in_department` | Cumulative distribution within department |
| `third_highest_salary_in_department` | Third-highest department salary |
"""

DESC_31 = """# **Problem 2. Department Salary Analytics**

**Difficulty:** Hard  
**Concepts:** `AVG() OVER()`, `SUM() OVER()`, `MIN() OVER()`, `MAX() OVER()`, `ROWS BETWEEN`

---

### **Problem Statement**
The finance department wants to conduct a detailed compensation analysis to understand the salary distribution and payroll expenditure across different departments.

Management wants an employee-level report that compares every employee's salary with their department's average and total salary expenditure.

The company also wants to understand the proportion of departmental payroll contributed by each employee and how salary contributions accumulate when employees are arranged from highest-paid to lowest-paid.

Additionally, the HR department wants to monitor salary accumulation according to employee joining dates to understand how departmental payroll has developed over time.

---

### **Requirements**
1. Display employee ID, employee name, department, and salary.
2. Display the average salary of each employee's department using `AVG() OVER (PARTITION BY department)`, rounded to 2 decimal places.
3. Display the total salary expenditure of the employee's department using `SUM() OVER (PARTITION BY department)`.
4. Display the minimum salary in the employee's department using `MIN() OVER (PARTITION BY department)`.
5. Display the maximum salary in the employee's department using `MAX() OVER (PARTITION BY department)`.
6. Calculate the difference between the employee's salary and their department's average salary (`salary - department_avg`), rounded to 2 decimal places.
7. Calculate each employee's percentage contribution to the total departmental salary (`salary * 100.0 / department_total`), rounded to 2 decimal places.
8. Calculate a running salary total within each department ordered by joining date ascending and employee ID ascending.
9. Calculate the cumulative percentage contribution of salary within each department, ordered by salary descending and employee ID ascending (`running_sum * 100.0 / department_total`), rounded to 2 decimal places.
10. Identify whether an employee earns strictly more than the average salary of their department (`'Yes'` or `'No'`).
11. Sort the result by `department ASC`, `salary DESC`, and `emp_id ASC`.
"""

DESC_32 = """# **Problem 3. Customer Order History and Navigation Analytics**

**Difficulty:** Hard  
**Concepts:** `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, `NTH_VALUE()`, Window Frames

---

### **Problem Statement**
An e-commerce company wants to develop an advanced customer order history system to understand how individual customers change their purchasing behavior over time.

The sales analytics team wants to monitor every customer's order amount, identify increases and decreases between consecutive orders, and determine the first and last order values recorded for each customer.

Management also wants to display the previous and next order amounts for every transaction to understand how customer purchasing activity changes throughout the year.

---

### **Requirements**
1. Display order ID, customer ID, customer name, order date, amount, and status. Include all order statuses (`Completed`, `Pending`, `Cancelled`).
2. Use `LAG()` to display the previous order amount for the same customer chronologically (`ORDER BY order_date ASC, order_id ASC`).
3. Use `LEAD()` to display the next order amount for the same customer chronologically.
4. Calculate the difference between the current order amount and the previous order amount (`amount - previous_amount`). Display `0` when no previous order exists.
5. Calculate the percentage change compared with the previous order (`(current - previous) * 100.0 / previous`), rounded to 2 decimal places. Display `NULL` when no previous order exists.
6. Create a flag indicating whether the current order amount is greater than the previous order amount (`'Yes'` or `'No'`).
7. Use `FIRST_VALUE()` to display the first order amount for every customer across their full history.
8. Use `LAST_VALUE()` with `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to display the last order amount for every customer.
9. Display minimum, maximum, and average order amounts for each customer using aggregate window functions. Round the average to 2 decimal places.
10. Use `NTH_VALUE()` to display the second chronological order amount for every customer.
11. Display the first and latest order dates alongside every order using `FIRST_VALUE()` and `LAST_VALUE()`.
12. Sort the result by `customer_id ASC`, `order_date ASC`, and `order_id ASC`.
"""

DESC_33 = """# **Problem 4. Customer Running Total and Rolling Purchase Analysis**

**Difficulty:** Hard  
**Concepts:** `SUM() OVER()`, `AVG() OVER()`, `MIN() OVER()`, `COUNT() OVER()`, `ROWS BETWEEN`

---

### **Problem Statement**
A retail organization wants to develop a customer purchasing analytics system that monitors the progression of customer spending over time.

The company wants to understand how much each customer has spent cumulatively after every transaction and how their purchases have changed over the most recent three orders.

The sales analytics team has decided to calculate running totals, rolling averages, rolling totals, minimum transaction amounts and transaction counts for every customer.

---

### **Requirements**
1. Display order ID, customer ID, customer name, order date, and order amount. Include all order statuses.
2. Calculate a running total of order amounts for each customer from the first transaction up to the current transaction (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).
3. Calculate a rolling three-order total consisting of the current order and up to two immediately preceding orders (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`).
4. Calculate a rolling average over the same three-order window, rounded to 2 decimal places.
5. Calculate the running minimum order amount for each customer up to and including the current order.
6. Calculate the running count of orders for each customer up to and including the current order.
7. Partition all calculations by `customer_id` and order chronologically by `order_date ASC, order_id ASC`.
8. Sort the final output by `customer_id ASC`, `order_date ASC`, and `order_id ASC`.
"""

DESC_34 = """# **Problem 5. Company-Wide Order Timeline and Employee Sales Performance**

**Difficulty:** Hard  
**Concepts:** `LAG()`, Global `SUM() OVER()`, Employee `MAX() OVER()`, Conditional Window Functions

---

### **Problem Statement**
A growing e-commerce company wants to build a centralized sales monitoring system to understand its transaction history and employee-level sales performance.

The sales operations team wants to examine how the company's total transaction amount changes over time. At the same time, management wants to analyze how individual employees handle orders and identify their highest-value transactions.

---

### **Requirements**
1. Retrieve order ID, order date, customer ID, employee ID, employee name, order amount, and order status.
2. Calculate the company-wide running total of all order amounts across every employee ordered by `order_date ASC, order_id ASC`. Include all order statuses.
3. Use `LAG()` to display the previous order amount handled by the same employee (`PARTITION BY emp_id ORDER BY order_date ASC, order_id ASC`).
4. Calculate the running maximum order amount handled by each employee up to and including the current order (`PARTITION BY emp_id`).
5. Calculate the highest Completed order amount handled by each employee across their entire history (`status = 'Completed'`).
6. Create a flag `is_employee_highest_completed_order` (`'Yes'` or `'No'`) that identifies whether the current order is the employee's highest-value Completed order.
7. Sort the complete result chronologically by `order_date ASC` and `order_id ASC`.
"""

DESC_35 = """# **Problem 6. Customer Revenue Leaderboard and Top Transaction Selection**

**Difficulty:** Hard  
**Concepts:** Common Table Expressions (CTEs), `RANK()`, `ROW_NUMBER()`, Multi-Level Window Filtering

---

### **Problem Statement**
An e-commerce company wants to identify its most valuable customers in every city based on their completed transaction history.

The sales management team wants to generate a city-wise customer leaderboard that ranks customers according to the total value of their Completed orders.

Management also wants to examine the largest individual transactions made by each eligible customer (top 3 completed orders).

---

### **Requirements**
1. Calculate the total Completed order amount for every customer (`status = 'Completed'`). Exclude Pending and Cancelled orders.
2. Join the `customers` table to obtain the customer's city.
3. Use `RANK()` to rank customers within each city based on completed revenue in descending order (`customer_rank_in_city`).
4. Include customers whose city-wise rank is 1 or 2 (including all ties at rank 2).
5. For every eligible customer, rank their individual Completed orders using `ROW_NUMBER()` ordered by `amount DESC, order_date ASC, order_id ASC` (`order_rank_for_customer`).
6. Display only the top three Completed orders for every eligible customer (`order_rank_for_customer <= 3`).
7. Retrieve `customer_id`, `customer_name`, `city`, `completed_order_total`, `customer_rank_in_city`, `order_rank_for_customer`, `order_id`, `order_date`, `order_amount`, and `handled_by_employee` (`emp_name`).
8. Sort the final output by `city ASC`, `customer_rank_in_city ASC`, `customer_id ASC`, and `order_rank_for_customer ASC`.
"""

DESC_36 = """# **Problem 7. Customer Latest Order and Completed Transaction History**

**Difficulty:** Hard  
**Concepts:** `ROW_NUMBER()`, `LAG()`, CTEs, Multi-Stream Sequence Analysis

---

### **Problem Statement**
An e-commerce organization wants to create a customer order status monitoring system to track each customer's transaction history and identify their latest activities.

The customer support team needs a report containing the earliest order date, the latest overall order, and the most recent Completed order for every customer.

An important distinction must be maintained between the latest order (any status) and the latest Completed order.

---

### **Requirements**
1. Return exactly one record per customer for all registered customers.
2. Display `customer_id`, `customer_name`, and `city`.
3. Display the earliest order date (`first_order_date`) and latest overall order date (`latest_order_date`) for each customer.
4. Display the latest overall order ID, amount, and status (`latest_order_id`, `latest_order_amount`, `latest_order_status`).
5. In a separate Completed-order sequence, use `LAG()` to identify the previous Completed order amount.
6. Display the latest Completed order ID, date, and amount (`latest_completed_order_id`, `latest_completed_order_date`, `latest_completed_order_amount`).
7. Display the amount of the previous Completed order (`previous_completed_order_amount`).
8. If a customer has no completed orders, display `NULL` for completed order fields.
9. Sort the final result by `customer_id ASC`.
"""

DESC_37 = """# **Problem 8. Employee Sales Contribution and Department Revenue Ranking**

**Difficulty:** Hard  
**Concepts:** `LEFT JOIN`, `RANK()`, `DENSE_RANK()`, Cumulative Window Calculations, `COALESCE`

---

### **Problem Statement**
The senior management team wants to evaluate employee-level sales contributions and compare the performance of employees belonging to different departments.

Management wants to ensure that employees without Completed orders are not removed from the report. Such employees must remain visible with a completed order count of zero and completed revenue of zero.

---

### **Requirements**
1. Start with the `employees` table and use `LEFT JOIN` on `orders` to retain all employees.
2. Calculate the number of Completed orders handled by each employee (`completed_order_count`).
3. Calculate the total Completed order amount handled by each employee (`completed_revenue`), defaulting to 0 via `COALESCE`.
4. Calculate the average Completed order amount for each employee, rounded to 2 decimal places (or `NULL` if no completed orders).
5. Calculate the highest Completed order amount handled by each employee (or `NULL` if no completed orders).
6. Use `RANK()` to rank employees within their respective departments based on `completed_revenue DESC` (`department_sales_rank`).
7. Use `DENSE_RANK()` to calculate department-wise revenue ranking without gaps (`department_sales_dense_rank`).
8. Calculate the cumulative department revenue percentage: running sum of employee completed revenue within the department divided by total departmental completed revenue (`running_sum * 100.0 / dept_total_revenue`), rounded to 2 decimal places. Break ties deterministically with `emp_id ASC`.
9. If a department has 0 total completed revenue, display `100.00` for cumulative percentage.
10. Return exactly one record per employee.
11. Sort the result by `department ASC`, `completed_revenue DESC`, and `emp_id ASC`.
"""

# ─────────────────────────────────────────────────────────────────────────────
# Execution & Packaging
# ─────────────────────────────────────────────────────────────────────────────

def build_all_new_questions():
    problems_def = [
        (30, "Employee Salary Ranking and Distribution Report", "Hard", 35,
         "Ranking & Distribution (ROW_NUMBER, RANK, NTILE, CUME_DIST)",
         ["SQL", "Window Functions", "ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE", "PERCENT_RANK", "CUME_DIST", "NTH_VALUE"],
         DESC_30, QUERY_30, get_p1_ten_variants()),
        (31, "Department Salary Analytics", "Hard", 35,
         "Aggregate Window Functions & Frames",
         ["SQL", "Window Functions", "SUM OVER", "AVG OVER", "MIN/MAX OVER", "Running Total", "Window Frames"],
         DESC_31, QUERY_31, get_p2_ten_variants()),
        (32, "Customer Order History and Navigation Analytics", "Hard", 35,
         "Navigation & Value Functions (LAG, LEAD, FIRST_VALUE, LAST_VALUE)",
         ["SQL", "Window Functions", "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE", "Percentage Change"],
         DESC_32, QUERY_32, get_p3_ten_variants()),
        (33, "Customer Running Total and Rolling Purchase Analysis", "Hard", 35,
         "Window Frames & Rolling Calculations (ROWS BETWEEN)",
         ["SQL", "Window Functions", "Running Total", "Rolling Average", "ROWS BETWEEN", "Running Min", "Running Count"],
         DESC_33, QUERY_33, get_p4_ten_variants()),
        (34, "Company-Wide Order Timeline and Employee Sales Performance", "Hard", 35,
         "Multi-Partition Timeline & Running Aggregates",
         ["SQL", "Window Functions", "LAG", "Global Running SUM", "Running MAX", "Conditional MAX"],
         DESC_34, QUERY_34, get_p5_ten_variants()),
        (35, "Customer Revenue Leaderboard and Top Transaction Selection", "Hard", 35,
         "Leaderboard & Partitioned Top-N Selection (CTE, RANK, ROW_NUMBER)",
         ["SQL", "Window Functions", "CTE", "RANK", "ROW_NUMBER", "Top-N", "Partition Filtering"],
         DESC_35, QUERY_35, get_p6_ten_variants()),
        (36, "Customer Latest Order and Completed Transaction History", "Hard", 35,
         "Event Slicing & Sequence Isolation (ROW_NUMBER, LAG, CTE)",
         ["SQL", "Window Functions", "ROW_NUMBER", "LAG", "CTE", "Status Isolation", "Latest Record"],
         DESC_36, QUERY_36, get_p7_ten_variants()),
        (37, "Employee Sales Contribution and Department Revenue Ranking", "Hard", 35,
         "LEFT JOIN, Ranking & Cumulative Revenue Percentage",
         ["SQL", "Window Functions", "LEFT JOIN", "RANK", "DENSE_RANK", "Cumulative Percentage", "COALESCE"],
         DESC_37, QUERY_37, get_p8_ten_variants())
    ]

    new_questions = []

    for qid, title, diff, pts, subtopic, tags, desc, query, variants in problems_def:
        print(f"\nProcessing Q{qid}: {title}...")
        test_cases = build_test_cases(query, variants)
        sample_cols, sample_rows = run_query(query, BASE_DATA_SQL)
        sample_output_str = format_table(sample_cols, sample_rows[:8])

        # Self-test: verify canonical query against all 10 test cases!
        for tc in test_cases:
            conn = create_connection(SCHEMA_SQL, tc["testData"])
            exec_res = execute_query(conn, query)
            conn.close()
            matched, reason = compare_sql_results(
                exec_res["columns"], exec_res["rows"],
                tc["expectedColumns"], tc["expectedRows"],
                order_sensitive=tc["orderSensitive"]
            )
            if not matched:
                raise Exception(f"Validation FAILED for Q{qid} Case {tc['id']}: {reason}")

        print(f"  All {len(test_cases)}/10 test cases PASSED (100% verification)!")

        q_obj = {
            "id": qid,
            "title": title,
            "difficulty": diff,
            "points": pts,
            "track": "SQL",
            "category": "Window Functions",
            "subtopic": subtopic,
            "tags": tags,
            "description": desc,
            "type": "sql",
            "tableSchema": SCHEMA_SQL.strip(),
            "testData": BASE_DATA_SQL.strip(),
            "sampleInput": "Standard window_function_lab database (12 Employees, 8 Customers, 30 Orders)",
            "sampleOutput": sample_output_str,
            "boilerplate": "-- Write your SQL window function query here\n",
            "testCases": test_cases
        }
        new_questions.append(q_obj)

    return new_questions

if __name__ == "__main__":
    new_qs = build_all_new_questions()
    
    with open("data/questions.json", "r") as f:
        existing_qs = json.load(f)
    
    existing_qs = [q for q in existing_qs if q["id"] < 30]
    existing_qs.extend(new_qs)

    with open("data/questions.json", "w") as f:
        json.dump(existing_qs, f, indent=2)

    total_testcases = sum(len(q["testCases"]) for q in new_qs)
    print(f"\nSuccessfully saved {len(existing_qs)} total questions in data/questions.json!")
    print(f"Added {len(new_qs)} new window function questions with {total_testcases} verified test cases!")
