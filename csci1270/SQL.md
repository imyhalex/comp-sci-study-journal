# SQL

__SQL Components:__
- Data Manipulation Language (DML)
    - Purpose: Work with the data inside tables
    - Think: CURD oprations
- Data Definition Language (DDL)
    - Purpose: Define and manage the structure of the databse objects
    - Think: Define the blueprint of the database
- Data Control Language (DCL)
    - Purpose: Control accessd and permissions
    - Think: "Who" can do what
- Also includes:
    - View definition
        - Purpose: Create virtual tables that are stored queries
        - Useful for:
            - Simplifying queries
            - Providing abstraction/security(hide sensitive columns)
    - Integrity & Referential Constraints
        - Purpose: Ensure valid, consistent data.
    - Transactions
        - Purpose: Group multiple operations into a single logical unit, that is
            - Atomic
            - Consistent
            - Isolated
            - Durable
        - Think: Bank transfer -- debit and credit must both succeed or bot fail

Summary Tables:
| Component                   | Purpose            | Examples                                 |
| --------------------------- | ------------------ | ---------------------------------------- |
| **DML**                     | Manipulate data    | `SELECT`, `INSERT`, `UPDATE`, `DELETE`   |
| **DDL**                     | Define schema      | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`    |
| **DCL**                     | Control access     | `GRANT`, `REVOKE`                        |
| **View Definition**         | Virtual tables     | `CREATE VIEW ...`                        |
| **Integrity & Constraints** | Data consistency   | `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK` |
| **Transactions**            | Reliability (ACID) | `BEGIN`, `COMMIT`, `ROLLBACK`            |

__Aggregations__
- Functions that return a single vaue from a bag of tuples
- Can be used in the SELECT output list

__HAVING__:
- Filter result based on aggregation computation (typically used after GROUP BY)
- If you don’t use GROUP BY, you can still use HAVING, but it will apply to the entire result set as one group. For example:
    ```sql
    SELECT COUNT(*) 
    FROM employees
    HAVING COUNT(*) > 10;
    ```
- Typical Order:
    ```sql
    SELECT department_id, COUNT(*) AS employee_count
    FROM employees
    WHERE hire_date >= '2020-01-01'
    GROUP BY department_id
    HAVING COUNT(*) > 5
    ORDER BY employee_count DESC;
    ```

__Questions__
Two Valid SQLs:
```sql
SELECT SUM(a)
FROM T
GROUP BY a;

This do:
GROUP BY a → groups rows by distinct values of a.
Within each group, a is constant, so SUM(a) = a * COUNT(*) for that group.
It’s redundant (since you could just select a and COUNT(*)), but it’s syntactically valid and runs in every major database.

SELECT SUM(b)
FROM T
GROUP BY a;

This do:
GROUP BY a → still groups by distinct a.
For each group, SUM(b) adds up the b values belonging to rows with that a.
This is the classic, useful GROUP BY query: one column defines the groups, another column gets aggregated.
```
Why Valid (second example case study)?
- The GROUP BY a defines how rows are partitioned.
- SUM(b) is an aggregate, so it’s legal in the SELECT list.
- SQL does not require you to display the grouping column (a); __it only requires that any non-aggregated column in SELECT must appear in the GROUP BY__.
- GROUP BY defines the partitioning.
- You don’t have to list the grouping column in SELECT, but if you don’t, you’ll only see the aggregates, without knowing which group they belong to.

Got it — here’s a clean version without icons or decoration:

__Nested Queries__
__1. `IN`__

Checks whether a value matches any value in a list or subquery. Equivalent to `= ANY`.

```sql
SELECT name
FROM employees
WHERE department_id IN (10, 20, 30);
```
Same as: employee’s department\_id = 10 OR 20 OR 30.

With subquery:

```sql
SELECT name
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM departments
    WHERE location = 'NY'
);
```

__2. `EXISTS`__

Checks whether a subquery returns at least one row (true/false).

```sql
SELECT name
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM departments d
    WHERE d.department_id = e.department_id
      AND d.location = 'NY'
);
```

Employees are returned only if their department exists in NY.


__3. `ANY` (or `SOME`)__

Compares a value against a list or subquery and returns true if the condition is true for at least one element.

```sql
SELECT name
FROM employees
WHERE salary > ANY (
    SELECT salary
    FROM employees
    WHERE department_id = 10
);
```

Meaning: an employee’s salary is greater than at least one salary in department 10.
This is equivalent to `salary > MIN(...)` from that subquery.


__4. `ALL`__

Compares a value against a list or subquery and returns true only if the condition is true for all elements.

```sql
SELECT name
FROM employees
WHERE salary > ALL (
    SELECT salary
    FROM employees
    WHERE department_id = 10
);
```

Meaning: an employee’s salary is greater than every salary in department 10.
This is equivalent to `salary > MAX(...)` from that subquery.

## Relational Algebra: Join

__Cross Join__
- Cartesian production (every pair)
- Every row from table A is paired with every row from table B.
- No condition required.

__Inner Join__
- Every Pair tht matches; drop non-matching pairs
- `Natural Join` is a shorthand for an Inner Join that automatically matches columns with the same name in both tables.
    - It only returns rows where those column values match.
    - Diff between `INNER JOIN` and `NATURAL JOIN`:
        - `INNER JOIN` is a general join where you explicitly say which columns must match.
        - `NATURAL JOIN` is not the same thing — it’s a shorthand form of inner join that automatically uses all columns with the same name in both tables as the join condition.
            ```sql
            -- Natural Join
            SELECT *
            FROM Students
            NATURAL JOIN Enrollments;

            -- Explicit Inner Join
            SELECT *
            FROM Students s
            INNER JOIN Enrollments e
            ON s.student_id = e.student_id;
            ```
        - Why `NATURAL JOIN` is not common:
            - If tables have multiple columns with the same name, SQL will join on all of them (sometimes unintentionally).
            - If schema changes (e.g., new column with the same name is added), your query results can change silently.

- Theta / Equi Join
    - Match tuples using some arbitary join predicate define by theta
    - if theta is just equality predicate, then it is called an "Equi Join"
- Semi Join
    - Generate relation that contains tuples of R that match with tuples in S
    - Same as thetajoin except that output relation only contains attributes from the first relation
    - A semi join returns rows from one table only if they have a match in the other table.
    - BUT unlike an inner join, it does not return columns from the other table.
    - In other words: it’s like saying “Give me all rows in A that have a match in B”, without dragging in B’s data.
    - Example
        ```sql
        -- Semi Join: Employees who are assigned to at least one project
        SELECT e.emp_id, e.name
        FROM Employees e
        WHERE EXISTS (
            SELECT 1
            FROM Projects p
            WHERE p.emp_id = e.emp_id
        );
        ```
- Anti Semi Join
    - Generate relation that contains tuples of R that do not match with any tuple in S
    - __This is not techinally an inner join__

__Outer Join__
- Every pair that matches; and keep all non-matching tuples from one or both sides & fill the missing side (if exists) with NULLsq
- Left Outer Join (LEFT JOIN) (R⟕S)
    - Genrate all combinations of tuples in R and S that are equal on their shared attributes, in addition to tuples in R that have no matching tuples in S.
- Right Outer Join (RIGHT JOIN) (R⟖S)
    - Same as LEFT JOIN but with the input relations reversed
- Full Outer Join (R⟗S)
    - Uion of LEFT and RIGHT JOIN

