# Operator execution Continue

## Family #2: Hash Join

__Basic Hash Join Algorithm__
```text
build hash table HT_R for R. // build phase
    foreach tuple s ∈ S // probe phase
        output, if h1(s) ∈ HTR.
```
- __Often the best general-purpose join when no indexes or sorting exist__
- Phase #1: Build
    - Choose ont table (usually the smaller one, say `R`)
    - Build an in-memory hash table using `h₁(key)`
    - Key = join attribute(s) from R
    - Value = rest of tuplesd (or pointer)
- Phase #2: Probe
    - Scan the other table (`S`)
    - For each tuple in S:
        - Compute h₁(S.key)
        - Check if a matching key exists in hash table HT_R
- The Problem:
    - If most tuplesd in S do not have a match in R, then we are wasting CPU time by probing the hash table over: each costs CPU cycles and cache misses.

__Hash Table Content__
- Key: The attribute(s) that the query is joining the tables on
    - we always need the original key to verify that we have a correct match in case of hash colision
- Value: Varies per implementation
    - Depends on what the oprators above the join in the query plan expect as its input
    - Early vs. Late Materialization

__Optimization : Probe Filter (Bloom Filter)__
- Create a _Bloom Filter_ during the __build phase__
- Use it in the __probe phase__ to decide if an actual probe is needed

__Bloom Filter = "Fast Pre-Check Chache"__
- During the build phase, while we insert keys from R into the hash table, we also insert them into a Bloom Filter
- __What is Bloom Filter?__
    - A compact bitmap that quickly tell you:
        - "This key is defintly not in the set" (Flase negative never occurs)
        - "This key might be in the set" (Flase positive can occur)
- Probabliistic data structure (bitmap) that answers set memebership queries
    - False negatives never occurs = __impossible (never say “not in set” if it actually is)__
    - Flase positive can occur = __possible (might say “maybe” even if not really in set)__

- __How it is used in Hash Join?__
    - Insert(x):
        - Use k hash functions to set bits in the filter to 1
    - Lookup(x):
        - Check whether the bits are 1 for each hash function.
    - Build Phase:
        - For every tuple in R:
            - Insert its join key into both:
                1. Hash table (`HT_R`)
                2. Bloom Filter(`BF`)
    - Probe Phase:
        - For every tuple in S:
            1. First check the Bloom filter (`BF`) using `h₁(S.key)`
            2. If `BF` says, _"definitely not present" → skip the hash probe (cheap rejection)_
            3. If `BF` says, _"maybe present" → probe the hash table `HT_R` as normal_
    - So Bloom Filter acts as a lightweight pre-check to avoid expensive lookups

__Probe Filter (Summary)__
- Create a Bloom Fliter during the build phase when the key is likely to not exist in the hash table
- The filter is then check before probing the hash table
- This will be faster since the filter will fit in CPU caches and may reduce relatively expensive hash lookups
- __Q:__ A bloom filter used to optimize a hash-based join can only decrease but never increase the number of probes to the hash table. (__True__/False)
    - Because:
        - Every probe you skip is guaranteed correct (no false negative)
        - In the worst case (if bloom filter may has many false positive), you still probe the same tuples as before: no worse
    - So:
        - Best case: you skip many uncessary probes -> faster
        - Worst case: Bloom Filter gives no benefit -> same number of probes

### External Hash Join
- The problem is:
    - Table `R` (or `S`) is too large to build an in-memory hash table
    - Memory = B pages (too small)
    - If we ket OS swap pages randomly, we'd give terrible I/O performance (thrashing)
        - We do not want to let the buffer pool manager swap out the hash table pages at random.
- So instead, the DBMS takes control and performs the join in two phases:
    - Using the same divide-and-conquer idea as `external hash aggregation`

