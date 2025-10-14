# Operator Execution

__Query Plan__
- Scans
- Sorts
- Aggregations
- Joins

__Access Methods__
- The way the the DBMS access the data stored in a table
    - When a query plan says "how" to get data from a table, it must choose an access path: this is called the access method
    - Not defined in relational algebra
- Two basic approaches
    - Table Scan (sequential)
    - Index Scan (many variants)


## Scans

__Table Scan__
- The DBMS reads every page of the table, one by one
- For each page in the table
    - It retrives it from the buffer pool (or disk if not cached)
    - It retrives over each tuple.
    - It checks whether the tuple satisfies the `WHERE` condition
- It maintains an internal _cursor_: keeps track of the last page and slot it examined(so it can resume, pause, or yield to other oprations like joins)
- When to use:
    - No useful index exists
    - Most row will patch the predicate (low selectively)
    - The table is small
- Plan Example:
    ```sql
    Seq Scan on Students
        Filter: age > 20
    ```

__Index Scan__
- The DBMS picks an index (e.g. B+Tree or Hash index) to jump directly to relevant tuples.
- The optimizer chooses which index to use based on:
    - Which attributes the index contains
    - Which attributes appear in the query predicate
    - The selectivity (how many rows are expected to match)
    - Whether the index is unique
    - How the predicate is composed (e.g., equality vs range conditions)
- Example:
    ```sql
    SELECT * FROM Students WHERE id = 42;
    ```
    - Usedr idnex on `id`
- Plan Example
    ```sql
    Index Scan using idx_students_id on Students
        Index Cond: (id = 42)
    ```
    - Variants
        - Index Only Scans -> read from the index alone (no need to fetch base table tuples)
        - Bitmap Index Scan -> combines multiple index lookups efficiency
        - Range Scan -> when using B+Tree index for range (`WHERE age BETWEEEN 18 AND 20`)

__Multi-Index Scan__
- This is used when more than one index could help satisfy the `WHERE` clause
- Instead choosing one, the DBMS can use several indexes together
- Example:
    ```sql
    SELECT * 
    FROM Students 
    WHERE age > 20 AND gpa > 3.5;
    ```
    - If there is:
        - an index on `age`
        - an index on `gpa`
- The DBMS can:
    - Lookup the set of tuple IDs (TIDs) matching each index condition
    - Combine them using set operations (AND = intersection, OR = union)
    - Fetch only those matching tuples from the table.
- This often implemented as a `bitmap index scan`:
    - Each index lookup produces a bitmap of page/row matches
    - The DBMS performs bitwise operations to merge results
- Advantages:
    - Efficient for multi-predicate queries
    - Avoids full table scan.
    - Especially good when each index is highly selective
- Plan Example:
    ```sql
    BitmapAnd
        -> Bitmap Index Scan on idx_age  (age > 20)
        -> Bitmap Index Scan on idx_gpa  (gpa > 3.5)
    ```

## Sortings

__Sorting__
- Relational Model/SQL is unsorted
- The DBMS often sorts tuples internally even when you do not ask for it.
- Why? Because many operations benefits from sorted input
    - Queries may request that tuples are sorted in a specific way (`ORDER BY`): Query can be run faster
    - But even if a query does not specify an order, we may still want to sort to do other things
        - Trivial to support duplicate elimination (`DISTINCT`): Easy to detect duplicates when data is sorted
        - Aggregations (`GROUP BY`): Group boundaries become easy to find
        - Merge joins: Requires both inputs sroted on join key
        - Bulk loading sorted tuples into a B+Tree index is faster: Faster if input is already sorted by key

__Two Major Scenarios__
- _In-Memory Sorting_
    - Used when all data fits in RAM
    - If data fits in memroy, then we can use a standard in-place sorting algorithms (e.g. quicksort, bubble sorts)
    - Time Comlexity `O(N log N)`
    - Example: Sorting 1000 rows in a small table
    - Plan Example:
        ```sql
        Sort (cost=...)
            -> Seq Scan on students
        ```
- _External Sorting_
    - If data does not fit in memroy then we need to use a technique that is aware of the cost of reading and writing disk pages. (sortings must be I/O-aware), because:
        - Disk acces is millions of time slower than memory
        - Random I/O is very expensive
    - So DBMS have two-phase algorithm called __External Merge Sort__
