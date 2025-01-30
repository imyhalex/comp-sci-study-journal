# Quick SQL Cheatsheet

A quick reminder of all relevant SQL queries and examples on how to use them. 

This repository is constantly being updated and added to by the community. 
Pull requests are welcome. Enjoy!

# Table of Contents 
1. [ Finding Data Queries. ](#find)
2. [ Data Modification Queries. ](#modify)
3. [ Reporting Queries. ](#report)
4. [ Join Queries. ](#joins)
5. [ View Queries. ](#view)
6. [ Altering Table Queries.](#alter)
7. [ Creating Table Query.](#create)

<a name="find"></a>
# 1. Finding Data Queries

### **SELECT**: used to select data from a database
* `SELECT` * `FROM` table_name;

### **DISTINCT**: filters away duplicate values and returns rows of specified column
* `SELECT DISTINCT` column_name;

### **WHERE**: used to filter records/rows
* `SELECT` column1, column2 `FROM` table_name `WHERE` condition;
* `SELECT` * `FROM` table_name `WHERE` condition1 `AND` condition2;
* `SELECT` * `FROM` table_name `WHERE` condition1 `OR` condition2;
* `SELECT` * `FROM` table_name `WHERE NOT` condition;
* `SELECT` * `FROM` table_name `WHERE` condition1 `AND` (condition2 `OR` condition3);
* `SELECT` * `FROM` table_name `WHERE EXISTS` (`SELECT` column_name `FROM` table_name `WHERE` condition);

### **ORDER BY**: used to sort the result-set in ascending or descending order
* `SELECT` * `FROM` table_name `ORDER BY` column;
* `SELECT` * `FROM` table_name `ORDER BY` column `DESC`;
* `SELECT` * `FROM` table_name `ORDER BY` column1 `ASC`, column2 `DESC`;

### **SELECT TOP**: used to specify the number of records to return from top of table
* `SELECT TOP` number columns_names `FROM` table_name `WHERE` condition;
* `SELECT TOP` percent columns_names `FROM` table_name `WHERE` condition;
* Not all database systems support `SELECT TOP`. The MySQL equivalent is the `LIMIT` clause
* `SELECT` column_names `FROM` table_name `LIMIT` offset, count;

### **LIKE**: operator used in a WHERE clause to search for a specific pattern in a column
* % (percent sign) is a wildcard character that represents zero, one, or multiple characters
* _ (underscore) is a wildcard character that represents a single character
* `SELECT` column_names `FROM` table_name `WHERE` column_name `LIKE` pattern;
* `LIKE` ‘a%’ (find any values that start with “a”)
* `LIKE` ‘%a’ (find any values that end with “a”)
* `LIKE` ‘%or%’ (find any values that have “or” in any position)
* `LIKE` ‘_r%’ (find any values that have “r” in the second position)
* `LIKE` ‘a_%_%’ (find any values that start with “a” and are at least 3 characters in length)
* `LIKE` ‘[a-c]%’ (find any values starting with “a”, “b”, or “c”

### **IN**: operator that allows you to specify multiple values in a WHERE clause
* essentially the IN operator is shorthand for multiple OR conditions
* `SELECT` column_names `FROM` table_name `WHERE` column_name `IN` (value1, value2, …);
* `SELECT` column_names `FROM` table_name `WHERE` column_name `IN` (`SELECT STATEMENT`);

### **BETWEEN**: operator selects values within a given range inclusive
* `SELECT` column_names `FROM` table_name `WHERE` column_name `BETWEEN` value1 `AND` value2;
* `SELECT` * `FROM` Products `WHERE` (column_name `BETWEEN` value1 `AND` value2) `AND NOT` column_name2 `IN` (value3, value4);
* `SELECT` * `FROM` Products `WHERE` column_name `BETWEEN` #01/07/1999# AND #03/12/1999#;

### **NULL**: values in a field with no value
* `SELECT` * `FROM` table_name `WHERE` column_name `IS NULL`;
* `SELECT` * `FROM` table_name `WHERE` column_name `IS NOT NULL`;

### **AS**: aliases are used to assign a temporary name to a table or column
* `SELECT` column_name `AS` alias_name `FROM` table_name;
* `SELECT` column_name `FROM` table_name `AS` alias_name;
* `SELECT` column_name `AS` alias_name1, column_name2 `AS` alias_name2;
* `SELECT` column_name1, column_name2 + ‘, ‘ + column_name3 `AS` alias_name;

### **UNION**: set operator used to combine the result-set of two or more SELECT statements
* Each SELECT statement within UNION must have the same number of columns
* The columns must have similar data types
* The columns in each SELECT statement must also be in the same order
* `SELECT` columns_names `FROM` table1 `UNION SELECT` column_name `FROM` table2;
* `UNION` operator only selects distinct values, `UNION ALL` will allow duplicates

### **INTERSECT**: set operator which is used to return the records that two SELECT statements have in common
* Generally used the same way as **UNION** above
* `SELECT` columns_names `FROM` table1 `INTERSECT SELECT` column_name `FROM` table2;

### **EXCEPT**: set operator used to return all the records in the first SELECT statement that are not found in the second SELECT statement
* Generally used the same way as **UNION** above
* `SELECT` columns_names `FROM` table1 `EXCEPT SELECT` column_name `FROM` table2;

### **ANY|ALL**: operator used to check subquery conditions used within a WHERE or HAVING clauses
* The `ANY` operator returns true if any subquery values meet the condition
* The `ALL` operator returns true if all subquery values meet the condition
* `SELECT` columns_names `FROM` table1 `WHERE` column_name operator (`ANY`|`ALL`) (`SELECT` column_name `FROM` table_name `WHERE` condition);

### **GROUP BY**: statement often used with aggregate functions (COUNT, MAX, MIN, SUM, AVG) to group the result-set by one or more columns
* `SELECT` column_name1, COUNT(column_name2) `FROM` table_name `WHERE` condition `GROUP BY` column_name1 `ORDER BY` COUNT(column_name2) DESC;

### **HAVING**: this clause was added to SQL because the WHERE keyword could not be used with aggregate functions
* `SELECT` `COUNT`(column_name1), column_name2 `FROM` table `GROUP BY` column_name2 `HAVING` `COUNT(`column_name1`)` > 5;
> __used based on the result of aggregated functions__, and HAVING keyword shold be placed after GROUP BY and before ORDER BY
### **WITH**: often used for retrieving hierarchical data or re-using temp result set several times in a query. Also referred to as "Common Table Expression"
* `WITH RECURSIVE` cte `AS` (<br/>
    &nbsp;&nbsp;`SELECT` c0.* `FROM` categories `AS` c0 `WHERE` id = 1 `# Starting point`<br/>
    &nbsp;&nbsp;`UNION ALL`<br/>
    &nbsp;&nbsp;`SELECT` c1.* `FROM` categories `AS` c1 `JOIN` cte `ON` c1.parent_category_id = cte.id<br/>
  )<br/>
  `SELECT` *<br/>
  `FROM` cte


<a name="modify"></a>
# 2. Data Modification Queries

### **INSERT INTO**: used to insert new records/rows in a table
* `INSERT INTO` table_name (column1, column2) `VALUES` (value1, value2);
* `INSERT INTO` table_name `VALUES` (value1, value2 …);

### **UPDATE**: used to modify the existing records in a table
* `UPDATE` table_name `SET` column1 = value1, column2 = value2 `WHERE` condition;
* `UPDATE` table_name `SET` column_name = value;

### **DELETE**: used to delete existing records/rows in a table
* `DELETE FROM` table_name `WHERE` condition;
* `DELETE` * `FROM` table_name;

<a name="report"></a>
# 3. Reporting Queries

### **COUNT**: returns the # of occurrences
* `SELECT COUNT (DISTINCT` column_name`)`;
> What is counted as a distinct value depends on the column’s collation. For example, with the default column collation of %SQLUPPER, values that differ in letter case are not counted as distinct values. To count every letter-case variant as a distinct value, use COUNT(DISTINCT(%EXACT(expression))). __NULL values are not included in COUNT DISTINCT counts.__

___COUNT(*) returns the number of rows in the table or view. COUNT(*) counts all rows, including ones that contain duplicate column values or NULL values.___
```sql
SELECT COUNT(*) FROM Sample.Person;
```
___COUNT(expression) returns the number of values in expression, which is a table column name or an expression that evaluates to a column of data. COUNT(expression) does not count NULL values.___
```sql
SELECT COUNT(Name) AS TotalNames FROM Sample.Person;
```

### **MIN() and MAX()**: returns the smallest/largest value of the selected column
* `SELECT MIN (`column_names`) FROM` table_name `WHERE` condition;
* `SELECT MAX (`column_names`) FROM` table_name `WHERE` condition;

### **AVG()**: returns the average value of a numeric column
* `SELECT AVG (`column_name`) FROM` table_name `WHERE` condition;

### **SUM()**: returns the total sum of a numeric column
* `SELECT SUM (`column_name`) FROM` table_name `WHERE` condition;

<a name="joins"></a>
# 4. Join Queries

###  **INNER JOIN**: returns records that have matching value in both tables
* `SELECT` column_names `FROM` table1 `INNER JOIN` table2 `ON` table1.column_name=table2.column_name;
* `SELECT` table1.column_name1, table2.column_name2, table3.column_name3 `FROM` ((table1 `INNER JOIN` table2 `ON` relationship) `INNER JOIN` table3 `ON` relationship);

### **LEFT (OUTER) JOIN**: returns all records from the left table (table1), and the matched records from the right table (table2)
* `SELECT` column_names `FROM` table1 `LEFT JOIN` table2 `ON` table1.column_name=table2.column_name;

### **RIGHT (OUTER) JOIN**: returns all records from the right table (table2), and the matched records from the left table (table1)
* `SELECT` column_names `FROM` table1 `RIGHT JOIN` table2 `ON` table1.column_name=table2.column_name;

### **FULL (OUTER) JOIN**: returns all records when there is a match in either left or right table
* `SELECT` column_names `FROM` table1 ``FULL OUTER JOIN`` table2 `ON` table1.column_name=table2.column_name;

### **Self JOIN**: a regular join, but the table is joined with itself
* `SELECT` column_names `FROM` table1 T1, table1 T2 `WHERE` condition;

<a name="view"></a>
# 5. View Queries

### **CREATE**: create a view
* `CREATE VIEW` view_name `AS SELECT` column1, column2 `FROM` table_name `WHERE` condition;

### **SELECT**: retrieve a view
* `SELECT` * `FROM` view_name;

### **DROP**: drop a view
* `DROP VIEW` view_name;

<a name="alter"></a>
# 6. Altering Table Queries

### **ADD**: add a column
* `ALTER TABLE` table_name `ADD` column_name column_definition;

### **MODIFY**: change data type of column
* `ALTER TABLE` table_name `MODIFY` column_name column_type;

### **DROP**: delete a column
* `ALTER TABLE` table_name `DROP COLUMN` column_name;

<a name="create"></a>
# 7. Creating Table Query

### **CREATE**: create a table
* `CREATE TABLE` table_name `(` <br />
   `column1` `datatype`, <br />
   `column2` `datatype`, <br />
   `column3` `datatype`, <br />
   `column4` `datatype`, <br />
   `);`
  
### Window Functions[[Link](https://www.geeksforgeeks.org/window-functions-in-sql/)]


### Common Table Expression[[Link](https://www.geeksforgeeks.org/cte-in-sql/)]

# Window Functions cheat sheet from ChatGPT:

## 1. Introduction to Window Functions

- **Window functions** allow you to perform calculations across rows that are somehow related to the current row, without collapsing the result set (unlike `GROUP BY`).
- Typical usage:
  ```sql
  function_name([arguments]) OVER (
      [PARTITION BY partition_expression, ...]
      [ORDER BY sort_expression, ...]
      [frame_clause]
  )
  ```
- **Frame clause** (optional) defines which set of rows in a partition is used for the calculation. Common frame clauses:
  - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
  - `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`
  - `RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`
  - etc.

---

## 2. Basic Syntax Components

1. **PARTITION BY**: Groups rows (similar to GROUP BY), but without merging them into a single row.
2. **ORDER BY**: Sorts rows within each partition. Often required for functions like `ROW_NUMBER()`, `LAG()`, etc.
3. **Frame clause**:
   - **ROWS** vs. **RANGE**:
     - `ROWS`: Physical offsets of rows (e.g., the last 10 rows).
     - `RANGE`: Logical offset based on values of the ordering column(s) (e.g., up to and including the current row’s value in a sorted sense).
   - **UNBOUNDED PRECEDING**: Start from the first row in the partition.
   - **UNBOUNDED FOLLOWING**: Go to the last row in the partition.
   - **CURRENT ROW**: The row being evaluated.
   - **N PRECEDING / N FOLLOWING**: A specific number of rows before or after the current row in the partition.

---

## 3. Common Window Functions

1. **Aggregate Functions** (e.g., `SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) used with an `OVER()` clause:
   ```sql
   SUM(column) OVER (PARTITION BY ... ORDER BY ... frame_clause)
   ```
2. **Ranking Functions**:
   - `ROW_NUMBER() OVER (...)` – continuous, no ties.
   - `RANK() OVER (...)` – gaps in ranking on ties.
   - `DENSE_RANK() OVER (...)` – no gaps on ties.
   - `NTILE(n) OVER (...)` – divides rows into `n` groups.
3. **Value Functions**:
   - `LAG(value, [offset], [default]) OVER (...)` – gets the value in a prior row.
   - `LEAD(value, [offset], [default]) OVER (...)` – gets the value in a future row.
   - `FIRST_VALUE(value) OVER (...)` – gets the first value from the frame.
   - `LAST_VALUE(value) OVER (...)` – gets the last value from the frame.

---

## 4. Examples

### 4.1 Running Total (Cumulative SUM)

**Goal**: Calculate a running total of `sales_amount` per customer in chronological order.

```sql
SELECT
    customer_id,
    order_date,
    sales_amount,
    SUM(sales_amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales
ORDER BY customer_id, order_date;
```

**Explanation**:
- `PARTITION BY customer_id`: Each customer has their own running total.
- `ORDER BY order_date`: Sorts rows by date for each customer.
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: For each row, sum all previous rows (including the current) in the partition.

---

### 4.2 Rolling 7-Day Moving Average (Time-based)

**Goal**: For each date, compute the average of the `daily_value` for the 7 previous days (inclusive).

```sql
SELECT
    date_col,
    daily_value,
    AVG(daily_value) OVER (
        ORDER BY date_col
        RANGE BETWEEN '7 days' PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg
FROM daily_metrics
ORDER BY date_col;
```

**Explanation**:
- `RANGE BETWEEN '7 days' PRECEDING AND CURRENT ROW`: Uses a range of dates (7 days before to current date). 
- This requires an **ORDER BY** column that’s typed as date/time.  
- Note: `RANGE` is based on value comparisons (date or timestamp), not row counts.

---

### 4.3 Rolling 3-Row Sum

**Goal**: Sum the current row’s value and the two previous rows’ values (by order).

```sql
SELECT
    id,
    value,
    SUM(value) OVER (
        ORDER BY id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_3row_sum
FROM your_table
ORDER BY id;
```

**Explanation**:
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`: For each row, look at that row plus the 2 preceding rows in the ordering.

---

### 4.4 Ranking Rows

**Goal**: Assign a ranked order to rows within partitions. Example: rank employees by salary within each department.

```sql
SELECT
    department_id,
    employee_id,
    salary,
    RANK() OVER (
        PARTITION BY department_id
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees
ORDER BY department_id, salary DESC;
```

**Explanation**:
- `PARTITION BY department_id`: Restart ranking for each department.
- `ORDER BY salary DESC`: Higher salaries get rank 1, ties have the same rank, then skip rank number(s).

---

### 4.5 Finding Differences Between Rows with `LAG`

**Goal**: Compare a row’s value to the previous row’s value to find a difference.

```sql
SELECT
    id,
    date_col,
    value,
    LAG(value, 1, 0) OVER (ORDER BY date_col) AS prev_value,
    (value - LAG(value, 1, 0) OVER (ORDER BY date_col)) AS value_diff
FROM daily_metrics
ORDER BY date_col;
```

**Explanation**:
- `LAG(value, 1, 0)`: Looks at the previous row’s `value`. If there is no previous row, use `0`.
- `value_diff`: Subtracts the lagged value from the current value.

---

### 4.6 First and Last Values Within a Frame

**Goal**: Identify the earliest and latest prices each day within a time-based frame (e.g., trading day).

```sql
SELECT
    trade_date,
    trade_time,
    price,
    FIRST_VALUE(price) OVER (
        PARTITION BY trade_date
        ORDER BY trade_time
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS opening_price,
    LAST_VALUE(price) OVER (
        PARTITION BY trade_date
        ORDER BY trade_time
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS closing_price
FROM trades
ORDER BY trade_date, trade_time;
```

**Explanation**:
- `FIRST_VALUE(price)` / `LAST_VALUE(price)`: Return the first/last row in the partition’s frame.
- `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`: Expand the window to the entire partition (i.e., entire day).

> **Tip**: By default, `FIRST_VALUE` and `LAST_VALUE` limit themselves to the **current** frame. You often need to set the frame to `UNBOUNDED` if you want the entire partition.

---

## 5. Notes on Performance & Usability

1. **Index usage**: While `ORDER BY` in window functions does not necessarily use the same index as a top-level `ORDER BY`, having an index on the sort column can help the planner.
2. **Memory considerations**: For large partitions, consider that the entire partition might be processed in memory.
3. **Frame definition**: Carefully choose `ROWS` vs. `RANGE`. `ROWS` is more predictable if you want a fixed number of preceding/following rows. `RANGE` is useful for time-series or value-based boundaries.
4. **Filtering**: If you need post-aggregation filtering on window calculations, you can’t use a simple `WHERE` clause on a window function directly (window functions are computed after `WHERE`). Instead, use a subquery or a **common table expression (CTE)**.

---

## 6. Quick Reference Summary

**Window function general form**:
```sql
[function_name]([expression]) 
OVER (
  [PARTITION BY partition_column,...] 
  [ORDER BY sort_column [ASC|DESC],...] 
  [frame_clause]
)
```

- **Frame Clauses**:
  - `UNBOUNDED PRECEDING`
  - `UNBOUNDED FOLLOWING`
  - `N PRECEDING`
  - `N FOLLOWING`
  - `CURRENT ROW`

- **Examples**:
  - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
  - `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`
  - `RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`
  - `RANGE BETWEEN '7 days' PRECEDING AND CURRENT ROW` (for date/time data)

---

### Example Cheat-Sheet Snippet

| **Task**                      | **Function**                 | **Window Clause Example**                                                         |
|-------------------------------|------------------------------|------------------------------------------------------------------------------------|
| Cumulative Sum                | `SUM(col)`                   | `OVER (PARTITION BY X ORDER BY Y ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`|
| Rolling Average (n rows)      | `AVG(col)`                   | `OVER (ORDER BY Y ROWS BETWEEN n PRECEDING AND CURRENT ROW)`                      |
| Ranking                       | `RANK()` / `DENSE_RANK()`    | `OVER (PARTITION BY X ORDER BY Y DESC)`                                           |
| Row Number                    | `ROW_NUMBER()`               | `OVER (ORDER BY Y)`                                                               |
| Period-based Rolling Avg      | `AVG(col)`                   | `OVER (ORDER BY date_col RANGE BETWEEN 'n days' PRECEDING AND CURRENT ROW)`       |
| Compare to Prior Row          | `LAG(col)`                   | `OVER (ORDER BY Y)`                                                               |
| Compare to Next Row           | `LEAD(col)`                  | `OVER (ORDER BY Y)`                                                               |
| First/Last in Partition       | `FIRST_VALUE(col)` / `LAST_VALUE(col)` | `OVER (PARTITION BY X ORDER BY Y RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)` |

---

**Use this cheat sheet** for quick lookups and as a template for writing window function queries in PostgreSQL. Experiment with different frame clauses to achieve the precise sliding window or cumulative calculations needed for your data analysis tasks.

---