cmake_minimum_required(VERSION 2.8.3)
project(roar_bringup)

## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
)

## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
 catkin_python_setup()
 catkin_package()


install(PROGRAMS src/roar_bringup/bringup.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
   )


install(FILES src/roar_bringup/config.json
   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
   )