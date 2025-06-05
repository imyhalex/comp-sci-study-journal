# Networking Basics[[Link](https://neetcode.io/courses/system-design-for-beginners/3)]

- __Scnario:__
    ```text
    Alice and Bob are good friends living in different parts of the country. Alice wants to invite Bob to her birthday party, so she creates a 
    personalized invitation. In networking, each device is assigned a unique IP address. This IP address acts as an identifier, allowing devices to send 
    and receive data on the network. More specifically, Alice and Bob represent devices connected to the network.
    ```
- __IP Address__
    - An identifier for a machine
    - Allow devices to send and receive data on the network
    - Distinct number identifier for every device connected to a computer network
    - Two main types in IP address:
        - IPv4
            - 32-bit (4 bytes)
            - 4 group of 8 bit
            - range 0.0.0.0 - 255.255.255.255
            - theoretically allows for about 4.3 billion unique IP address
            - due to design choices during its creation and the exponential growth of the internet, the actual number of usable address is consierdably 
            lower, leads to the development of IPv6
        - IPv6
            - 128-bit (16 bytes)
            - consit of 8 group of 16 bits, each grop is in 4 hexadecimal digits
            - range `::` - `ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff`
            - this expanded address space allow for a virtual infinite number of unique IP address, making address exhaustion highly improbable
        - This rule of address machine follows specific rules known as protocol, which govern the trasmission of data over the internet. This is the 
        Interent Protocol (IP)
- __Protocols of sending data over a network__
    - Scnario:
        ```text
        Let's keep following our example with Alice and Bob and see how data transfer in computer networks relates to their invitation exchange. Imagine 
        Alice grabbing an envelope for the invitation. She records her and Bob's details on the envelope, where Bob's information on the envelope can be 
        equated to the IP and TCP headers, and the actual invitation inside the envelope is similar to the payload or data of the packets.
        ```
    - `IP and data packets`
        - Data is transferred over a network in the form of data packets, which consists of:
            - IP & TCP header: contains important info such as source and destinatio IP addresses
            - data
                - data is divided into multiple packets, and they may not arrive in the exact order they were sent
                    - to handle this, another protocol called TCP (Transmission Control Protocol) comes into action
            - trailer
    - `TCP (Transmission Control Protocol)`
        - When substantial volum of data needs to be transmitted, often use multiple packets
        - Responsible for the accurate transmission of these packets, ensuring they arrive in the right sequence
        - Anatomy of a TCP packet </br>
            ![viz tcp packet](../imgs/sharpen=1%20(2).avif)
            - When TCP sends a large chunk of application data, it splits it into multiple segments
            - Each TCP segment will have its own IP and TCP header.
            - A typical IP and TCP header looks like:
                ```c
                struct ipv4_header {
                    uint8_t  version_ihl;        // 4 bits version + 4 bits header length
                    uint8_t  type_of_service;
                    uint16_t total_length;

                    uint16_t identification;
                    uint16_t flags_fragment_offset;

                    uint8_t  ttl;
                    uint8_t  protocol;           // e.g., 6 for TCP
                    uint16_t header_checksum;

                    uint32_t source_ip;
                    uint32_t destination_ip;

                    // optional fields (if IHL > 5)
                };


                struct tcp_header {
                    uint16_t source_port;
                    uint16_t destination_port;

                    uint32_t sequence_number;      // <--- This field tells the position in the byte stream

                    uint32_t acknowledgment_number;

                    uint8_t  data_offset;          // header length
                    uint8_t  flags;                // SYN, ACK, FIN, etc.
                    uint16_t window_size;

                    uint16_t checksum;
                    uint16_t urgent_pointer;
                    
                    // optional fields may follow
                };
                ```
    - `Application Data`
        - This data can come from different shape such as HTTP POST request, where the information we wish to transmit reside in the application segment 
        of the packet
        - Conversely, it could be GET request whereby the data segment of the packet signifies the retrived response
    - `Network Layers`
        - Protocols within a computer network are systematically arragned into separate layers
            - IP is located in the network layer
                - sets physical pathway for the transmission of data
            - TCP is in the transport layer
                - takes care of the dependable transimission of data
            - HTTP operates in the application layer
                - makes interaction between clients and servers
- __Public vs. Private Network__
    - Public IP address
        - A unique identifier given to a device connect to the internet, supplied by the Internet Service Provider(ISP)
        - Reachable from any device on the internet
        - Is utillized when communication needs to occur between devices on separate network
            - application server
    - Private IP address
        - Employed within a confined network like a home or office network
        - These IP addresses aren't accessible to the broader internet
        - Are only reachable within a LAN (Local Area Network)
        - Usually the router hold private + public IP address, and assign one private IP address to local computer
            - Router has a puiblic IP assigned by Internet Service Provider (ISP), the external or "WAN" IP
            ```markdown
            | Device         | IP Address                               | Type             |
            | -------------- | ---------------------------------------- | ---------------- |
            | Your laptop    | `192.168.1.5`                            | Private LAN IP   |
            | Your router    | `192.168.1.1` (LAN), `74.125.88.1` (WAN) | Private + Public |
            | Website server | `142.250.190.78`                         | Public IP        |
            ```
