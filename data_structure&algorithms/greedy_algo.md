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

        for (int i = n - 1; i >= 0; i++) { 
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
