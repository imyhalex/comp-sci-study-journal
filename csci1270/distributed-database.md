# Distributed Database

- Distributed Databases
    - Sharding / Partitioning
    - Distributed Transactions

__Database Partitioning__
- Split a database accross multiple machine or storage units
- Often called sharding iin NoSQL system
- Each partition holds a subsets of data
- How Queries run
    - DBMS sends query fragments to each partition
    - Each partition computes its part of the answer
    - Results are combined to form the final output
- Way to partition
    - Physical Partitioning
        - Each node owns its own data + storage
        - True sharding: data is physically separated
    - Logical Partitioning
        - Data stored in one disk subsystem, but logically divided
        - Nodes coordiate which logical paritions they handled

__Benefits of Logical Partitioning__
- Allows the DBMS to choose partitions based on data location, not arbitrary rules.
- DBMS knows which partition contains which ranges/hashes of data → targeted queries.
- Unlike round-robin or load-based access, logical partitions preserve data locality.
- __Compared to Round-Robin Access__
    - Round-robin spreads tuples evenly but destroys locality.
    - A query like `WHERE id = 101` must check every node.
    - Logical partitioning sends the query only to the correct partition → less work.
- __Compared to Load-Based Access__
    - Load-based decisions ignore data meaning.
    - Tuples may be placed anywhere → queries become scattered.
    - Logical partitions allow consistent placement based on keys (range/hash) → predictable routing.


__Data (Distribution) Transparency__
- Applications should not need to know where data lives in a distributed DBMS.
- A query that works on a single-node DBMS should return the same result on a distributed DBMS.
- The system hides physical data placement from the application (“transparency”).
- In practice, developers need to be aware of the communication costs of queries to avoid excessively "expensive" data movement.

__Naive Table Partitioning__
- Assigne an entire table to a single node
- Assume that each node has enough storage space for an entire table
- Ideal if queries never join data across tables stored on different node and access patterns are uniform

__Vertical Partitioning__
- Split a table's attribues into separate partitions
- Must store tuple information to reconstruct the original record

__Horizontal Partitioning__
- Split a table's tuples into disjoint subset based on some partitioning key and partitioning scheme
    - Choose columns that divides the database equally in term of size, load, or usage
- Popular partitioning schemes
    - Range-based partitioning 
    - Hash-based partitioning
* Split a table into disjoint subsets (partitions) based on a **partitioning key**.
* Each tuple is assigned to a partition by a rule (e.g., `hash(id) % N`).
* Query like `WHERE partitionKey = ?` goes directly to the correct partition.
* Reduces work: only one partition needs to be accessed.

**Horizontal Partitioning (Dynamic / Non-Aligned Partitions)**

* When partitions are added or removed, the mapping changes.
* Old mapping: `hash(id) % 4` → P1, P2, P3, P4.
* Adding/removing a partition forces **many keys to move**.
* Causes expensive rebalancing and heavy data movement.

**Consistent Hashing**
* Places partitions (servers) on a **hash ring** from 0 to 1.
* Each key is mapped to the *next* node clockwise on the ring.
* Only keys falling between affected positions move when node joins/leaves.
* Minimizes rebalancing → only a **small fraction** of data moves.
* Used in DynamoDB, Cassandra, Riak, Memcached, etc.
* Works regardless of number of objects or number of servers.

**Consistent Hashing Question**
* Claim: “When a new server joins, only a fraction of the data from the previous server moves.”
* **Answer: True**. Only the keys between the new server’s position and its predecessor migrate.

__Distributed Transactions__
- Local (single-node) transactions
    - Access/update data at only one database
- Global (multi-node) transactions
    - Access/update data at more than one database
- Key issue: how to ensure ACID properties for transactions in a system with global transactions spanning multiple nodes

__Distributed Transaction Management__
- Each __transaction coordinator (TC)__ is responsible for:
    - Starting the execution of transactions
    - Distributing sub-transactions at appropriate sites
    - Coordiateing the termination of each transaction
- Each __local tranasction manager (TM)__ responsible for:
    - Coordinating the execution and commit/abort
    - Maintaining a log for recovery purpose

__System Failure Modes__
- Failure unique to distributed systems:
    - Loss of message
    - Failure of a communication link
    - Network partition
        - A network is said to be partitioned when it has been split into two or more subsystems that lack any connection between them
- Network partitioning and site failures are generally indistinguishable. 

