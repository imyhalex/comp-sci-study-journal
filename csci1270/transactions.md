# Transactions
- Is the execution of a sequence of one or more operations (e.g SQL queries) on a database to perform some higher-level function
- It is the atomic unit of change in a DBMS
    - Partial transactions are not allowed

__Transaction in SQL__
- A new transaction starts with `BEGIN` command
- The transaction stops with either `COMMIT` or `ABORT/ROLLBACK`
    - If abort, all changes are undone so that it is llike as if the trasaction never executed at all
    - If commit, the DBMS either save all the trasaction's changes or abort it
- So abort can be either:
    - self-infliceted by ABORT or caused by the DBMS

__Definitions__
- A transaction may carry out many operations on the data retrived from the database
- The DBMS is only concerned about what data is read/written from/to the database
    - Change to the "outside world" are beyond the scope of the DBMS
- Formal Definition
    - Database: A fixed set of name data object/entities (e.g. A, B, C, ...)
    - Transaction: A sequence of read and write operations (e,g. R(A), W(B))
    - This is DBSM's abstract view of a user program

__Transactional Properties: ACID__
- Atomicity: All actions in transaction happen, or non happen.
- Consistency: If each transaction is consistent and DB starts consistent, then it remains consistent after transaction.
- Isolation: Execution of one transaction is isolated from that of other transactions
- Durability: If a transaction commits, its effects persist.

__Consistency__
- If a transaction executes on a consistent db state, it produces another consitent database state
- A consistent db state satisfies all integrity constraint and application-level rules
- This is shared respoinsibility of the user/application and the DBMS
    - Applications sepcify all integrity constraints and rules
    - DBMS enforces those during the transaction execution
        - Even when multiple transactions are running concurrently

__Isolation of Transactions__
- User submit transactions, and each transaction executes as if it was running by itself
    - Easier programming model to reason about
- But the DBMS achieves concurrency (thus higher performance) by interleaving the actions (read/write of DB object) of transactions
- We need a way to interleave transactions but the end result should appear as if they ran one-at-a-time
- The DBMS does not guarantee execution order based on submission order.
- It only guarantees serializability: i.e., that the final state is equivalent to some serial order.

__Interleaving Transactions__
- We interleave txns to increase concurrency
    - Slow disk/network I/O.
    - Multi-core CPUs.
- When one txn stalls because of a resource (e.g., page fault), another txn can continue executing and make forward progress.
- It would only be logically wrong if:
    - The order matters semantically to the user (e.g., “transfer before applying interest” must always happen).
    - And the system doesn’t enforce that order (because it allows concurrent execution).
    - In that case, the user (or application) must explicitly control the order, for example:
        ```sql
        BEGIN;
        EXECUTE T1;
        EXECUTE T2;
        COMMIT;
        ```

__Formal Properties of Schedules__
- Serial Shcedule
    - A schedule that does not interleave the actions of different transactions
- Equivalent Schedules
    - For any database state, the effect of executing the first schedule is identical to the effect of executing the second schedule.
- Serializable Schedule
    - A schedule that is equivalent to some serial execution of the transactions.
    - __Connecting back to Consistency__: If each txn preserves consistency (which we assume), every serializable schedule preserves consistency.
    - Serializability is a less intuitive notion of correctness compared to txn initiation time or commit order, but it provides the DBMS with more flexibility in scheduling operations.
        - More flexibility means better parallelism.


__How to Determine Seralizability__
- Check to see if a particular shceudle produces a state equivalent to a db state that results from a serial execution?
- When multiple transactions run concurrently, we want to ensure they behave as if they ran one after another (in some
order).
- That’s what “serializability” means:
    - A concurrent (interleaved) schedule is serializable if its final result (and all read/write effects) are the same 
    as some serial execution of those transactions.
    - So:
        - If the interleaved schedule’s final database values are identical to one of the serial orders (e.g., `T₁→T₂` or `T₂→T₁`), that schedule is serializable.
- What if N! serial order: not pratical


__Alternative: Serializability Using Conflicting Opeartions__
- Instead, we used a formal notion of equivanence that can be implemented efficienctly based on the notion of "conflicting" operations
- __Two operations conflict if__:
    - They are from different transactions
    - They access the same data item
    - At least one is a write
    - __Meaning of “Not Conflict-Serializable”__
        - There is no equivalent serial order of the transactions that produces the same result on the database.
        - The interleaving operations changes the final outcome compared to any serial (one-after-the-other)
        - The database may end up in a state that could not happend if transactions had run one at a time
- Interleaved Execution Anomalies
    - Read-Write Conflict (R-W)
    - Write-Read Conflicts (W-R)
    - Write-Write Conflicts (W-W)

__Why Care About Conflicting Operations__
- Read-Write Conflict
    - __Unrepeatable Read:__ Txn gets different values when reading the same object multiple times.
    - Examle: T1 reads A, then T2 writes A
- Write_read Conflict
    - __Dirty Read:__ One txn reads data writen by another txn that is not commited yet
    - Example: T1 writes A, then T2 reads A
