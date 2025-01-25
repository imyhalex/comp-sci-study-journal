# Hashing

- Mapping data to a specific index in a hash table (an arry of items) using a __hash function__ that enables fast retrieval of information based on its key
- All three operation (search, insert, and delete) in \(O(n)\)

## Hash Function
A Function that translates keys to array indices is known as a hash function. The keys should be evenly distributed across the array via a decent hash function to reduce collisions and ensure quick lookup speeds.

- __Integer universe assumption:__ The keys are assumed to be integers within a certain range according to the integer universe assumption. This enables the use of basic hashing operations like division or multiplication hashing.
- __Hasing by division__: This straightforward hashing technique uses the key’s remaining value after dividing it by the array’s size as the index. When an array size is a prime number and the keys are evenly spaced out, it performs well.
- __Hasing by multiplication:__ This straightforward hashing operation multiplies the key by a constant between 0 and 1 before taking the fractional portion of the outcome. After that, the index is determined by multiplying the fractional component by the array’s size. Also, it functions effectively when the keys are scattered equally.

## Hash Data Structure in Java and common used metods

Below is an extended explanation that **completes** your notes on hashing. It covers **collision resolution**, **open addressing**, **separate chaining**, and provides an overview of **hash data structures in Java** along with commonly used methods. Feel free to modify the structure or content based on your needs!



## Collision Resolution
A **collision** happens when a hash function maps more than one key to the **same index** in the hash table. Even with a good hash function, collisions are inevitable when many keys share the same array index. To handle collisions, there are two primary strategies:

1. **Separate Chaining (Open Hashing)**  
   - Each cell of the hash table **stores a linked list** (or another secondary data structure) of entries that share the same index.  
   - When a collision occurs, a new key-value pair is added to the list at that index.  
   - **Advantages**:  
     - Simple to implement.  
     - Less sensitive to load factor (you can always add more nodes to the linked list).  
   - **Disadvantages**:  
     - Potentially higher memory usage (an extra data structure per slot).  
     - In the worst case (all keys in the same slot), access can degrade to \(O(n)\).  
     
   > **Example**: If the hash function maps keys 7, 14, and 21 to index 3, we just append them to a linked list (or similar structure) at table\[3\].

2. **Open Addressing (Closed Hashing)**  
   - All entries are stored in the **same hash table** (no extra data structure).  
   - When a collision occurs, the algorithm seeks the **next empty slot** in the table using a probing sequence.  
   - Several probing techniques exist:  
     1. **Linear Probing**: If index \( i \) is occupied, try \( (i + 1) \mod m \), \( (i + 2) \mod m \), etc., until an empty slot is found.  
     2. **Quadratic Probing**: If index \( i \) is occupied, try \( (i + 1^2) \mod m \), \( (i + 2^2) \mod m \), and so on.  
     3. **Double Hashing**: Use a second hash function \( h_2 \) to compute an offset, so you try \( i + h_2(key) \mod m \), \( i + 2h_2(key) \mod m \), etc.  
   - **Advantages**:  
     - Doesn’t require extra data structures.  
     - Often more cache-friendly (sequential memory).  
   - **Disadvantages**:  
     - Can suffer from clustering (especially with linear probing).  
     - More sensitive to the **load factor**: if the table is too full, performance can degrade.  



## Load Factor
The **load factor** (\(\alpha\)) in a hash table is defined as the ratio:
\[
\alpha = \frac{\text{Number of items in the table}}{\text{Size of the table}}
\]
- A **high load factor** means the table is relatively full, increasing the likelihood of collisions.  
- Many implementations **resize** (grow) the hash table when the load factor exceeds a certain threshold (e.g., 0.75).  



## Hash Data Structures in Java
Java provides several built-in implementations of hash-based data structures in the **java.util** package. The most common ones are:

1. **HashMap\<K, V\>**  
   - Stores **key-value** pairs.  
   - Uses **separate chaining** with a **linked list** or **tree bin** (in modern versions of Java) at each index for collision handling.  
   - Average-case time complexity of \(\mathcal{O}(1)\) for `get`, `put`, and `remove`. Worst-case \(\mathcal{O}(n)\) if all keys end up in the same bucket (though tree bins reduce worst-case in many scenarios).  

