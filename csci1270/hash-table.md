# Hash Table

__DBMS has two type of Data Structure:__
- Hash Tables
- Trees

__DBMS DATA STRUCTURE USES__
- Core Data Storage
- Internal Meta-Data
- Temporay Data
- Table Indexes

__Design Decision:__
- Data Origanization
- Concurrency

__Hash Table__
- Implements an unordered assositavie array that maps key to values
- Uses a has function to compute an offset into this array for a given key, from which the desired value can be found
- Space Complexity: O(1)
- Time Complexity: O(1) average, O(n) worst
- Simple Static Hash table
    - Allocate a giant array that has one solots for every elements you need to store
    - To find an entry , mod the hash value by the number of elements to find the offset in the array
    - (Unrealistic) Assumptions
        - Assumption 1: Number of elements is known ahead of time and fixed
        - Assumption 2: Each key is unique
        - Assumption 3: Perfect hash function
            - if key1 != key2, then hash(key1) != hash(key2)
- Design Decisions:
    - Decision 1: Hash Function
        - How to map a large key space into a dmaller domain
        - Trade-off between being fast vs. collision rate
    - Decision 2: Hashing Scheme
        - How wto handle key collision after hashing
        - Trade-off between allocating a large hash table vs. additional instructions to get/put keys.
__Hash Function__
- For an input key, return an integer representation of that key
- We want something that is fast and has a low collision rate.
- We don't want/need cryptograpgic hash functions for DBMS hash tables (e.g. SHA2)
- Examples:
    - CRC-64 (1975)
    - MurmurHash (2008)
    - Google CityHash (2011)
    - Facebook XXHash (2012)
    - Google FarmHash (2014)

__Static Hashing Scheme__
- Definition: Hash table of fixed size.
- Problem: Multiple keys may map to the same slot (collision).
- Solution: Use a collision resolution strategy.
- Limitation: If load factor grows too high → must rebuild from scratch.
- Use case: Often inside query execution operators (e.g., hash join).
- Fixed size hash table; resize from scratch ad needed typically used during query execution
- Approaches:
    - Approach 1: Linear Probe Hashing (90% of the commercial DBs)
        - Idea: If the target slot is occupied, linearly check the next slot (wrapping around if needed) until you find a free spot.
        - Pro: Very cache-friendly (good locality).
        - Con: Clustering problem — once a run of occupied slots forms, it grows quickly.
        - DELETE:
            - Approach 1: Rehash Keys until you find the first empty slot
            - Approach 2:
                - Set a marker to indicate that the entry in the slot is logically deleted.
                - You can reuse the slot for new keys.
                - May need periodic garbage collection.
    - Approach 2: Robin Hood Hashing
        - Idea: Like linear probing, but tries to balance probe sequence lengths.
        - Rule: When inserting, if the current key has probed fewer steps than the resident key, they swap. (“Steal from the rich, give to the poor.”)
            - If a new key had to probe 3 steps, but it finds a key that only probed 1 step → swap them.
            - Example: `key | val [0]` <- a meta data of "jumps" from first posistion
        - Pro: Reduces variance of search times → fairer.
        - Con: More complicated to implement than simple linear probe.
        - Each key tracks the number of positions they are from where its optimal position in the table
        - On insert, a key takes the slot of another key if the first key is farther away from its optimal position (poor key) than the second key (rich key).
    - Approach 3: Cuckoo Hashing
        - Idea: Each key can live in one of two (or more) possible positions, each determined by a different hash function.
        - Insert: If both spots full, evict the existing key (“kick it out”), and reinsert it into its alternate location. This may cascade.
        - Pro: Lookup is O(1) worst case (check at most 2 slots).
        - Con: Insertions can be expensive (lots of kick-outs, may need rehash).
        - On insert, check every table and pick anyone that has a free slot.
        - If no table has a free slot, evict the element from one of them and then re-hash it to find a new location.
- Summary:
    - Static hash tables require the DBMS to know the number of elements it wants to store.
        - Otherwise, it must rebuild the table if it needs to grow/shrink in size.
        - Based on the Load Factor (_lf_) is a meausre of how full the table is
            - Typically, # full slots / # slots. E.g. ff _lf_ > 0.7, double size
            - Reduce collisions but increase memory usage
__Dynamic Hashing Scheme__
- Table can grow/shrink as to support more/less key support incremental sizing
- Chained Hashing
    - Idea: Each slot of the hash table points to a linked list (or bucket) of records.
    - If collisions occur, all items with the same hash are chained together.
    - Dynamic because lists can grow without resizing the table.
    - Con: Worst-case lookup is O(n) if many items hash to the same slot.
    - Pro: Simple and flexible (easy insert/delete).
- Extendible Hashing
    - Idea: Uses a directory of pointers to buckets.
    - The directory can double in size when buckets overflow.
    - Each bucket has a “local depth” (how many hash bits are being used).
    - Very popular in databases because you can grow/shrink gracefully.
- Linear Hashing
    - Idea: Instead of doubling the directory, it splits buckets gradually.
    - Uses a “split pointer” that moves through the table one bucket at a time.
    - This way, resizing is incremental, not a sudden doubling.
    - Lookup may require checking one of two possible buckets depending on whether it has been split yet.

- __Q__: Why Chain Hashing is not a great idea?