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
- Two operations conflict if:
    - They are on the same object (A, B, etc)
    - They belong to different transactions
    - Af least one is a write
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

__Using Locks__
- Transactions request locks
- Lock Manager grants or blocks requests
- Transactions release locks
- Lock manager updates its internal lock table
    - It keeps track of what transactions hold what locks and what transactions are waithing to acquire any locks.

__Concurrency Control Protocol__
- __Two-phase locking (2PL)__ is a concurrency control protocol that determines whether a txn can access an objeect in the database at runtime
- The protocol does not need to know all the queries that a txn will execute ahead of time

__Two-phase locking (2PL)__
- Phase #1: Growing
    - Each txn requests the locking that needs from the DBMS's lock manager
    - The lock manager grants/denies lock requests
- Phase #2: Shrinking
    - The txn is allowed to only release/downgrade locks that it previouly acquired. It cannot acquire new locks.
- The txn is not allowed to acquire/upgrade locks after the growing phase finishes

__2PC Guarantees Conflict Serializability__
- Lock point is when txn reaches end of growth phase
- At lock point:
    - Everything txn needs is locked
    - Any conflicting transactions either started its shirink phase earlier or are blocked by this txn
- The __order of lock points__ give us the equivalent serial order

__Problem w/2PL: Cascanding Aborts__
![img](./img/Screenshot%202025-10-28%20121836.png)

__2PL Observations__
- There are potential schedule that are serializable but would not be allowed by 2PL becuase locking limits concurrency
    - Most DBMSs prefer correctness before performance
- May still have "dirty reads" thus cascading aborts
    - Solution: __Strong Strict 2PL (aka Rigorous 2PL)__

__Strong Strict 2PL (aka Rigorous 2PL)__
- The txn is only allowed to release locks after it has ended (i.e., committed or aborted)
- Allows only conflict serializable schedules, but it is often stronger than needed for some apps

__2 PL Deadlocks__
- A deadlock is a cycle of transactions waithing for locks to be relased by each other
- Two ways of dealing with deadlocks:
    - Approach #1: Detection & Resolution
    - Approach #2: Prevention

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
- After sleecting a txn to abort, the DBMS can also decide on how far to rollback the txn's changes
- Approach #1: Completely
    - Rollback entire txn and tell the application it was aborted
- Approach #2: Partial (Savepoints)
    - DBMS roll back a portion of txn (to break deadlock) and then attemps to re-execute the undone queries

__Deadlock Prevention：Protocols__
- Assign priorites based on timestamps:
    - Higher Priority = Older Timestamp (e.g., T1 > T2)
- __Wait-Die ("Old waits for Young")__
    - If requestiong txn has higher priority than holding txn, then requestiong txn waits for holding txn
    - Otherwiese requesting txn aborts
- __Wound-Wait ("Yong Waits for Old")__ 
    - If requesting txn has a higher priority than holding txn, then holding txn aborts and release lock
    - Otherwise requesting txn waits

__Deadlock Prevention：Questions__
![img](./img/Screenshot%202025-10-28%20131506.png)
- Why do these schemes guarantee no deadlocks?
    - Only one "type" of direction allowed when waiting for a lock.
        - Only old-waits-for-young (Wait-Die) or
        - Only young-waits-for-old (Wound-Wait)
- When a txn restarts, what is its (new) priority?
    - Its original timestamp to prevent it from getting starved for resources.


__Lock Granilarities__
- When a txn wants to acquire a "lock", the DBMS can decide the granularity (i.e., scope) of that lock.
    - Attribute? Tuple? Page? Table?
- The DBMS should ideally obtain fewest number of locks that a txn needs.
- Trade-off between parallelism versus overhead.
    - Fewer Locks, Larger Granularity vs. More Locks, Smaller Granularity.