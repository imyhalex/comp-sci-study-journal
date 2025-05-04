# Computer Architecture[[Link](https://neetcode.io/courses/system-design-for-beginners/1)]

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
