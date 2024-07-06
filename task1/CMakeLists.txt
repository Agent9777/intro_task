cmake_minimum_required(VERSION 3.5)
project(task1)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)

add_executable(drawing_circles src/drawing_circle.cpp)

#target_include_directories(drawing_circles PRIVATE

ament_target_dependencies(drawing_circles
  rclcpp
  geometry_msgs
  turtlesim
)

install(TARGETS
  drawing_circles
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()

