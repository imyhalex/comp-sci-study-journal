# Data Warehouse

__OLAP & Data Warehousing__
- A data warehouse is a database designed to perform large scale analytics
    - __Online Analytical Processing (OLAP):__
        - Focuses on processing large volumes of historical data to identify patterns, trends, and business insights
        - Also called __Business Intelligent (BI)__ or __Decision Support__
- Typically involves read-only queries that touch a lot of data
    - Example: “find total sales of Toyota’s over the last two years for each state and city in the USA”
- Workload charateristic:
    - Mostly read-only queries
    - Queries scan huge portions of data
    - Example: “Find total Toyota sales in the last two years, grouped by state and city.”
- Usually the result of Extract-Transform-Load (ETL) process

__OLTP vs. OLAP__
- OLTP (On-line Transaction Processing)
    - Recording current activities/events
    - Short-lived read/write txns
    - Small footprint
    - Repetitive operations
- OLAP (On-line Analytical Processing)
    - Analyzing past activities/events
    - Long-running, read-only quries
    - Complex joins, large aggregates
    - Exploratory ac-hoc queries

__Bifurcated Environment__
* **Two separate systems**: OLTP for real-time operations, OLAP for analytics.
* **Reason**: Heavy analytical queries slow down OLTP, so analysis happens somewhere else.

**OLTP Databases**

* Handle real-time business operations (e.g., bookings, payments, orders).
* Many small, short-lived read/write transactions.
* Must be fast, consistent, and always online.
* Optimized for concurrency and low latency.
* Cannot support long-running analytical scans without hurting performance.

**ETL (Extract–Transform–Load)**

* **Extract**: Pull data from one or more OLTP systems.
* **Transform**: Clean, normalize, aggregate, or reformat.
* **Load**: Store the processed data into an OLAP warehouse.
* Happens periodically (e.g., nightly, hourly) so OLAP stays up to date without affecting OLTP.

**OLAP Data Warehouse**

* Stores consolidated historical data from OLTP systems.
* Designed for large scans, big joins, and heavy aggregations.
* Used for analytics, reports, dashboards, BI, and data science.
* Long-running, read-only, ad-hoc queries.
* Updated periodically via ETL, not continuously.

**Data Marts**

* Subsets of a data warehouse.
* Focus on a department/subject area (e.g., sales, marketing, finance).
* Provide more specialized views for specific business units.

__Schemas in Data Warehouse__
- OLAP uses star or snowflake schemas
- Star Schema
    - Central fact table (metircs like sales, revenue, click)
    - Surrounding denormalized dimension tables (customer, product, time, location).
    - Simple structure → faster queries for OLAP.
    - Preferred for most data warehouses and BI tools.
- Snowflake Schema
    - A normalized version of the star schema.
    - Dimension tables are further split into sub-dimensions (e.g., product → product → category → department).
    - Reduces redundancy but increases number of joins.
    - Used when data consistency and storage optimization matter more than query speed.

__Star vs. Snowflake Schema__
- Issue #1: Normalization
    - (More normalized) Snowflake schemas take up less storage space
    - (Less Normalized) Star Schemas may incur integirity and consistency violations
- Issue #2: Query Efficiency
    - (Less efficient) Snowflake schemas require more joins to get the data needed for a query
    - (More efficient) Queires on star shcemas wll (usually) be faster


**Row-Store vs. Column-Store**

* **Row-Store (what we use in OLTP)**

  * Store *all attributes* of a single tuple contiguously in a page.
  * Ideal for point lookups and small read/write transactions.
  * Great for OLTP: inserting/updating whole rows quickly.

* **Column-Store (popular in OLAP)**

  * Store *values of a single attribute* for all tuples contiguously.
  * Ideal for scanning a few columns across millions of rows.
  * Great for OLAP: aggregations, filters, analytic queries.

**Why Data Warehouses Prefer Column-Stores**

**Advantages (why column-stores are good for OLAP)**

* Only read the columns needed for the query (I/O efficient).
* Much better compression (same-type values stored together).
* Faster scans + vectorized execution on contiguous column data.
* Great for aggregates (SUM, AVG, COUNT).
* Efficient for analytical workloads with massive sequential reads.

**Disadvantages**

* Writes/updates expensive (touch many column files).
* Bad for OLTP workloads (inserting a full row becomes scattered).
* Harder to maintain transactional semantics.
* Joins can be more costly without indexing strategies.


__Data Lakes__
- Repository for storing large amount of stuctured, semi-structure, and unstructured data without having define a schema or ingest the data into proprietary internal formats
- Store raw, unprocessed data from many sources (CSV, logs, JSON, images, streams).
- Schema-on-read: data structure is applied only when you query it.
- Cheap, scalable storage (e.g., S3, GCS, HDFS).
- Used for data science, machine learning, and exploratory analytics.
- Supports semi-structured + unstructured data (text, video, telemetry).
- Flexible: ingest now, decide schema later.
- Use the ELT (Extract-Load-Transform) model (not ETL)
    - Extract: pull data from many sources (apps, logs, IoT, DBs).
    - Load: store raw data immediately into the lake (e.g., S3).
    - Transform: apply structure only when reading/querying (schema-on-read).

__Parallel vs. Distributed__
- Parallel DBMS
    - Nodes are physically close to each other.
    - Nodes connected with high-speed LAN.
    - Communication is assumed to be fast and reliable.
    - Multiple processors/machines in a single tightly-coupled system.
    - Shared memory or shared disk; high-speed interconnect.
    - Designed for speeding up a single large query using parallelism.
    - All nodes under one DBMS instance (one logical database).
    - Focus: performance (faster execution of OLAP workloads).
- Distributed DBMS
    - Nodes can be far from each other.
    - Nodes connected using public network.
    - Communication cost and problems cannot be ignored.
    - Multiple nodes/machines in a loosely-coupled network.
    - Each node stores part of the data; nodes communicate over normal networks.
    - Data is partitioned/replicated across locations.
    - Appears as a single database, but data physically lives on many machines.
    - Focus: scalability, fault tolerance, and geographical distribution.


**Distributed DBMSs**

* Extend single-node DBMS techniques (indexing, logging, concurrency control) to work across multiple machines.
* Support distributed transaction processing, query execution, replication, and partitioning.
* Make multiple physical nodes appear as one logical database.

**System Architectures**

* **Shared Everything**

  * All CPUs share memory + disks.
  * Rare today (scales poorly).

* **Shared Memory**

  * Multiple CPUs share memory, but disks may be attached separately.
  * Limited scalability; used in small parallel systems.

* **Shared Disk** *(one of the most common for DBMS)*

  * All nodes have their own CPU + memory.
  * All nodes share the same disk subsystem.
  * Easier failover and coordination, but disk can become bottleneck.
  * Can sacle execution layer independently from the storage layer.

* **Shared Nothing** *(most popular for DBMS + distributed systems)*

  * Each node has its own CPU, memory, and storage.
  * Nodes communicate only over the network.
  * Maximizes scalability and fault isolation.
  * Basis of systems like Google Spanner, Amazon Redshift, Cassandra, Snowflake
  * This is traditional DBMS architecture
    * Harder to scale capacotu
    * Harder to ensure consistency
    * Better performance & efficiency