- Write-Write Conflicts
    - __Lost Update:__ One txn overwites uncommited data from another uncommited txn
    - Example: T1 writes A, then T2 overwrites A

__Conflict Serializable Schedules__
- Two schedules are conflict equivalent if:
    - They involve the same set of operations
    - The order of every conflicting pair of opeartions is the same
- Schedule S is conflict serializable if:
    - S is conflict equivalent to some serial schedule
    - Intuition: you can transform S into a serial schedule by swapping consecutive non-conflicting opeartions of different transactions.
- A schedule is conflict-serializable if:
    - It can be transformed into a serial schedule by swapping non-conflicting operations.

__Dependency Graphs__
![img](./img/Screenshot%202025-10-24%20120327.png)
![img](./img/Screenshot%202025-10-24%20120327.png)
![img](./img/Screenshot%202025-10-24%20120559.png)
- An efficient way to check serializability:
    - Create one node per transaction.
    - For every conflict Ti → Tj, draw a directed edge.
    - If the graph is acyclic, the schedule is conflict-serializable.

__Serrializability__
- In practice, Conflict Serializability is what systems support becuase it can be enforced efficiency.
- There are more flexible notions such as View Serializability, which is hard to enfoce
- To allow more concurrency, some special cases can get handled separately at the application level
- Allows parralelism on the inside, but (look like) one-at-a-time outside.

# Transaction II

__Executing With Locks__
![img](./img/Screenshot%202025-10-28%20115119.png)
- T1 beigns and request lock on A
    - `LOCK(A)` by T1
    - Lock Manager checks if A is free -> Granted (T1 -> A)
    - T1 can now safely read/write A
- T2 beigns and requests a lock on A (while T1 still holds it) 
    - LOCK(A) by T2
    - Lock Manager sees A is already locked by T1 -> Denied(T2 waits)
- T1 continues working
    - Peforms `R(A)`, `W(A)` while holding the lock
    - Then execute `UNLOCK(A)` -> Lock Manager marks A as released(T1 -> A)
- Lock Manager rechecks the waitithing queue
    - It sees T2 has been waiting -> now grants the lock to T2 Granted(T2 -> A)
- T2 executes its read/write operations
    - Reads and writes A
    - Finally `UNLOCK(A)` -> Released(T2 -> A)

__Using Locks__
- Transactions request locks
- Lock Manager grants or blocks requests
- Transactions release locks
- Lock manager updates its internal lock table
    - It keeps track of what transactions hold what locks and what transactions are waithing to acquire any locks.
- Lock Manager's Job
    - Maintains an internal lock table
        - Which transactions hold which locks
        - Which transactions are waititing
    - Handles grant, block and release requests

__Concurrency Control Protocol__
- __Example__
    ![img](./img/Screenshot%202025-11-08%20140608.png)
    - Explain
        - X-lock granted to T1
        - T1 releases its lock before commit
        - Then T2 get the lock, modifies A
        - T1 still hasn't committed yet (not finished)
        - After T2 commits, T1 later commits too
- __Why locking alone does not guarantee conflict-serializability__
    - Bcause just "having locks" does not force transactions to hold them long enough to preserve serializability
    - A system can use locks. but if transactions: Release them too early(before commit), Or reacquiring locks after releaseing
        - then operations can interleave in a non-serializable way.
- __Two-phase locking (2PL)__ 
    - Is a concurrency control protocol that determines whether a txn can access an objeect in the database at runtime
    - The protocol does not need to know all the queries that a txn will execute ahead of time
    - GOAL: Ensure that all interleaved transactions still hebave as if they ran in some serial order

__Two-phase locking (2PL)__
- This definition describes the per transactions level:
    - Each transaction has its own growing phase and shrinking phase
    - A transaction can keep acquiring new locks as long as it hasn’t started unlocking anything.
- Phase #1: Growing
    - Each txn requests the locking that needs from the DBMS's lock manager
    - The transaction can request new locks (shared or exclusive)
    - The lock manager grants or denies them depending on conflicts
    - Once a transaction release its first lock, this phase __ends__
- Phase #2: Shrinking
    - After releasing a lock, the transaction cannot request or upgrade any new locks
    - It can only release the ones it already holds
- __Why 2PL Guarantees Conflict-Serializability__
    - Every conflicting pair ot transactions will have a clear order in which one holds the lock first
    - That order defines the edges direction in the precedence graph
    - Since locks cannot be reacquired later, the edges cannot form a cycle

__Executeing with 2PL__
![img](./img/Screenshot%202025-11-08%20142922.png)
- Two transactions T₁ and T₂, both want to read/write the same item A.
    - Both use X-LOCK(A) because they intend to write
    - The lock Manager decides who can access `A` and when.
- Step 1: T1 Beigns
    - T1 request an exclusive lock (`X-LOCK`) on `A`
    - For now, A is free
    - T1 ask the Lock Manager, Lock Manager checks -> A is free -> Grants the lock to T1
    - So not, T1 owns A (T1 -> A)
    - So T1 can safely do R(A) W(A)
