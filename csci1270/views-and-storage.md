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

__OS Support for File Management__
- Virtual memory: extends usable memory beyond RAM
- Memory-mapped files: maps a file into virtual address spcae. Allow file to be manipulated like an array
- The DBMS can use memory mapping (mmap) to store the contens of a file into the address space of a program

__Why not use OS__
- DBMS always(almost) wants to control things itself and can do a better job than OS
- Becaue it knows more about the queries being executed
- Examples:
    - Flushing dirty pages to disk in the correct order (for recovery)
    - Specialized prefetching (during scan)
- Sometimes the OS can even get in the way
    - Example: double buffering (in both OS and DBMS)
        - The OS buffer cache already keeps a copy of disk pages in memory.
        - The DBMS often keeps its own buffer pool (a cache of database pages).
        - That means the same data can be cached twice: once by the OS, once by the DBMS.
        - Result: wasted memory and extra copying between the two caches.

__Disk-Oriented DBMS__
![img](./img/Screenshot%202025-09-18%20at%2013.17.29.png)

* **Disk (bottom)** stores the database file, organized into fixed-size **pages** (1, 2, 3, 4, 5, …).
* **Buffer Pool in memory (top)** is the DBMS’s private cache of those disk pages.
* When the execution engine asks for **page #2**, the DBMS checks its buffer pool:

  * If it’s already there → just hand back a pointer.
  * If not → bring it from disk, store it in the buffer pool, then hand back a pointer.

* So: instead of relying on the OS page cache, the DBMS controls **which pages stay in memory** and **how they’re replaced**.

Why not just let the OS handle this? If the DBMS relied on the OS:

1. **Double buffering** → page #2 could live in both the OS cache *and* the DBMS memory. Wasteful.
2. **Wrong eviction policy** → OS might evict a hot DB page (e.g., a B-tree root) while keeping some cold file in RAM. DBMS knows better.
3. **Write-order control** → DBMS needs to flush the WAL log before data pages. The OS might delay or reorder writes, breaking crash recovery guarantees.
4. **Predictable performance** → Databases want consistent latency; OS page cache is optimized for general apps, not high-throughput transactions.

### Questions:

__Q:__ What is Memory-Mapped Files?
- A way for a program to treat the contents of a file as if it were part of the computer's main memory (RAM). 
- Instead of reading and writing normal files I/O system calls, the OS maps the file into the processes's Virtual Address Space
- Means the program can access the file just by using pointers, as if it were an array in memory
- OS handles fetching file data from disk into memory page and writhing changes back to disk when needed

__Q:__ Why DBMS don't rely only (some db like SQLite canuse mmap(), Postgres, MySQL, Oracle, SQL Server not rely at all) on meomry-mapping?
1. Buffer Pool Control
    - A DBMS wants predictable caching (predictable control)
    - With memory-mapping, the OS decides what stays in RAM and what get evicted
    - But database need fine-grained control (e.g. keep hot pages in RAM, flush dirty pages at specific times)
2. Transaction Management & Recovery
    - Database use write-ahead log and careful ordering of writes for crash recovery
    - Memory-mapped file blur when data actually reaches disk (OS may flush lazily)
    - That could violate durability
3. Portability & Performance Tuning
    - Different OSs implement memory-mapping differently
    - DBMS vendors want consistent performance arcoss Linux, Windows, macOS, etc,
    - By managing their own buffer pool, they don't depend on OS heuristics
4. Concurrency Control
    - The DBMS already need to handle locsk, latches, and isolation for queries


## Problem #1: How the DBMS represents the database in files on disk.
- The DBMS stores a database as one or more files on disk typically in a proprietary format.
    - The OS doesn't know anything about the contents of these files.
- The __storage manager__ is responsible for maintaining a database's file
    - Some do their own scheduling for reads and writes to improve spatial and temporal locality of pages.
- It organizes the files as a collection of pages.
    - Tracks data read/written to pages.
    - Tracks the available space.
- A __page__ is a fixed-size block of data
    - It can contain tuples, meta-data, indexes, log records ...
    - Most systems do not mix page types
    - Some systems requires a page to be self-contained
