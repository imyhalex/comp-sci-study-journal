# Computer Architecture[[Link](https://neetcode.io/courses/system-design-for-beginners/0)]

- __Disk:__
    - Store all data for computer
    - Persistent: the data will be persisted regardless of the state of the machine(turned on or off)
    - Modern computer store information in dist in TB(terabytes)
        - __Note__: 
            - 1 byte = 8 bits
            - 1 terabyte = 10^12 bytes
            - A disk storage like USB drive might have storage on the order of GBs (gigabytes), 1 gigabytes = 10^9 bytes
    - __HDD vs. SDD__:
        - HDD: Hard Disk Drive
            - Mechanical, have a read/write head[[Link](https://en.wikipedia.org/wiki/Disk_read-and-write_head)]
            - Older they get, the more wear and tear they collect, lead to slows down overtime
        - SDD: Solid-State Drive
            - More popular and faster
            - Cost a bit more
            - Significantly faster because do not have moving parts
            - Rely on reading and writing data electronically (similar to RAM)
- __RAM(Random Access Memory):__
    - Storing information but a lot smaller in size compared to disk
    - Size generally vary from 1GB- 128GB
    - Much more expensive than disk space
    - Benefit: write to RAM is significantly faster than disk
        - unit: in microseconds (10^-6 second), but write same amount data to a disk is in milliseconds(10^-3 second)
    - Data is not persisted in RAM once PC turns off
    - Keeps applications you have opend in memroy, include any variables the program has allocated
    - RAM and disk do not directly communicate with each other, they reply on the CPU to facilitate data transfer between them
    - RAM vs ROM:
        - RAM: Random Access Memory
        - ROM: Read Only Memory
            - Permanent, non-volatile type of memory (won't change when PC turns off)
            - Can't change after it is created, only access
            - Generally slower than RAM but faster than hard drive
            - Stores the BIOS(Basic Input/Output Systems) or UEFI(Unified Extensible Firmware Interface)
                - the first software dun when turn on PC and initializes hardware components
                - this software (BIOS or UEFI) initiates the boot process and helps load the operating system
    - SRAM(Static RAM)
        - Faster but more expensive
        - Used for cache memory in CPUs
    - DRAM(Dynamic RAM):
        - Slower but less expensive than SRAM
        - Used for main memory(RAM) in computers
- __CPU(Central Processing Unit):__
    - The intermediary between RAM and disk
    - Also is the "brain" of the computer
    - It read/write from the RAM and disk(s)
    ```text
    For example, when you write code and run it, your code is translated into a set of binary instructions stored in RAM.
    This sentence could be made clearer: "The CPU reads and executes these instructions, which may involve manipulating 
    data stored elsewhere in RAM or on disk. An example of reading from disk, would be opening a file in your file system 
    and reading it line-by-line.
    ```
    - All computations are done within the CPU, occurs in a matter of milliseconds
        - Fetchs instructions from the RAM
        - Decodes those instructions
        - Executes the decoded instructions
        - ___All these instructions are represented as bytes___
    - CPU consits of a __cache__
- __Cache:__
    - CPU contains this memory component
    - Most CPUs have an L1, L2, and L3 cache (L1: smallest & fastest; L3: largest & slowest)
        - they are physical components
        - much faster than RAM
        - stores data on the order of KBs or tens of KBs
    - When read operation is requested, the cache is checked before the RAM and the disk
        - if data requested in the cache, and it is unchaged since the last time it was accessed
            - it will fetched crom the cache, not the RAM
    - Read/Write from cache is lot faster than RAM and disk, usually happened in nanoseconds
    - It is up to OS to decide what gets stored in the cache
    - Caching is an important concepte applied in many areas beyond computer architecture
        - Web Browsers: use cache to keep track frequently accessed web pages to load them faster
            - data might include HTML, CSS, JavaScript, and images
            - in this case, browswer is using the disk as cache, because making internet request is a lot slower than reading from disk
                - __Why?__
                    - Disk access is much faster than downloading data over the internet.
                    - So instead of fetching the same resources again from a remote server (which takes more time and bandwidth), the browser first checks if the content is already cached on the local disk.
                    - If the cache is still valid (not outdated), it loads the content from disk, making the page appear much faster.
- __[Moore's Law](https://en.wikipedia.org/wiki/Moore%27s_law):__
    - What is it:
    ```text
    Moore's Law is an observation, which suggests that the number of transistors in a CPU double every two years. Looking at the visual below, it looks 
    like a linear graph, but looking at the scale on the y-axis explains that it is exponential. So while the number of transistors doubles, the cost of 
    computers tends to halve. In the recent years however, the number of transistors, and thus the speed of the computers, has begun to plateau.
    ```  

# Application Architecture[[Link](https://neetcode.io/courses/system-design-for-beginners/1)]
![application architecture high-level](../imgs/sharpen=1.avif)
- __A developer's perspective__
    - Developer write code that is deployed to a server
    - Server
        - A computer that handle requests from another computer
        - This server also requires persistent storage to store the application data
        - A server may have built-in storage, but has limitaion in size
        - Server may talk to an external storage system(database, cloud etc)
            - Storage may not be part of the same server, and is instead connected through a network
- __A user's pserspective__
    - Somone makes a request from the server(ususally through web broswer)
    - If a user wants to use front-end feature, server will respond with the necessary JS/HTML/CSS code, compiled to display what the user requested
    - When a lots of user making request
        - Need to scale our server
- __Scaling Server__
    - Vertical Scaling: upgrading components within the same PC
        - Add more RAM
        - Upgrad CPU with more cores and higher clocking speed
        - Limitation: every computer has a limitaion in terms of upgrading
        - Sufficient and easier to implement for simple application
    - Horizontal Scaling: upgrading by combining multiple PC
        - Can have multiple server running the code
        - Distribute the user requests among these servers
        - Ensure:
            - Speed of each server remains intact
            - If one server goes down, we can direct traffic to other servers
        - Requires much more engineering effort
    - Large system prefer horizontal scaling
    - Multi-server determines which requests go to which server by using `load balancer`
        - A load balancer will evenly distribute the incoming requests across a group of servers
    - Important: servers don't exist in isolation,
        - It is higly likely that servers are interacting with external servers through APIs
        - For instance: neetcode.io website interact with other services like Stripe through an API
- __Logging and Metrics__
    - Give the dev a log of all the activity that happend
    - Can be written to the same server, but for better reliability they are commonly written to another external server
    - Gives dev insight into how request went
        - if error occur
        - what happend before a server crashed
        - but logs don't provide complete picture
    - If RAM has become the bottleneck of our server or CPU resources are restricting the request being handled efficienctly
        - require `metric` service
            - collect data from different resources within our server environment such as:
                - CPU usage
                - network traffic...(etc)
            - allow dev to gain insight into server's behavior and identify potential bottleneck
- __Alert__
    - Explain:
    ```text
    As developers, we wouldn't want to keep checking metrics to see if any unexpected behavior exhibits itself. 
    This would be like checking your phone every 5 minutes for a notification. It is more ideal to receive a push notification. 
    We can program alerts so that whenever a certain metric fails to meet the target, the developers receive a push notification.
    For example, if 100% of the user requests receive successful responses, we could set an alert to be notified if this metric dips under 95%.
    ```

# Design Requirements[[Link](https://neetcode.io/courses/system-design-for-beginners/2)]

- __Thinking in System Design__
    - `Moving Data`
        ```text
        As we discussed earlier in the chapter on computer architecture, data is moved between the disk, RAM, and CPU. However, when designing large 
        systems, our focus shifts to moving data between different clients and servers, which may be geographically dispersed across the world. This is 
        significantly more challenging compared to local data movement.
        ``` 
    - `Storing Data`
        - Q: how do we store data? Database? Blob Store? File Sytem? Distributed System?
            ```text
            This might remind you of picking between different data structures to find the optimal solution. For example, choosing an array over a BST to 
            store data doesn't mean that an array is better than a BST in all scenarios, but rather it depends on the use case. By the same token, we have 
            to choose how we want to store data and which way will be the most efficient, given the scenario.
            ```
    - `Transforming Data`
        ```text
        Lastly, we want to transform data. It wouldn't be very fun if all we were doing was moving and storing data. If we were given a bunch of server 
        logs, one way to transform this data would be to output the % of successful requests vs % of failed requests. This is sometimes handled by a 
        monitoring service. Perhaps, we are given some medical records, and we want to filter the patients by age. These are just two basic examples, 
        and there are countless ways to transform data. Regardless of how complex or how simple the process, the fundamental question is: what is the 
        most efficient way to transform the given data?
        ```
    - Note:
        - Picked bad algo or changing bad code won't be challenging
        - But bad design in the application architecture can be very costly
            - choose wrong DB will have more severe consequences
                - need to migrate data
                - rewrite portions of the application
- __What is a good design?__
    - Q: what constitues a good design? evaluate:
        - a number of factors
        - performance measures
        - certain metrics
        - ___in essence:___ need to do compare and contrast and identify trad-offs by evaluating these factors
    - `Availability`
        - Heart of an effective system
        - Refers to the percentage of time in system is available, as in, up and running for a given period of time
            - Formula: availability = uptime / uptime + downtime
                - downtime can be planned or unplanned
                    - planned: software update, verification, back-up etc.
                    - unplanned: hardware/software failure, natural disaster
                    - takeaway: hard to predict unplanned downtime but chances of occuring can be minimized
                - Example:
                    ```text
                    Using the equation above, let's say that we had an uptime of 23 hours out of 24 hours. This would result in a total availability of 
                    96%. From a system design and a business perspective, this is rather poor, because we are losing money and users for 1 hour a day.
                    ```
                    - Ideally: 100% availability, but it is not possible due to unplanned downtime
                        - companies will aim for at least 99% availability, but:
                            - still poor in performance
                            - calculate: (1 - 99%) * 365 days = 3.65 days shut down
                                - will loose lots of money for company like amazon
                            - if reduce downtime by factor of 10
                                - take uptime to 99.9% and downtime to 0.1%, which is a big jump
                    - A good target for companies to have 99.999%, which is 5 min downtime in 365 days
                        - hard to achive but it is important for mission critical system
        - Measure of availability is used to define `SLO`(service level objective) and `SLA`(service level aggrement)
            - SLA: An aggrement a company makes with their clients or users to provide a certain metric of uptime, responsiveness, and responsibilities.
            - SLO: Refers to an objective your team must hit to meet the SLA requirements.
            - For example: AWS's monthly SLA is 99.99% and if not met, they refund a percentage of service credit.
            - And SLO is an aggrement within an SLA
- __Reliability, Fault Tolerance, and Redundancy__
    - `Reliability`:
        - Referes to the system's ability to perform its intended fuctions without failure or errors over a specific period of time.
        - When discussing reliability of a system, we are talking about the probability that the server won't fail
            - if thousands of users are making requests, or if there are DDoS(Distributed Denial-of-Service) attacks, how easily our server go down
                - this brings to fault tolerance
    - `Fault Tolerance`:
        - If one of our system has a fault, it fails, and we have another server, it means our server is somewhat fault tolerant
        - Refers to how well the system can detect and heal itself from a probelm, some actions like
            - disable a function
            - revert to a different mode
            - switch to a different server...(etc.)
        - To let system be fault tolerance, we can have a redundant server (Redundancy)
    - `Redundancy`:
        - Refers to something that is unessential in English
        - Is provided by backup server which essentially "shadow" the contents of a server
            - we don't need this server, but it only comes into play if primary server fails
            - only have this redundancy, we are able to have Fault Tolerance
            - second server a simply backup, what if we had two servers that were both active? This would be called `active-active redundancy`
        - Note: in most cases, by redundancy we mean active-active redundancy
- __Throughput__
    - Refers to the amount of data or operations we can handle over some period of time
    - Throuput of a client making request to a server would be measured through the `number of requests/second`
    - If want to improve throughput, perform:
        - vertical scaling
        - horizontal scaling
    - Another measure of throughput is `queries/second`, which measure the number of requests made by user to a server or DB
        - this make more sense when discussing design in terms of users
    - Also has measure of `bytes/second`, refering the maximum amount of data that can be sent over a network at any given time
        - more sense when having a data pipeline where are required to process given data in a different format
        - the data isn't related to a single user
- __Latency__
    - Refers to the delay between the client making the request and the server responding to that request
    - Diff between Throughput and Latency:
        - Throughput refers to how many requests can be sent oer a network per second
        - Calculation:
         ![viz latency](../imgs/sharpen=1%20(1).avif)
        - Latency refers to the amount of time it takes for each individual request to be completed
        - Latency is not exclusive to network
            - even exists within a computer's internal components such as RAM and each cache making requests from the CPU

    