- Step 2: Transaction T2 starts
    - T2 also wants to write A, so it ask Lock Manager
    - Lock Manager checks -> A is no free -> Request denied
    - Fow now, T2 is blocked
- Step 3: T₁ finishes its work
    - T₁ is done reading/writing A.
    - It now calls `UNLOCK(A)` and releases the lock.
    - Lock Manager marks A as free again.
    - At this moment, T₁ has entered its __shrinking phase__: it can no longer acquire new locks.
- Step 4: T₂’s turn
    - Lock Manager notices T₂ was waiting.
    - Now that A is free → Grants the lock to T₂.
    - When done, T₂ also calls `UNLOCK(A)` → releases the lock.

__Problem w/2PL: Cascanding Aborts__
![img](./img/Screenshot%202025-10-28%20121836.png)
- One of the main weakness of baisc 2PL: Cascading Abort Problem
    - Example Shceudle timeline:
        1. T₁ starts, locks A and B (exclusive locks) → allowed under 2PL.
        2. T₁ reads `A`, writes `A (W(A))`, and then unlocks A early (before commit).
        3. T₂ now requests `X-LOCK(A)` → granted, because T₁ released it.
        4. T₂ reads A, but the version of A it reads is the one modified by T₁, whic has not yet committed.
            - This called a dirty read (T2 read uncommited )
        5. Later, T1 aborts: its changes must be undone
        6. But T2 has already used that "dirty" version of A
            - DBMS must also abort T2, because its results are now invalid
    - Problem here:
        - Even though this schedule follows the 2PL rules, it still causes trouble
        - When T₁ aborts, T₂ must also abort.
        - And if other transactions had used T₂’s results, they would also have to abort.
        - This can cause a chain reaction ->__“Cascading aborts.”__
        - Why it happend?
            - In __basic 2PL__, a transaction is allowed to release locks before it commits.
            - That means other transactions can see uncommitted data.
            - If the first transaction aborts later, everyone who depended on its data must roll back too

__2PL Observations__
- _Observation #1_: 2PL may reject some “safe” schedules
    - 2PL prevents all non-serializable schedules, but it also blocks some schedules that would have been serializable.
    - This happens because transactions might need to wait longer for locks, even when the actual operations wouldn’t have conflicted.
    - Most DBMSs prefer correctness before performance
    - Trade-off:
        - 2PL = safety first (guaranteed serializability)
        - less concurrency / performance
- _Observation #2_: 2PL still allows dirty reads -> cascading aborts
    - May still have "dirty reads" thus cascading aborts
    - Solution: __Strong Strict 2PL (aka Rigorous 2PL)__

__Strong Strict 2PL (aka Rigorous 2PL)__
- __Rule__:
    - A txn can release no locks at all until it commits or aborts
    - The txn is only allowed to release locks after it has ended (i.e., committed or aborted)
    - That means:
        - Hold all S-locks and X-locks until the very end.
        - Only after commit (or abort) does the DBMS release all locks at once.
    - Allows only conflict-serializable schedules, but it is often stronger than needed for some apps

__2PL Deadlocks__

![img](./img/Screenshot%202025-11-09%20105743.png)
- Even thought 2PL guarantees conflict-serializability, it does not prevent deadlocks
- Timeline:
    - Step 1: T1 starts
        - T1 begins and request `X-LOCK(A)` to write A
        - Lock Manager grants it: Granted (T₁ → A).
        - T1 holds A exclusively
    - Step 2: T2 starts
        - T2 beigns and requests S-LOCK(B) to read B
        - Lock manager grants it: Granted (T₂ → B).
        - T2 now holds B (shared mode, but that is enough to block others from writing B)
    - Step 3: T1 request another lock
        - T1 now wants to write B -> `X-LOCK(B)`
        - Lock Manager checks:
            - But T2 already hold a `S-LOCK(B)`
            - Shared + Exclusive are incompatible
        - Requested denied: T1 must wait for B to be released
    - Step 4: T2 requests another lock
        - T2 now wants to read A -> `S-LOCK(A)`
        - Lock Manager checks:
            - But T1 holds and `X-LOCK(A)`
            - Incompatible again
            - Requested denied -> T2 must wati for A to be released

- __Definition:__
    - A deadlock is a cycle of transactions waithing for locks to be relased by each other
- __Two ways of dealing with deadlocks__:
    - Approach #1: Detection & Resolution
        - The DBMS build a wailt-for graph
            - Node = transaction
            - Edge = "Tᵢ is waiting for Tⱼ"
        - If a cycle is found -> deadlock
        - The system aborts one transaction (the victim) to break the cycle
    - Approach #2: Prevention
        - Avoid cycle by imposing rules
            - Wait-Die
                - older transactions wait, younger abort
            - Wound-Wait
                - older transactions force abort yonger ones
            - Or always acquire locks ina predefined global order

__Deadlock Detection__
- The DBMS creates a _waits-for graph_ to keep track of what locks each txn is waithing to acquire:
    - Node are transactions
    - Edge from Ti to Tj if Ti is waithing for Tj to release a lock