- __Staic vs. Dynamic IP Address__
    - Dynamic IP
        - Allocated on a temporary basis and can change every time the device establish a connection
        - This type is frequently employed in home network
        - Automatically assigned
        - Drawback in changeability, so they are typically allocated to clilent not servers
        - Important: clients can also possess static IP address, but dynamic IP address are more commonly utilized for clients since they offer greater 
        adaptability in managing the restricted pool of available IP address
    - Static IP
        - Require manual configuration4
- __Ports__
    - Application ports(aka. network ports)
    - Numeric identifiers untilized to distinguished between multiple applications services runnig on a single device
        - If you've ever executed a full-stack project, you'll know that you cannot operate the frontend and backend on the same port.
    - Port number is a 16-bit integer, ranging from 0 to 65,535
    - Instances of these ports include port 80, typically used for HTTP (default port 80).
    - For HTTPS, default port is 443 (eg. https://www.google.com implicitly use port 443 (for encrypted communication via `TLS/SSL`))
    - `127.0.0.1` is the reserved loopback IP address, commonly known as: localhost
        - when application running on local computer it looks like `localhost:port no.` or `127.0.0.1:port no.`

# TCP and UDP[[Link](https://neetcode.io/courses/system-design-for-beginners/4)]

- __The use cases for TCP__
    - TCP (Transmission Control Protocol)
        - Use case: 
            - Email sending (under SMTP protocol)
            - User make HTTPs requests in a system
        - Pros: Reliable
        - Cons: 
            - Brings more overhead
            - Tend to be slower due to its rigorous approch to ensure delivery (latency)
        - Ensures lost packaets are reliably delivered, by:
            - setting up two-way connection (commonly referred to as a 3-wat connection)
        - Requires both the client and server establish a reliable connection before any data exchange take place
        - Bidirectional comminication can begin after the connection is established
        - If data pacakect is sent without receiving an acknowledgement
            - assumes it wasn't received and triggers retransmission
    - UDP (User Datagram Protocal)
        - Less reliable
        - Faster data transmission
        - Does not attempt to resend lost packets or reorder them
        - Use cases (opt for UDP), scenarios like:
            - Online gaming
            - Video streaming
                - Because: it is often preferable to skip a dropped frame rather than resend it
                - ensures smoother gameplay or uniterrupted streaming
            - Overall: UDP is selected over TCP in situtation where speed and efficiency take precendence over reliability and error correction

# DNS[[Link](https://neetcode.io/courses/system-design-for-beginners/5)]
- __DNS (Domain Name System)__
    - Operates as a decentralized hierarchical naming system that converts easily readable webasite name into IP address
        - When we input a domain name such as google.com into our web browser, the Domain Name System (DNS) translates it into an IP address (like 142.251.211.238).
    - Overall coordination, security, and operation of domain names within DNS is managed by ICANN (Internet Corporation for Assigned Names and Numbers)

- __ICANN and Domain Name Registrars__
    - ICANN:
        - Like shopping center's management company
        - Ensures the efficient running of the internet's infrastructure
    - Domain Regestrars
        - Resemble the individual store lease providers
        - Are certified by ICANN to offer domain name registration services
        - Assit us in searching for available domain name and oversee the registration procedure
    - ICANN doesn't own domain name directly
    - Domain name are sold by approved domain registrars, such as:
        - GoDaddy
        - Google Domains
        - HostGator
            - These registrars maintain the registration records and ensure that the domain is registered in our name
- __DNS Records__
    - Serve to store information related to a domain or subdomain
        - The A(Address) record, associates a domain with IPv4 address
            ```text
            Let's consider a scenario where you send a request to neetcode.io, which is linked to the IP address 192.158.1.39. The DNS 
            record for neetcode.io would house this IP address. Upon receiving your request, the DNS server would reference this 
            record to route your request to the server hosting the neetcode.io website. This server then sends a response back to 
            your computer.
            ```
    - To enhance future access speed, if a server has a static IP address
        - computer can store this IP address in its cache or memory
        - enables computer to retrive the IP address quickly instead of making another DNS query to the DNS server
    - DNS records and DNS server play a crucial role in ensuring that your requests reach the correct server by mapping domain name to thier corresponding IP address
- __Anatomy of a URL (Uniform Resource Locator)__
![anatomy of url](../imgs/anatomy-url.avif)
    - `Protocol (Scheme)`
        - Commonly start with either HTTP or HTTPS
        - Is also commonly referred to as the scheme
        - HTTPS has become more dominant protocol for URLs on the World Wide Web
        - Several other protocols that URLs can begin with:
            - FTP (File Trasfer Protocols):
                - denoted by `ftp://`
                - utilized to access files and directories on remote servers
                - servers as a means for transferring files between systems
            - SSH (Secure Shell):
                - denoted by `ssh://`
                - extensively employed for establishing secure remote connections to servers or computers
            - Examples:
                - `ftp://ftp.example.com/pub/file.txt`
                    ```text
                    In this example, "ftp://" indicates the use of the FTP protocol. "ftp.example.com" represents the FTP 
                    server's domain name or IP address. "pub" is the directory on the FTP server where the file "file.txt" 
                    is located. So, this FTP URL would be used to access and download the file named "file.txt" from the "pub" 
                    directory on the FTP server at "ftp.example.com".
                    ```
                - `ssh://username@example.com:22`
                    ```text
                    In this example, "ssh://" indicates the use of the SSH protocol. "username" represents the username you would 
                    use to authenticate yourself on the remote server. "example.com" is the domain name or IP address of the 
                    SSH server you want to connect to. ":22" specifies the port number (in this case, port 22) on which the SSH 
                    server is running
                    ```
    - `Domain`: e.g.: domains.google.com
        - Subdomain
            - In our example, the subdomain "domains" establishes a distinct section within the website, differentiating its content from the root domain. 
        - Primary Domain
            - The primary domain of google.com signifies the core identity of the website.
            - When we acquire a domain through a registrar, we gain ownership of this primary domain. 
        - Top Level Domain (TLD)
            - ".com" portion corresponds to the top-level domain
            - For instance, ".com" signifies commercial websites, while ".io" is commonly utilized by tech companies. 
            - Offers a way to categorize and classify websites based on their intended purpose on industry
        - Path
            - A path within a domain is denoted by using forward slashes, /. 
            - Signifies a specific location or route within the website
            - Enables more precise linking and navigation within a website's structure
        - Ports
            - HTTP/HTTPS protocol already default to certain port number (HTTP: 80; HTTPS: 443), call implcitly
            - For non-standard port must be specified in the URL
# Supplementaries
- __DNS__
    - Hierachical, with a few authoritative servers at the top of the level
    - Thr router or ISP provides information about which DNS server to contact whe doing a lookup
    - Lower levl DNS server cache mapping,
    - DNS results can also cached by your browser or OS for a certain period of time
        - NS record (name server): specifies the DNS server for your domain/subdomain
        - MX record (mail exchange): specifies the mail server for accepting messages
        - A record (address): points a name to an IP address
        - CNAME (canonical): points a name to another name or CNAME (example.com to www.example.com) or to `A` record
    - Some DNS can route traffic through various methods:
        - Weight round-robin
        - Latency-based
        - Geolocation-based
    - Disadvantage of DNS:
        - Accessing DNS introduces slight delay although caching 
        - DNS server management could be complex and is generally managed by government, ISPs (Internet Server Providers), and large companies
- __CDN__
    - A globally distributed network of proxy servers
    - Generally, static files such as HTML/CSS/JS, photos, and videos are served from CDN, although some CDNs such as Amazon's CloudFront support dynamic content
    - The site's DNS resolution wil tell client which server to contact
    - Serving content to CDN signicantly improve performance in two ways:
        - User receive content from data center close to them
        - Servers do not have to serve requests that the CDN fulfills
    - `Push CDNs`
        - What: You (the content owner) manually upload (or push) your content to the CDN’s edge servers in advance.
        - How it works:
            - You decide which files to upload.
            - You use FTP, APIs, or other methods to transfer them to the CDN.
            - The CDN then stores these files at its edge locations, ready to serve them directly to users.
        - Example: Good for large, static assets that don’t change often (e.g., video, software downloads).
    - `Pull CDNs`
        - What: The CDN only fetches (or pulls) content from your origin server when a user requests it.
        - How it works:
            - When a user requests a file, the CDN checks if it’s already cached at the edge.
            - If not, it retrieves the file from your origin server (pulls it) and caches it for future requests.
            - No need to upload all assets to the CDN in advance.
        - Example: Great for dynamic content or assets that change often.
    - Disadvanatage of CDN:
        - Costs can be significantly depending on traffic
        - Content might be stale if it is updated before the TTL expires it
        - Require changing URLs for static content to point to the CDN
- __Load Balancer__
    - Distribute incoming client requests to computing resources such as application servers and databases
    - Returns the response from the computing resource to the appropriate client
    - Effective at:
        - preventing requests from going to unhealthy server
        - preventing overloading resources
        - helping to elimiate a single point of failure
    - Can be implemented with hardware (expensive) or with software such as HAProxy
    - More benefits:
        - SSL termination:
            - Definition: is when the load balancer handles the encryption and decryption of HTTPS traffic
            - Offloads the CPU-intensive task of SSL/TLS encryption from the backend servers
            - Simplfies SSL certificate management: only the load balancer needs the certificate
            - Flow:
                - Client sends HTTPS requests -> Load balancer decrypts it
                - Load Balancer sends unencrypted request to backend servers (optional: re-encrypts if for secure internal traffic)
        - Session persistence:
            - Definition: Ensures all requests from a user go to the same backend server during a session
            - Why it matters:
                - Some applications store session data locally on the server (e.g., shopping cart, login state), so sending the same user to different 
                servers can break functionality.
            - How it works:
                - The load balancer uses a method like cookies, source IP hashing, or custom header to "stick" a client to a specific server.
    - Can route traffic based on various metrics:
        - Random
        - Least Loaded
        - Session/cookies
        - Round-robin or weight round robin
        - Layer 4
        - Layer 7