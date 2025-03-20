# Greedy Algorithm

- __What is Greedy Algorithms[[Link](https://www.geeksforgeeks.org/introduction-to-greedy-algorithm-data-structures-and-algorithm-tutorials/?ref=outind)]__

- An algorithm builds up up a solution piece by piece
- Always choosing the next piece that offers the most obvious and immediate benefit

__This algorithm solve problem with following properties__
- `Greedy Choice Property`: The optimal solution can be constructed by making the best local choice at each step.
- `Optimal Substructure`: The optimal solution can be constructed by making the best local choice at each step.

__Characteristics__
- simple and easy to implement.
- efficient in terms of time complexity
- do not reconsider previous choices, make decisions based on current information without looking ahead

## How it Works
```text
1. Start with the initial state of the problem. This is the starting point from where you begin making choices.

2. Evaluate all possible choices you can make from the current state. Consider all the options available at that specific moment.

3. Choose the option that seems best at that moment, regardless of future consequences. This is the “greedy” part – you take the best option available 
now, even if it might not be the best in the long run.

4. Move to the new state based on your chosen option. This becomes your new starting point for the next iteration.

5. Repeat steps 2-4 until you reach the goal state or no further progress is possible. Keep making the best local choices until you reach the end of the 
problem or get stuck.
```

__Example__
Let’s say you have a set of coins with values `[1, 2, 5, 10]` and you need to give minimum number of coin to someone change for 39.

```text
The Greedy algorithm for making change would works as follow
    - Step-1: Start with the largest coin value that is less than or equal to the amount to be changed. In this case, the largest coin less than or 
    equal to 39 is 10.

    - Step- 2: Subtract the largest coin value from the amount to be changed, and add the coin to the solution. In this case, subtracting 10 from 39 
    gives 29, and we add one 10-coin to the solution.

```
Repeat steps 1 and 2 until the amount to be changed becomes 0.

```java
class GreedyEg { 

    static int minCoins(int[] coins, int amount) { 
        int n = coins.length;
        Arrays.sort(coins);
        int res = 0;

        for (int i = n - 1; i >= 0; i--) { 
            if (amount >= coins[i]) {
                // find the maximum number of ith coin we can use 
                int cnt = amount / coins[i];

                res += cnt;

                amount -= (cnt * coins[i]);
            }

            if (amount == 0)
                break;
        }
        return res;
    }

    public static void main(String[] args) { 
        int[] coins = {5, 2, 10, 1};
        int amount = 39;

        System.out.println(minCoins(coins, amount));
    }
}
```

## Greedy Algorithms General Structure[[Link](https://www.geeksforgeeks.org/greedy-algorithms-general-structure-and-applications/)]

__How to Identify Greedy Problems__

1. Can wen break the problem into smaller parts?
    - For example – In activity selection problem, once we have selected a activity then remaining subproblem is to choose those activities that start 
    after the selected activity.

2. Will Choosing the best option at each step lead to the best overall solution?
    - For example – In Dijkstra’s shortest path algorithm, choosing the minimum-cost edge at each step guarantees the shortest path.


__Difference between Greedy and Dynamic Programming__

1. Greedy algorithm works when the problem has `Greedy Choice Property` and `Optimal Substructure`. Dynamic Programming also works when a problem has optimal substructure but it also requires `Overlapping Subproblems`.

2. In greedy algorithm each local decision leads to an optimal solution for the `entire problem` whereas in dynamic programming solution to the main problem `depends on the overlapping subproblems`.


## Popular Greedy Alogrithms

- [Fractional Knapsack](#fractional-knapsack)
- Dijkstra's Algorithm
- Kruskal's Algorithm
- Huffman Coding
- Prim's Algorithm


### Fractional Knapsack[[Link](https://www.geeksforgeeks.org/fractional-knapsack-problem/)]

Given the weights and profits of N items, in the form of {profit, weight} put these items in a knapsack of capacity W to get the maximum total profit in the knapsack. In Fractional Knapsack, we can break items for maximizing the total value of the knapsack.

```text
Input: arr[] = {{60, 10}, {100, 20}, {120, 30}}, W = 50
Output: 240 
Explanation: By taking items of weight 10 and 20 kg and 2/3 fraction of 30 kg. 
Hence total price will be 60+100+(2/3)(120) = 240


Input:  arr[] = {{500, 30}}, W = 10
Output: 166.667
```

__Illustration:__
Check the below illustration for a better understanding:


Consider the example: __arr[] = {{100, 20}, {60, 10}, {120, 30}}, W = 50.__


Sorting: Initially sort the array based on the profit/weight ratio. The sorted array will be __{{60, 10}, {100, 20}, {120, 30}}.__


___Iteration:___


- For i = 0, weight = 10 which is less than W. So add this element in the knapsack. profit = 60 and remaining W = 50 – 10 = 40.
- For i = 1, weight = 20 which is less than W. So add this element too. profit = 60 + 100 = 160 and remaining W = 40 – 20 = 20.
- For i = 2, weight = 30 is greater than W. So add 20/30 fraction = 2/3 fraction of the element. Therefore profit = 2/3 * 120 + 160 = 80 + 160 = 240 and remaining W becomes 0.

So the final profit becomes 240 for W = 50.


Follow the given steps to solve the problem using the above approach:

- Calculate the ratio (profit/weight) for each item.
- Sort all the items in decreasing order of the ratio.
- Initialize __res = 0__, __curr_cap = given_cap__.
- Do the following for every item i in the sorted order:
    - If the weight of the current item is less than or equal to the remaining capacity then add the value of that item into the result
    - Else add the current item as much as we can and break out of the loop.
Return __res__.

__Implementation of the above approach(Python):__
```python
class Item:
    def __init__(self, val, wt):
        self.profit = val
        self.weight = wt

def fractional_knapsack(W, arr):
    arr.sort(key=lambda x: (x.profit/x.weight), reverse=True)

    # result
    res = 0.0

    for item in arr:
        # if adding item won't overflow, add it completely
        if item.weight <= W:
            res += item.profit
            W -= item.weight

        # if can't add current item, add fractional part of it
        else:
            fraction = W / item.weight
            res += item.profit * fraction
            break
    
    return res

if __name__ == "__main__":
    W = 50
    arr = [Item(60, 10), Item(100, 20), Item(120, 30)]
    max_val = fractional_knapsack(W, arr)
    print(max_val)

```
- Time Complexity: O(N logN)
- Auxiliary Space: O(N)

__Implementation of the above approach(Java):__
```java
import java.lang.*;
import java.util.Arrays;
import java.util.Comparator;

class FractionalKnapScak 
{

    static class ItemValue 
    { 
        int profit, weight;

        ItemValue(int val, int wt) { 
            this.weight = wt;
            this.profit = val;
        }
    }

    private static double getMaxValue(ItemValue[] arr, int capacity) 
    { 
        // sort items by profit/weight ratio:
        Arrays.sort(arr, Comparator<ItemValue>() {
            @Override
            public int compare(ItemValue item1, ItemValue item2) { 
                double cp1 = new Double((double)item1.profit / (double)item1.weight);
                double cp2 = new Double((double)item2.profit / (double)item2.weight);

                if (cp1 < cp2)
                    return 1;
                else
                    reutrn -1;
            }
        });

        double res = 0.0;

        for (ItemValue i : arr) { 
            int curWt = (int) i.weight;
            int curVal = (int) i.profit;

            if (capacity - curWt >= 0) {
                capacity -= curWt;
                res += curVal;
            }
            else { 
                double fraction = ((double)capacity / (double)curWt)
                res += (curVal * fraction);
                capacity = (int)(capcaity - (curWt * fraction));
                break;
            }
        }
        return res; 
    }

    static void main(String[] args) 
    {
        ItemValue[] arr = { new ItemValue(60, 10),
                            new ItemValue(100, 20),
                            new ItemValue(120, 30) };
 
        int capacity = 50;
 
        double maxValue = getMaxValue(arr, capacity);
 
        // Function call
        System.out.println(maxValue);
    }
}
```


### Dijkstra’s Algorithm[[Link](https://www.geeksforgeeks.org/introduction-to-dijkstras-shortest-path-algorithm/)]

- A popular algorithm for solving many single-source shortest path problems having non-negative edge weight in the graphs.
- It is to find the shortest distance between two vertices on a graph

__Pseudo code__:
```text
function Dijkstra(Graph, source):
   // Initialize distances to all nodes as infinity, and to the source node as 0.

    distances = map(all nodes -> infinity)

    distances = 0

   // Initialize an empty set of visited nodes and a priority queue to keep track of the nodes to visit.
   visited = empty set
   queue = new PriorityQueue()
   queue.enqueue(source, 0)

   // Loop until all nodes have been visited.
   while queue is not empty:
       // Dequeue the node with the smallest distance from the priority queue.
       current = queue.dequeue()


       // If the node has already been visited, skip it.
       if current in visited:
           continue


       // Mark the node as visited.
       visited.add(current)


       // Check all neighboring nodes to see if their distances need to be updated.
       for neighbor in Graph.neighbors(current):
           // Calculate the tentative distance to the neighbor through the current node.
           tentative_distance = distances[current] + Graph.distance(current, neighbor)


           // If the tentative distance is smaller than the current distance to the neighbor, update the distance.
           if tentative_distance < distances[neighbor]:
               distances[neighbor] = tentative_distance


               // Enqueue the neighbor with its new distance to be considered for visitation in the future.
               queue.enqueue(neighbor, distances[neighbor])


   // Return the calculated distances from the source to all other nodes in the graph.
   return distances
```

### Code Implementation
```python
import heapq

def dijkstra(V, adj, S):
    # initialize distance array with infinity and source distance as 0
    dist = [float('inf')] * V
    dist[S] = 0

    # min-heap to process node
    pq = [(0, S)] # (distance, node)

    while pq:
        current_distance, node = heapq.heappop(pq)
        
        # if processed before with a smaller distance, skip
        if current_distance > dist[node]:
            continue

        # explore neighbors
        for neighbor, weight in adj[node]:
            new_distance = current_distance + weight

            # Update if a shorter path is found
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    return dist  # Shortest distances from source to all nodes

def main():
    V = 6  # Number of vertices
    edges = [(0, 3, 9), (0, 5, 4), (1, 4, 4), (2, 5, 10), (4, 5, 3)]
    
    # Create adjacency list
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))  # Since it's an undirected graph

    S = 1  # Source node

    result = dijkstra(V, adj, S)
    print(result)

if __name__ == "__main__":
    main()
```