import cv2
import numpy as np

# Mode:
# 0 = Normal
# 1 = Average blur 5x5
# 2 = Average blur 9x9
# 3 = Gaussian blur (custom kernel + filter2D)
# 4 = Sharpen
mode = 0

def gaussian_kernel_2d(ksize, sigma):
    gk = cv2.getGaussianKernel(ksize, sigma)
    return gk @ gk.T

sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Gagal membuka webcam")
    exit()

print("Kontrol keyboard: 0=Normal, 1=Avg5x5, 2=Avg9x9, 3=Gaussian9x9, 4=Sharpen, q=Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output = frame.copy()

    if mode == 1:
        output = cv2.blur(frame, (5,5))
    elif mode == 2:
        output = cv2.blur(frame, (9,9))
    elif mode == 3:
        k = gaussian_kernel_2d(9, 1.5)
        k = k / k.sum()
        output = cv2.filter2D(frame, -1, k)
    elif mode == 4:
        output = cv2.filter2D(frame, -1, sharpen_kernel)

    modes_text = {0:"Normal", 1:"Avg 5x5", 2:"Avg 9x9", 3:"Gaussian 9x9", 4:"Sharpen"}
    cv2.putText(output, f"Mode: {modes_text.get(mode,'Unknown')}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Tugas1 - Blur & Sharpen", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        mode = 0
    elif key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('3'):
        mode = 3
    elif key == ord('4'):
        mode = 4
    elif key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