__External Merge Sort__
- Divide-and-Conquer algo, that
    - splits data into separate runs
    - sorts them individually, and
    - combines them into longer sorted runs
- Phase # 1: Sorting
    - Read as many pages as fit in memory (say, `B` pages)
    - Sort them in memory
    - Write the sorted data back to disk as a run.
    - You now have many sorted run on disk:
        ```text
        run1: 10, 20, 30
        run2: 5, 15, 25
        run3: 8, 12, 40
        ...
        ```
- Phase # 2: merging
    - Reapeatly merge sorted runs into __larger runs__
    - Each merge read multiple runsd (says, `B-1` runs at a time) and output a new sorted run.
    - Continue untile one fully sorted file remains
- Cost:
    - If N pages of data, and B buffer pages in memory, total cost=O(N log_B N) I/Os

__(Sorted) Run__
- A run is a sorted chunk of data produced during the external sort.
- Each run contains
    - Key: the attribute(s) used for sorting
    - Value: Two choices
        - Tuple (early materilalization)
        - Record IDs (late materialization)
- Early vs. Late Materialization
    - Early: key -> tuple
        - Meaning: The run stores the full tuples already sorted
        - Use Case: Simpler but heavior I/O (more data written)
    - Late key -> record ID
        - Meaning: the run stores only tuple pointers, not full tuples
        - Use case: Save space and I/O; full tuples fetch later if needed
    - Example
        - Early: `[age=20, name="Alice", gpa=3.8]`
        - Late: `[age=20 → (page=42, slot=5)]`


__2-Way External Merge Sort__
- Core Idea:
    - External Merge Sort sorts large data on disk using only a limited number of __buffer pages (B)__ in memory.
- Each pass:
    - Read several sorted runs from disk.
    - Merge them into longer runs
    - Writes them back to disk
- The "K" in `K-way merge` = how many runs can be merged at once in memory
    - "2" is the number of runs that we are going to merge in to a new run for each pass
- Data is broken up into N pages
- The DBMS has a finite number of B buffer pool pages to hold input and output data
- First pass: bring each pahe into memory, sort the page by itself, write it back out
- Second pass: generate runs are twice the size of previous pass
- Number of Passes: `1 + log₂N`
- In each pass, we read and write every page in the file.
- Total `I/O cost: 2N * (# of passes)` 
- __Q:__ What is the minum # buffer pages does 2-way merge require?
    - B=3 pages, One per each input run and one for the output run
    - Only need one buffer page for output and n pages for n-way merge
    - __Analysis__
        - Parameters:
            - `N` = total pages of data
            - `B` = number of buffer pages avibale in memroy
        - Phase 0: Initial Sorting
            - Read `B` pages (maybe 1 if `B=3` small). sort them in meory, and write back
            - Produces many small sorted _runs_
            - If `N=8` and `B=3`, we first produces 8 runs of size __1 page__ each 
                ```sql
                run1: [page1 sorted]
                run2: [page2 sorted]
                ...
                run8: [page8 sorted]
                ```
        - Phase 1+: Merging
            - In 2-way merege, we merge __2 runs__ at a time
            - Each merge requires:
                - 1 buffer page for each input run (e.g. one for `run1` and one for `run2`)
                - 1 buffer page for output (constant 1)
        - So:
            - Minimum B = 3 pages (2 inputs + 1 output)
            - __Minimum buffer required for K-way merge is `k+1`__

__General External Merge Sort__
![img](./img/Screenshot%202025-10-13%20231700.png)
- Pass #0:
    - Use `B` buffer pages
    - Produce [N / B] sorted runs of size `B`
- Pass #1, 2, 3
    - Merge `B-1` runs (i.e., K-way merge, where K = B - 1)
