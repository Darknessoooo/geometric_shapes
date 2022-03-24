from threading import main_thread
import cv2
from cv2 import circle
from cv2 import ellipse
from cv2 import rectangle
from cv2 import contourArea
import numpy as np
import math

def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

img = cv2.imread("pool_two_bins.jpg")
drawing = img.copy()
collor = (
            (30 , 80  , 0 ),
            (70 , 200 , 255)
         )
conturs = find_contours(img , collor)

if conturs:
    for cnt in conturs:
        if cv2.contourArea(cnt) > 50:
            contour_area = cv2.contourArea(cnt)
            print("Площадь контура:", cv2.contourArea(cnt))
            cv2.drawContours(drawing , [cnt] , 0 , (255, 255 , 255) , 2)
            (circle_x , circle_y) , circle_radius = cv2.minEnclosingCircle(cnt)
            circle_area = math.pi * circle_radius**2
            print("Площадь окружности:", circle_area)
            cv2.circle(drawing, (int(circle_x) , int(circle_y)), int(circle_radius) , (255 , 255 , 0) , 2 )



            try:
                triangle = cv2.minEnclosingTriangle(cnt)[1]
                triangle = np.int0(triangle)
                triangle_area = cv2.contourArea(triangle)
                cv2.drawContours(drawing , [triangle] , -1 , (100 , 255 , 255) , 2)
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
            cv2.drawContours(drawing, [box] , 0 , (0  , 155 , 255) , 2)

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

            print()

cv2.imshow("drawing" , drawing)
cv2.waitKey(0)