- Each page is given unique identifier
    - The DBMS uses an indirection layer to map page IDs to physical locations.
- Three different notions of "pages"
    - Hardware Page (usually 4KB)
    - OS Page (usually 4KB)
    - Database Page (4KB-16KB)
- A hardware page is the largest block of data that the storage device can guarantee failsafe writes (e.g., all or nothing).

__Page Storage Architecture__
- Heap File Orgainzation
- Sequential / Sorted File Organization (ISAM)
- Tree File Orgainzation
- Hashing File Organization

__Heap File__
- A __heap file__ is a collection of pages with tuples that are store in random order
    - create/get/write/delete page
    - must also support itertion over all pages
- Page Directory
    - The DBMS keeps special directory pages that point to the data pages
    - The directory tracks:
        - Which pages exist
        - How much free space each has
        - Which one are empty and reusable


__Header__
- Every `page` contains a header of meta-data about the pages's content
    - Page Size
        - Confirms the byte length (e.g. 4KB, 8KB, 16KB)
    - Checksum
        - A small hash to detect corruption
    - DBMS version
    - Transaction Visibility
        - Metadata for concurrency control
    - Compression Information
        - Indicates if the page is compressed, and if so, how to decompress it.
        - Saves disk space and sometimes I/O costs.
- Some systems require pages to be self-contained (e.g. Oracle)

__Page Layout (Big Picture)__
- Two approach:
    - Tuple-oriented (Tuple Storage):
        - The page is like a simple array of tuples.
        - The DBMS keeps a counter of how many tuples are stored.
        - New tuple -> append at the end of the page
        - Keep track of the number of tuples in a page and then just append a new tuple to the end
            - What happend if we delete a tuple?
                - Leave a hole
                - DBMS must either:
                    - Mark the slot as free and reuse it later, or
                    - Compact the page (move tuples around)
            - What happend if we have a variable-length attributes?
                - Harder, becuase not every tuple is the same size
                - Compating after deletion get expensive
    - Log-structured
        - Inspired by log-structured file systems.
        - Instead of overwriting or compacting, the DBMS appends changes like a log.
        - Old versions stay around until garbage collection.

__Slotted Pages (Alternative approach for Tuple Storage, refined solution)__
- The most common layout scheme
- The slot arrray maps slot to the tuple starting position offsets
- The header keeps track of 
    - the number of used solts
    - the offset of the __starting location of the last slot used__
- Each tuple has a fix slot entry (slot directory):
    - (`offset`, `length`, `flags`)
    - offset → where the tuple starts.
    - length → how big the tuple is.
    - flags → e.g., valid/deleted.
- Compaction can be delayed
    - Compaction = rearranging tuples inside a page to eliminate holes and make free space contiguous.
- More precise explaination:
    - tuples can be:
        - variable length
        - inserted/deleted
        - compacted over time


__RECORD IDs (addressing tuples)__
- A tuple is identified by (page_id, slot_id) instead of “raw offset.”
- Because slots point to offsets, a tuple can move inside the page (during compaction) but still be found via the same record ID.
- The DBMS needs a way to keep track of individuals tuples
- Each tuple is assigned a unique __record identifier__
    - RID = (`page_id`, `slot_id`)
    - Most common: `page_id` + `offset` or `slot`
    - Can also contain file location info
- An application cannot rely on these IDs to mean anything

__Tuple Header (metadata about the tuple itself)__
- Stored alongside the tuple’s data.
- Tracks concurrency (visibility info), and whether attributes are NULL (via bitmap).
- Each tuple is prefixed with a header that contains meta-data about it
    - Visibility info(concurrency control)
    - Bit Map for NULL values
- We do not need to store meta-data about the schema

__Tuple Data (actual user attributes)__
- Laid out in the order of the schema (unless DBMS optimizes).
- Attributes are typically stored in the order that you specify them when you create the table.
- This is done for software engineering reasons (i.e., simplicity).
- However, it might be more efficient to lay them out differently.