- The system periodically checks for cycles in wait-for graph and then decides how to break it.

__Deadlock Resolution__
- When the DBMS detects the deadlocks, it will select a txn to rollback to break the cycle
- The victim txn will either restart or abort depending on how it was invoked
- There is a trade-off between the frequency of checking for deadlocks and how long txns wait before deadlocks are broken.
- __Considerstions__
    - Selecting the proper txn to terminate depends on a lot of different variables
        - By age (e.g., highest timestamp)
        - By progress (e.g., leaast/most queries executed)
        - By the # of items already locked
        - By the # txns that we have to rollback with it
    - We also should consider the # of times a txn has been restarted to past to prevent starvation

__Deadlock Resolution: Rollback Length__
- After selecting a txn to abort, the DBMS can also decide on how far to rollback the txn's changes
- Approach #1: Completely Rollback
    - The DBMS rolls back the entire transaction
    - Rollback entire txn and tell the application it was aborted
    - The transaction will restrat from scratch or report failure to the application
- Approach #2: Partial (Savepoints) Rollback
    - Mordern DBMSs let tranasctions define savepoint
    - DBMS roll back a portion of txn (to break deadlock) and then attemps to re-execute the undone queries

__Deadlock Prevention__
- Insted of detecting and fixing a deadlock later, the DBMS can prevent one from ever happening by forcing and abort early
- How Prevention Works:
    - Whenever a transaction tries to acquire a lock that’s already held by another transaction:
        - Instead of letting it wait and risk a deadlock later, the DBMS uses a priority rule (based on timestamps) to decide:
            - Should it wait, or
            - Should it abort immediately?
- When a txn tries to acquire a lock that is held by another txn, the DBMS terminates one of them to prevent a deadlock.
    - __This approach does not require a waits-for graph or detection algorithm.__

__Deadlock Prevention：Protocols__
- Assign priorites based on timestamps:
    - Higher Priority = Older Timestamp (e.g., T1 > T2)
    - __Defition:__
        - Requesting Tranaction: The transaction that is trying to acquire a lock (but the lock is currently held by someone else)
        - Holding Transaction: The transaction that already owns the lock on the data item
- __Wait-Die ("Old waits for Young")__
    - If requestiong txn has higher priority than holding txn, then requestiong txn waits for holding txn
    - Otherwiese requesting txn aborts
- __Wound-Wait ("Yong Waits for Old")__ 
    - If requesting txn has a higher priority than holding txn, then holding txn aborts and release lock
    - Otherwise requesting txn waits
- Example:
    ![img](./img/Screenshot%202025-11-09%20130555.png)
    - Scenario 1:
        - T1 older, T2 yonger
        - T1 is the requesting txn
        - T2 is the holding txn
        - __Wait-Die:__
            - If the requester is younger, it aborts.
            - If the requester is older, it waits.
            - Result: T1 wait
        - __Wound Wait:__
            - If the requesting txn yonger, it wait
            - If the requester is older, it “wounds” (forces abort) the holder.
            - Result: T2 aborts
    - Scenario 2:
        - T1 older, T2 yonger
        - T1 is the holding txn
        - T2 is the requesting txn
        - __Wait-Die:__
            - T2 abrots
        - __Wound Wait:__
            - T2 waits

__Deadlock Prevention：Questions__
- __Why do these schemes guarantee no deadlocks?__
    - Both Waut-Die and Wound-Wait are designed so that cycles like this can never form
        - because all waiting goes only one direction
    - Only one "type" of direction allowed when waiting for a lock.
        - Only old-waits-for-young (Wait-Die) or
        - Only young-waits-for-old (Wound-Wait)
- __When a txn restarts, what is its (new) priority?__
    - When a transaction aborts (due to a deadlock prevention rule) and restarts, it keeps its original timestamp.
    - Why:
        - To prevent starvation.
        - If a transaction geot a new (later) timestamp everytime it restart, it would always be "youngest" : always have the loes priority might keep aborting forever
        - So the DBMS keeps the same original timestamp, meaning its priority stays the same
            - eventually it will become old enough that no one can wound or kill it

__Lock Granilarities__
- `Lock granularity` = how big or small the “unit” of locking is.
- When a transaction locks something, the DBMS can choose what that “something” means:
    - a tuple (row)
    - a page (block of rows)
    - a whole table
    - or even an entire database
- The DBMS should ideally obtain fewest number of locks that a txn needs.
- There’s a performance trade-off between parallelism versus overhead.
    - Fewer Locks, Larger Granularity vs. More Locks, Smaller Granularity.
    - Parallelism (Concurrency) — how many transactions can run at the same time
    - Locking Overhead — how much memory and CPU time it costs to track locks
| Lock Granularity                       | Pros                                                    | Cons                                   |
| -------------------------------------- | ------------------------------------------------------- | -------------------------------------- |
| **Fine (small)** — e.g., row/attribute | High concurrency (many txns can work on different rows) | More locks to manage → higher overhead |
| **Coarse (large)** — e.g., page/table  | Fewer locks to manage → lower overhead                  | Less concurrency (others are blocked)  |


