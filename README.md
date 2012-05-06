Python-AI-Robots
================

AI techniques for autonomous actions and events that simulate Autonomous Robots collaborating in a dynamic environment to achieve certain goals while working cooperatively and competitively.

Requirements
================
Download and Install the following:
<ul>
<li><a href="http://www.panda3d.org">Panda 3D</a></li>
<li><a href="http://www.python.org">Python</a></li>
</ul>

Running the Program
================

To run your program on Windows or Mac, enter the following in a terminal (command prompt):

ppython main.py

To run it on GNU/Linux, enter the following in a terminal:

python main.py

Description
================

The game involves an autonomous number of nodes in a spatially defined space that move around and play the game “Tag”. The purpose of this game is that a defined node or “seeker” tries to chase other nodes in an attempt to touch or “tag” one of them and thus making that node the “seeker” and itself becoming a normal node again. The nodes try to escape the “seeker” if the “seeker” is chasing them. The game does
on indefinitely.

Current Progress
================

Introducing Kalman Filters and Particle Filters for Robot Localization. A* and Dynamic Programming algorithms for optimal path finding. PID COntroller with path smoothing and CTE Calculation for improving paths. As well as introducing Twiddle (aka Coordinate Ascent) to find good Control Gains for PID controller. 
Work is also being done adding SLAM algorithm in particular Graph SLAM for Simultaneous Localization and Mapping to build 2-D or 3-D maps.

Try and introduce all these algorithms on the robots in the game in order to make them autonomous.
These algorithms are also used to program self-driving cars.


Finite State Machines
=====================

Each robot or node would have its own Finite State Machine depending on its role in the game. (Seeker, Leader, Weak Member, etc..). A robot can be in any of those states, and each state would define its actions and the next possible actions, events, and states it can be in. The states of each node are the following:

<ul>
<li>The “Im_it” state is the state where the node is itself the seeker.</li>

<li>The “Im_not_it” state is the state for all the other nodes that is not the seeker.</li>

<li>The “Im_out” state which is a temporary state for when a node has just got done tagging another node.</li>

<li>The “step” state is when it puts the node that was before seeking back in the game after 1 second.</li>

<li>The “iAmAleader” state is when a node is assigned as a leader that uses an intelligent strategy to avoid seekers and for the followers to follow.</li>

<li>The “setLeader” state is to assign a node as the weak member to find a leader to follow.</li>
</ul>

AI Behavior
=====================

Found in main.py

<ul>
<li><b><i>Wander: </i></b><span>The nodes move at a constant speed and do self-rotations. It is in the state “Im_not_it”. In the game the node will be highlighted in the color “blue”. Function: def _steerForWander(self,dt):</span></li>
<li><b><i>Evade: </i></b><span>If a node that is in a state of “Im_not_it” is approached by a certain distance by a node that is in the state “Im_it”, then it will interact with other nodes and start the evade process where it will move at a faster speed than the ‘Wander’ constant speed to run away from the “seeker”. If a node was approached by the seeker but then the seeker was seeking another node, then it will be in the state of ‘Evade’ but switch back to the “Wander” state. In the game the node will be highlighted in the color “blue”. Function: def _steerForFlee(self,dt)</span></li>
<li><b><i>Seek: </i></b><span>The node that is in the state of “Im_it” generally is in the ‘SEEK’ behavior. Here the node moves at a speed faster than the constant wander speed and interacts with other nodes based on their distance and which node to choose to seek and follow in order to tag. If the seeker finds another node closer to it while seeking then it reroutes its path and start seeking the other node. In the game the node will be highlighted in the color “red”. If it just got tagged, during that instant, it will turn from “blue” to “green” then to “red”. Function: def _steerForSeek(self,dt):</span></li>
<li><b><i>Herding: </i></b><span>The node that is in the state of “iAmALeader” generally is in the ‘WANDER’ behavior. Here the node moves at a constant speed and does self-rotations and interacts with the seekers based on their distance through the calculated nodepaths in order to evade them as best as possible. In the game the node will be highlighted in the color “pink”. If it just got tagged, during that instant, it will turn from “pink” to “green” then to “red”. The follower node in the state of “setLeader” is assigned as the weak member in order to find a leader. The node will be at a wander state. Once it approaches a leader, it will start following it in order to best avoid the seekers since the leader has a better strategy at evading seekers.</span></li>
</ul>

Constraints
=====================

There are many constraints that affect the game play.
The constraints of the behaviors are the following:

