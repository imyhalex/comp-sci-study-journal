# Aggregations & Joins

__Operator execution:__
- Aggregations
- Joins

## Aggregations
- Aggregation = collapse many rows into one (per group)
- Example:
    ```sql
    SELECT dept, AVG(salary)
    FROM employees
    GROUP BY dept;
    ```
    - We take many tuples per department,
    - Combine them into one result per group (the department),
    - Compute something (AVG, SUM, COUNT, etc.).
    - So the DBMS must find all tuples that share the same group key: that is the hard part
- Collapse values for a single attribute from multiple tuples into a single scalar value.
- The DBMS needs a way to quickly find tuples with the same distinguishing attributes for grouping.
- Two implementation choices (two main strategies):
    - Sorting-based Algorithm
        - Key Idea: Sort tuples by group key so identical keys are adjancent
        - When Used: When data already sorted (e.g, clustered index, `ORDER BY`)
    - Hashing-based Algorithm
        - Key Idea: Use a hash table keyed by group attribute(s)
        - When Used: When ordering isn't needed (faster for larger unordered data)

__Sorting Aggregation__
- Filter
- Removes Columns
- Sort
- Eliminate Duplicates 
- Imagine `GROUP BY dept;`
    1. Scan table and filter tuples if needed
    2. Remove unnecessary colums (key only `dept`, `salary`)
    3. Sort all tuples by `dept`
    4. Collapse adjancent duplicates - when `dept` changes, finalize the previous group

__Alternative to Sorthing__
- What if we do not need the datat to be ordered?
    - Removing duplicates in `DISTINCT` (no ordering)
    - Forming groups in `GROUP BY` (no ordering)
- Hash is ususally a better alternative in this scenario
    - Only need to remove duplicates, no need for ordering.
    - Can be computationally cheaper than sorting.

__Hashing Aggregate__
- If the query does not need order, sorting is overkill
- We can istead build a temporay hash table while scanning tuples
- Populate a temporary hash table as the DBMS scansthe table. For each record, check whether there is already an entry in the hash table:
    - DISTINCT: Discard duplicate
    - GROUP BY: Perform aggregate computation
- Algorithm outline:
    1. Initialize an empty hash table
    2. For each input table:
        - Compute its hash key = hash(group attribute(s))
        - If key already exist -> update aggregate value (add `SUM`, increment `COUNT`, etc)
        - Else -> insert a new entry (groupKey->RunningVal)

__Running Aggregates (Incremental Updates)__
- This is just an optimization of hash aggregation
- Some aggregations can ususlay be done on the fly
- Store pairs of the form (GroupKey->RunningVal)
- When we wan to insert a new tuple into the hash table:
    - If we find a matching GroupKey, just update the RunningVal appropriately
    - Else insert a new GroupKey→RunningVal

__External Hashing Aggregates__
- Hash-based aggregation is great, but only works easily if everything fits in memory
- If your table is huge, (say, billions of rows) and your hash table can’t fit:
    - the DBMS must spill to disk and use a two-phase process called External Hashing (just like External Merge Sort did for sorting).
- Geberal Idea: Suppose we want to compute something like:
    ```sql
    SELECT dept, AVG(salary)
    FROM employees
    GROUP BY dept;
    ```
    - But the table `N` page, and our buffer pool only has `B` pages
    - We can not hold all groups in memory at once: so partition the data first
    - Then Aggregate each partition separately