__Partitioned Hash Join (Grace Join)__
![img](./img/Screenshot%202025-10-09%20at%2013.39.38.png)
```text
build hash table HT_R,0 for bucketR,0
    foreach tuple s ∈ bucketS,0
        output, if h2(s) ∈ HTR,0
```
- __Phase #1: Partitioning (Divide)__
    - Key Idea: Tuples can join will always hash to the same partition
        - So we only need to join corresponding paris `(bucketR[i], bucketS[i])`
    1. _Hash R_ into k partitions on disk using hash function h₁:
        - For each tuple `r ∈ R`
            - Compute `bucketID = h₁(r.key)`
            - Write it into correponding partition file `bucketR[i]`
    2. _Hash S_ into k partitions using the same hash function h₁:
        - For each tuple `s ∈ S`
            - compute `buckectID = h₁(s.key)`
            - Write it to `bucketS[i]`
- __Phase #2: Build & Probe (Conquer)__
    - For each partition pair `(Ri, Si)`
        1. Build an in-memory hash table __on__ `Ri` using hash function `h₂` (to avoid collision bias).
        2. Probe with all tuples in `Si`, checking matches using `h₂`
- Cost Analysis:
    - Phase #1: Partitioning Phase 
        - Read and write both R and S once.
        - So, `2(M + N)`
    - Phase #2: Probing Phase: 
        - Read each partition once (for both R and S).
        - So, `M + N`
    - Total Cost: 
        - `3(M + N)`
- Why “Grace” Hash Join Works So Well
    - Each partition fits into memory for the second phase
    - All access in both phases is sequential I/O: no random swapping
    - Each page is read/write a small, fixed number of time (3 total)

## Family #3: Soret-Merge Join

__Sort-Merge Join__
- Phase #1: Sort
    - Sort both table on the join key(s)
    - We can use the external merge sort we discussed
- Phase #2: Merge
    - Step through the two sorted table with cursors and emit matching tuples
        - May need to some backtracking in the inner table
- Sort Cost (R): 2M ∙ (1 + ⌈ logB-1⌈M / B⌉ ⌉)
- Sort Cost (S): 2N ∙ (1 + ⌈ logB-1 ⌈N / B⌉ ⌉)
- Merge Cost: (M + N)
- Total Cost: Sort + Merge
- When is sort-merge join useful?
    - One or both tables are already sorted on join key.
    - Output must be sorted on join key.
    - Relations don’t fit in main memory.
    - The input relations may be sorted either by an explicit sort operator, or by scanning the relation using an index on the join key.

__Join Algo Summary__
![img](./img/Screenshot%202025-10-09%20at%2014.01.59.png)

# Query Plan (Lecture 10 & 11)
- DBMS converts query into plan comprised of logical operators
    - Represented as a tree
    - Technically a Directed Acyclic Graph (DAG)
- Data flows from the leaves of the tree up towards the root.
- The output of the root node is the result of the query.

__Processing Model__
- A DBMS's processing model defines how the system executes a query plan.
- Approach #1: Iterator Model
- Approach #2: Materialization Model
- Approach #3: Vectorized / Batch Model

__Iterator Model__
![img](./img/Screenshot%202025-10-14%20at%2013.10.53.png)
- Each query plan opeator implements three functions:
    - `Open()`
    - `Close()`
    - `Next()`
    - On each invocatoin, the oprator returns either a single tuple or a null marker if there are no more tuples
    - The operator implements a look that calls Next() on its children to retrive their tuples and then process them
- This is called the iterator model (aka _tuple-at-a-time_, or _pipeline_ model)
- Used on almost every DBMS. Allow for tuple pipelining
- Some operators must block until their children emit all their tuples
    - Hash joins, hash aggregaties, order by
    - Thee are called pipeliine breakers
- No intermediate buffers needed
- Ouput control works easily with this approach(e.g. `LIMIT`)

__Materialization Model__
![img](./img/Screenshot%202025-10-14%20at%2013.11.35.png)
- Each oprator processes its inoyt all at once and them emits its putput all at once
    - The oprator "materializer" its output as a single result.
    - The DBMS can push down hint (e.g. LIMIT) to avoid scanning too many tuples

__Iterator vs. Materilization Tradeoffs__
- Number of function calls
- Buffer Spcae
- Early Result and concurrency
    - The pipeline model can emit results early and overlap work

