import cv2
import os

path = os.path.abspath('result')
count = 0
for root, _, filenames in os.walk(path):
    for filename in filenames:
        img_path = os.path.join(root, filename)

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                      7, 2)
        count += 1
        if count > 3049:
            cv2.imwrite(img_path, image)
            print(f'progress: {count} element')

