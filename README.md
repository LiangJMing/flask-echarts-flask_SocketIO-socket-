# flask-echarts-flask_SocketIO-socket-
  使用flask框架实现网页的二维曲线图的显示，通过socket服务器端发送包含曲线图各点坐标的txt文件，flask创建线程接收txt文件,通过flask_SocketIO更新前端图表的data数据。初次完成版，待改进。 运行步骤： 先运行server_test 再运行falsk_socket 在server_test的窗口输入 post|boundaries1.txt 或post|boundaries2.txt 在路径 http://127.0.0.1:5000/test 显示不同的图
