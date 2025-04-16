# This program is the original version workflow of the 'Shrimp Intestinal Tract Detection (SITD)' algorithm.
from ultralytics import YOLO
import cv2  
import numpy as np
from scipy.interpolate import splprep, splev
import scipy.interpolate as spi
from PIL import Image, ImageDraw, ImageFont
import threading

class AI_Fun():
    def __init__(self, file_name = "shrimp_demo_2"):
        self.red_point_length = 0 
        self.yellow_point_length = 0
        self.two_point_length = 0
        self.file_name = file_name
        threading.Thread(target=self.run, daemon = True).start() # 啟動 AI function
    def run(self):
        print(self.file_name)
        cap = cv2.VideoCapture(f'video_set\\{self.file_name}.mp4') 
        model = YOLO('models\\ShrimpModelV1.pt')  

        def nothing(x):
            pass

        cv2.namedWindow('Parameter Adjuster')
        cv2.resizeWindow('Parameter Adjuster', 830, 270)

        # Before Cropping
        cv2.createTrackbar('BeforeCropping:ImageSize', 'Parameter Adjuster', 22, 100, nothing)
        # After Cropping
        cv2.createTrackbar('AfterCropping:ImageSize', 'Parameter Adjuster', 400, 500, nothing)
        cv2.createTrackbar('AfterCropping:Blur', 'Parameter Adjuster', 7, 21, nothing)
        cv2.createTrackbar('AfterCropping:C.H.T.', 'Parameter Adjuster', 134, 255, nothing)
        cv2.createTrackbar('AfterCropping:C.L.T', 'Parameter Adjuster', 128, 255, nothing)

        cv2.createTrackbar('speed', 'Parameter Adjuster', 5000, 15000, nothing)
        
        origin_y, origin_x = 1080, 1920

        while(cap.isOpened()):
            ret, frame = cap.read()  # 讀取一幀
            if(not ret):
                break  # 如果無法讀取，跳出循環

            BC_ImageSize = cv2.getTrackbarPos('BeforeCropping:ImageSize', 'Parameter Adjuster')
            
            AC_ImageSize = cv2.getTrackbarPos('AfterCropping:ImageSize', 'Parameter Adjuster')
            AC_Blur = cv2.getTrackbarPos('AfterCropping:Blur', 'Parameter Adjuster')
            AC_canny_high_threshold = cv2.getTrackbarPos('AfterCropping:C.H.T.', 'Parameter Adjuster')
            AC_canny_low_threshold = cv2.getTrackbarPos('AfterCropping:C.L.T', 'Parameter Adjuster')
            
            speed_value = cv2.getTrackbarPos('speed', 'Parameter Adjuster')
            
            """
            數字處理，排除可能錯誤的參數
            """
            if(AC_Blur % 2 == 0):
                AC_Blur += 1  # 如果是偶數，則加1變成奇數
            if(speed_value == 0):
                speed_value += 1
            
            # 調整畫面的大小
            x = int(origin_x / 100 * BC_ImageSize)
            y = int(origin_y / 100 * BC_ImageSize)
            frame = cv2.resize(frame, (x, y))  
            
            # 定義銳化濾波器
            sharpening_filter = np.array([[0, -1, 0],
                                        [-1, 5, -1],
                                        [0, -1, 0]])

            # 應用銳化濾波器
            sharpening_frame = cv2.filter2D(frame, -1, sharpening_filter)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

            results = model([img])

            for result in results:
                sourceTensor = result.boxes.data
                data = sourceTensor.clone().detach().tolist()        
                formatted_data = [[int(value) if idx == None else round(value, 3) for idx, value in enumerate(inner_list)] for inner_list in data]
                confidence_list = [] # 信心度列表
                for i in range(len(formatted_data)):
                    x_min, y_min, x_max, y_max, _, cls_id = map(int, formatted_data[i]) # 取得物件的座標
                    _, _, _, _, conf, _ = map(float, formatted_data[i]) # 取得物件的信心度
                    confidence_list.append(conf) # 串聯信心度

                    if(cls_id == 0):
                        cv2.putText(frame, f'shrimp:{(conf*100):.2f}%', (x_min, y_min-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # 在物件上顯示可信度
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 1)  # 畫矩形框 
                # ============================================================= 
                if(confidence_list != []):   
                    max_confidence = max(confidence_list) # 找出最高信心度
                    max_confidence_index = confidence_list.index(max_confidence) # 找出最高信心度的index
                    x_min, y_min, x_max, y_max, _, _ = map(int, formatted_data[max_confidence_index]) # 取得物件的座標
                    cropped_region = sharpening_frame[y_min:y_max,x_min:x_max] # 切割出信心度最高的蝦
                    # 調整切出影像的大小
                    y, x, _ = cropped_region.shape
                    x = int(x / 100 * AC_ImageSize)
                    y = int(y / 100 * AC_ImageSize)
                    cropped_region = cv2.resize(cropped_region, (x, y))

                    # show_image = cv2.GaussianBlur(cropped_region, (3, 3), 2)
                    show_image = cv2.filter2D(cropped_region, -1, sharpening_filter)
                    
                    # SITD 演算法流程 input:frame output:Shrimp Intestinal Tract
                    SITD_gray = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
                    SITD_blur = cv2.GaussianBlur(SITD_gray, (AC_Blur, AC_Blur), 2)
                    SITD_canny = cv2.Canny(SITD_blur, AC_canny_low_threshold, AC_canny_high_threshold)
                    kernel = np.ones((3, 3), np.uint8)
                    # ========================================================================
                    dilated_image_1 = cv2.dilate(SITD_canny, kernel, iterations=1) # 執行膨脹操作
                    blur_1 = cv2.blur(dilated_image_1, (5, 5)) # 模糊
                    eroded_image_1 = cv2.erode(blur_1, kernel, iterations=1) # 執行侵蝕操作
                    sharpening_1 = cv2.filter2D(eroded_image_1, -1, sharpening_filter)
                    # ========================================================================

                    # ========================================================================
                    height, width = sharpening_1.shape # 獲取圖像
                    mid_row = height // 2 # 計算中間行數

                    # 切割圖像
                    upper_half = sharpening_1[:mid_row, :]  # 上半部
                    lower_half = sharpening_1[mid_row:, :]   # 下半部

                    # 顯示結果
                    #cv2.imshow('Upper Half', upper_half)
                    #cv2.imshow('Lower Half', lower_half)


                    # ========================================================================
                    SITD_contours_upper, _ = cv2.findContours(upper_half, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                    SITD_contours_lower, _ = cv2.findContours(lower_half, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                    if not SITD_contours_upper:
                        print("No contours found.")
                    else:
                        max_contour = max(SITD_contours_upper, key=cv2.contourArea) # 獲取最大輪廓
                        max_contour = max(SITD_contours_upper, key=cv2.contourArea) # 獲取最大輪廓
                        # 找到輪廓中最遠的兩個點
                        max_dist = 0
                        point1 = point2 = None

                        for i in range(len(max_contour)):
                            for j in range(i+1, len(max_contour)):
                                dist = np.linalg.norm(max_contour[i] - max_contour[j])
                                if dist > max_dist:
                                    max_dist = dist
                                    point1, point2 = max_contour[i], max_contour[j]
                        
                        
                        # 轉換點為 (x, y) 坐標
                        point1 = list(point1[0])
                        point2 = list(point2[0])

                        up1, up2 = point1, point2

                        # 繪製最遠的兩個點
                        cv2.circle(show_image, point1, 3, (0, 0, 255), -1)
                        cv2.circle(show_image, point2, 3, (0, 0, 255), -1)

                    if not SITD_contours_lower:
                        print("No contours found.")
                    else:
                        max_contour = max(SITD_contours_lower, key=cv2.contourArea) # 獲取最大輪廓
                        # 找到輪廓中最遠的兩個點
                        max_dist = 0
                        point1 = point2 = None

                        for i in range(len(max_contour)):
                            for j in range(i+1, len(max_contour)):
                                dist = np.linalg.norm(max_contour[i] - max_contour[j])
                                if dist > max_dist:
                                    max_dist = dist
                                    point1, point2 = max_contour[i], max_contour[j]

                        # 轉換點為 (x, y) 坐標
                        point1 = list(point1[0])
                        point2 = list(point2[0])

                        upper_half_height, upper_half_width = upper_half.shape
                        point1[1] += upper_half_height
                        point2[1] += upper_half_height

                        dp1, dp2 = point1, point2
                        
                        # 繪製最遠的兩個點
                        cv2.circle(show_image, point1, 3, (0, 255, 255), -1)
                        cv2.circle(show_image, point2, 3, (0, 255, 255), -1)
                    # ====================================================================================
                    # 創建一個黑色的畫布
                    height, width = 250, 180
                    information_frame = np.zeros((height, width, 3), dtype=np.uint8)
                    pil_information_frame = Image.fromarray(information_frame)
                    # 設定要顯示的資訊

                    up1 = np.array(up1)
                    up2 = np.array(up2)
                    dp1 = np.array(dp1)
                    dp2 = np.array(dp2)

                    u_distance = cv2.norm(up2 - up1)
                    d_distance = cv2.norm(dp2 - dp1)
                    self.two_point_distance = cv2.norm(dp1 - up2)

                    self.red_point_length = f"紅點長度:{u_distance:.0f}px"
                    self.yellow_point_length = f"黃點長度:{d_distance:.0f}px"
                    self.two_point_length = f"間距:{self.two_point_distance:.0f}px"
                    draw = ImageDraw.Draw(pil_information_frame)
                    font = ImageFont.truetype("msjh.ttc", 16)
                    draw.text((10, 10), self.red_point_length, font=font, fill=(255, 255, 255))
                    draw.text((10, 40), self.yellow_point_length, font=font, fill=(255, 255, 255))
                    draw.text((10, 70), self.two_point_length, font=font, fill=(255, 255, 255))
                    information_frame = np.array(pil_information_frame)
                    # ====================================================================================

            cv2.imshow('sharpening_frame', sharpening_frame)
            #cv2.imshow('gray', gray)    
            #cv2.imshow('frame', frame) 
            #cv2.imshow('sharpening_frame', sharpening_frame)
            #cv2.imshow('Cropped Region', cropped_region)
            #cv2.imshow('SITD_gray', SITD_gray)
            #cv2.imshow("SITD_blur", SITD_blur)
            #cv2.imshow("SITD_canny", SITD_canny)
        # =======================================================
            #cv2.imshow("dilated_image", dilated_image_1)
            #cv2.imshow("blur_1", blur_1)
            #cv2.imshow("eroded_image_1", eroded_image_1)
            #cv2.imshow("sharpening_1", sharpening_1)

            cv2.imshow("information_frame", information_frame)
            cv2.imshow("show_image", show_image)



            if cv2.waitKey(speed_value) == ord('q'):  # 如果按下 'q' 鍵，則退出
                break
            
        cap.release()  # 釋放 cap
        cv2.destroyAllWindows()  # 關閉所有 OpenCV 窗口

if __name__ == "__main__":
    ai = AI_Fun()