- __Phase #1: Partition__
    - Goal: Break data into smaller partitionsd that each can fit in memory later
        1. Read input tuples using __1 input__ buffer page
        2. Compute hash of group key using a first hash function `h₁`.
        3. Send each tuple to one of __B-1 output buffers__, each representing one partition
        4. When an output buffer fills up -> write it to disk
    - Why `B-1`: We are assigned B buffers to process the data, and one buffer for input data so the B - 1 buffer for partition
    - Key Rule: A group key will appear in only one partition: because it always hashes to the same value under `h₁`
    - Slides version:
        - Divide tuples into partitions based on grouping keys
        - Write them out to disk when they get full
        - Use a hash function h1 to split tuples into partitions on disk.
            - A partitions is one or more pages that contain the set of keys with the same hash value
                - the hash funciotion can be light-weight, it just needs to split keys evenly into a number of partitions
            - Partitions are “spilled” to disk via output buffers.
        - Assume that we have B buffers. We will use B-1 buffers for the partitions and 1 buffer for the input data.

- __Phase #2: ReHash__
    - Now we process each partition one at a time:
        1. Read one partition back into memory
        2. Build a __hash table__ in memory using a second hash function `h₂` (to distribute key evenly in a RAM)
        3. For each tuple:
            - If the grop key already exists -> update its running aggregate value
            - Else -> create a new entry
        4. When done:
            - Write the aggregated results (one per group) for this partition
            - Move on to the next partition
    - Slides version:
        - Read in each parittion
        - Build in-memory hash table for each partition and compute the aggregation
        - For each partition on disk:
            - read it into memory and build an in-memory hash table based on second hash function h2
            - then go through each bucket of this hash table to bring together matching tuples
        - __This assumes that each partition fits in memory__
- __Q:__ What is the minumum __number of buffer pages__ do we need for the external hash-based aggregate? Assume N pages of inputs (I/O Cost Breakdown)
    - Partition Stage: 2N
        - We read N pages (the input table)
        - We write N pages (the output table)
    - Rehash Stage: N
        - We read each partition once more to compute aggregates
    - Total = 3N
    - Minimum Buffer Page Required to process the data
        - 1 buffer input buffer, B-1 buffer output buffer, so minumum B=3 pages


## Joins

__Basic Setup for Cost Analysis__

__Joins__
- We normalize tables in a relational database to aviod redundancy
- We then use the join operator to reconstruct the original tuples without any information loss.
- Join Algos: 
    - All physical join operators are built around the same idea:
        - Foe each tuple in table R, find all matching tuples in the other table S
    - Binay Joins(two tables) using inner equijoin algo
        - These algorithms can be tweaked to support other joins.
        - Multi-way joins exist primarily in research literature.
- _Cost Analysis Criteria_
    - Assume:
        | Symbol          | Meaning                                 |
        | --------------- | --------------------------------------- |
        | R               | Left relation                           |
        | S               | Right relation                          |
        | M               | # of pages in R                         |
        | N               | # of pages in S                         |
        | m               | # of tuples in R                        |
        | n               | # of tuples in S                        |
        | **Cost metric** | # of page I/Os (reads/writes from disk) |
        - M pages in table R, m tuples in R
        - N pahes in table S, n tuples in S
        - Cost Metric: # of I/Os to compute join
    - We will ignore output costs (for now) since that depends on the output and how it will be consumed
- Nested Loop Join
    - Simple
    - Block
    - Index
- Hash Join
- Sort-Merge Join

### Family #1: Nested Loop Join (Baseline)
- Nested Loop Join already processes data one tuple or block at a time — it doesn’t try to load whole tables into memory.
- That means:
    - Even if relations are huge,
    - You can still run a nested loop join by streaming both from disk.
- Takeaways:
    - Pick the smaller table as the outer table.
    - Buffer as much of the outer table in memory as possible.
    - Loop over the inner table (or use an index).

__Simple Nested Loop Join (Tuple-at-a-time)__
```text
foreach tuple r ∈ R: <- Outer
    foreach tuple s ∈ S: <- Inner
        emit, if r and s match
```
- Meaning:
    - For each tuuple `r` in `R`:
        - For each tuple `s` in `S`:
            - If they match -> output `(r, s)`
- R ⨝ S
- Why is this algo a bad one?
    - For each tuple in the outer table, we must do a sequential scan to check for a match in the inner table.
    - for every tuple R, it scans S once
    - __Cost: M + (m * N)__