2. **HashSet\<E\>**  
   - Implements the **Set** interface using a `HashMap<E, Object>` internally.  
   - Stores **unique** elements only.  
   - Operations like `add`, `remove`, `contains` run in average \(\mathcal{O}(1)\).  

3. **LinkedHashMap\<K, V\>**  
   - Similar to `HashMap`, but maintains a **doubly-linked list** of the entries in insertion order.  
   - Good if you need to iterate in the same order that entries were inserted.  

4. **Hashtable\<K, V\>** (legacy class)  
   - Synchronized, older version of hash table; generally replaced by `ConcurrentHashMap` for thread-safety in modern code.  
   - Operations similar to `HashMap`, but default methods are thread-safe via synchronization.  

---

## Common Methods in Java’s HashMap

1. **`V put(K key, V value)`**  
   - Inserts the specified **key-value** pair into the map.  
   - If the key already exists, this method **overwrites** the old value and returns it.  
   - If the key does not exist, returns `null`.  
   - **Time Complexity**: Average \(\mathcal{O}(1)\).

2. **`V get(Object key)`**  
   - Returns the value associated with the specified key, or `null` if the key is not found.  
   - **Time Complexity**: Average \(\mathcal{O}(1)\).

3. **`V remove(Object key)`**  
   - Removes the entry for the specified key if it is present.  
   - Returns the value that was removed, or `null` if the key wasn’t present.  
   - **Time Complexity**: Average \(\mathcal{O}(1)\).

4. **`boolean containsKey(Object key)`**  
   - Checks if the map contains the given **key**.  
   - **Time Complexity**: Average \(\mathcal{O}(1)\).

5. **`boolean containsValue(Object value)`**  
   - Checks if the map contains one or more **keys** mapped to the given **value**.  
   - Potentially needs to scan over entries.  
   - **Time Complexity**: Can be \(\mathcal{O}(n)\) in the worst case, because it may require scanning all buckets.

6. **`int size()`**  
   - Returns the number of **key-value** pairs in the map.  
   - **Time Complexity**: \(\mathcal{O}(1)\).

7. **`void clear()`**  
   - Removes **all** entries from the map.  
   - **Time Complexity**: \(\mathcal{O}(n)\) since it must clear the internal structure.

8. **`boolean isEmpty()`**  
   - Checks if the map contains **no** key-value pairs.  
   - **Time Complexity**: \(\mathcal{O}(1)\).

<br/>

## Example of Using a HashMap in Java

```java
import java.util.HashMap;

public class HashMapExample {
    public static void main(String[] args) {
        // Create a HashMap to store student ID and their names
        HashMap<Integer, String> studentMap = new HashMap<>();

        // Insert some key-value pairs into the HashMap
        studentMap.put(101, "Alice");
        studentMap.put(202, "Bob");
        studentMap.put(303, "Charlie");

        // Retrieve a value by key
        String name = studentMap.get(101);  // "Alice"
        System.out.println("Student with ID 101: " + name);

        // Check if a key exists
        if (studentMap.containsKey(202)) {
            System.out.println("Key 202 is present in the map.");
        }

        // Remove a key-value pair
        String removedName = studentMap.remove(202);
        System.out.println("Removed student: " + removedName);

        // Check the size of the map
        System.out.println("Size of the map: " + studentMap.size());

        // Check if the map is empty
        System.out.println("Is map empty? " + studentMap.isEmpty());
    }
}
```
<br/>

## Time Complexity Review
- **Hash-based data structures** typically offer **\(\mathcal{O}(1)\)** average-case complexity for:
  - **Search** (e.g., `get` for a HashMap, `contains` for a HashSet)  
  - **Insert** (e.g., `put` in a HashMap, `add` in a HashSet)  
  - **Delete** (e.g., `remove` in a HashMap or HashSet)  
- **Worst-case** time complexity can degrade to \(\mathcal{O}(n)\) if many keys end up in the same bucket or if you have a pathological hash function. However, **good hash functions** and **resizing** strategies typically prevent this scenario from being common.