# Transaction III

## Crash Recovery
- Recovery algorithms are techniques to ensure ACID properties despite failures.
- Recovery algorithms have two parts:
    - a. During Normal Transcation Processing (crash happend during transaction processing)
        - The DBMS must record enough information so that it can:
            - Undo uncommited transactions, and
            - Redo commityrf one after a crash
        - Actions included:
            - Write-Ahead Logging (WAL): Before modifying any data on disk, log the change
            - Fore/Steal policies: Decided whether to flush dirty pages or delay them
        - These are Actions during normal txn processing to ensure that the DBMS can recover from a failure.
    - Actions after a failure to recover the database to a state that ensures atomicity, consistency, and durability.
        - Analyze -> figure out which transactions were active/committed at crash.
        - Redo -> reapply updates of committed transactions to ensure durability.
        - Undo -> roll back incomplete transactions to ensure atomicity.

### Actions during normal txn processing to ensure that the DBMS can recover from a failure.
__Storage Type__
- Stable Storage:
    - A non-existent form of non-volatiile storage that survice all possible failure scenarios
    - Use multiple storage devices (redundancy) to approximate.

__Failure Classifications__
- __Transaction Failures:__
    - These affect the a single transaction, not the whole system
    - Logical Errors
        - Transaction cannot complete due to some internal error conditions (e.g., integrity constraint violation).
        - Action: DBMS aborts that transaction and rolls back its changes.
    - Internal State Errors
        - DBMS must terminate an active transaction due to an error condition (e.g., deadlock).
        - Action: DBMS aborts the victim transaction and undoes partial updates.
    - Recovery mechanism: Undo logging (or WAL UNDO phase) reverts modifications of aborted txns.

- __System Failures__:
    - These crash the DBMS process or host machine: all active transactions are interrupted.
    - Software Failure
        - Problem with the OS or DBMS implementation (e.g. uncaught divide-by-zero exception).
        - Examples:
            - Segmentation fault in DBMS code
            - OS panic or bug in memory allocator
        - Effect: All in-memory state is lost.
    - Hadware Failure
        - Example: Power outage, sudden restart, CPU failure
        - The computer hosting the DBMS crashes (e.g., power plug gets pulled).
        - Fail-stop Assumption:
            - Data on disk remains intact (only volatile memory lost).
            - So the DBMS can safely replay logs from disk to recover.
    - Recovery mechanism: ARIES-style recovery (Analysis → Redo → Undo) uses WAL logs to rebuild consistent state.

- __Storage Media Faiure__:
    - These are the worst-case scenarios: physical corruption of non-volatile storage.
    - Examples
        - Disk head crash
        - SSD controller failure
        - Bit rot (undetected data corruption)
    - Non-Repairable Hardware Failure
        - A head of crash or similar disk failure destroys all or part of non-volatile storage
        - Destruction is assumed to be detectable (e.g. disk controller use checksums to detect failures)
    - No DBMS can recover from this, database must be restored from archilved version

__Goals__
- The DBMS needs to ensure Atomicity (all or nothing):
    - The changes for any txn are durable once the DBMS has told somebody that it committed.
    - No partial changes are durable if the txn aborted.

__Undo vs. Redo__
- Undo: __removing__ the effect of an __incomplete or aborted txn__
- Redo: __re-applying__ the effects of a __committed txn__ for durability

__Buffer Pool Policy__
- Steal Policy:
    - Definition: Whather the DBMS allows page modified by __uncommited__ transactions to be written to disk.
    - STEAL
        - Allowed to write uncommited data to disk
        - Needed when buffer pool is full -> must "steal" a frame to load new page
        - But this means dirty pages from uncommited transactions might end up on disk
    - Implication: The DBMS must be able to UNDO these changes during recovery
    - NO-STEAL
        - Never writes pages __touched by uncomiited__ transactions (to disk)
        - Guarantees disk only has committed data -> simpler recovery
        - But needs to keep all uncommited data in memory -> require huge buffer
- Force Policy:
    - Whether all dirty pages of a committed transaction must be written on disk before the commit completes
    - FORCE
        - On commit, the DBMS forces all dirty pages for that txn to disk
        - Guarantees durability: no need to redo later
        - But causes lots of random writes: slow commits
    - NO-FORCE
        - On commit, the DBMS may delay writing dirty pages
        - Faster commits (just flush log), but:
            - Some committed updates might not yet be on disk -> need Redo after crash
