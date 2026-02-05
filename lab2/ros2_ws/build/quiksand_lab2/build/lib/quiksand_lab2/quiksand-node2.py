import rclpy

def main():

    #初始化

    rclpy.init()

   #创建节点

    node =rclpy.create_node("htlloword_py")

    #输出

    node.get_logger().info("hello world by python!")

    #释放资源

    rclpy.shutdown()



if __name__ == '__main__':

    main()
