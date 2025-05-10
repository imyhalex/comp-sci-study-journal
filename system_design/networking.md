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