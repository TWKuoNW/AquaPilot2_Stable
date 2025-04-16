import cv2

video_path = "D:\\AquaPilot2_DemoVersion\\video_set\\shrimp_demo_2.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))  # 帧率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 宽度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 高度
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码器格式
output_path = "output_video0.mp4"
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 保存前三帧
frame_count = 0
while(True):
    ret, frame = cap.read()
    if not ret:  # 如果视频结束或出错
        print("视频帧不足")
        break
    if(frame_count ==1 or frame_count ==2 ):
        out.write(frame)  # 写入帧到输出文件

    print(frame_count)
    frame_count += 1

# 释放资源
cap.release()
out.release()

print(f"前三帧已保存到 {output_path}")
