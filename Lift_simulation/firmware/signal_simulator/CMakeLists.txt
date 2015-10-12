cmake_minimum_required(VERSION 2.8.3)

include_directories(${ROS_LIB_DIR}
    ${catkin_INCLUDE_DIRS})


generate_arduino_firmware(signalSimulator
  SRCS signalSimulator.cpp ${ROS_LIB_DIR}/time.cpp ros.h
  BOARD uno
  PORT /dev/ttyACM0
)