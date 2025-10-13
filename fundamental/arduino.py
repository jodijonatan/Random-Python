import cv2
import serial
import time

# Hubungkan ke Arduino (sesuaikan port, misalnya COM3 di Windows atau /dev/ttyUSB0 di Linux/Mac)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Tunggu koneksi stabil

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # Konversi gambar ke skala abu-abu
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Jika ada gerakan, nyalakan LED
    if len(contours) > 0:
        arduino.write(b'1')  # Kirim sinyal '1' ke Arduino untuk menyalakan LED
        print("Gerakan terdeteksi! LED ON")
    else:
        arduino.write(b'0')  # Kirim sinyal '0' untuk mematikan LED
        print("Tidak ada gerakan. LED OFF")

    # Tampilkan hasil
    cv2.imshow("Camera", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    # Keluar jika tombol 'q' ditekan
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