- Example Database:
    - Table R: M = 1000, m = 100,000
    - Table S: N = 500, n = 40000
- Cost Analysis:
    - M + (m * N) = 1000 + (100000 ∙ 500) = 50,001,000 IOs
    - At 0.1 ms/IO, Total time ≈ 1.3 hours
- What if smaller table (S) is used as the outer table?
    - N + (n ∙ M) = 500 + (40000 ∙ 1000) = 40,000,500 IOs
    - At 0.1 ms/IO, Total time ≈ 1.1 hours
    - _In general, we want the smaller table to be the outer table._

__Block Nested Loop Join (Page-at-a-time)__
```text
foreach block BR ∈ R:
    foreach block BS ∈ S:
        foreach tuple r ∈ BR:
            foreach tuple s ∈ Bs:
                emit, if r and s match
```
- Meaning:
    - For each page (or block) of `R`:
        - For each page of `S`
            - Join tuples in memory
- This algo performs fewer disk access
    - For every block in R, it scans S once.
- Still bad if both large, but fewer I/Os than tuple-at-a-time
- Now, __suppose B buffers__ to process data
    - __Case #1 Cost: M + (M * N)__
        - This is the Naive Nested Loop Join (B=3 pages)
            - 1 page for `R` (outer)
            - 1 page for `S` (inner)
            - 1 page for output
    - __Case #2 Cost: M + ( ceil(m/(B-2)) * N)__
        - We can use more buffers to process the data
            - still 1 page for `S` (inner)
            - 1 page for output
            - but this time we use __B-2 pages__ for `R` at once
    - __Case #3: If the Outer Relation `R` fits in Memory -> Cost: M + N__
        - When B-2 >= M, we can load the entire `R` into memory
            - Read R once (M I/Os)
            - Scan S once (N I/Os)
- _Example database:_ 
    - Table R: M = 1000, m = 100,000
    - Table S: N = 500, n = 40,000
    - Case #1: Naive way
        - Cost Analysis:
            - `M + (M * N) = 1000 + (1000 * 500) = 501,000 IOs`
            - At 0.1 ms/IO, Total time ≈ `50 s`
    - Case #2: More buffers (B-2 buffers for `R`)
        - Cost Analysis, and we suppose `B=12`:
            - `M + (ceil(M / (B - 2)) * N) = 1000 + (ceil(1000/ (12 - 2)) * 500) = 1000 + (1000 / 10) * 500 = 1000 + 100 * 500 = 51,000 IOs`
            - At 0.1 ms/IO, Total time 51,000 * 0.1ms = `5.1s`
    - Case #3: If the Outer Relation Fits in Memory
        - Cost Analysis:
            - `M + N = 1000 + 500 = 1500 IOs`
            - At 0.1 ms/IO, Total time 1500 * 0.1ms = `0.15s`

- If we have __B buffers__, we can improve:
    - This algo use B-2 buffers for sacnning R
    - 1 page for S
    - 1 page for output
        - __Cost: M + ([m/(B-2)]*N)__
    - What if the outer relation completely fits in memory (B-2 >= M)?
    - Use smaller relations?
        - Cost: M + N = 1000 + 500 = 1500 IOs
        - At 0.1 ms/IO, Total time approximatly 0.15 seconds

__Index Nested Loop Join__
```text
foreach tuple r ∈ R:
    foreach tuple s ∈ Index(ri = sj):
        emit, if r and s match
```
- Meaning: If `S` has a an index on the join key:
    - For each tuple `r` in `R`, use the index on `S` to find matches quickly 
- Skip the sequential scan
- Use an existing index for the join.
- Assume the cost of each index probe is some `C` per tuple.
    - __Cost: Cost: M + (m * C)__ -> M (scan `R`) + `m * cost(index lookup on S)`

