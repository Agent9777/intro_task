cmake_minimum_required(VERSION 3.5)
project(task1)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)

# Add executable
add_executable(drawing_circles src/drawing_circle.cpp)

# Include directories
#target_include_directories(drawing_circles PRIVATE
#  ${geometry_msgs_INCLUDE_DIRS}
#  ${turtlesim_INCLUDE_DIRS}
#)

# Link the executable with ROS 2 libraries
ament_target_dependencies(drawing_circles
  rclcpp
  geometry_msgs
  turtlesim
)

# Install the executable
install(TARGETS
  drawing_circles
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files, if any
# install(DIRECTORY
#   launch
#   DESTINATION share/${PROJECT_NAME}/
# )

# Install Python scripts, if any
# install(PROGRAMS
#   scripts/my_script.py
#   DESTINATION lib/${PROJECT_NAME}
# )

# Install package.xml
ament_package()