__Vectorization Model__
![img](./img/Screenshot%202025-10-14%20at%2013.21.34.png)
- Like the iterator model where each operator implements a Next() function, but..
- Each operator emits a batch of tuples instead of a single tuple.
    - The operator's internal loop processes multiple tuples at a time. 
    - The size of the batch can vary based on hardware or query properties.
- Reduces the number of incoration per operators
- Allows for operators to more easily use vectorized (SIMD) instructions to process batches of tuples.
- A happy middle between tuple-at-a-time and full materialization models

## Query Optimization

__Architecture Overview__
![img](./img/Screenshot%202025-10-14%20at%2013.21.34.png)

__Query Optmization__
1. Logical plan optimization via Heuristic /Rules
2. Physical plan optimiztion via Cost-based Search

__Logical plan optimization__
- Rewrite a logical plan into an equivalent logical plan using pattern matching rules (aka rewrite rules)
- The goal is to increase the likelihood of enumerating the optimal plan in the search
- Cnnot compare plans because there is no cost model but "direct" a transformation to a preferred side.
- Common Example
    - Split Conjunctive Predicates
    - Predicate Pushdown
    - Replace Cartesian Products with Joins
    - Projection Pushdown

__Physical plan optimization__
- Cost Estimation
    - The DBMS uses a cost model to predict the behavior of a query plan hiven a database states
    - This is an internal cost that allows the DBMS to compare one plan with another.
- Cost Model Component
    1. Physical Cost
        - Predict IO, CPU cycles, cache misses, RAM consumption, network messages
        - Depends heavily on hardware
    2. Logical Cost
        - Estimate output size per operator
        - Independent of the operator algorithm
        - Need cardinality estimations for result sizes
    3. Algorithm Costs
        - Complexity of the operator implementation.

__Postgres: Cost Model__
- Uses a combination of CUP and I/O costs that are weighted by "magic" constant factors
- e.g.:
    - Cost = cup_tuple_cost * number_of_rows + seq_page_cost * number_of_pages
- Default settings are for a disk-resident database without a lot of memroy:
    - processing a tuple in memory is 400x faster than reading a tuple from disk
    - Sequential I/O is 4x faster than random I/O
- `EXPLAIN` prints the plan chosen from a given query, plus the estimated cost and result set size
- `ANALYZE` also runs the query, prints the acutal values

__Statistics__
- The DBMS stores internal statistics about tables, attribtues, and idexes in its internal cataglog
- Different system update them at different time
- Manual invocation:
    - Postgres/SQLite: ANALYZE
    - Oracle/MySQL: ANALYZE TABLE
    - SQL Server: UPDATE STATISTICS
    - DB2: RUNSTATS

__Slection Cardinatliy__
- The selectively (sel) of a predicate P is fraction of tuples that qualify (i.e. what fractio of tuples will be selected)
- Example
    ```sql
    SELECT * FROM people WHERE age = 9;
    ```
- Equality Predicates: A=constant
    - sel (A=constant) = #occurences/abs(R)
    - Example sel(age=9)
- Statistic Collections
    - Choice #1: Histograms
        - Equi-Width Histograms
            - Maintain counts for a group of values instead of each uniqe key
            - All buckets have the same width (i.e. same # of values)
        - Equi-Depth Histograms
            - Vary the width of buckets so that the total number of occurrences for each bucket is roughly the same.
        - Equi-Width vs. Equi-Depth Histograms
            - Equi-width histograms:
                - Simple, fixed bin size
                - Well suited for uniform data
                - Inefficient for sparse data
            - Equi-depth histograms:
                - Expensive, variable bin sizes
                - Accommodates data skew
    - Choice #2: Sketches
        - Probabilistic data structures that generate approximate statistics about a data set.
        - Cost-model can replace histograms with sketches to improve its selectivity estimate accuracy.
    - Choice #3: Sampling
        - Modern DBMSs also collect samples from tables to estimate selectivities.
        - Update samples when the underlying tables changes significantly.