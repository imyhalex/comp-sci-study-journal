# SQL[[Link](https://neetcode.io/courses/system-design-for-beginners/14)]
- __B+ Tree__
    - Multi-way trees that can have more than two children per node
    - Store all their data in the leaf nodes which are linked in a sorted order
    - Interior nodes contains only keys and pointers to other nodes
    - Let's say: Each node has at most M children
        - node must contains M - 1 keys, a node contains [2, 5] then it would have three children
    - Provide indexing
        - improve the speed of data retrival operations on a database table
- __Trade-offs of RDMS__
    - ACID
        - Atomicity
            - all changes to data are performed as if they are single operation
                - either all the changes are performed, or none of them are
        - Consistency
            - Ensure data integrity
            - Refers to the adherence to predefined rules and constraints that maintain the validity of the data throughout the execution of multiple transactions
        - Isolation
            - refers to an intermediate state of transaction, such that a transaction is invisible to other transactions
            - transactions that run concurrently appear to be serialized
            - this property ensures the concurrent transactions do not interfere with each other and the effects of one transaction are isolated from other transactions until it is commited
            - suppose:
                - Alice: $1000, Bob $500 and Alice -> $500 to Bob
                - after this operation commit, there is a second operations to add $200 to Alice account, this violate the isolation property
                    - thus the second operation has to wait until the first transaction completed
        - Durability
            - after a transaction successfully completes, changes to data persist and are not undone
            - if the power goes out after a transaction occurs, the transaction will still be recorded in the database
    - Redis is not ACID because it use memory to store data, which lack of Durability

# NoSQL[[Link](https://neetcode.io/courses/system-design-for-beginners/15)]
- Don't organize data in tables
- More flexible and scalable than SQL
    - were designed to overcome the limitations of SQL databases, which have certain constraints in terms of scalability and performance. 
    - SQL databases can be scaled vertically, but there are limitations to this method
- Specifically engineered to handle large-scale data and high speed workload
- Can scaled horizontally
- Different types of NoSQL database
    - __Key-Value Database__
        - Just like a hashmap
        - key serves as unique identifier
    - __Document Database__
        - JSON-like
        - Provides flexibility because individual fields in a document can be added or removed independently
    - __Wide-Column Database__
        - Stores data in columns rather than rows
        - Allow effcient storage and retrival of large database
        - Good at handling very large scale data
            - especially excel in handling and manage a lot of timestamp data
    - __Graph Database__
        - Use graph-like structure
        - Each node refers to an entity
        - Node in a graph db are connected to each other through edges or relationships
            - can represents various kind of relationship, friendships and association between entities
        - Useful when the data has complex relationship and interconnectedness
- __Why NoSQL__
    - No strict constraints like RDMS, the data can be split and store on differnt servers.
        - This means half the data can be stored on one database, in one part of the world and the other half can be stored on another database, in a totally different part of the world.
    - NoSQL are designed with distributed architecture in mind
    - BASE stands for "Basically Available, Soft state, Eventual consistency"
    - Eventual Consistency
        - Leader/follower architecture
            ```text
            Suppose that we have three database replicas and the query request to fetch the data can be directed to any one of 
            these replicas. However, the first one may be said to be a primary database node. However, one of the nodes in the 
            replica set will be a primary node. Updates and writes can only be done to the primary node and the primary node 
            eventually updates the rest of the nodes. In this case, the primary node can be said to be the leader and the rest 
            of the nodes being the followers.

            Because the nodes, apart from the primary node are only eventually being updated, there might be times when a user 
            requests data and it is stale. This can be true in apps like Twitter or Instagram where updating the follower 
            count may be delayed because the leader node has not updated the rest of the nodes.
            ```
# Replication and Sharding[[Link](https://neetcode.io/courses/system-design-for-beginners/16)]
- Two techniques commonly used together in a distributed system to achive high availability and throughput
- __Replication__
    - Involves creating a copy of the dataset called replica
        - replica(s) hosted on a separate machine or server
        - sync with the original database
    - To increase data availabilty, improve scalability, and increase data durability
    - In a leader/follower architecture:
        - data replication flows from the leader to the follower
        - leader is responsible for updating the follower
    - `Synchronous Replication`
        - Every write transaction on the leader is immediately replicated to the follower
            - ensure consistency between two replicas
        - This approach introduce latency (consitency in distributed system level)
        - Benefit: the mostly updated follower can take its place if leader gose down
    - `Asynchronous Replication`
        - Involves a delay in data replication
        - Leader database commits the transaction and sends replication data to the follower without waiting for the follower to acknowledge or apply the changes immediately
            - This reduce latency
            - but if a client makes a request to the follower before leader has updated it, the data might be stale untile the leader updates
            - This trad-off made for increased availabilty
    - `Master-Master(leader-leader;multi-leader) Replication`
        - Is used when data needs to be served in different regions
            - one leader server west while another servers east
        - Both leaders can be written to and read from
            - make it ideal for distributing data accross different parts of world
            - but synchronization latency between leaders can be a challenge, and measures like periodic updates are needed to keep them sync
