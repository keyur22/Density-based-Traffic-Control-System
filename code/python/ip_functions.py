import sys
import numpy as np
import cv2
import math
cascade_src = 'cars.xml'

def read_image(img_name):
    return cv2.imread(img_name, 0)

def display_image(windowName, image):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.imshow(windowName, image)

def noOfVehicles(image_name, direction):
    og = cv2.imread(image_name, 0)
    #display_image(image_name + " og", og)
    if direction=='L':
        og = og[:, :og.shape[1]/2]
    elif direction=='R':
        og = og[:, og.shape[1]/2:]
    car_cascade = cv2.CascadeClassifier(cascade_src)
    cars = car_cascade.detectMultiScale(og, 1.1, 1)
    """for (x,y,w,h) in cars:
        cv2.rectangle(og,(x,y),(x+w,y+h),(0,0,255),2)"""
    #display_image("detected", og)
    #print cars
    if len(cars)==0:
        return 0
    return cars.shape[0]

def cut_paste(og, patch, x, y):
    og[x:x+patch.shape[0], y:y+patch.shape[1]] = patch
    return og

def gamma_correction(img_name, c, g):
    img = cv2.imread(img_name, 0)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            img.itemset(i, j, 255*pow(img.item(i, j)/255.0, (1/float(g))))
    return img

def compare(img1_name, img2_name):
    img1 = cv2.imread(img1_name)
    img2 = cv2.imread(img2_name)
    if img1.shape[0]!=img2.shape[0] or img1.shape[1]!=img2.shape[1]:
        return 0
    change_cnt = 0
    for i in range(0, img1.shape[0]):
        for j in range(0, img1.shape[1]):
            if img1.item(i, j)!=img2.item(i, j):
                change_cnt += 1
    print change_cnt
    print float(img1.size)
    print change_cnt/float(img1.size)

    return (change_cnt/float(img1.size))*100

"""
def main():
    patch = og[200:250, 150:200]
    print noOfVehicles('try.jpg', 'L')
    #display_image("try", patch)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
"""