- These four can form combinations for a policy

    | Policy                  | What Happens                                          | Undo Needed? | Redo Needed? | Example                                      |
    | ----------------------- | ----------------------------------------------------- | ------------ | ------------ | -------------------------------------------- |
    | **NO-STEAL + FORCE**    | Uncommitted never hit disk; commit forces all to disk | ❌            | ❌            | Simplest, but unrealistic                    |
    | **STEAL + FORCE**       | Uncommitted may hit disk; commit flushes all          | ✅            | ❌            | Safe but slow                                |
    | **NO-STEAL + NO-FORCE** | Keeps uncommitted in memory; delays commit flush      | ❌            | ✅            | Simple Redo only                             |
    | **STEAL + NO-FORCE**    | Uncommitted may hit disk; commits don’t flush         | ✅            | ✅            | 🔥 Most flexible but complex — used by ARIES |

__NO-STEAL + FORCE__
- Advantage:
    - Never have to undo changes for an aborted txn because the changes were not written to disk
    - Never have to redo changes of a committed txn because all the changes are guaranteed to be written to disk at commit.
- However, we cannot support write sets that exceed the amount of physical memory available. Thus, no system implements this approach!

__SHADOW PAGING__
- Key idea: Intead of modifying data in place, the DBMS makes a copy (shadow) of any page that is about to be changed
- The DBMS copies pages on write to crate two versions:
    - Primary Page: The currently committed, durable database (safe on disk)
    - Shadow Page: Copies of modified pages created by ongoing, uncommited transactions.
- When the transaction commits:
    - The DBMS atomatically switches a single pointer (root of the page table) from the old page (primary) to the new one (shadow)
    - That is the "Commit Point"
- This makes recovery trivial:
    - If the system crashes before commit -> ignore the shadow pages
    - If the system crashes after commit -> new root points to new pages (already consistent)
- __Advantages:__
    - Supporting rollbacks and recovery is easy
    - Undo: Just discard the shadow pages; since primary pages were never modified, no rollback I/O is needed.
    - Redo: Not needed at all: commit is an atomic root pointer swap; all committed pages are already on disk.
- __Disadvantages:__
    - `Copy-on-Write Overhead`: Every update requires copying an entire page (even if only one tuple changes). This causes high I/O cost and space blow-up.
    - `Poor Performance for Large Transcations`: A transaction touching many pages must copy them all: expensive in both time and space.
    - `Fragmentation`: Old and new versions of pages get scattered all over disk: poor locality and degraded read performance over time.
    - `Difficult to Handle Concurrency`: Managing multiple active transactions (each with its own shadow copies and roots) is complex and memory-heavy.
    - `Hard to Support Incremental Changes or Partial Commits`: A single crash during root-pointer swap can corrupt the page table pointer, leaving the DB inconsistent unless protected by extra mechanisms.

__Write-Ahead Log (WAL)__
- The standard recovery mechanism used by almost all modern DBMSs
- Component:
    - Log file
    - Data file
    - Stable storage
    - Log Sequence Number (LSN)
- Maintain a log file that contains the changes that txns make to database
    - Log is separate from data files
    - Log will also be written to stable storage
    - Log contains enough information to perform the necessary undo and redo actions to restore the database
- WAL property:
    - Before any data page is written to disk, the log records describing its changes must first be written to disk
    - This ensures:
        - You can always __Undo uncommited__ changes (old values are logged)
        - You can always __Redo committed__ one (new values are logged)
- Buffer Pool Policy: **STEAL + NO-FORCE** 
- Is WAL a good idea:
    - Decouples writing log pages from writting data pages
    - __WAL is efficient because it is:__
        - Sequential Writes: Logs are appended linearly: this is fast even on spinning disks (and trivial for SSDs).
        - Compact Records:
            - Each log record stores only: `<TxnID, PageID, Offset, OldValue, NewValue>`
            - small footprint compared to entire page writes.
        - Asynchronous Data Writes: Data pages can be written lazily; the log ensures recovery correctness.


__WAL Protocol__
- The DBMS stages of all a txn's log records in volatile storage.
- All log records pertaining to an updated page are written to non-volatile storage before the page itself is overwritten in non-volatile storage.
- A txn is not considered committed until all its log records have been written to stable storage.
- Write a <BEGIN> record to the log for each txn to mark its starting point
- When a txn finishes, the DBMS will:
    - Write a <COMMIT> record on the log
    - Make sure that all log records are flushed before it returns an acknowledgement to application.

__WAL Implementation__
- The Problem: Log Flushing Bottleneck
    - When a transaction commits, it must guarantee durability:
        - All its log records must be safely stored on disk before confirming “COMMIT”.
    - However:
        - Each disk flush = an expensive fsync() call (tens of microseconds to milliseconds).
        - If every transaction flushes individually → massive bottleneck.
    - So, even if each transaction updates only a few bytes, you’d be doing one disk flush per commit → throughput plummets.
- Flushing the log buffer to disk every time a txn commits will become a bottleneck.
- The DBMS can use the group commit optimization to batch multiple log flushes together to amortize overhead, or use a flush trigger:
    - When the buffer is full, flush it to disk.
    - Or if there is a timeout (e.g., 5 ms).

__Buffer Pool Policy__
- Almost every DBMS uses NO-FORCE + STEAL
    - key assumption: crashes, thereby recovery, will be rare

__Logging Schemes__
- Physical Logging
    - Exact byte-level changes to a specific page in the buffer pool.
    - Example: git diff
