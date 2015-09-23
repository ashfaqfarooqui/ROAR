# Simulation environment for ROAR
========

###Folder structure

__ROAR_msgs__ contains the message files required for the working of the application. **Event.msg** is used by the **controller_bridge** node that will be an interface between the triggered sequence events to the simulation environment.

__controller_bridge__ this folder contains the node program that will be an interface between the web based **Explorer** to the simulation environment. It continuouslly listens to any triggered events and provides the same to the simulator.

__roar_sim__ folder contains the launch files and __Rviz__ configuration files for the project.

__roar_bringup__ contains the core code that runs the simulator. It aslo a JSON config file that is used to generate bins,robot and truck at specified positions.

###Running the code

To run the code, first make sure the progam is installed using catkin_make or catkin_make_isolated and the correct workspace is sourced.

To run the simulator first run the __Explorer__ in one terminal and in another terminal window use the command 

```roslaunch roar_sim roar_sim.launch```

This will start up all the required nodes to simulate the system.
If the explorer is running on a different system or on a port other than 8080, then hostname and port need to be given as arguments with the name 'hostname' and 'port'. Example:

```roslaunch roar_sim roar_sim.launch hostname:="0.0.0.0" port:= "1111"```

##Event syntax
The current simulation allows four different operations.
1. moveTo
2. attachBin
3. dettachBin
4. emptyBin

The syntax to use these operations is: "<Object performing the task>\_<Task to perform>\_< object on which operation must be performed>"

for example:
```Robot1_moveTo_Bin1``` here _Robot1_ would perform the operation, _moveTo_ is the operation that is performed and _Bin1_ is the object on which the operation is performed. In our case _Bin1_ specifies the position of _Bin1_ as defined in the [config](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task1/roar_bringup/src/roar_bringup/config.json) file, and not the current position of the bin. Names _Robot1_ and _Bin1_ correspond to the names provided in the [config](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task1/roar_bringup/src/roar_bringup/config.json) file.

Opperation _moveTo_, _attachBin_ and _dettachBin_ can be performed by the robots. Operation _emptyBin_ can be performed by the truck only.