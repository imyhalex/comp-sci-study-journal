# Stack Drawing

## Ret to Libc
![img](./img/Screenshot%202025-12-01%20172416.png)
![img](./img/Screenshot%202025-12-01%20172435.png)
![img](./img/Screenshot%202025-12-01%20173205.png)
```text
Use the NOP sled technique:
1. Move the shellcode right below the overwritten return address.
2. Fill the beginning of the buf[] with NOP (0x90) instructions.
3. Overwrite the return address with an address belonging to the
“middle” of the NOP sled.
```
![img](./img/Screenshot%202025-12-01%20175247.png)

## Advance Code Reuse (Ret2Libc Chaining)
![img](./img/Screenshot%202025-12-01%20180115.png)
![img](./img/Screenshot%202025-12-01%20180147.png)

## ROP
![img](./img/Screenshot%202025-12-01%20183237.png)
![img](./img/Screenshot%202025-12-01%20183243.png)