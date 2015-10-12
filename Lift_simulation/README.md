# Simulation environment for lift movement
=====

##Installing drivers for kinect
Drivers bundled with source are not always perfect and may not be updated, hence its best to install from source. Kinect uses [libfreenect](https://github.com/OpenKinect/libfreenect) drivers.

To install the drivers first uninstall preexisitng drivers that may be outdated using:
```sudo apt-get remove libfreenect*``` 
**Warning: This will remove a number of additional packages that depend on libfreenect. Make sure to reinstall them after completing the setup**

Then fetch and build the drivers from source using the following commands:
```
sudo apt-get install git-core cmake freeglut3-dev pkg-config build-essential libxmu-dev libxi-dev libusb-1.0-0-dev
git clone https://github.com/OpenKinect/libfreenect
cd libfreenect
mkdir build
cd build
cmake -L ..
make
sudo make install
sudo ldconfig /usr/local/lib64/
```
To test and see if the installation was a success run: ```sudo freenect-glview```, this should open up a window showing the depth camera view.

To use the kinect in non-sudo mode do: ```sudo adduser $USER video```

You may also need a udev rules file to access the camera, create a file using ```sudo nano /etc/udev/rules.d/51-kinect.rules```
and paste the following text into it:

```
 # ATTR{product}=="Xbox NUI Motor"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02b0", MODE="0666"
 # ATTR{product}=="Xbox NUI Audio"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02ad", MODE="0666"
 # ATTR{product}=="Xbox NUI Camera"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02ae", MODE="0666"
 # ATTR{product}=="Xbox NUI Motor"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02c2", MODE="0666"
 # ATTR{product}=="Xbox NUI Motor"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02be", MODE="0666"
 # ATTR{product}=="Xbox NUI Motor"
 SUBSYSTEM=="usb", ATTR{idVendor}=="045e", ATTR{idProduct}=="02bf", MODE="0666" 
 ```

Be sure to logout then back in to see the changes take affect, restarting the system would also be recommended.
For additional help on installing drivers can be found [here](https://github.com/OpenKinect/libfreenect) and [here](http://openkinect.org/wiki/Getting_Started#Ubuntu_Manual_Install).

##Running the code

To start up all nodes run:

```roslaunch roar_lift_sim sim_lift.launch port:=/dev/ttyACMX``` (where X is the port arduino is connected to, read below)

##Tweaking the physical setup

To make changes to the physical dimensions of the system the [URDF](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/roar_lift_sim/urdf/lift.urdf) files needs to be modified accordingly. Maximum and minimum joint movements need to be defined in the URDF as well as [here](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/simulate_lift/src/simulate_lift/simulate_lift.py)

To change the position and orientation of the camera, the transform with respect to the base_link should be defined  in the [launch](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/roar_lift_sim/launch/sim_lift.launch#L10) file.
The format to specify tf is: ```static_transform_publisher x y z yaw pitch roll frame_id child_frame_id period_in_ms```

##Using the arduino to simulate lift
The current branch has code that uses an arduino to simulate the joystick control of the lift. The input is on A0 of the arduino. By providing +5V the lift moves up, GND will move the lift down and +.3V will hold the lift in its place. These values can be adjusted and modified in the [firmware code](https://github.com/ashfaqfarooqui/ROAR/blob/arduinoSim_devel/Lift_simulation/firmware/signal_simulator/signalSimulator.ino) and uploaded using arduino software. 

####Running the arduino node
Once the code is burnt on the arduino, running ```rosrun rosserial_python serial_node.py /dev/ttyACMX```, where X is the ACM port on which arduino is connected, will connect the arduino to the ROS network. This is already done in the [launch](https://github.com/ashfaqfarooqui/ROAR/blob/arduinoSim_devel/Lift_simulation/roar_lift_sim/launch/sim_lift.launch#L12) file. Running the launch file with the correct port value will suffice, ```roslaunch roar_sim_lift sim_lift.launch port:=/dev/ttyACMx```

##Making the lift move (If you plan not to use the arduino)
The movement of the lift is made as an [action server](http://wiki.ros.org/actionlib) in ROS. It can be moved by providing a goal as "up" or "down". The action message is available [here](https://github.com/ashfaqfarooqui/ROAR/blob/master/Task2/lift_msgs/action/LiftMovement.action), and can be modified to suit the needs of the client. A simple client can be created following this [example](http://wiki.ros.org/actionlib_tutorials/Tutorials/Writing%20a%20Simple%20Action%20Client%20%28Python%29), where the action server is named: **LiftMovementActionServer**.