- Logical Logging
    - Record the high-level operations executed by txns
    - Example: UPDATE, DELETE, and INSERT queries
    - Not restricted to a single page
- Physiological Logging
    - Hybrid approach with byte-level changes for a single tuple identified by page id + slot number
    - Does not specify organization of the page.

__Physiacl vs. Logical Loggings__
- Logical logging requires less data written in each log record than physical logging.
    - for undo, need the before-state of the records
- Difficult to implement recovery with logical logging if you have concurrent txns.
    - Hard to determine which parts of the database may have been modified by a query before crash.
- Also takes longer to recover because you must re-execute every txn all over again.
- Most systems use physiological logging.

__WAL Summary__
- Write-Ahead Logging (WAL) is (almost) always the best approach to handle loss of volatile storage.
- WAL is append-only, compact and can be written sequentially.
- WAL property requires that the log record (of an update) is persisted before the corresponding data record.
- WAL is the ground truth. The DB state is whatever WAL represents.

__Why not just use the log for query processing?__
```txt
We use the log for recovery. But since the log records
every change, could we in theory just query the log instead
of the data pages? In other words — if the log contains
every insert, update, and delete, why do we still need the
data pages at all?

Answer: The log is designed for recovery: append only, optimized for sequential writes. The data pages are deisigend for querying: 
random access, indexing and efficeint read.  It is possible for processing to just use the log. But the performance would be very 
poor since the log would be horrible for quering
```

### Actions after a failure to recover the database to a state that ensures atomicity, consistency, and durability. 

__Checkpoints__
- After a crash, the DBMS must replay the WAL to recover committed transactions and undo uncommitted ones.
- A checkpoint is a snapshot in time: a moment where the database state on disk is consistent with the log.
- Without Checkpoints:
    - The WAL could be huge (possibly gigabytes long).
    - The DBMS would have to replay it from the beginning, which is very slow.
- The DBMS periodically takes a checkpoint where it flushes all buffers out to disk
    - This synchronizes the WAL and the data pages on disk
    - It also provides a hint on how far back it needs to replay the WAL after a crash
- Blocking Checkpoint Protocol:
    - Pauses all queries
    - Flush all WAL records in memory to disk
    - Flush all modified pages in the buffer pool to disk
    - Write a <CHECKPOINT> entry to WAL and flush to disk
    - Resume queries

__Checkpoints: Frequency__
- Checkpointing too frequently caues the runtime performance to degrade
    - system spends too much time flushing buffers
- But waiting a long time is just as bad
    - The checkpoint wil be large and slow
    - Makes recovery time much longer.
    - Tunable option that depends on application recovery time requirements. 

__ARIES(Algorithm for Recovery and Isolation Exploiting Semantics)__
- ARIES is the standard crash recovery algorithm used by most modern DBMSs:
- Main Idea
    - Write-Ahead Logging:
        - Any change is recorded in log on stable storage before the database change is written to disk
        - Use **STEAL+NO-FORCE** buffer pool policies
    - Repeat History Duration Redo:
        - On DBMS restrat, retrace actions and restore database to exact state before crash
    - Logging Changes During Undo:
        - Any Undo action is also logged: ensures recovery can resume correctly if a crash occurs during recovery itself..

__Log Sequence Numbers (LSNs)__
- Every log record includes a globally unique log sequence number (LSN)
    - LSNs represent the physical order that txns make changes to the database.
    - In effect, LSNs form a logical timeline for the database
    - Various components in the system keep track of LSNs that pertain to them... 

__Important LSN__
- Each component in ARIES tracks an LSN(Log Sequence Number): a monotonically increasing ID that tells where in the log each change lives
- `flushedLSN`
    - Location: Disk (Log Manager)
    - Definition: The last LSN that’s actually written to stable storage (persistent).
- `pageLSN`
    - Location: In each data page (on disk or buffer)
    - Definition: The LSN of the most recent update applied to that page.
- `lastLSN`
    - Location: Per transaction (in memory)
    - Definition: The LSN of the most recent log record written by that transaction.
- `MasterRecord`
    - Location: Disk (in WAL header)
    - Defition: The LSN of the most recent checkpoint. Used as starting point for recovery.
