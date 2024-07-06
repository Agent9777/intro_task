
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/srv/spawn.hpp"
#include "turtlesim/msg/pose.hpp"
#include <memory>
#include <chrono>
#include<cmath>

class CircleDrawer : public rclcpp::Node
{
public:
    CircleDrawer()
        : Node("circle_drawer")
    {
        //for turtle1 
        cmd_vel_publisher_= this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        pose_subscriber_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose", 10, std::bind(&CircleDrawer::poseCallback, this, std::placeholders::_1));
        drawCircle(1.0,2.0);
        //spawning the turtle and changing the controlto turtle2
        cmd_vel_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle2/cmd_vel", 10);
        pose_subscriber_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle2/pose", 10, std::bind(&CircleDrawer::poseCallback, this, std::placeholders::_1));
        spawnTurtle(turtle_posx,turtle_posy);
        drawCircle(1.0,-1.8);    
    }

private:
    double turtle_posx=0;
    double turtle_posy=0;
    double turtle_pos_theta=0;

    void drawCircle(double linear_vel_x,double angular_vel)
    {
        geometry_msgs::msg::Twist cmd_vel;
        cmd_vel.linear.x = linear_vel_x;
        cmd_vel.angular.z = angular_vel; 
        cmd_vel_publisher_->publish(cmd_vel);
        //calculating the circle time duration
        double circle_duration=sqrt(pow((6.28/angular_vel),2));
        auto stop_time = std::chrono::steady_clock::now() + std::chrono::duration<double>(circle_duration);
        while (rclcpp::ok() && std::chrono::steady_clock::now() <= stop_time) {
            cmd_vel_publisher_->publish(cmd_vel);
        }
        cmd_vel.linear.x = 0.0;
        cmd_vel.angular.z = 0.0;
        cmd_vel_publisher_->publish(cmd_vel);

        RCLCPP_INFO(this->get_logger(), "Turtle finished drawing circle.");
        
    }
    void spawnTurtle(double x,double y){
        auto client = this->create_client<turtlesim::srv::Spawn>("/spawn");
        auto request = std::make_shared<turtlesim::srv::Spawn::Request>();
        request->x = x;
        request->y = y;
        request->name = "turtle2";

        auto result = client->async_send_request(request);
        RCLCPP_INFO(this->get_logger(), "Turtle2 Spawned!");
    }

    void poseCallback(const turtlesim::msg::Pose::SharedPtr msg)
    {
        //to track the position of turle for spawning the second turtle 

        turtle_posx=msg->x;
        turtle_posy=msg->y;
        turtle_pos_theta=msg->theta;



    
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscriber_;
    
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CircleDrawer>());
    rclcpp::shutdown();
    return 0;
}
