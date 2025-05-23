# Proxies and Load Balancing[[Link](https://neetcode.io/courses/system-design-for-beginners/12)]
Here's a clean and concise markdown summary of the key concepts related to **Proxies** and **Load Balancers**, based on the article you shared:

---

# Proxies and Load Balancers (System Design Essentials)
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