- __WAL Property:__ 
    - Before the DBMS can write page x to disk, it must flush the log at least to the point where __pageLSNₓ ≤ flushedLSN__
    - What the dule ensures:
        - When the DBMS writes a dirty page (a modified buffer page) back to disk, it must first make sure that the log record describing that modification is already safe on disk
        - So __pageLSNₓ ≤ flushedLSN__ means “The latest log entry that modified this page has been persisted to stable storage."
        - So if the system crashes after the page is written but before the nex log flush, the DBMS still has enough log info to 
            - Redo the change (if committed)
            - Undo (if it wansn't)
        - Fail to comply this will results in __WAL Property violation__

__Transaction Commit__
- When a transaction finishes successfully, ARIES ensures durability through the WAL commit protocol.
- When a txn commit, the DBMS write a `COMMIT` record to log and guarantees that all log records up to txn's `COMMIT` record are flushed to disk
    - Log flush are sequential, synchronous write to disk
    - Many log records per log page
    - Ensure durability
- When the commit succeeds, write a special `TXN-END` record to log.
    - Indicates that no new log record for a txn will appear in the log ever again
    - This does not need to be flushed immediatly 
    - Ensures final cleanup

__Transaction Abort__
- A transaction abort means stopping and undoing a transaction because it cannot finish successfully.
- Aborting a txn is a special case of the undo opeartion applied to only one txn
- Undo operations:
    - The process of reverting the effects of a transaction that didn't sucessfully commit
- For efficiecn (not required): we add another field to our log records:
    - `PrevLSN`: The previous LSN for the txn
    - This maintains a linked-list for each txn that makes it easy to walk through its record

__Compensation Log Record (CLRs)__
- Definition:
    - A special log entry written by ARIES when it performs an Undo operation
    - It records what undo action was performed:
        - So, if the system crashes again while undoing, the recovery process knows where to resume without accidentally undoing something twice
- CLR content, each includes:
    - All normal log fields `(LSN, txnID, pageID, old/new values, etc.)`
        | Field                   | Description                                                                |
        | ----------------------- | -------------------------------------------------------------------------- |
        | **LSN**                 | Unique identifier (like all log records)                                   |
        | **TxnID**               | The transaction being undone                                               |
        | **PageID**              | The page that was modified                                                 |
        | **Before/After Values** | The “redo” info for the undo (so we can reapply the undo if needed)        |
        | **undoNextLSN**         | 👈 Pointer to the *next* record that still needs to be undone for this txn |

    - `undoNextLSN` -> the next record that still needs to be undone
- __Why CLRs Exist__
    - Without CLRs
        - If a crash happens during undo, you might redo the same undo again after restart
        - This could revert a value twice -> corrupt state
    - With CLRs
        - ARIES knows exactly how far undo has progressed and can resume safely for that point
- What ARIES Does with CLRs:
    - Write them as it perform undos
    - Does not wait to flush them before acknowledging abort to the client (becuase rollback durability is not required by the user)
    - But they will evetually be flushed -> be ensure crash-safe recovery if the system crashes mid-undo
- Example:


__Abort Algorithm__
- First write an ABORT record to log for the txn.
- Then analyze the txn's updates in reverse order. For each update record:
    - Write a CLR entry to the log.
    - Restore old value.
- Lastly, write a TXN-END record and release locks.
- Notice: CLRs never need to be undone.
- Detailed explaination
    - When a single transaction aborts (before any crash), ARIES performs a __controlled undo__ using its own log records
    - Steps
        1. Write an `ABORT` record
            - Marks the start of the rollback
            - Ensures recovery knows the transactions is in the process of aborting if a crash occurs
        2. Process log records in reverse (useing `prevLSN`)
            - __Restore the old value__ to the page (undo the change)
            - __Write a Compensation Log Record (CLR)__ to WAL, containing:
                - What was undone
                - `undoNexLSN`

__ARIES: Recovery Phases__
- Phase #1: Analysis
    - Goal: Figure out what was going on at the time of the crash
    - Starts at:
        - `MasterRecord.LSN` -> point to the most recent checkpoint
        - Scans: WAL forward to rebuild two in-memory table
            - `Transaction Table`: Which transactions were active at crash
            - `Dirty Page Table`: Which pages were dirty (modified but not yet written to disk)
        - Result of Analysis:
            - Set of transactions that were active but not commiteed (-> need Undo)
            - Earliest LSN that must be redone (-> start of Redo phase)
    - Examine the WAL in forward direction starting at the latest checkpoint (`MasterRecord`) to identify the active txns at the time of the crash.
- Phase #2: Redo
    - Repeat all actions starting from `MasterRecord` in the log (even txns that will abort)
    - Goal: Repeat history: restore the database to exactly the start it was in at crash time
    - Starts at:
        - The smallest `LSN` in the `Dirty Page Table` (first dirty update not yet reflected on disk)
    - Prodecure:
        1. Scan WAL forward from that point
        2. For each log record:
            - Check if the change needs to be reapplied using
                - Whether the affected pages is in the `Dirty Page Table`
                - Whether `pageLSN < record.LSN`
        3. If needed, redo the update on that page
    - __Key point:__ 
        - Even uncommitted transactions’ updates are redone
        - Why: Because ARIES wants the DB to look exactly as it did at crash time, then the Undo phase will remove uncommitted work.
- Phase #3: Undo
    - Goal: Undo all actions from transactions that were not commited at crash time
    - Starts with:
        - The active transactions found in the Analysis phase
        - Prodecure:
            1. For each uncommitted transactions:
                - Follows its log backward using `prevLSN`
                - For each update record:
                    - Undo the change
                    - Write a _CLR_ to the log
                    - Use `undoNextLSN` to continue if crash happens mid-undo
            2. When done, Write a `TXN-END` for each