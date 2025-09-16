# VIEW

__VIEW__
- A virtaul table that is expressed as the result of a SQL query
    - when you query the view, it executes the underlying query
    - doesn't store any data
    - often used for security (i.e, restrict assess to some table/attributes)
    - update data in real-time
- Example
    ```sql
    -- Base table
    CREATE TABLE Employees (
        id INT,
        name VARCHAR(50),
        department VARCHAR(50),
        salary INT
    );

    -- Create a view showing only employees in the IT department
    CREATE VIEW IT_Employees AS
    SELECT id, name, salary
    FROM Employees
    WHERE department = 'IT';

    -- Use the view just like a table
    SELECT * FROM IT_Employees;
    ```

__MATERIALIZED VIEW__
- A materialized view is like a regular view, but with one big difference:
    - A normal view is just a saved query (data is not stored, it’s recalculated every time).
    - A materialized view stores the query result physically in the database.
- This means:
    - You don’t recompute the data every time you query the view.
    - Reads are much faster.
    - But… you need to refresh it when the underlying data changes.
- Example
    ```sql
    -- Create a materialized view
    CREATE MATERIALIZED VIEW HighSalaryEmployees AS
    SELECT id, name, salary
    FROM Employees
    WHERE salary > 80000;

    -- Query it just like a table
    SELECT * FROM HighSalaryEmployees;

    -- If underlying Employees table changes, refresh it:
    REFRESH MATERIALIZED VIEW HighSalaryEmployees;
    ``` 

__VIEW vs, MATERIALIZED VIEW (cont)__
- Regular VIEW:
    - No storage: only the SQL definition is stored.
    - When you query it, the database executes the underlying SQL on the base tables right then.
    - So, if base tables change, you always see the changes immediately.
- MATERIALIZED VIEW:
    - Stores results: when you create or refresh it, the query results are physically written into storage (like a table).
    - When you query it, the DB just reads from that stored snapshot.
    - If base tables change, the snapshot doesn’t magically update — you need to refresh it.

__What makes a "good" database shcema?__
- Goal 1: We want to ensure data integrity
- Goal 2: we also want to get good performance


## Normalization

__Anomaly__
![img](./img/Screenshot%202025-09-16%20at%2013.53.57.png)
- Update Anomalies
    - e.g.: if the room number changes, we need to make sure that we change all student records
- Insert Anomalies:
    - e.g.: may not be possible to add a student unless they are enrolled in a course
- Delete Anomalies:
    - If all the sutdents enrolled in a course are deleted, then we lose the room number
    ```text
    we implcity assume:
    sid -> name, address
    cid -> room
    sid, cid -> grade

    this is functional dependency
    ```
- So we split a single relation R into a set of relatoins. This decomposition process to reduce redundancy is called `normalization`
![img](./img/Screenshot%202025-09-16%20at%2014.00.36.png)

__1NF__
- Atomic data only
__2NF__
- No partial dependencies
__3NF, BCNF__
- No transitive dependencies
__BCNF__
__4NF__
__5NF__

## Relation DBMS Layer
- Query Planning
- Operator Execution
- Access Methods
- Buffer Pool Manager
- Disk Manager

__Disk - Based architecture__
- The DBMS assumes the primary storage location of the daabse is on non-volatile disk
- The DBMS's components manage the movement of data between non-volatile and volatile storage.

__Storage System Design Goals__
- Allow the DBMS to manage databses that exceed the memory available
- Reading/Writing to disk is expensive, so it must be managed carefully to avoid large stalls and performance degreation
- Furthermore: random access on disk is usually much slower than sequential access, so the DBMS will want to maximize sequential access.
    - DBMS will want to maximuze seqential access
    - Algos try to reduce number of writes to random pages so that data is stored in contiguous blocks