<ul>
<li>The node speed</li>
<li>The spatial boundary of the topology</li>
<li>The collision of nodes with other nodes</li>
<li>The time frame</li>
<li>The rotation of the nodes</li>
</ul>

Kalman Filter
=====================

Found in kalmanfilter.py

It is a popular technique for estimating the state of a system. Kalman filters
estimate a continuous state and gives a uni-modal distribution. In Kalman filters the distribution is given in what is called a Gaussian, which is a continuous
function over the space of locations. The area underneath the Gaussian adds up to one. It iterates two things: Measurement Updates (measurement cycle) and Motion Updates (prediction).

X=estimate, P=uncertainty covariance, F=state transition matrix, U=motion vector, Z=measurement, H=measurement function, R=measurement noise, I=identity matrix.

Here, the robot should use radars and lasers to estimate the distance and the velocity of other robots in the environment using a Kalman Filter where it uses the range data from the lasers and uses the state spaces of the relative distances and velocities.

Particle Filter
=====================

Found in particlefilter.py

Robot uses range sensors, i.e. sonar sensors (use uf sound), to range the distance of nearby obstacles. They help the robot determine a good posterior distribution as to where it is. The particles generates guess where the robot might be moving. The particles that are more consistent with the measurements are more like to survive. As such, places of high probability will collect more particles. The particles together give the approximate belief of the robot as it localizes itself.

A* search algorithm
=====================

Found in alltogether.py

Used for path finding. It does the minimum amount of work necessary to make the maximum progress towards the goal. It uses a heuristic function, which is a function that has to be set up, though it doesn't have to be accurate. The heurisitic function has to be a function that helps you to find out where to search next int he case of ties, and it has to be just so that it underestimates, or at best equal the true distance from the goal.
The Robots, or self-driving cars, uses a function like this to solve free-form navigation problems. It boils down to the distance to a target location, not to the number of grid cell steps.

Dynamic Programming
=====================

Found in dynamicprog.py

It is an alternative method for planning. It will find the shortest path like A*. Given a map and one or more goal positions, it will output the best path from any possible starting location. It is not limited to one starting location, but from any starting location. It will give us an optimum action (called policy) to perform for every navigable grid. For example, when you run it, the output shows the grid overlaid with directional arrows representing the optimum policy for each location. 

Smoothing
=====================

Found in alltogether.py

Algorithm to generate smooth paths for actual Robot Motion. This will help the robot move smoothly and fast, rather than taking 90-degree turns within the grid cells and move really slowly around corners.

PID Control
=====================

Found in alltogether.py

If the robot is a car with steerable front axle and two non-steerable wheels in the back, you will want the car to drive along the reference trajectory which is a portion of the output of the smoother. Therefore the steering angle of the car is set which makes it challenging to make it follow the reference trajectory. And this is where the PID control comes in.

P controller, where P stands for proportional. This is because you steer in proportion to the ststem error, the cross-track error (CTE)

The PD controller helps avoid the overshoot to stop the car from oscillating. It is not just related to CTE but also to the time derivative of the CTE. This means that when the car has turned enough to reduce the CTE, it will not just go on trying to reach the x-axis but will notice that it has already reduced the error. The error becomes smaller over time. Eventually, the car counter-steers, namely steers up again. This allows the car to gracefully approach its target trajectory.

The PID controller tries to solve the systematic bias. It is if the front wheels of the car are not 100% properly aligned, it will cause a big CTE. Thus if the car is moving toward a trajectory far away from the goal, and over a long epriod of time it is not getting closer, you will have to steer more to compensate for the bias. So in order to recognize the sustained bias, you will have to measure it by adding up the CTE errors over time.

Twiddle
=====================

Found in alltogether.py

The Twiddle algorithm is used to determine the optimal parameters (also knows as control gains) to use in the PID controller.

SLAM
=====================

Found in slam.py and onlineslam.py

The Graph SLAM algorithm is used for Simultaneous Localization and Mapping to build 2-D or 3-D maps. This is an on-going research topic. It is used in the Google Self-Driving Car. It will use localization and mapping to create a 2-D or 3-D map of the environment to know where it is and where and how it should navigate to.

Thank You
=====================

Special thanks to Dr. Sebastian Thrun for sharing and teaching us his amazing work on self-driving cars!
Take the CS373: Programming a Robotic Car course with him on <a href="http://www.udacity.com">Udacity!</a> Its free!