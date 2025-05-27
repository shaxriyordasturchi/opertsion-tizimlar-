import cv2
import face_recognition
import pickle
import os

name = input("Ismingizni kiriting: ")
surname = input("Familiyangizni kiriting: ")
username = input("Login kiriting (eng): ")

cap = cv2.VideoCapture(0)

print("📸 Kamerani ishga tushirdik. Yuzingizni ko‘rsating...")
while True:
    ret, frame = cap.read()
    cv2.imshow("Yuzni tanish", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            encoding = face_recognition.face_encodings(frame, face_locations)[0]
            path = f'encodings/{username}.pkl'
            with open(path, 'wb') as f:
                pickle.dump({
                    'username': username,
                    'firstname': name,
                    'lastname': surname,
                    'encoding': encoding
                }, f)
            print(f"✅ {name} {surname} saqlandi: {path}")
            break

cap.release()
cv2.destroyAllWindows()
