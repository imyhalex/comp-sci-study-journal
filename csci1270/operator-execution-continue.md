# Operator execution Continue

__Basic Hash Join Algorithm__
```text
build hash table HTR for R. // build phase
    foreach tuple s ∈ S // probe phase
        output, if h1(s) ∈ HTR.
```
- Phase #1: Build
    - Scan the outer relation and populate a hash table using the hash function h1 on the join attributes.
    - We can use any hash table that we discussed before but in practice linear probing usually works well.
- Phase #2: Probe
    - Scan the inner relation and use h1 on each tuple to jump to a location in the hash table and find a matching tuple.

__Hash Table Content__
- Key: The attribute(s) that the query is joining the tables on
    - we always need the original key to verify that we have a correct match in case of hash colision
- Value: Varies per implementation
    - Depends on what the oprators above the join in the query plan expect as its input
    - Early vs. Late Materialization

__Optimization : Probe Filter__
- Create a _Bloom Filter_ during the __build phase__
- Use it in the __probe phase__ to decide if an actual probe is needed

__Bloom Filter__
- Probabliistic data structure (bitmap) that answers set memebership queries
    - False negatives never occurs
    - Flase positive can occur
- Insert(x):
    - Use k hash functions to set bits in the filter to 1
- Lookup(x):
    - Check whether the bits are 1 for each hash function.
- Imagine a row of light switches (bits) all turned off initially: You have multiple friends (hash functions) — each friend, when given a name, flips specific switches.
    - When you add a name, all friends flip their switches.
    - When you check a name, you ask each friend: “Is your switch on?”
        - When you check a name, you ask each friend: “Is your switch on?”
            - If any friend says “off,” the name was definitely never added.
            - If all say “on,” it might have been added (but possibly not — due to collisions).

__Probe Filter (Summary)__
- Create a Bloom Fliter during the build phase when the key is likely to not exist in the hash table
- The filter is then check before probing the hash table
- This will be faster since the filter will fit in CPU caches and may reduce relatively expensive hash lookups
- Q: A bloom filter used to optimize a hash-based join can only decrease but never increase the number of probes to the hash table. (True/__False__)
    - In a hash join:
        - You build a hash table on the smaller relation (say, `R`).
        You probe it using tuples from the larger relation (say, `S`).
    - Each probe checks whether a tuple from S has a matching key in R.
    - Before probing, we can create a Bloom filter on all the join keys of `R`.
        - Then, for each tuple in S:
            - We first check the Bloom filter.
            - If the filter says “not in R,” we skip the probe.
            - If it says “maybe in R,” we perform the probe (and confirm).
        - Effect on Probes
            - False negatives: never happen → we’ll never skip a key that’s actually in R.
            - False positives: may happen → sometimes we’ll still probe unnecessarily.
        - So:
            - The Bloom filter can eliminate some probes
            - It never adds extra probes, since false negatives don’t exist.
        - It can only decrease (or leave unchanged) the number of probes — never increase them.

## External Hash Join
- What happens if we do not have enough memory to fit the entire hash table?
- We do not want to let the buffer pool manager swap out the hash table pages at random.

__Partitioned Hash Join (Grace Join)__
![img](./img/Screenshot%202025-10-09%20at%2013.39.38.png)
```text
build hash table HTR,0 for bucketR,0
    foreach tuple s ∈ bucketS,0
        output, if h2(s) ∈ HTR,0
```
- Hash R into (0, 1,..., max) `buckets` (aka `partitions`)
- Hash S into the same # of buckets with the same hash function
- Perform regular hash join on each pair of matching buckets in the same level between R ad S
- Cost of external hash join?
    - Assume that we have enough buffers
    - Partitioning Phase: 
        - Read+Write both tables
        - 2(M + N)
    - Probing Phase: 
        - Read both table
        - M + N
    - Total Cost: 
        - 3(M + N)

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

## Query Plan
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
- Ouput control works easily with this approach(e.g. LIMIT)