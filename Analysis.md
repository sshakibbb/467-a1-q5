# Group 16 Assignment 1 Question 5 in CP467
### Written answers which are also included in our PDF submission.

<br>

**Selection and explanation of h3**

In our A* algorithm approach for the 8-puzzle, we decided to utilize Chebyshev Distance as our third heuristic. We decided to pick this one as we were curious in observing the efficiency improvements over Hamming and Manhattan heuristics mentioned in the research paper provided by the professor.

The heuristic is implemented by taking double the summation of the Chebyshev Distance calculated on all states progressively, in comparison to the goal state. It’s similar to the Manhattan Distance implementation, but comes with a very notable improvement. The formula for this can be denoted as the following:

(equation is better written out in katex in our PDF submission, but here it is):
h3 = 2 * summation of (max (| x_k - x_kg |, | y_k - y_kg |))

x_k and y_k represent the current horizontal and vertical states, and x_kg and y_kg represent the horizontal and vertical goal states. We can see that the distance from goal to current state is being measured for both horizontal and vertical dimensions, and the maximum of either is being taken for each summation. After all the summations are done, we double our result to achieve the heuristic’s final value.

There are a couple of interesting observations we discovered regarding this heuristic. Firstly, we implemented it without the multiplier of 2 at the beginning, and found that it did not perform as well as Manhattan Distance. After further research in the article, we realized this is because although in Manhattan Distance we are also measuring distance between current and goal states, it will not necessarily be a smaller sum than Chebyshev Distance unless the latter is doubled. The following formula from the research paper describes this relationship:

a + b <= 2 * max(a,b) and we can see it hold in some examples: 
3+3 <= 2*(3), the closest the left side of the equation can be to the right side
2+3 <= 2*(3), every other instance, where left side is less than right side

This means that by doubling the Chebyshev Distance’s result, we always achieve a more dominant function. This was reflected in our space complexity observations, where Manhattan Distance took about 1500 node expansions, Chebyshev took 5400, and Chebyshev doubled took about 1200.

<br>

**Analysis of heuristic functions**

We can observe sample output (attached also in doc) for implementation of the A* algorithm using our three heuristics. While observing these across 100 different puzzles, we can look at the averages that were computed above and make a couple observations. Heuristic 3, which was the modified Chebyshev Distance method, had the lowest number of average nodes expanded, giving us the best efficiency in space complexity. 

We know this was the result for a couple of reasons, with the main advantage being the mathematical advantage in the doubled Chebyshev Distance heuristic which ensures it is dominant over Manhattan Distance. 

As mentioned above, we know that a + b <= 2 * max(a,b) holds true for all cases and thus by doubling Chebyshev Distance in our h3 implementation we can see that it had the 23.37 average steps to the solution and the lowest number of average nodes expanded (1189.71) across the 100 8-puzzle runs. 

And so in second place we had Manhattan Distance, with about 22.75 average steps to the solution and 1735.44 average nodes expanded. Lastly, we have the Misplaced Tiles heuristic, which performed significantly worse than the other two with 14,490.21 average nodes expanded. This heuristic alone made our A* algorithm run longer than the others and we had to take various measures to make sure our implementation of the search algorithm itself was efficient enough to run this heuristic reasonably. Overall, this heuristic was not smart or efficient enough in pruning trees early on and it struggles to find out what moves look better than others as it can’t work off of a distance metric like Manhattan and Chebyshev do.
