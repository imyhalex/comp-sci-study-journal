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