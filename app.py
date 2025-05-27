import os
import cv2
import face_recognition
import pickle
import time
from datetime import datetime, timedelta
import pytz
from geopy.geocoders import Nominatim
import requests
import telegram
from telegram import Bot
import pandas as pd
from reportlab.pdfgen import canvas
import numpy as np
import logging
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
CONFIG = {
    'telegram_token': '7899690264:AAH14dhEGOlvRoc4CageMH6WYROMEE5NmkY',
    'telegram_chat_id': ' 7750409176',
    'allowed_location': 'Tashkent, Uzbekistan',
    'work_schedule': {
        'default': {'start': '09:00', 'end': '18:00', 'break': '13:00-14:00'},
        # Can add individual schedules per employee
    },
    'data_path': 'employee_data',
    'encodings_file': 'face_encodings.pkl',
    'attendance_log': 'attendance_log.csv',
    'error_log': 'error_log.txt'
}

# Initialize Telegram bot
bot = Bot(token=CONFIG['telegram_token'])

# Initialize face encodings dictionary
try:
    with open(os.path.join(CONFIG['data_path'], CONFIG['encodings_file']), 'rb') as f:
        face_encodings = pickle.load(f)
except (FileNotFoundError, EOFError):
    face_encodings = {}

# Initialize logging
logging.basicConfig(filename=CONFIG['error_log'], level=logging.INFO)

