### ROAD TRIP!

#### Design

* As traversing through the huge network of cities in US map is hard the traditional methods of Breadth First Search(BFS) 
  and Depth First Search(DFS) takes huge amount of time for planning out the route so, we come across the better version 
  by calculating the heuristic value and using A* Search.

* The state space in this case will be all possible routes from the source to destination.

* The successor function in this case will be the function which returns the intermediate cities of source city before 
  reaching destination and also which returns destination city.

* The edge weights are considered in the format g(s), the value of g(s) will be same to all the nodes on same level and 
  gets incremented by 1 after travelling to next node.

* The goal state will be the destination city.

* The heuristic value h(s) will be depending on the heuristic chosen in our case there are four heuristic functions
  (number of segments, number of miles, time taken and the probability of accident). In this case all the four heuristics 
  are admissible as the values are predefined in question itself and the values are never overestimated and are fixed.
  
#### Program Description

* The first step is loading road segments and we stored in a dictionary of dictionary format for easy access where the 
  first key is the start_city and the second key is end_city which consists of the values number of miles, speed limit 
  and the highway name

* After that we load the co-ordinates of the cities.

* We have four types of cost function number of segments, distance, time and safety so we wrote a function which returns 
  the cost value depending on the input we give.

* For calculating the distance between we the two cities we considered Euclidean method.

* Now for getting the route we defined an empty fringe and inserted initial state which has priority index value which 
  was calculated depending on the heuristic considered, route which is start_city, number of miles which is 0, number 
  of segments which is 0, number of accidents which is 0 and time taken which will be zero initially.

* So depending on the sum of heuristic value and cost function(g) and the destination that user has to go, the fringe gets 
  popped out of the priority queue and then the successor states get added to fringe and finally when we pop out the 
  destination from the fringe we will terminate the program and then return the output in the required format.

#### Problem Faced.
* Initially when we tried to import data from raw data files, we faced lot of difficulty on which data structure can give 
  us better results like whether to use dictionary or 2D-array or other.
* Among the 4 heuristic parameters given(time, segments, distance, safety), calculating segments took more efforts from 
  us compared to other three. 
