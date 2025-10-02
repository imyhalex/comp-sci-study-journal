# Operator Execution

__Query Plan__
- Scans
- Sorts
- Aggregations
- Joins

__Access Methods__
- the way the the DBMS access the data stored in a table
    - Not defined in relational algebra
- Two basic approaches
    - Table Scan (sequential)
    - Index Scan (many variants)

__Table Scan__
- For each page in the table
    - retrive it from the buffer pool
    - iterate over each tuple and check whether to include it
- The DBMS maintains an internal _cursor_ that tracks the last page/slot it examined

__Index Scan__
- The DBMS picks an index to find the tuples that the query needs
- Which index to use depends on:
    - What attributes the index contains
    - What attributes the query references
    - The attribute's vallue domains
    - Predicate composition
    - Whether the index has unique or non-unique keys

__Multi-Index Scan__


__Sorting__
- Relational Model/SQL is unsorted
- Queries may request that tuples are sored in a specific way (`ORDER BY`)
- But even if a quer does not specify an order, we may still want to sort to do other things
    - Trivial to support duplicate elimination (`DISTINCT`)
    - Aggregations (`GROUP BY`)
    - Merge joins
    - Bulk loading sorted tuples into a B+Tree index is faster

__In-Memory Sorting__
- If data fits in memroy, then we can use a standard in-place sorting algorithms (e.g. quicksort, bubble sorts)

__External Sorting__
- If data does not fit in memroy then we need to use a technique that is aware of the cost of reading and writing disk pages.
- External Merge Sort
    - Divide-and-Conquer algo, that
        - splits data into separate runs
        - sorts them individually, and
        - combines them into longer sorted runs
    - Phase # 1: Sorting
    - Phase # 2: merging

__(Sorted) Run__
- A run is a sorted list of key/val pairs
- Key: the attrbute(s) to compare to compute the sort order
- Value: Two choices
    - Tuple (early materilalization)
    - Record IDs (late materialization)
- Early vs. Late Materialization
    - Early: key -> tuple
    - Late key -> record ID

__2-Way External Merge Sort__
- "2" is the number of runs that we are going to merge in to a new run for each pass
- Data is broken up into N pages
- The DBMS has a finite number of B buffer pool pages to hold input and output data
- First pass: bring each pahe into memory, sort the page by itself, write it back out
- Second pass: generate runs are twice the size of previous pass
- Number of Passes: 1 + log2^n
-In each pass, we read and write every page in the file.
- Total I/O cost: 2N * (# of passes)
- Q: What is the minum # buffer pages does 2-way merge require?
    - B=3 pages, One per each input run and one for the output run
    - Only need one buffer page for output and n pages for n-way merge

__General External Merge Sort__
- Pass #0:
    - Use `B` buffer pages
    - Produce [N / B] sorted runs of size `B`
- Pass #1, 2, 3
    - Merge `B-1` runs (i.e., K-way merge, where K = B - 1)
- Number of passes = 1 + log b-1 ^ [N / B]

__Using B+Tree for Sorting__
- If the table that must be sorted already has a B+Tree index on the sort attribute(s), then we can use that to accelerate sorting.
- Retrieve tuples in desired sort order by simply traversing the leaf pages of the tree.
- Case #1: Clustered B+Tree
    - Traverse to the left-most leaf page, and then retrieve tuples from all leaf pages.
    - This is always better than external sorting because there is no computational cost, and all disk access is sequential.
- Case #2: UnClustered B+Tree
    - Chase each pointer to the page that contains the data
    - This is almost always a bad idea. In genral, one I/O per data record