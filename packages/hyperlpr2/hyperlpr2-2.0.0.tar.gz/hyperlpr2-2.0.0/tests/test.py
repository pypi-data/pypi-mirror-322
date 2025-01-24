import cv2

image = cv2.imread('img.png')
import hyperlpr

print(hyperlpr.HyperLPR_plate_recognition(image))