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
- Consistency: Is each transaction is consistent and DB starts consistent, the it remains consistent after transaction.
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
- Check to see if a particular shceudle produces a state equivalent to a db state that results from a serial execution?]
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
    - They are by different transactions
    - They are on the same object and one of them is a write.
- Interleaved Execution Anomalies
    - Read-Write Conflict (R-W)
    - Write-Read Conflicts (W-R)
    - Write-Write Conflicts (W-W)

__Why Care About Conflicting Operations__
- Read-Write Conflict
    - __Unrepeatable Read:__ Txn gets different values when reading the same object multiple times.
- Write_read Conflict
    - __Dirty Read:__ One txn reads data writen by another txn that is not commited yet
- Write-Write Conflicts
    - __Lost Update:__ One txn overwites uncommited data from another uncommited txn

__Conflict Serializable Schedules__
- Two schedules are conflict equivalent if:
    - They involve the same actions of the same transactions
    - Every pair of conflicting actions is ordered the same way
- Schedule S is conflict serializable if:
    - S is conflict equivalent to some serial schedule
    - Intuition: you can transform S into a serial schedule by swapping consecutive non-conflicting opeartions of different transactions.

__Dependency Graphs__
![img](./img/Screenshot%202025-10-24%20120327.png)
![img](./img/Screenshot%202025-10-24%20120327.png)
![img](./img/Screenshot%202025-10-24%20120559.png)
- One node per txn
- Edge from Ti to Tj if:
    - An operation Oi of Ti conflicts with an operation Oj of Tj and
    - Oi appears earlier in the schedule than Oj.
- Also known as a precedence graph.
- A schedule is conflict serializable if its dependency graph is acyclic.

__Serrializability__
- In practice, Conflict Serializability is what systems support becuase it can be enforced efficiency.
- There are more flexible notions such as View Serializability, which is hard to enfoce
- To allow more concurrency, some special cases can get handled separately at the application level
- Allows parralelism on the inside, but (look like) one-at-a-time outside.