class Employee:
    def __init__(self, name, employee_id, position):
        self.name = name
        self.id = employee_id
        self.position = position
        self.face_encoding = None
        self.phone = None
        self.telegram_id = None
        self.schedule = CONFIG['work_schedule']['default']
        
    def add_face_encoding(self, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            self.face_encoding = encodings[0]
            face_encodings[self.id] = {
                'name': self.name,
                'encoding': self.face_encoding
            }
            self._save_encodings()
            return True
        return False
    
    def _save_encodings(self):
        with open(os.path.join(CONFIG['data_path'], CONFIG['encodings_file']), 'wb') as f:
            pickle.dump(face_encodings, f)

class AttendanceSystem:
    def __init__(self):
        self.attendance_data = self._load_attendance()
        self.current_2fa_codes = {}
        
    def _load_attendance(self):
        try:
            return pd.read_csv(os.path.join(CONFIG['data_path'], CONFIG['attendance_log']))
        except FileNotFoundError:
            columns = ['date', 'employee_id', 'name', 'check_in', 'check_out', 
                     'location', 'late_minutes', 'early_departure', 'total_hours']
            return pd.DataFrame(columns=columns)
    
    def save_attendance(self):
        self.attendance_data.to_csv(
            os.path.join(CONFIG['data_path'], CONFIG['attendance_log']), 
            index=False
        )
    
    def check_in(self, employee_id, location):
        now = datetime.now()
        today = now.date()
        time_str = now.strftime('%H:%M')
        
        # Check if already checked in today
        today_entries = self.attendance_data[
            (self.attendance_data['employee_id'] == employee_id) & 
            (pd.to_datetime(self.attendance_data['date']).dt.date == today
        ]
        
        if not today_entries.empty and pd.notna(today_entries.iloc[0]['check_in']):
            return False, "Already checked in today"
        
        # Calculate late minutes
        schedule = face_encodings.get(employee_id, {}).get('schedule', CONFIG['work_schedule']['default'])
        work_start = datetime.strptime(schedule['start'], '%H:%M').time()
        late_minutes = max(0, (now - datetime.combine(now.date(), work_start)).total_seconds() / 60)
        
        new_entry = {
            'date': today,
            'employee_id': employee_id,
            'name': face_encodings[employee_id]['name'],
            'check_in': time_str,
            'check_out': None,
            'location': location,
            'late_minutes': late_minutes,
            'early_departure': 0,
            'total_hours': 0
        }
        
        self.attendance_data = pd.concat([
            self.attendance_data, 
            pd.DataFrame([new_entry])
        ], ignore_index=True)
        
        self.save_attendance()
        return True, "Checked in successfully"
    
    def check_out(self, employee_id):
        now = datetime.now()
        today = now.date()
        time_str = now.strftime('%H:%M')
        
        # Find today's entry
        mask = (
            (self.attendance_data['employee_id'] == employee_id) & 
            (pd.to_datetime(self.attendance_data['date']).dt.date == today
        )
        
        if self.attendance_data[mask].empty:
            return False, "No check-in found for today"
        
        idx = self.attendance_data[mask].index[0]
        
        if pd.notna(self.attendance_data.loc[idx, 'check_out']):
            return False, "Already checked out today"
        
        # Calculate early departure and total hours
        check_in_time = datetime.strptime(self.attendance_data.loc[idx, 'check_in'], '%H:%M')
        check_out_time = datetime.strptime(time_str, '%H:%M')
        
        schedule = face_encodings.get(employee_id, {}).get('schedule', CONFIG['work_schedule']['default'])
        work_end = datetime.strptime(schedule['end'], '%H:%M').time()
        
        early_departure = max(0, (datetime.combine(now.date(), work_end) - now).total_seconds() / 60)
        total_hours = (check_out_time - check_in_time).total_seconds() / 3600
        
        # Subtract break time if exists
        if 'break' in schedule:
            break_start, break_end = map(
                lambda x: datetime.strptime(x, '%H:%M'), 
                schedule['break'].split('-')
            )
            if check_in_time < break_start and check_out_time > break_end:
                total_hours -= (break_end - break_start).total_seconds() / 3600
        
        self.attendance_data.loc[idx, 'check_out'] = time_str
        self.attendance_data.loc[idx, 'early_departure'] = early_departure
        self.attendance_data.loc[idx, 'total_hours'] = total_hours
        
        self.save_attendance()
        return True, "Checked out successfully"
    
    def generate_2fa_code(self, employee_id):
        code = str(np.random.randint(100000, 999999))
        self.current_2fa_codes[employee_id] = {
            'code': code,
            'expires': datetime.now() + timedelta(minutes=5)
        }
        return code
    
    def verify_2fa_code(self, employee_id, code):
        if employee_id not in self.current_2fa_codes:
            return False
        
        code_data = self.current_2fa_codes[employee_id]
        
        if datetime.now() > code_data['expires']:
            del self.current_2fa_codes[employee_id]
            return False
        
        if code_data['code'] == code:
            del self.current_2fa_codes[employee_id]
            return True
        
        return False
    
    def get_employee_stats(self, employee_id):
        employee_data = self.attendance_data[self.attendance_data['employee_id'] == employee_id]
        
        if employee_data.empty:
            return None
        
        stats = {
            'total_days': len(employee_data),
            'average_hours': employee_data['total_hours'].mean(),
            'late_days': len(employee_data[employee_data['late_minutes'] > 0]),
            'early_departures': len(employee_data[employee_data['early_departure'] > 0]),
            'last_week': employee_data.tail(7)
        }
        
        return stats
    
    def generate_payroll_pdf(self, employee_id, month, year):
        employee_name = face_encodings[employee_id]['name']
        monthly_data = self.attendance_data[
            (self.attendance_data['employee_id'] == employee_id) &
            (pd.to_datetime(self.attendance_data['date']).dt.month == month) &
            (pd.to_datetime(self.attendance_data['date']).dt.year == year)
        ]
        
        total_hours = monthly_data['total_hours'].sum()
        # Assuming hourly wage is stored elsewhere
        hourly_wage = 25  # Example value
        total_pay = total_hours * hourly_wage
        
        filename = f"payroll_{employee_id}_{month}_{year}.pdf"
        filepath = os.path.join(CONFIG['data_path'], filename)
        
        c = canvas.Canvas(filepath)
        c.drawString(100, 800, f"Payroll for {employee_name}")
        c.drawString(100, 780, f"Month: {month}/{year}")
        c.drawString(100, 760, f"Total hours worked: {total_hours:.2f}")
        c.drawString(100, 740, f"Hourly wage: ${hourly_wage:.2f}")
        c.drawString(100, 720, f"Total pay: ${total_pay:.2f}")
        c.save()
        
        return filepath

def get_location():
    try:
        # In a real app, you would get this from the device GPS or browser
        # This is a simplified version using IP geolocation
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return data.get('city', '') + ', ' + data.get('country', '')
    except:
        return "Location unknown"

def is_location_allowed(location):
    # Simple check if location contains the allowed location string
    return CONFIG['allowed_location'].lower() in location.lower()

def recognize_face(frame):
    # Convert image from BGR color (OpenCV) to RGB color
    rgb_frame = frame[:, :, ::-1]
    
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encs = face_recognition.face_encodings(rgb_frame, face_locations)
    
    recognized = []
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encs):
        # See if the face is a match for known faces
        matches = face_recognition.compare_faces(
            [e['encoding'] for e in face_encodings.values()], 
            face_encoding
        )
        
        name = "Unknown"
        employee_id = None
        
        # If a match was found, use the first one
        if True in matches:
            first_match_index = matches.index(True)
            employee_id = list(face_encodings.keys())[first_match_index]
            name = face_encodings[employee_id]['name']
            
            recognized.append({
                'id': employee_id,
                'name': name,
                'location': (left, top, right, bottom)
            })
        
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
    
    return frame, recognized

# Flask routes for web interface
@app.route('/')
def home():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee_id = session['employee_id']
    attendance = AttendanceSystem()
    stats = attendance.get_employee_stats(employee_id)
    
    return render_template('dashboard.html', 
                         name=face_encodings[employee_id]['name'],
                         stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # In a real app, you would verify credentials
        employee_id = request.form.get('employee_id')
        password = request.form.get('password')
        
        if employee_id in face_encodings:  # Simple check
            session['employee_id'] = employee_id
            return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/check_in', methods=['POST'])
def web_check_in():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee_id = session['employee_id']
    location = get_location()
    
    attendance = AttendanceSystem()
    success, message = attendance.check_in(employee_id, location)
    
    if success:
        # Send 2FA code via Telegram
        code = attendance.generate_2fa_code(employee_id)
        try:
            bot.send_message(
                chat_id=face_encodings[employee_id].get('telegram_id', CONFIG['telegram_chat_id']),
                text=f"Your verification code is: {code}"
            )
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")
    
    return {'success': success, 'message': message}

@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee_id = session['employee_id']
    code = request.form.get('code')
    
    attendance = AttendanceSystem()
    if attendance.verify_2fa_code(employee_id, code):
        return {'success': True, 'message': "Verification successful"}
    else:
        return {'success': False, 'message': "Invalid or expired code"}

@app.route('/check_out', methods=['POST'])
def web_check_out():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee_id = session['employee_id']
    attendance = AttendanceSystem()
    success, message = attendance.check_out(employee_id)
    
    return {'success': success, 'message': message}

@app.route('/admin/register', methods=['GET', 'POST'])
def register_employee():
    # This would be protected by admin auth in a real app
    if request.method == 'POST':
        name = request.form.get('name')
        employee_id = request.form.get('employee_id')
        position = request.form.get('position')
        
        # Save uploaded image
        if 'photo' not in request.files:
            return "No photo uploaded", 400
            
        photo = request.files['photo']
        if photo.filename == '':
            return "No selected file", 400
            
        if photo:
            filename = f"{employee_id}.jpg"
            photo_path = os.path.join(CONFIG['data_path'], 'employee_photos', filename)
            os.makedirs(os.path.dirname(photo_path), exist_ok=True)
            photo.save(photo_path)
            
            # Create employee and add face encoding
            employee = Employee(name, employee_id, position)
            if employee.add_face_encoding(photo_path):
                return redirect(url_for('home'))
            else:
                return "Failed to detect face in image", 400
    
    return render_template('register_employee.html')

def main():
    # Create data directory if it doesn't exist
    os.makedirs(CONFIG['data_path'], exist_ok=True)
    
    # Start web interface
    app.run(debug=True)

if __name__ == '__main__':
    main()
