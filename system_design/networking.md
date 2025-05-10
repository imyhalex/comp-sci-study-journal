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
    ```text
    Let's keep following our example with Alice and Bob and see how data transfer in computer networks relates to their invitation exchange. Imagine 
    Alice grabbing an envelope for the invitation. She records her and Bob's details on the envelope, where Bob's information on the envelope can be 
    equated to the IP and TCP headers, and the actual invitation inside the envelope is similar to the payload or data of the packets.
    ```
    
    - `IP and data packets`
        - 