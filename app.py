import streamlit as st
import sqlite3
import face_recognition
import cv2
import numpy as np
import os
import pickle
from datetime import datetime
from telegram import Bot
import pytz

TELEGRAM_BOT_TOKEN = "7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY"
ADMIN_CHAT_ID = "7750409176"  # o'zingizniki

bot = Bot(token=TELEGRAM_BOT_TOKEN)

DB_PATH = "worktime.db"
ENCODING_DIR = "encodings"

def get_current_time():
    tz = pytz.timezone("Asia/Tashkent")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def load_encodings():
    known_encodings = []
    known_users = []
    for file in os.listdir(ENCODING_DIR):
        if file.endswith(".pkl"):
            with open(f"{ENCODING_DIR}/{file}", "rb") as f:
                data = pickle.load(f)
                known_encodings.append(data['encoding'])
                known_users.append(data)
    return known_encodings, known_users

def mark_attendance(user, mode="login"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = get_current_time()
    if mode == "login":
        c.execute("INSERT INTO attendance (username, firstname, lastname, login_time) VALUES (?, ?, ?, ?)",
                  (user['username'], user['firstname'], user['lastname'], now))
        msg = f"✅ <b>{user['firstname']} {user['lastname']}</b> ishga KIRDI\n🕒 {now}"
    else:
        c.execute('''
            UPDATE attendance SET logout_time = ? 
            WHERE username = ? AND logout_time IS NULL
            ORDER BY login_time DESC LIMIT 1
        ''', (now, user['username']))
        msg = f"❌ <b>{user['firstname']} {user['lastname']}</b> ishdan CHIQDI\n🕒 {now}"

    conn.commit()
    conn.close()

    # Telegramga xabar
    send_telegram_message(get_chat_id(user['username']), msg)

def get_chat_id(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id FROM employees WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ADMIN_CHAT_ID

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        st.error(f"Telegram xatosi: {e}")

def recognize_face(mode):
    cap = cv2.VideoCapture(0)
    stframe = st.empty()
    known_encodings, known_users = load_encodings()

    result = "Hech kim tanilmadi"
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                user = known_users[best_match_index]
                mark_attendance(user, mode)
                result = f"{user['firstname']} {user['lastname']} aniqlandi"
                cap.release()
                cv2.destroyAllWindows()
                return result

        stframe.image(frame, channels="BGR")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result

# ==== Streamlit UI ====

st.set_page_config("Yuz bilan Kirish/Chiqish", layout="centered")
st.title("🧑‍💼 Xodim Yuz Tanish Paneli")

option = st.selectbox("Amalni tanlang:", ["Ishga Kirish", "Ishdan Chiqish"])

if st.button("Yuzni Skanirovka Qilish"):
    st.info("⏳ Kamera ishga tushdi. Yuzingizni ko‘rsating...")
    if option == "Ishga Kirish":
        result = recognize_face("login")
    else:
        result = recognize_face("logout")
    st.success(result)
