import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Gagal membuka webcam")
    exit()

# Rentang HSV contoh (sesuaikan dengan pencahayaan)
lower_blue = np.array([100, 120, 50])
upper_blue = np.array([140, 255, 255])

lower_green = np.array([40, 70, 50])
upper_green = np.array([80, 255, 255])

# Untuk merah: dua rentang karena hue merah melintasi batas 0/179 di OpenCV
lower_red1 = np.array([0, 120, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 50])
upper_red2 = np.array([179, 255, 255])

# Kernel morfologi untuk membersihkan mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))

print("Menjalankan deteksi warna (biru, hijau, merah). Tekan q atau ESC untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Bersihkan mask dengan operasi morfologi
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)

    display = frame.copy()

    def detect_and_overlay(mask, label, color_bgr):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        found = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:  
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(display, (x,y), (x+w, y+h), color_bgr, 2)
                cv2.putText(display, f"{label} Detected", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_bgr, 2)

                overlay = display.copy()
                cv2.rectangle(overlay, (0,0), (display.shape[1], display.shape[0]), color_bgr, -1)
                cv2.addWeighted(overlay, 0.06, display, 0.94, 0, display)
                found = True
                break
        return found

    blue_found = detect_and_overlay(mask_blue, "Blue", (255,0,0))
    green_found = detect_and_overlay(mask_green, "Green", (0,255,0))
    red_found = detect_and_overlay(mask_red, "Red", (0,0,255))

    if red_found and not (blue_found or green_found):
        action_text = "Deteksi: Merah"
        action_color = (0,0,255)
    elif blue_found and not (green_found or red_found):
        action_text = "Deteksi: Biru"
        action_color = (255,0,0)
    elif green_found and not (blue_found or red_found):
        action_text = "Deteksi: Hijau"
        action_color = (0,255,0)
    elif red_found and blue_found and not green_found:
        action_text = "Deteksi: Merah & Biru"
        action_color = (255,0,255)
    elif red_found and green_found and not blue_found:
        action_text = "Deteksi: Merah & Hijau"
        action_color = (0,255,255)
    elif blue_found and green_found and not red_found:
        action_text = "Deteksi: Biru & Hijau"
        action_color = (0,255,255)
    elif red_found and blue_found and green_found:
        action_text = "Deteksi: Merah, Biru & Hijau"
        action_color = (200,200,200)
    else:
        action_text = "Tidak ada objek terdeteksi"
        action_color = (200,200,200)

    cv2.putText(display, action_text, (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, action_color, 2)

    cv2.imshow("Tugas2 - HSV Single Window (Red Added)", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
