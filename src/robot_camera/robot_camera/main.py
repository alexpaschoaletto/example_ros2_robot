import cv2                                      # OpenCV
import mediapipe as mp                          # biblioteca extra do Google para o openCV
from cv_bridge import CvBridge                  # camada de tradução OpenCV <--> ROS2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image               # formato de mensagens de imagem no ROS2
from geometry_msgs.msg import Twist

source = 'http://192.168.1.218'                 # endereço IP (ou 0 para webcam)
renderer = mp.solutions.drawing_utils
pose_handler = mp.solutions.pose
pose = pose_handler.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


class CameraNode(Node):
    def __init__(self):
        super().__init__('robot_camera')

        self.direction = 1.0
        self.camera_publisher = self.create_publisher(Image, '/camera', 1)
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 5)

        self.camera = cv2.VideoCapture(source)
        if not self.camera.isOpened():
            self.get_logger().error(f'FAILED to get video from {source}')
            rclpy.shutdown()
        
        self.timer = self.create_timer(0.01, self.process)
        self.timer = self.create_timer(1, self.control)
        self.bridge = CvBridge()


    def process(self):
        ret, frame = self.camera.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                joints = results.pose_landmarks.landmark

                # seu código vem AQUI

                # joints contém as coordenadas [x, y]
                # normalizadas para o tamanho da câmera.
                # sabendo as coordenadas de cada junta,
                # podemos determinar o ângulo de cada
                # uma e com isso determinar a posição da pessoa.

                # joints[12] --> ombro direito
                # joints[14] --> cotovelo direito
                # joints[16] --> punho direito

                # joints[11] --> ombro esquerdo
                # joints[13] --> cotovelo esquerdo
                # joints[15] --> punho esquerdo

                # se precisar: https://logessiva.medium.com/an-easy-guide-for-pose-estimation-with-googles-mediapipe-a7962de0e944

                # esta linha apenas visualiza a detecção
                # do ser humano, pode retirar daqui se quiser
                renderer.draw_landmarks(image, results.pose_landmarks, pose_handler.POSE_CONNECTIONS)
            except:
                # caímos aqui quando nenhum
                # humano é detectado
                pass
            finally:
                image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_NEAREST)
                msg = self.bridge.cv2_to_imgmsg(image, encoding='bgr8')
                self.camera_publisher.publish(msg)
        else:
            self.get_logger().error('FAILED to capture image')


    def control(self):
        msg = Twist()
        msg.linear.x = self.direction
        self.direction = -self.direction
        self.cmd_vel_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.camera.release()
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
