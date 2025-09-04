# Proxies and Load Balancing[[Link](https://neetcode.io/courses/system-design-for-beginners/12)]
- __Forward Proxy__
    * Acts on behalf of the client.
    * Hides the **client's identity** (IP address) from the destination server.
    * Clients are aware of the proxy's presence.
    * Common uses:
        * **Privacy**: Client’s IP is masked.
        * **Caching**: Frequently requested data is stored and reused.
        * **Access control**: Blocks access to certain websites (e.g., in schools or companies).
    * Analogy: A friend sends a letter on your behalf, masking your return address.
- __Reverse Proxy__
    * Acts on behalf of the server.
    * Hides the **server's identity** from the client.
    * Clients **do not know** which backend server actually handles the request.
    * Common uses:
        * **Load balancing**
        * **DDoS (Distributed Denial of Service) protection**
        * **Caching** of static assets
    * Example: **CDNs** like Cloudflare or Akamai serve as reverse proxies.
- __Load Balancers (a type of Reverse Proxy)__
    - Distributes incoming client traffic across multiple backend servers.
    - Improves performance, fault tolerance, and scalability.

- __Common Load Balancing Strategies:__
    * **Round Robin**
        * Each server gets requests in a rotating order.
        * Assumes all servers are equally capable.
    * **Weighted Round Robin**
        * Distributes requests based on server “weight” (capacity).
        * E.g., Server A (50%), Server B (25%), Server C (25%)
    * **Least Connections**
        * Routes new requests to the server with the fewest active connections.
        * Best for variable workload requests (e.g., during online sales).
    * **User Location (Geo-based)**
        * Sends users to the **nearest geographical server** to reduce latency.
        * Improves speed and user experience.
    * **Consistent Hashing**
        * \[Mentioned but not covered in this lesson; used for sticky sessions and caching.]

- __Layer 4 Load Balancing__
    * Operates at the **transport layer** (TCP/UDP).
    * Makes routing decisions based on IP and port only.
    * **Faster**, but less flexible.

- __Layer 7 Load Balancing__
    * Operates at the **application layer** (HTTP/HTTPS).
    * Makes routing decisions based on content (URL, headers, cookies, etc).
    * **More intelligent**, supports complex routing logic (e.g., route /api differently from /images).

| Feature           | Forward Proxy               | Reverse Proxy                        | Load Balancer                           |
| ----------------- | --------------------------- | ------------------------------------ | --------------------------------------- |
| Hides             | Client                      | Server                               | Server                                  |
| Acts on behalf of | Client                      | Server                               | Server                                  |
| Client aware?     | Yes                         | No                                   | No                                      |
| Use Cases         | Privacy, Filtering, Caching | Load distribution, Security, Caching | Distribute traffic, Improve reliability |
| Examples          | Corporate firewall, VPN     | CDN, API gateway                     | NGINX, HAProxy, AWS ELB                 |


# Consistent Hashing[[Link](https://neetcode.io/courses/system-design-for-beginners/13)]
- Hashing is another technique can be used to map request to servers in the context of load balancing
- Concept:
    - each requeset will have an ip address, user id, and request id associate with it
    - cacluate the the hash using unique identifier (ip) and mod it by number of servers available
        - assign to specific server
- Issue with regular hashing:
    - if one server goes down, it means need to recalculate the modular arithmetic again: change the number to mod, leads to 
        - new mapping may differ for exisiting running requests hashing
    - Solution
        - use ring-based structure
            - if server goes down, the request it handled are assigned to the next available server in a clockwise direction on the ring
- Is just one approach to load balancing
- Other ways like round-robin or weight round-robin are useful when caching is not a concern
- This technique find applicability in scenarios such as Content Delivery Network (CDNs), particulary when it is necessary to route specific users to the same cache server in their respective regions.
- Also applied to databased where a user's data reside on a specific server, and consistent hashing of that user to that server is desired

# Supplementaries
- __Reverse Proxy (web server)__
    - Is a web server that centralizes internal services and provides unified interfaces to the public
    - Load Balancer vs. Reverse Proxy
        - Load balancer is a specialized reverse proxy that balance load
        - Deploying a load balancer is useful when you have multiple servers. 
        - Reverse proxy can be useful even with just one web server or application server
    - Benefits includes:
        - `Increased security` - Hide information about backend servers, blacklist IPs, limit number of connections per client
        - `Increased scalability and flexibility` - Clients only see the reverse proxy's IP, allowing you to scale servers or change their configuration
        - `SSL termination` - Decrypt incoming requests and encrypt server responses so backend servers do not have to perform these potentially expensive operations
        - `Compression` - Compress server responses
        - `Caching` - Return the response for cached requests
        - `Static content` - Serve static content directly
            - HTML/CSS/JS
            - Photo
            - Videos
            - Etc
    - Disadvantage: reverse proxy
        - Introduce reverse proxy results in increase complexity
        - A single reverse proxy is a single point of failure, configuring multiple reverse proxies (ie a failover) further increases complexity.