__Bitmap for NULL Values (within tuple header)__
- Compactly encodes which attributes are NULL so you can skip storing them.
- At the start of each tuple, the DBMS keeps a small bitmap.
- Each bit corresponds to one attribute.
    - 0 → value is present
    - 1 → value is NULL
- If the attribute is NULL, the actual storage for that value is skipped.
- Example:
    - Suppose a table row has 4 attributes: (id, name, age, salary)
    - Tuple header bitmap = 0101
        - id: 0 → present
        - name: 1 → NULL
        - age: 0 → present
        - salary: 1 → NULL
    - Then the tuple only stores the values for id and age
- Q: Benefits? 
    - Saves space (no wasted bytes for NULL attributes).
    - Makes it fast to check if an attribute is NULL (just look at the bitmap).
    - Works well with variable-length attributes, since you know exactly which ones to skip.

__Final Illustration (illustration of a single page)__
```txt
[ Page Header | ... Tuple Area ... | Slot Directory ]
                     |
                     --> [ Tuple Header | Bitmap | Attributes ]
                            |
                            --> [ Tuple Header 
                                    | Null Bitmap 
                                    | Offsets (if variable-length) 
                                    | Attributes ]
                     --> [ Tuple Header | Bitmap | Attributes ]

Page Header = metadata about the page.
Tuple Area = actual stored tuples (headers + data).
Slot Directory = fixed-size entries pointing to each tuple’s offset.
Tuple Header = per-tuple metadata (visibility, null-bitmap).
Attributes = the actual row values.
```
_Takeaways (`For variable-length fields, if the value is null, what would be stored in the offset and
length fields?`):_
- What if the value is NULL?
    - The null bitmap already says "this attribute is NULL, don't read it."
    - So the actual offset/length does not matter: the DBMS won’t use them.
    - To avoid confusion, most system just set `offset = 0` and `length = 0` as a consistent convention

## Problem #2: How the DBMS manages its memory and moves data back-and-forth from disk.
__Buffer Pool Organization__
- High-Level Concepts:
    - Memory region is organized as an array of fixed-size pages.
    - An array entry is called a frame.
    - When the DBMS requests a page, an exact copy is placed into one of these frames.
    - Dirty pages are buffered and not written to disk immediately
        - Write-Back Cache (vs. Write-Through Cache)
- More precisily explainations:
    - Buffer pool = Managed Region of RAM
    - Buffer pool is the middleman between DBMS and the disk
        - Query needs a tuple -> DBMS figures out which page it lives on (by `page ID`)
        - DBMS checks if that page is already in the buffer pool (RAM)
            - If yes -> return the in-memory copy
            - If no -> DBMS issues an I/O to the disk, load the page into a free frame in the buffer pool
        - Page Modification (Write path)
            - If a tuple is inserted/upadted/deleted, the change is made __only in the buffer pool copy__
            - The page is now marked __dirty__
            - Later, the DBMS will flush the dirty page back to disk (write-back policy)

__Buffer Pool Meta-data__
- The page table keeps track of pahes that are currently in memory
- Ususally a fix-sized map protected with latches to ensure thead-safe access
    - Protect in-memory structures (like a buffer pool page, hash table bucket, or slot array).
    - Very short-lived — usually only held for the few microseconds while a thread reads or updates that structure.
    - Invisible to the user — purely an implementation detail.
- Also maintains additional meta-data per page:
    - Dirty Flag means:
        - The page in the buffer pool (RAM) has been modified (some tuple was inserted, deleted, or updated).
        - The version on disk is now out of date compared to the version in memory.˝
    - Pin/Reference Counter
- _Question_: The DBMS cannot evict pages from the buffer pool if the dirty flag is set to true. (True/__False__)
    - If a page’s dirty flag = true, it just means the page has changes that haven’t been written back to disk yet.
    - The DBMS can evict it — but only after flushing the page to disk first (to preserve durability).
    - So the sequence is:
        - See dirty flag = true.
        - Write the page back to disk (flush).
        - Mark dirty flag = false.
        - Now evict it from the buffer pool.

