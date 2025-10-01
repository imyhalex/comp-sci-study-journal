# B+ Tree
- Discuss about another Access Methods: B+ Tree

__DBMS Data Structure Uses__
- Core Data Storage
- Internal Meta-Data
- Temporay Data
- Table Indexes X

__Table Indexes__
- Is a replica of (a subset of) a table's attributes that are organized and / or sorted for efficient access using those attributes
- The DBMS ensures that the contents of the table and the index are logically synchronized
- An index in a database is like the index of a book.
    - A book index doesn’t list the entire content of the book, just keywords and page numbers.
    - Similarly, a table index doesn’t store full rows of the table. Instead, it stores one or more attributes (columns) plus pointers to the full rows.
- Imagine a library:
    - The bookshelf is the actual table (all the rows, data stored unsorted).
    - The catalog card system is the index (sorted by title, or by author).
- Example:
    ```sql
    -- Create a table
    CREATE TABLE Customers (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );

    -- Create an index on email
    CREATE INDEX idx_email ON Customers(email);

    -- Query with index use
    SELECT * FROM Customers WHERE email = 'alice@example.com';
    ```
- It is DBMS admin/user's job to specify what indexs to create
- It is the DBMS's job to figure out the best index(es) to use to execute each query
    - The DBMS Query Optimizer decides whether to use an index (and which one) when a query is run.
    - Sometimes it chooses Index Scan (use the index).
    - Sometimes it chooses Sequential Scan (scan the whole table) if that’s cheaper.
    - Example:
        ```sql 
        EXPLAIN SELECT * FROM Orders WHERE customer_id = 123; 
        ```
        - The `EXPLAIN` output will show if the DBMS used:
        - or Seq Scan on Orders (if the table is small or statistics say index use is slower).
- There is a trade-off regarding the number of indexes to create per database
- Why people do not create lot of indexes
    - Write performance penalty
        - Every INSERT, UPDATE, or DELETE must also update all relevant indexes.
        - If a table has 10 indexes, each write must touch 10 index structures.
        - This can make writes much slower.
    - Storage cost (Storage Overhead)
        - Each index is essentially another data structure (often a B-Tree or hash table).
        - Indexes can easily be as large as, or even larger than, the base table.
        - This increases storage and cache pressure.
    - Maintenance overhead
        - Indexes need to be rebuilt or reorganized sometimes (fragmentation).
        - DBAs must keep track of which indexes are still useful and drop unused ones.
    - Query optimizer confusion
        - Too many indexes can make the optimizer spend extra time figuring out which index to use.
        - It might even choose a suboptimal index if statistics are outdated.

__B+ Tree__
![img](./img/Screenshot%202025-10-01%20004138.png)
- A self-balancing tree data structure that keeps data stored and allow searches, sequential access, insertions, and deletion always in O(log n)
- Generalization of a binary search tree, since a node can have more than two children
- Optimized for systems that read and write large blocks of data
- A B+ Tree is a multi-way serach tree with the following properties:
    - It is perfectly balanced (every leaf node is at the same depth in the tree)
    - Every node other than the root is at leat half-full: `[m / 2] - 1 <= #key <= m - 1` (m / 2 take the ceiling)
        - `m` is the degree of the tree(aka fanout, order, branching factor)
            - degree is the maximum number of children you can have
        - Every node with `d` keys has `d+1` non-null children
        - Root has at least 1 key

__Nodes and B+ Tree Leaf Nodes__
![img](./img/Screenshot%202025-10-01%20010349.png)
![img](./img/Screenshot%202025-10-01%20010436.png)
- Every B+ Tree node is compreised of an aray of key/value pairs
    - The keys are derived from the attribute(s) that the index is based on
    - The value will differ based on whether the node is classified as an inner node or a leaf node
- The array are (usually) kept in sorted key order

__Leaf Node  Values__
- Approach #1: Record IDs
    - A pinter to the location of the tuple to which the index entry corresponds
    - Secondary indexes must store the Record ID as their values
- Approach #2: Tuple Data
    - The leaf nodes store the actual contents of the tuple
    - Only clustered/primary index can do this

__Clustered vs. Non-Clustered Index__
- Clustered Index
    - Index key is the key on which the file is physicaly ordered on disk
    - Physical order: Rows on disk are stored in order of the index key.
    - Leaf nodes: Contain the actual full rows (tuples).
    - only one clustered index per table (One per table: Because the rows can only be physically sorted one way.)
    - sometimes called the "primary index" as the clustering key is often the primary key (Often used as primary index: Usually the primary key, but doesn’t have to be.)
    - Downsides: Inserting into the middle (to keep order) may cause page splits and extra I/O. (requires moving tuples on disk)
- Non-Clustered Index
    - Separate structure: Rows are not ordered by this index.
    - leaf nodes store pointers to tuples multiple non-clustered indexes per table. Leaf nodes: Store pointers (row IDs or clustering key values) that point to the actual rows.
    - called "secondary index": Good for flexible query access (secondary attributes).
    - Many per table: Because you can build multiple lookup structures.
    - Downsides: Requires extra lookup — find in index, then fetch row from table/clustered index (this is called a bookmark lookup).

__B-Tree Family__
- B-Tree
- B+Tree
- B*Tree
- B^link-Tree

__B-Tree vs. B+Tree__
- B-Tree stores keys and values in all nodes in the tree
- B+Tree stores value only in leaf nodes. Inner nodes only guide the search process
- Relative advantage?
    - B-Tree Pros
        - Slightly fewer hops sometimes (can find value in an internal node).
        - May need fewer I/Os if the tree is small.
    - B+Tree Pros (why DBMSs love it)
        1. Better range queries
            - Leaf nodes are linked, so you can scan sequentially (BETWEEN, ORDER BY).
            - B-Tree doesn’t give you this easy linked structure.
        2. More fan-out, shorter height
            - Internal nodes only store keys (not values), so each page can fit more keys.
            - Shallower tree → fewer I/Os.
        3. Uniform access
            - Every search goes all the way to a leaf.
            - More predictable performance compared to B-Tree (sometimes stopping early, sometimes not).
        4. DBMS page-aligned design
            - Works perfectly with fixed-size disk pages (internal = directory, leaf = actual data pointers).

__B+Tree: INSERT__
- Find correct leaf node L
- Insert data entry into L in sorted order
- Otherwise, split L keys into L and new node L2
    - Redistribute entries evenly, copy up middle key
    - Insert index entry pointing to L2 into parent of L.
- To split inner node, redistribute entries evenly, but push up middle key
- Can propagate to root

__B+Tree: DELETE__
- Start at root find leaf L where entry belongs
- Remove the entry
- If L is at least half-full, done!
- Othevise:
    - Try to re-distribute, borrowing from sibling (adjancent node with same partent as L)
    - If re-distribution fails, merge L and sibling
- If merge occured, must delete entry (pointing to L or sibling) from parent of L