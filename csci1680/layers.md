# Layers
- Same concept to abstraction: break the problem down into parts, solve each problem independently

__Q: How to deliver a package__
- Add metadata that tells us where data should go (label on package)
- Data: content, also call payload
- Metadata: header

## Layering
- Application
- TCP, UDP
- IP
- Link Layer

__Application (Layer 7)__
- The applications/programs/etc you use every day
- Examples:
    - HTTP/HTTPS: Web traffic (browser, etc)
    - SSH: secure shell
    - FTP: file transfer
    - DNS

__How to make apps use the network?__
- Want to send useful messages, not packets
- Don’t have to care about how path packet takes to get from A->B, we just want it to get there

__Transport Layer (Layer 4)__
- OS provide interface for "socket": API for making network connections
- Creates a "pipe" to send/recv data to another endpoint, like a file descriptor
- Two classic transport layer protocal: TCP (reliable) and UDP (unreliable)
- OS keeps track of sockets which sockets belong to which app => multiplexing
- __Multiplexing applications__
    - multiplexing provided by port numbers
    - 16-bit number: 0-655355
    - Servers use well-known port numbers, clients typically choose one at random

__Network Layer (Layer 3)__
- Provided by: Internet Protocol (IP)
- Moving packets between any two hosts anywhere on the internet
- Responsible for forwardning, and routing packacts between nodes.

__Lower Layers__
- Link Layer (L2): Individual links between nodes
    - Ethernet, wifi, cellular, etc
- Physical Layer (L1): how to move bits over link 

__IP as the "narrowing point"__
- Applications built using IP
- IP connects many heterogeneous networks

__Takeaway__
- Each layer provides a service for the layers “above” it
- Each layer is defined by some protocol
- Layer N uses the services provided by N-1 to operate