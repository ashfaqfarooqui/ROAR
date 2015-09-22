# Simulation environment for lift meovement
=====
##Running the code

To start up all nodes run:

```roslaunch roar_lift_sim sim_lift.launch```

##Tweaking the physical setup

To make changes to the physical dimensions of the system the [URDF](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/roar_lift_sim/urdf/lift.urdf) files needs to be modified accordingly. Maximum and minimum joint movements need to be defined in the URDF as well as [here](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/simulate_lift/src/simulate_lift/simulate_lift.py)

To change the position and orientation of the camera, the transform with respect to the base_link should be defined  in the [launch](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/roar_lift_sim/launch/sim_lift.launch#L10) file.
The format to specify tf is: ```static_transform_publisher x y z yaw pitch roll frame_id child_frame_id period_in_ms```

##Making the lift move
The movement of the lift is made as an [action server](http://wiki.ros.org/actionlib) in ROS. It can be moved by providing a goal as "up" or "down". The action message is available [here](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/lift_msgs/action/LiftMovement.action), and can be modified to suit the needs of the client. A simple client can be created following this [example](http://wiki.ros.org/actionlib_tutorials/Tutorials/Writing%20a%20Simple%20Action%20Client%20%28Python%29), where the action server is named: **LiftMovementActionServer**.
