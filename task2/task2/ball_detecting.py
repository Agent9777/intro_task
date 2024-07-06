import cv2
import rclpy
from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge
import numpy as np
from geometry_msgs.msg import Point, PointStamped
dist=lambda x1,y1,x2,y2 : (x1-x2)**2+(y1-y2)**2

class DetectingBall(Node):
    
    def __init__(self):
        super().__init__('Ball_Detecter')
        self.prevCircle=None


        self.camaraDeviceNumber=0
        
        self.camera=cv2.VideoCapture(self.camaraDeviceNumber)
        
        self.bridgeObject=CvBridge()
        
        self.topicNameFrames='topic_camera_image'
        
        self.queueSize=20
        self.publisher=self.create_publisher(Image,self.topicNameFrames,self.queueSize)
        self.periodComunication =0.04
        self.timer =self.create_timer(self.periodComunication,self.timer_callbackFunction)
        self.i=0
        self.screen_pub =self.create_publisher( Point,"/ball/screen_coordinates",20)
    def timer_callbackFunction(self):
        success,frame =self.camera.read()

        frame=cv2.resize(frame,(640,480),interpolation=cv2.INTER_CUBIC)

        if success==True:
            ROS2ImageMessage=self.bridgeObject.cv2_to_imgmsg(frame)
            self.publisher.publish(ROS2ImageMessage)
        self.i+=1
        openCVImage =self.bridgeObject.imgmsg_to_cv2(ROS2ImageMessage)
        
        grayFrame=cv2.cvtColor(openCVImage,cv2.COLOR_BGR2GRAY)
        blurFrame=cv2.blur(grayFrame,(13,13),0)
        
        circles=cv2.HoughCircles(blurFrame,cv2.HOUGH_GRADIENT,1.2,100,param1=80,param2=40,minRadius=50,maxRadius=200)
        #increase or decrease the param1 and param2 if it is either detecting random circles or not detecting circles
        #  -increase if detecting random circle
        #  -decrease if not detecting circle/ball

        if circles is not None:
            circles=np.uint16(np.around(circles))
            chosen=None
            for i in circles[0,:]:
                if chosen is None: chosen=i
                if self.prevCircle is not None:
                    if dist(chosen[0,chosen[1],self.prevCircle[0],self.prevCircle[1]])<=dist(i[0],i[1],self.prevCircle[0],self.prevCircle[1]):
                        chosen=i
            
            cv2.circle(frame,(chosen[0],chosen[1]),1,(0,100,100),3)
            cv2.circle(frame,(chosen[0],chosen[1]),chosen[2],(0,100,100),3)
            #algorithem used-houghcircle method 
            #video -  https://youtu.be/RaCwLrKuS1w?si=JR4qBAXUFHzOsP5m  for more detail
            prevCircle=chosen
            screen_point = Point()
            screen_point.x = float(chosen[0])
            screen_point.y = float(chosen[1])
            screen_point.z = 0.0
            self.screen_pub.publish(screen_point)
   

        cv2.imshow("camera video",frame)
        cv2.waitKey(1)

def  main(args=None):
    rclpy.init(args=args)
    DetectingBallObject=DetectingBall()
    rclpy.spin(DetectingBallObject)
    DetectingBallObject.destroy_node()
    rclpy.shutdown()

if __name__== '__main__ ':
    main()

        


