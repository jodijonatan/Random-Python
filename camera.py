import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Warna yang tersedia
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]  # Biru, Hijau, Merah, Kuning
color_index = 1  # Warna awal (Biru)

# Kanvas kosong untuk menggambar
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Buka kamera
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Balikkan gambar agar seperti cermin
    h, w, c = frame.shape
    
    # Konversi ke RGB untuk MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Ambil posisi ujung jari telunjuk (Index Finger Tip)
            index_finger_tip = hand_landmarks.landmark[8]
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            
            # Gambar lingkaran di ujung jari
            cv2.circle(frame, (x, y), 10, colors[color_index], -1)
            
            cv2.circle(canvas, (x, y), 5, colors[color_index], -1)
            
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            if abs(thumb_x - x) < 50 and abs(thumb_y - y) < 50:
                color_index = (color_index + 1) % len(colors)
                cv2.waitKey(500)
    
    frame = cv2.addWeighted(frame, 1, canvas, 0.5, 0)
    
    cv2.imshow("Virtual Paint", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
