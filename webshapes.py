import cv2
from threading import main_thread
from cv2 import circle
from cv2 import ellipse
from cv2 import rectangle
from cv2 import contourArea
import numpy as np
import math
# связываем видеопоток камеры с переменной capImg
capImg = cv2.VideoCapture(0)


def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

# запускаем бесконечный цикл, чтобы следить
# в реальном времени
while True:
# получаем кадр из видеопотока,
# кадры по очереди считываются в переменную frame
    ret, frame = capImg.read()

    drawing = frame.copy()
    collor = (
                (56 , 190  , 90 ),
                (74 , 255 , 255)
            )
    conturs = find_contours(frame , collor)

    if conturs:
        for cnt in conturs:
            contour_area = cv2.contourArea(cnt)
            if contour_area > 50:
                print("Площадь контура:", cv2.contourArea(cnt))
                cv2.drawContours(drawing , [cnt] , 0 , (255, 255 , 255) , 2)
                (circle_x , circle_y) , circle_radius = cv2.minEnclosingCircle(cnt)
                circle_area = math.pi * circle_radius**2
                print("Площадь окружности:", circle_area)
                



                try:
                    triangle = cv2.minEnclosingTriangle(cnt)[1]
                    triangle = np.int0(triangle)
                    triangle_area = cv2.contourArea(triangle)
                except:
                    triangle_area = 0
                print("Площадь треугольника:", triangle_area)


                (bounding_x , bounding_y, bounding_w , bounding_h) = cv2.boundingRect(cnt)
                bounding_pos1 = (bounding_x , bounding_y)
                bounding_pos2 = (bounding_x + bounding_w , bounding_y + bounding_h)
                rectangle = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rectangle)
                box = np.int0(box)
                rectangle_area = cv2.contourArea(box)
                print("Площадь прямогульника: " , rectangle_area)
                print("-----------------")
                print("Площадь прямоугольника:", bounding_w * bounding_h)
                

                rect_w , rect_h =rectangle[1][0], rectangle[1][1]
                aspect_ratio = max(rect_w , rect_h) / min(rect_w , rect_h)


                shapes_areas = {
                    'circle': circle_area ,
                    'rectangle' if aspect_ratio > 1.25 else 'square': rectangle_area,
                    'triangle': triangle_area
                }

                diffs ={
                    name: abs(contour_area - shapes_areas[name]) for name in shapes_areas

                }


                shape_name = min(diffs , key = diffs.get)
                if shape_name == "triangle": 
                    cv2.drawContours(drawing , [triangle] , -1 , (100 , 255 , 255) , 2)
                elif shape_name == "rectangle" or shape_name == "square":
                    cv2.drawContours(drawing, [box] , 0 , (0  , 155 , 255) , 2)
                else: 
                    cv2.circle(drawing, (int(circle_x) , int(circle_y)), int(circle_radius) , (255 , 255 , 0) , 2 )


                moments = cv2.moments(cnt)

                try:
                    x = int(moments['m10']/moments['m00'])
                    y = int(moments['m01']/moments['m00'])
                    cv2.circle(drawing, (x, y), 4, (0, 100, 255), -1, cv2.LINE_AA)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(drawing, shape_name, (x-40, y+31), font, 1, (0, 0, 0), 4, cv2.LINE_AA)
                    cv2.putText(drawing, shape_name, (x-41, y+30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                except ZeroDivisionError:
                    pass

                print()


# показываем кадр в окне ’Video’
    cv2.imshow('Video', drawing)
# организуем выход из цикла по нажатию клавиши,
# ждем 10 миллисекунд нажатие, записываем код
# нажатой клавиши
    key_press = cv2.waitKey(10)
# если код нажатой клавиши совпадает с кодом
# «q»(quit - выход),
    if key_press == ord('q'):
# то прервать цикл while
        break
# освобождаем память от переменной capImg
capImg.release()
# закрываем все окна opencv
cv2.destroyAllWindows()