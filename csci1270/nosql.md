# NoSQL
```text
“A NoSQL (non-SQL) database provides a mechanism for storage and retrieval of data
that use looser consistency modelsthan traditional relational databases in order
to achieve horizontal scaling and higher availability. Since this non-relational
database design does not require a schema, it offers rapid scalability to
manage large and typically unstructured data sets. Some authors refer to them as
"Not only SQL" to emphasize that some NoSQL systems do allow SQL-like query
language to be used.”
```

__NoSQL Characteristics__
- NoSQL used in database design (non-relational)
- Ability to store semi-strctured and structured data
- Reduced functionality with simpler data model
    - No schema required
- Optimized for queries and scaling (typically no ACID transactions)
    - Looser consistency models
    - Horizontal scaling

__Scaling Models__
- Vertical Scaling (scaling up)
    - Upgrade hardware
    - Limited by the resources you can put on a single machine
    - Low availbility, low scalability
    - Used by most traditional DBMS
- Horizontal Scaling (scaling out)
    - Add more machine
    - Requires database sharding and (perhaps) replication
    - Limited by read/write ratio and comminication overhead
    - High availability, high scalability
    - Used by NoSQL database

__NoSQL Flavors__
- Key-Val pair
- Document database
- Wide-Column stores
- Graph database

__MongoDB__
- Document database system 
- JSON-style documents
- Uses BSON (binary JSON)
- Schemaless
- Document-based queries
- Indexing for fast reads
- Auto-sharding for scalability
- Replication for high availability
- Terminology
    - Database = Database
    - Collection = Table
    - Document = Tuple
    - Field = Attribute
    - _id field = Primary Key
- Each documebnt (even in the same collection) can have a different schema

__Data Model__
- A document is built on two key structures:
    - An object is a series of name (field) & value pairs
    - A Value can be
        - An atomic value: string, number, true, false, null
        - An object
        - An array
- The _id field
    - Every document must have an _id field
    - Must be unique within the collection; serves as the primary key
    - If you don’t supply one, MongoDB automatically adds it for you

__Model Relationship in MongoDB__
- Two options
    - Referencing: Store references to other documents using their _id value (similar to using foreign keys)
    - Embedding: Embed documents within other documents explicitly (similar to denormallization)

__CRUD operations__
- CRUD operations:
    - Create
    - Read
    - Update
    - Delete
- Create
    - Insert operations add new documents to a collection
    - All write operations are atomic at the level of a single document.
- Read
    - Retrieve documents from a collection
- Update
    - Update operations modify existing documents in a collection.
    - All write operations are atomic at the level of a single document.
- Delete
    - Delete operations remove documents from a collection.

__Distributed Architecture__
- Heterogeneous distributed components
    - Shared nothing architecture
    - Centralized query router
- Primary-secondary replication
- Auto-sharding:
    - Define “sharding” attributes for each collection (hash or range)
    - When a shard gets too big, the DBMS automatically splits the shard and rebalances

__Sharding__
- Mongos routes queries to only the shards that contain relevant data if the queries contain the shard key.
- When a query doesn’t contain the shard key, the query is broadcast to all shards.

__Shard Key Selection__
- Hash or Range-based; Can be Composite
- An ideal shard key should
    - distributed documents and load evenly throughout the cluster, and 
    - facilitate common query patterns
- Considerations
    - Frequency with which shard key values occur
    - Query load for each key
    - Query patterns (range vs. point queries)
    - Cardinality of the shard key

__Replication__
- Write operations execute on the primary, which records the operations on its log. Secondaries replicate this log and apply the ooperations to their data set
- A write is commited when it is finalized on the primary and some secondaries (e.g. majority, or a specific number)
- If a primary failes (does not respond within a timeout period), one of the secondaries get as the new primary
- Lots of a parameters/options to control replication behavior

__Big Data__
- A buzzword that refers to challenges in modern large-scale data management and analytics
    - No longer just simple computations, also complex computations (e.g., data mining, machine learning)
    - Huge amount of data

__Big Data Needs Massive Parallel Processing__
- Assume each machine has a hard disk that can read data at 3Gbit/sec
- Scanning 100TB data takes:
    - For 1 machine: ~3.25 days
    - For 100 machines (in parallel): ~45 minutes
    - For 1000 machines (in parallel): ~27 seconds

__Side Effect of Using Many Machines__
- How do you program many machines?
    - Not one machine at a time!
    - Need a simple, parallel cluster programming model
- How do you deal w/ failures?
    - Mean time between failures (MTBF) for 1 machine ~3 years
    - MTBF for 1000 machines ~1 day
    - MTBF for 10000 machines ~ 1 minute

__Challenges of Commondity Clusters__
- Cheap nodes fail, especially when you have many
    - Solution: Build fault tolerance into system
- Commodity network = low bandwidth 
    - Solution: Push computation to the data
- Programming in a cluster is hard
    - Solution: Restricted programming model: E.g., users write data-parallel “map” and “reduce” functions, system handles work distribution and failures