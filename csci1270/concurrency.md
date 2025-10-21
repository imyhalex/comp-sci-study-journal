# Index Concurrency

__Concurrency Control__
- A concurency control protocol is the method that the DBMS use to ensure "correct" results for concurrent operations on a shared object,
- A protocol's correctness criteria can vary:
    - Logical Correctness: Can a thread see the data that it is supposed to see?
    - Physical Correctenss: Is the internal representation of the data structure sound?

## Physical Correctness

__Lock vs. Latches__
- Locks:
    - Protect the database's logical contents from other transactions
    - Held for the transaction's duration 
- Latches
    - Protect the critical sections of the DBMS's internal data structures from other threads
    - Held for operation duration.

__Latches Mode__
- Read Mode
    - Multiple thread can read the same object at the same time
    - A thread can acquire the read latch if another thread has it in read mode
- Write Mode  
    - Only one thread can access the object
    - A thread cannot acquire a write latch if another thread has it in any mode

__B+Tree Concurrency Control__
- We want to allow multiple threads to read and update a B+Tree at the same time
- We need to protect against two types of problems
    - Threads reading & modfying the contents of a node at the same time (single node)
    - Threads traversing & updating the tree structure (splts/merges) at the same time (multi node)

__Latch Crabbing / Coupling (hand-over-hand latching) in B+Tree__
- Protocol to allow multiple threads to access/modify B+Tree at the same time
    - Get latch for parent
    - Get latch for child
    - Release leath for parent/all ancestors if child is "safe"
- A safe node is one that will not split or merge when update
    - Not full
    - More than half-full (on delete)
- Find: Start at root with an R latch and traverse down the tree
    - Acquire R latch on child
    - Then unlatch parent
    - Repreat untill we reach the leaf node
- Insert/Delete: Start at root and go down, obtaining W latches as needed. Once child is latched, check if it is safe:
    - If child is safe, release all latches on ancestors
- Observations:
    - What was the first step that all the update examples did on the B+Tree?
        - Taking a write latch on the root every time becomes a bottleneck with higher concurrency.

__Optimistic Latching Algorithms__
- Most modification to a B+Tree will not require a split or merge
- Instead of assuming that there will be a split/merge, optimistically traverse the tree using read latches.
- If you guess wrong, repeat traversal with the pessimistic algorithm.
- Search: Same as before
- Insert/Delete:
    - Set latches as if for search, get to leaf, and set W latche on leaf
    - If leaf is not safe, release all latches, and restart thread using previous insert/delete protocol with write latches
- Works of low contentions case
- Observations
    - The threads acquire "top-down" manner
        - A thread can only acquire a latch from a node that is below its current node
        - If the desired latch is unavaible, the thread must wait until it becomes available.
    