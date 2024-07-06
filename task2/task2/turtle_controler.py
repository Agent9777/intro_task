import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point,Twist,Pose
import time

class TurtleControl(Node):
    def __init__(self):
        super().__init__('Turtle_controler')
        self.ball_sub = self.create_subscription( Point, "/ball/screen_coordinates", self.turtle_mover,20)
        self.turtle_pub = self.create_publisher( Twist,"/turtle1/cmd_vel",20)
        self.turtle_pos=self.create_subscription( Pose,"/turtle1/pose", self.pose_callback,20)
        #default values
        self.turtle_pos_x=5.5
        self.turtle_pos_y=5.5

    def turtle_mover(self, point):

        #considering 1 unit of linear velocity travels 45pixels
        # calculationg the linear velocity to travel in 0.04sec(depend on camera heartz,here its sets to 25 hertz) 
        linear_vel_x=((point.x /45)-self.turtle_pos_x)/0.04
        linear_vel_y=((point.x /45)-self.turtle_pos_y)/0.04


        twist = Twist()
        twist.linear.x = linear_vel_x
        twist.linear.y = linear_vel_y
        twist.angular.z = 0.0
        #runing the turtle for 0.04sec
        start_time = time.time()
        while time.time() - start_time <=0.04:
            self.turtle_pub.publish(twist)
            time.sleep(0.01)
        
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        self.turtle_pub.publish(twist)
    
    def pose_callback(self, pose):
        #track turtle osition
        self.turtle_pos_x=pose.x
        self.turtle_pos_y=pose.y





def  main(args=None):
    rclpy.init(args=args)
    TurtleControlObject=TurtleControl()
    rclpy.spin(TurtleControlObject)
    TurtleControlObject.destroy_node()
    rclpy.shutdown()

if __name__== '__main__ ':
    main()