__Commit Protocols__
- Used to ensure atomicity accorss nodes
    - Goal: a transaction that executes at multiple sites must either be commited at all sites or aborted at all the sites
- Two-phase commit (2PC) (widely used)
- Three-phase commit (3PC) (not used)
- Consensus protocols (Paxos, Raft)
    - These solve a more general problem; can also be used for atomic commit

__Important Assumptions__
- Assume that all nodes in a distributed DBMS are well-behaved and under the same administrative domain
    - If we tell a node to commit a txn, then it will commit the txn (if there is not a failure)
    - Fail-Stop model: If a node fails, it simply stops working (e.g. does not send any incorrect message to other nodes)
- If we do not trust the other nodes in a distributed DBMS, then we need to use a Byzantine Fault Tolerant protocol for txn (e.g. blockchain)

__2PC (Sucess Case)__
- Goal: Ensure all participants either all commit or all abort (atomic across nodes).
- Coordinator: Node 1
- Participants: Node 2, Node 3
- Phase #1: Prepare
    - Coordinator → participants: “Can you commit?”
    - Each participant:
        - Writes changes to its log (but does NOT commit yet).
        - Replies OK if ready, or Abort if cannot commit.
- Phase #2: Commit
    - If all participants reply OK
        - Coordinator sends Commit to each participant.
        - Participants commit and acknowledge.
    - Coordinator returns Success to the application server.

__2PC (Abort Case)__
- If any participant replies Abort in Phase 1:
    - Coordinator sends Abort to all participants.
    - Participants undo/rollback changes.
    - Coordinator replies Aborted to application server.
- Key Idea:
    - 2PC guarantees atomicity across distributed nodes:
        - All nodes commit → success
        - Any node aborts → all nodes abort


**Logging at Each Node (Revisited)**

* Each node keeps a **non-volatile log** of:
  * Inbound messages (PREPARE, COMMIT, ABORT).
  * Outbound responses (READY, OK).
  * Final decisions (COMMIT T, ABORT T).
* Logs allow nodes to recover after crashes and resume 2PC correctly.
* A node’s **latest log record** determines what it must do after recovery.


**2PC Participant Failures**
When a participant recovers, it looks at its log. The last record determines its action:

* **If log contains `<commit T>`**

  * Must redo T (transaction was committed).

* **If log contains `<abort T>`**

  * Must undo T (transaction was aborted).

* **If log contains `<ready T>`**

  * Participant had voted “YES” but had not received COMMIT/ABORT.
  * Must contact the coordinator to learn the global decision.
  * If coordinator committed → redo T.
  * If coordinator aborted → undo T.

* **If no control record exists (no READY)**

  * Means participant crashed **before** voting.
  * Therefore must abort T (safe default, local abort).
  * Undo T.


**2PC Coordinator Failures**

If coordinator fails during T:

* **Case 1: Participant has `<commit T>` or `<abort T>`**

  * Outcome is known → redo or undo T.

* **Case 2: Participant does NOT have `<ready T>`**

  * Participant had not __voted yet__.
  * Therefore must ABORT T.

* **Case 3: Participant has `<ready T>` and no outcome record**

  * Participant is in the “uncertain state.”
  * It cannot decide commit/abort on its own.
  * **Must block and wait** for the coordinator to recover.
  * This is the classic **2PC blocking problem**.

**2PC Question Answer**

**Question:**
A participant p fails during transaction T. When p recovers, it checks its log and decides to **abort T locally**. Under what circumstances does this happen?

**Answer (what must be in p’s log)**
p will abort T if its log shows **no `<ready T>` record**.

More explicitly:

* p crashed **before** sending a READY vote (i.e., before finishing phase 1).
* This means p never promised to commit, so it is safe to abort.
* Logs show only:

  * `<prepare T>` (optional)
  * OR no control records at all
  * BUT **not** `<ready T>`

**Therefore:**

* If the latest log record is **not** `<ready T>`, and **not** `<commit T>` and **not** `<abort T>`,
* p must unilaterally **abort T**.


__Avoiding Blocking__
- Use 3PC (3-Phase Commit)
    - Non-Blocking; adds a pre-commit satel no one uses it as it is expensive
- Or use a distributed consensus protocol: a set of n nodes need to agree on a decision
    - Should be made in such a waythat all nodes will make the same decision even if some nodes fail during the protocol, or there are network partitions
    - Further, the protocol should not block, as long as a majority of the nodes remain alive and can communicate
    - Several consensus protocols: Paxo and Raft are popular