- Number of passes = 1 + log b-1 ^ [N / B]
- __Q:__ Determine how many passes it takes to sort 108 pages with 5 buffer pool pages: N=108, B=5
    - Step 1 (pass #0): Sorting in Small Batches (Pass 0)
        - Since you can only fit 5 pages on your table
            - Take 5 pages at a time
            - Sort them in-memory
            - Write them out as one small __sorted pile__
        - You reapeat this until 108 pages are done
        - After this pass: `ceil(108 / 5) = 22 piles`
    - Step 2 (pass #1): Merging Piles together
        - Your table can still hold only 5 pages - but to merge, you need:
            - One "reading hand" per pile you are merging
            - One "writing hand" for your new output pile
        - That means with `B=5`, you can merge __4 pile at once:__
            - 4 input piles (each with one page buffer)
            - 1 output buffer
        - So you pick 4 piles at a time, merge them together into a bigger sorted pile
            - `ceil(22 / 4) = 6`
    - Step 3 (pass #2): repeat Step 2 -> `ceil(6 / 4) = 2`
    - Step 4 (pass #3): `merge 2 piles into 1, done`
        - Finally, merge the last 2 piles into one single fully sorted pile.
        - You can easily do that — since 2 ≤ 4 (your merge limit).
    - Visualization:
        ```text
        Start: 22 piles
        After Pass 1: 6 piles
        After Pass 2: 2 piles
        After Pass 3: 1 pile (done)

        Pass 0: [22 runs of 5 pages each]
            ↓ merge 4 at a time
        Pass 1: [6 runs of 20 pages each]
            ↓ merge 4 at a time
        Pass 2: [2 runs of 80/28 pages each]
            ↓ merge 2
        Pass 3: [1 fully sorted run of 108 pages]
        ```


## Using B+Tree for Sorting
__Problem Setup:__
- You have a query that needs results in sorted order, like:
    ```sql
    SELECT * FROM Students ORDER BY age;
    ```
- The DBMS must somewhere output tuples in sorted order, but it does not always need to run external merge sort
- If there is __aleary a B+Tree index__ on the sort key (`age`), then the DBMS might use that index to produce sorted output directly
- If the table that must be sorted already has a B+Tree index on the sort attribute(s), then we can use that to accelerate sorting.
- Retrieve tuples in desired sort order by simply traversing the leaf pages of the tree.
- __Why this work__:
    - A B+Tree is already sorted by its key.
    - That means its leaf pages are arranged in key order, and each leaf has a pointer to the next leaf
    - So if you simply walk the leaf nodes from left to right, you get all keys (and thus tuples) in sorted order for free.

__Case #1: Clustered B+Tree__
- Meaning:
    - The table's physical order on disk matches the index order
    - The data tuples themselves are stored in the leaves (or right next to them)
    - So walking the leaves = walking the data in sorted order
- Process:
    1. Traversse down to the left-most leaf (smallest key)
    2. Sequentially walk trhough all leaf pages, fetching tuples
    3. Done: data already sorted
- Why this is awesome:
    - All I/O is sequential -> very fast (disk prefetch, no random seek)
    - No CPU sorting
    - No need for external merge sort passes
    - Cost: O(N) I/Os (just like a table scan)

__Case #2: Unclustered B+Tree__
- Meaning:
    - The index and data are stored sequentially
    - the index's leaf entries store `pointers` (__record IDs__) to tuples scattered accross the heap file
- So when you walk the leaf pages:
    1. You get keys in sorted order
    2. But each key has a pointer to its tuple on a random page
    - You must follow each pointer to fetch the full tuple.
- Why this is bad:
    - Each tuple could be one a __different disk page__
    - So instead of 1 I/O per page, you get ≈ __1 I/O per tuple__ → huge cost!
    - CPU: lots of pointer chasing
    - I/O pattern: random
    - Cost: O(N) per record

## Questions
- __Q:__ The Query planning is optmizer's job
    ```sql
    SELECT department, AVG(salary)
    FROM Employees
    WHERE age > 30
    GROUP BY department
    ORDER BY AVG(salary) DESC;
    ```
    - the DBMS must decide many physical details:
        - How to access the data (`Table Scan` vs `Index Scan`)
        - How to filter (`age > 30`)
        - How to group and compute aggregates (`Hash Aggregate` vs `Sort Aggregate`)
        - How to sort results (`External Sort` vs `in-memory sort`)
        - How to join (if multiple tables — `Nested Loop`, `Hash Join`, `Merge Join`)
        - The order of operations (e.g., join first or filter first?)