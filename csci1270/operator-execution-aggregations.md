# Aggregations & Joins


__Operator execution:__
- Aggregations
- Joins

## Aggregations
- Collapse values for a single attribute from multiple tuples into a single scalar value.
- The DBMS needs a way to quickly find tuples with the same distinguishing attributes for grouping.
- Two implementation choices:
    - Sorting
    - Hashing


__Alternative to Sorthing__
- What if we do not need the datat to be ordered?
    - Removing duplicates in DISTINCT (no ordering)
    - Forming groups in GROUP BY (no ordering)
- Hash i ususally a better alternative in this scenario
    - Only need to remove duplicates, no need for ordering.
    - Can be computationally cheaper than sorting.

__Hashing Aggregate__
- Populate a temporary hash table as the DBMS scansthe table. For each record, check whether there is already an entry in the hash table:
    - DISTINCT: Discard duplicate
    - GROUP BY: Perform aggregate computation

__Running Aggregates__
- Some aggregations can ususlay be done on the fly
- Store pairs of the form (GroupKey->RunningVal)
- When we wan to insert a new tuple into the hash table:
    - If we find a matching GroupKey, just update the RunningVal appropriately
    - Else insert a new GroupKey→RunningVal

__External Hashing Aggregates__
- Phase #1: Partition
    - Divide tuples into partitions based on grouping keys
    - Write them out to disk when they get full
    - Contains:
        - Filter
        - Remove columns
        - B-1 parititons
            - one key that fill in one parition cannot be appeared on another one
    - Use a hash function h1 to split tuples into partitions on disk.
        - A partitions is one or more pages that contain the set of keys with the same hash value
            - the hash funciotion can be light-weight, it just needs to split keys evenly into a number of partitions
        - Partitions are “spilled” to disk via output buffers.
    - Assume that we have B buffers. We will use B-1 buffers for the partitions and 1 buffer for the input data.
- Phase #2: ReHash
    - Read in each parittion
    - Build in-memory hash table for each partition and compute the aggregation
    - For each partition on disk:
        - read it into memory and build an in-memory hash table based on second hash function h2
        - then go through each bucket of this hash table to bring together matching tuples
    - This assumes that each partition fits in memory
- Q: What is the minumum number of buffer pages do we need for the external hash-based aggregate? Assume N pages of inputs
    - Partition Stage: 2N
    - Rehash Stage: N
    - Total = 3N

__Joins__
- We normalize tables ina relational database to aviod redundancy
- We then use the join operator to reconstruct the original tuples without any information loss.
- Join Algos: 
    - Binay Joins(two tables) using inner equijoin algo
        - These algorithms can be tweaked to support other joins.
        - Multi-way joins exist primarily in research literature.
- _Cost Analysis Criteria_
    - Assume:
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

__Nested Loop Join__
```txt
foreach tuple r ∈ R: <- Outer
    foreach tuple s ∈ S: <- Inner
        emit, if r and s match
```
- R ⨝ S

__Simle nested loop join__
- Why is this algo a bad one?
    - For each tuple in the outer table, we must do a sequential scan to check for a match in the inner table.
    - for every tuple R, it scans S once
    - Cost: M + (m * N)
- N: N pages in S
- n: n tuples in S
- M: M pages in R
- m: m tuples in R
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

__Block Nested Loop Join__
```text
foreach block BR ∈ R:
    foreach block BS ∈ S:
        foreach tuple r ∈ BR:
            foreach tuple s ∈ Bs:
                emit, if r and s match
```
- This algo performs fewer disk access
    - For every block in R, it scans S once
    - Cost: M + (M * N)
- N: N pages in S
- n: n tuples in S
- M: M pages in R
- m: m tuples in R
- Example database: 
    - Table R: M = 1000, m = 100,000
    - Table S: N = 500, n = 40,000
- Cost Analysis:
    - M + (M * N) = 1000 + (1000 * 500) = 501,000 IOs
    - At 0.1 ms/IO, Total time ≈ 50 seconds
- We determine the size based on the number of pages, not the number of tuples
- What if we have B buffers availables?
- This algo use B-2 buffers for sacnning R
    - Cost: M + ([m/(B-2)]*N)
- What if the outer relation completely fits in memory (B-2 > M)?
- Use smaller relations?
    - Cost: M + N = 1000 + 500 = 1500 IOs
    - At 0.1 ms/IO, Total time approximatly 0.15 seconds

__Index Nested Loop Join__
```text
foreach tuple r ∈ R:
    foreach tuple s ∈ Index(ri = sj):
        emit, if r and s match
```
- Skip the sequential scan
- Use an existing index for the join.
- Assume the cost of each index probe is some `C` per tuple.
    - Cost: Cost: M + (m * C)