- __Sharding__
    - Is used when replication alone is insufficient to handle the high traffic volume on a single database
        - involves divide databased into smaller shards
        - each hosted on a separate machine or server
    - System acheives improved performance, scalability, and availability by distributing data and workload across multiple shards
    - Each shards contains only a subset of the entire dataset
        - do not have a complete copy of the original database
    - How data partitions:
        - Range-based approach
            - data split according to ranges
    - Determing how data is partitioned among shards is done using a shard key
- __Challenges with Sharding__
    - It can be complex to ensure related table with related data end up in the same shard when dealing with hundreds of tables
    - Challenge in maintaing ACID properties in RDMS
        - they are not designed fo distribution
        - MySQL, PostgreSQL do not inherently support sharding
    - NoSQL, designed with horizontal scaling in mind, are better suited for sharding
        - As they do not have the same constraints as relational databases.
        - They offer eventual consistency, where data consistency across nodes is achieved over time.

# CAP Theorem
- CAP stands for Consistency, Availablity, and Partition Tolerance
    - the concept suggests that a distributed system can only ensure two out of these three guarantees simultaneously
        - either Parition Tolerance or Availability, or Partition Tolerance and Consistency, but never all three at once
    - `Partition Tolerance`
        - Partition in a distributed system arises when a communication breakdown between the leader and follower nodes prevents the leader from updating the follower. various factors lead this include:
            - network failure
            - hardware issue
            - etc...
        - If a system demonstrates partition tolerance, it implies that it can persist in functioning despite network failures, thereby avoiding a total system collapse.
    - `Consistency`
        - in the context of the CAP theorem, refers to the uniformity of data between the leader and follower nodes. This should not be confused with consistency in `ACID`.
        - Ensures that all nodes within the system perceive the data identically at any given moment.
            - in the event of a data update, the clients will always access consistent data
        - Regardless of the node from which they fetch the data, the information will remain consistent across all potential data-reading nodes. Every read will retrieve the most recent written data.
        - If our system remains partitioned and data is written to the leader database, a client reading from the leader database will receive the most recent data.
            - However, since updates to the follower database are blocked, reading from it could yield outdated data.
                - A possible solution could be to **render the follower node redundant** (to prevent access from blocked node), ensuring no outdated data is read.
    - `Availability`
        - Differs from its definition in ACID, refers to every system request receives a response: be it successful or a failure, regardless of system faults.
            - ensures the system stays operational and can manage requests even amid failures
- __Consistency or Availability__
    - Availability over Consistency
        - Systems such as university's Learning Managment System:
            - High Availability might be more crucial
                ```text
                For instance, if a student is attempting to submit an assignment, the LMS must be available to accept the 
                submission. Even if there's a minor delay in updating the grade, it is unlikely to impact the operation negatively.
                ```
    - Consistency over Availability
        - Some cases need data is absolutely crucial, such as banking and healthcare system
            - consistency should be prioritized
                ```text
                In a banking system, the account balance must be correct and consistent across all nodes. If a network 
                partition occurs, it might be acceptable to stop the operations, but still ensuring that the data remains 
                consistent. In a similar manner, in a healthcare setting, having accurate and up-to-date medical 
                records is a matter of life and death and inconsistent data will lead to severe consequences, so prioritizing 
                consistency is critical.
                ```
    - Note:
        ```text
        Many modern databases aim to strike a balance between consistency and availability, rather than strictly adhering to 
        being CP or AP. These databases often provide "tunable consistency", permitting the system to dynamically adjust 
        between being more consistent and less available, or more available and less consistent.
        ```
- PACELC Theorem
    - "Given P (a network partition), choose A (availability) or C (consistency). Else, favor low Latency or Consistency."
        ```text
        To delve deeper, when a network partition occurs, we have two choices: prioritize either availability or consistency.

        Continuing within the leader-follower paradigm, in the absence of a network partition, we must opt to favor either latency or 
        consistency. This means that users will either receive consistent data or data with low latency.
        ```
        
