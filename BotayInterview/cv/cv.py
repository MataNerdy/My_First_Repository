# Примеры classic CV в действии
import cv2

# Загрузка изображения
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Яркость — простая гистограмма
mean_brightness = img.mean()
if mean_brightness > 200:
    print("Пересвет")
elif mean_brightness < 50:
    print("Слишком темно")

# Границы — фильтр Собеля
grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
edges = cv2.magnitude(grad_x, grad_y)

# Блюр — гауссов фильтр
blurred = cv2.GaussianBlur(img, (15, 15), 0)

# Обнаружение блюра — лапласиан
laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
if laplacian_var < 100:
    print("Изображение размыто")

# Ключевые точки — SIFT (в OpenCV может быть ограничен лицензией)
# sift = cv2.SIFT_create()
# keypoints, descriptors = sift.detectAndCompute(img, None)