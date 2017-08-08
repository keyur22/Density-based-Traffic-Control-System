import sys
import numpy as np
import cv2
import math
cascade_src = 'cars.xml'

def display_image(windowName, image):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.imshow(windowName, image)

def noOfVehicles(image_name, direction):
    og = cv2.imread(image_name, 0)
    #display_image(image_name + " og", og)
    if direction=='L':
        og = og[:, :int(og.shape[1]*0.65)]
    elif direction=='R':
        og = og[:, int(og.shape[1]*0.35):]
    car_cascade = cv2.CascadeClassifier(cascade_src)
    cars = car_cascade.detectMultiScale(og, 1.1, 1)
    for (x,y,w,h) in cars:
        cv2.rectangle(og,(x,y),(x+w,y+h),(0,0,255),2)
    display_image("detected", og)
    if len(cars)==0:
        return 0
    return cars.shape[0]

def main():
    print noOfVehicles('cases/CASE1/Lane3.png', 'L')
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
