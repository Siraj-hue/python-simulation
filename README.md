# python-simulation
Python3 / Pygame pandemic simulation SIR model

This is an pandemic simulation using SIR model made with Python 3 and Pygame. All the code for the simulation is in the file corona_main. The code can be directly used after downloading pygame and pylab. Simulation is inspired from the video of 3Blue1Brown called "Simulating an epidemic". The simulation can be configured for the inteded usage. It has 4 different modes which are normal, common place, communites, and air transportation simulations. User can play with the modes and see how do certain situtaions affect the spread of the disease. User can also change the parameters such as speed of the people, infection probability, infection radius, removal time etc... At the end of the simulations, graphs pop up. Those graphs show necessary information about the history of the virus like the infected person and basic reproduction number(R nought) over time. 

The blue squares represents susceptibles and red ones represent infected population. After a certain amount of time, those infected will be turn gray meaning that they are removed and can not spread the virus. 

In the air transportation mode, green lines are the path the person can go from. The magenta squares represents infected passenger and turquoise susceptible passenger.

The parameters of the simulation can be changed from the variables in the begininng of the runSimulation and communitySimulation functions. 

WARNING: The simulation might freeze in the middle of it. Try re-running it.

ps: Any advices regarding imporvment of the simulation would be aprreciated. 