# Object Storage[[Link](https://neetcode.io/courses/system-design-for-beginners/18)]
- More akin to file storage systems rather than traditional databases
- __Diff in DB and Object Storage__
    - Object Storage
        - the concept of folder doesn't exist
        - non-hierachical structure
            - objects are stored in flat address space
                - facilitates easier scalability compared to file storage systems
                ```text
                Object storage evolved from BLOB (Binary Large Object) storage and is commonly used for storing items such as 
                images, videos, and database backups. Prominent examples include AWS S3 and Google Cloud Storage.
                ```
        - treats each piece of data as an object, like:
            - actual data
            - metadata
            - unique identifier
        - when retriving data, direct read from the object store itself are typically not performed
            - a network HTTP request is made directly to the object storage to fetch the data
    - DB
        - hierachical structure
        - From a design perspective:
            ```text
           It's crucial to note that storing images or videos in a database is typically not a recommended practice. Querying 
           for specific images or videos in a database is rare, and storing such data in a database can hinder performance, 
           increase storage requirements, and result in frequent read and write operations on the database.

           Traditional RDBMSs are not optimized for handling large files, but object storage emerges as a solution to this 
           challenge. It is specifically designed to handle unstructured data efficiently and is well-suited for 
           storing large files. One significant advantage of using object-based storage is its scalability, allowing for easy 
           scaling of the flat architecture without encountering the limitations associated with file storage.
            ```

## Supplementaries
- Consistency Patterns:
    - Weak Consistency:
        - After a write, reads may or may not see it.
            - A best approach is taken
        - Does not garantee all clients will see the same version of the data at the same time, or that updates will be reflected immediately across all nodes
        - Means temporay lag between a write operation and when the update is visible to all clients
        - This approach works well in:
            - real-time use cases such as VoIP
                - Voice over Internet Protocol (VoIP), is a technology that allows you to make voice calls using a broadband Internet connection instead of a regular (or analog) phone line.
            - video chat
            - real-time multiplayer games
    - Eventual Consistency
        - Reads will eventually see it. Data is replicated asynchronously
        - This approach seen in systems such as DNS and email.
        - Works well in highly avaible system
            - Seach engine indexing
            - DNS, SMTP, snail mail
            - Amazon S3, SimpleDB
    - Strong Consistency
        - After a write, read will see it. Data is replicated synchronously
        - This approach seen in file systems and RDBMS.
        - Works well in system that need transactions.
            - What is transactions?
                - A sequence of operations that are treated as a single unit or work
                - Has ACID properties to ensure realiability and consistency
- Availability Patterns
    - Two complementary patterns to support high availbility: fail-over and replication
    - Fail-Over
        - Definition: When a primary system (like server or databse) fails, the system automatically switches to backup (secondary) system to keep things running smoothly 
        - Example: if main db goes down, system automatically switches to a replica to keep handing requests
        - Goal: Minimize downtime and ensure uninterrupted service
        - __Active-passive__
            - Heatbeats are sent between the active and the passive server (standby)
            - if the headtbeats interrputed, the passive server takes over the active's IP address and resume service
            - also be referred to as master-slave (leader-follower) failover
        - __Active-active__
            - Both servers are managing traffic, spreading the load between them
            - if the server are public-facing, the `DNS` would need to know about the public IPs of both servers.
            - if the servers are internal-facing, `application logic` would need to know about both servers.
            - also be referred to master-master failover
        - __Disadvantage for failover:__
            - Adds more hardware and additional complexity
            - Potential loss of data if the active system fails `before` any newly written data can be replicated to the passive
    - Replication
        - leader-follower vs. leader-leader
    - Availability in parallel vs. in sequence:
        - In sequence:
            - overall availability decreases when two components with availabilty less than 100% are in sequence:
                ```text
                Availability (Total) = Availability (Foo) * Availability (Bar)
                ```
            - if both Foo and Bar each had 99.9% availability, their total availability in sequence would be 99.8%.
        - In parallel:
            - overall availability increase when two component with availability less than 100% are in parallel
                ```text
                Availability (Total) = 1 - (1 - Availability (Foo)) * (1 - Availability (Bar))
                ```
            - if both Foo and Bar each had 99.9% availability, their total availability in parallel would be 99.9999%.
    - What is Failback?
        - Definition: After the primary system has recovered from the failure, the system swiches back from the backup system to the primary system.