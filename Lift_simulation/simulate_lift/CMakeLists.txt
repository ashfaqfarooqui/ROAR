cmake_minimum_required(VERSION 2.8.3)
project(simulate_lift)

## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
)

## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
 catkin_python_setup()
 catkin_package()

install(PROGRAMS src/simulate_lift/simulate_lift.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
   )

