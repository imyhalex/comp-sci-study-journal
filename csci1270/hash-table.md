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

## Static Hashing Scheme
- Definition: Hash table of fixed size.
- Problem: Multiple keys may map to the same slot (collision).
    - 
- Solution: Use a collision resolution strategy.
- Limitation: 
    - If the table becomes too full (the load factor gets high), then collision become more frequent and performance drops
        - Load Factor = (# filled slots) / (total slots)
        - Example: 70 slots filled out of 100 -> load factor = 0.7
        - Once it gets too high (say > 0.7), the only fix is to rebuild the table from strach: you cannot just expand it easily
- Use case: 
    - Often inside query execution operators (e.g., hash join).
    - This hash table:
        - Exisits only during query execution
        - Is discarded after the query finishes
        - So it’s fine if it’s static: it’s short-lived and rebuilt each time
- Fixed size hash table; resize from scratch ad needed typically used during query execution
- There are three main way to handle collisions:
    - Aproach #1: Linear Probe Hashing
    - Approach #2: Robin Hood Hashing
    - Approach #3: Cuckoo Hashing

__Approach #1: Linear Probe Hashing (90% of the commercial DBs)__
```text
index = hash(key)
if slot[index] is full:
    index = (index + 1) % table_size
```
- Idea: 
    - If your target slot is taken, just move forward linearly (check the next slot, and warp around if you reach the end) until you find an empty one.
- Pros: Very cache-friendly (good locality, slots are next to each other).
- Cons: 
    - Clustering problem: once consecutive filled slots start forming, they grow like a chain and slow down future lookups
- DELETE strategies:
    - Rehash: 
        - Remove the key and reinsert others that follow until you hit an empty slot.
    - Lazy delete:
        - Make slots ad deleted and reuse it later
        - Set a marker to indicate that the entry in the slot is logically deleted.
        - You can reuse the slot for new keys.
        - May need periodic garbage collection.

__Approach #2: Robin Hood Hashing__
- Idea:
    - A smarter version of linear probing: tries to make search time fairer
    - Each key keeps track of how far it is from its idea position
- Rule: When inserting, if the current key has probed fewer steps than the resident key, they swap. (“Steal from the rich, give to the poor.”)
    - If a new key had to probe 3 steps, but it finds a key that only probed 1 step → swap them.
    - Example: `key | val [0]` <- a meta data of "jumps" from first posistion
- Pros: 
    - Reduces variance of search times → fairer.
    - Equalizes probe lengths → more predictable performance.
- Cons: 
    - More complicated to implement than simple linear probe.
- Each key tracks the number of positions they are from where its optimal position in the table
- On insert, a key takes the slot of another key if the first key is farther away from its optimal position (poor key) than the second key (rich key).

__Approach #3: Cuckoo Hashing__
- Idea: 
    - Each key has two (or more) possible homes, each decided by a different hash function.
    - Each key can live in one of two (or more) possible positions, each determined by a different hash function.
- Insert: If both spots full, evict the existing key (“kick it out”), and reinsert it into its alternate location. This may cascade.
- Pro: Lookup is O(1) worst case (check at most 2 slots).
- Con: 
    - Insertions can be expensive (lots of kick-outs, may need rehash).
        - Insertions can trigger a chain of evictions, which is expensive.
    - Might have to rebuild the whole table if cycles form.
- On insert, check every table and pick anyone that has a free slot.
- If no table has a free slot, evict the element from one of them and then re-hash it to find a new location.

__Summary:__
- Static hash tables require the DBMS to know the number of elements it wants to store.
    - Otherwise, it must rebuild the table if it needs to grow/shrink in size.
    - Based on the Load Factor (_lf_) is a meausre of how full the table is
        - Typically, # full slots / # slots. E.g. ff _lf_ > 0.7, double size
        - Reduce collisions but increase memory usage

## Dynamic Hashing Scheme
- Table can grow/shrink as to support more/less key support incremental sizing

__Chained Hashing__
- Idea: 
    - Each slot of the hash table points to a linked list (or bucket) of records.
- If collisions occur, all items with the same hash are chained together.
- Dynamic because lists can grow without resizing the table.
- Cona: 
    - Worst-case lookup is O(n) if many items hash to the same slot.
    - User extra memory of pointers.
- Pros: 
    - Simple and flexible (easy insert/delete).
    - No need to resize the table


__Extendible Hashing[[Link1](https://www.youtube.com/watch?v=Bxfo2LwOIj4) | [Link2](https://en.wikipedia.org/wiki/Extendible_hashing)]__
- Two common way: LSB vs. MSB
- Idea: 
    - Instead of one big array, we have a directory for pointers to buckets
    - Each bucket holds the actual data records
    - As buckets overflow, the table splits. And occasionally, the directory doubles in size.
    - Uses a directory of pointers to buckets.
    - The directory can double in size when buckets overflow.
- Each bucket has a “local depth” (how many hash bits are being used).
- Very popular in databases because you can grow/shrink gracefully.
- __How it Works__
    1. Hash the key (bit string)
    2. Insert into the bucket
        - If the bucket has room, inert it
        - If it is full: overflow occurs
    3. Handle overflow
        - Case A: the bucket's `Local Depth` < `Global Depth`
            - Increments its `Local Depth`
            - Split the bucket into two:
                - one gets entries with bit = 0
                - the other with bit = 1 (based on the new bit)
            - Update the directory pointers to point to the right buckets
            - No directory expansion is needed
        - Case B: The bucket's `Local Depth` == `Global Depth`
            - You cannot split with the same number of bits, so:
                - Increment `Global depth`
                - Double the directory
                - Then split the bucket and update the directory
            - This is called Directory Expansion
- `Directories`: The directory store addresses of the buckets in pointers. And id is assigned to each directory wich may change each time when Directory Expansion takes place.
    - __directory size = 2 ^ global_depth__
- `Buckets`: The buckets are user to hash tha actual data
    - has a local depth showing how many bits of the hash are actually being used.
- `Global Depth`: It is associtated with the Directories. They denote the number of bits which are used by the hash function to categorize the keys. Global Depth = Number of bits in directory id.
- `Local Depth`: It is the same as that Global Depth except for the fact that Local Depth is associated witht the buckets and not the directories. 
    - Local Depth is accodance with global depth is used to decide the action that to be performed in case an overflow occurs.
    - Local Depth is always less than or equal to Global Depth
- `Bucket Splitting`: When the number of element in a bucket exceeds a particular size, then the bucket is split into two parts
- `Directory Expansion`: Directory Expansion takes place when a bucket overflow.
    - Note: It happend only when bucket's new Local Depth > Global Depth
    - If a bucket overflows:
        - Increase its local depth by 1 (LD++).
        - If the new LD ≤ GD → just split, no directory expansion.
        - If the new LD > GD → must expand the directory (GD++).
    - Why video says that a bucket hit its cap and LD = GD, need to directory expaision?
        - You have LD = GD at overflow.
        - After split → LD = GD + 1.
        - That means LD > GD → forces directory doubling.

__Linear Hashing__
- It grows gradually rather than doubling the directory at once.
- Idea:
    - The hash table has buckets numbered 0..N−1.
    - When the table fills up, split buckets one at a time, in sequence (0, 1, 2...).
    - A split pointer marks which bucket to split next.
- This avoids the sudden "doubling" of extendible hashing

__Hashing__
- Idea: Instead of doubling the directory, it splits buckets gradually.
- Uses a “split pointer” that moves through the table one bucket at a time.
- This way, resizing is incremental, not a sudden doubling.
- Lookup may require checking one of two possible buckets depending on whether it has been split yet.

## Quesions:
- __Q:__ Is it possible that a page is less than half-full (utilization < 50%), in extendible hashing?
(__Yes__/No)
    - Extendible hasihing __only splits bucket when overflow but never merge buckets when they underfilled__
    - So after a few insertions and splits, some buckets can end up holding just 1 or 2 records. Far less than 50% full: because the data distribution may not be even.

- __Q:__ Can we have 6 directory entries, pointing to the same disk page? (Yes/__No__)
    - Because the number of directory entires pointing to a single bucket must be a __power of two.__
    - Each bucket corresoponds to all directory indices that share the same prefix of `LocalDepth` bits
        - That is why
            - 1 entry → 2^0
            - 2 entries → 2^1
            - 4 entries → 2^2
            - 8 entries → 2^3
            - ..etc.