# Index Concurrency

__Concurrency Control__
- A concurency control protocol is the method that the DBMS use to ensure "correct" results for concurrent operations on a shared object,
- Why we need concurrency control in indexes
    - When multiple threads query or update a B+Tree simultaneously
        - They may __read or modify__ the same node concorrently
        - Or restructure the tree (split, merges) at the same time
    - Two types of correctness must be ensured
        - Logical Correctness: The results seen by users (e.g. records read or writen) are consistent with isolation semantics.
        - Physical Correctenss: The in-memory structure (pointers, node contents) remains valid and crash-safe even under concurrent access

## Physical Correctness

__Lock vs. Latches__
- Locks:
    - Protects: Logical content (rows, tables)
    - Scope: Transaction-level
    - Duration: Held for entire transaction
    - Purpose: Ensure isolation
    - Managed by: Lock Manager
    - Modes: Shared, Exclusive, Intent
- Latches
    - Protects: Physical data structure (nodes, pages)
    - Scope: Thread-level (short critical section)
    - Duration: Held only during operation
    - Purpose: Ensure structural integrity
    - Managed by: In-code critical sections (mutex-like)
    - Modes: Read, Write

__Latches Mode__
- Read Mode (R latch)
    - Many thread can safely red the same node
    - Multiple thread can read the same object at the same time
    - A thread can acquire the read latch if another thread has it in read mode
- Write Mode  
    - Exclusive: one thread only.
    - Only one thread can access the object
    - A thread cannot acquire a write latch if another thread has it in any mode

__B+Tree Concurrency Control__
- We need to allow concurrent:
    1. Read: multiple traversing the tree
    2. Updates (insert/delete): possibly restructing (splits/merges)
- Challenges:
    - Avoid race condition when multiple threads access/modify same node
    - Prevent structural coruption during concurrent splits/merges.
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

- __Addition Explainations__
    - This is the standard B+Tree concurrency algorithm
    - Basic Idea:
        - As you go down the tree, you __hold latches in parent and child__ temporaily
        - Once the child is "safe", you release the parent
        - "Safe" = node will not need to split or merge
    - Definition of "Safe":
        - Inert: Node is not full
        - Delete: Node is more than half-full
    - Example Find (Read-Only):
        - Start at root with __R latch__.
        - Before moving to child:
            - Acquire __R latch__ on child
            - Release __R latch__ on parent
        - Repeat until leaf
        - Allows concurrent readers to move through tree without blocking
    - Example: Insert/Delete(Update)
        - Start at root with __W latch__
        - Acquire W latch on child
        - Check if child is safe:
            - If safe -> releaase all ancestor latches (less blocking)
            - If unsafe -> hold parent latch (to safely split/merge later)
        - Continue downward

__Optimistic Latching Algorithms__
- __Observation:__ Most modification to a B+Tree will not require a split or merge
- Instead of assuming that there will be a split/merge, optimistically traverse the tree using read latches.
- If you guess wrong, repeat traversal with the pessimistic algorithm.
- Observations
    - The threads acquire "top-down" manner
        - A thread can only acquire a latch from a node that is below its current node
        - If the desired latch is unavaible, the thread must wait until it becomes available.
- Search: Same as before
- Insert/Delete:
    - Try to acquire W latch
    - If leaf is safe -> perform update
    - If not safe -> release everything and retry using full pessmistic protocal
- Pros:
    - Fewer write latches (less blocking)
    - Works well under low contention
- Cons:
    - If your guess was wrong (usafe leaf), must restart
- Works of low contentions case
- Top-Down Latch Acquistition Rule
    - All thread acquire latches __top-down:__
        - From Parnet -> child (never upward)
        - Prevents circular wait conditions
    - If latch unavailable -> thread waits
    - This ordering ensures no deadlocks (since all threads move in same direction)
- Deadlocks
    - Locks (transaction-level) can deadlock.
    - Latches do not, because:
        - Acquired in strict top-down order.
        - Released immediately when safe.
        - No cyclic waiting possible.

## Questions:
```text
In B+-tree concurrency control, which are true of the latch crabbing (hand-over-hand)
protocol? (Select all that apply)
a. Allows multiple threads to traverse the tree concurrently.
b. Always holds latches on all ancestor nodes until commit.
c. Releases parent latches once the child is known to be “safe.”
d. Prevents structural corruption during splits or merges.
e. Ensures logical isolation across transactions.
```
- False options: b, e
    - b. Always holds latches on all ancestor nodes until commit.
        - This would make the system extremely slow and serial.
        - Crabbing does the opposite: “Release the latch for the parent once the child is safe.”
        - You don’t hold all ancestor latches to the end: you only hold them temporarily while moving down.
        - __Commit__ is a transaction-level event, while latches are operation-level (short-lived). So b is wrong both conceptually (about “until commit”) and mechanically (we release ancestors early).
    - e. Ensures logical isolation across transactions.
        - So latch crabbing does not prevent one transaction from reading data another transaction is concurrently writing: that’s __logical isolation, handled later by the lock manager__ during transaction processing.