import cv2

def is_blurry(image_path):
    image = cv2.imread(image_path, 0)
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < 100  # threshold