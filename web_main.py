from flask import Flask, render_template, redirect, url_for, request
import speech_recognition as sr
from gtts import gTTS
import subprocess
import pygame

app = Flask(__name__)
running_processes = {}

def play_audio(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

@app.route('/')
def index():
    return render_template('page1.html')

def recognize_audio(source, recognizer, duration=5):
    text = None
    try:
        audio = recognizer.record(source, duration=duration)
        text = recognizer.recognize_google(audio, language="th")
    except sr.UnknownValueError:
        text = "ขอโทษครับ ไม่สามารถรับรู้เสียงได้"
    except sr.RequestError:
        text = "ขอโทษครับ เกิดข้อผิดพลาดในการเชื่อมต่อกับ Google API"
    return text

@app.route('/NextPage')
def NextPage():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text = "สวัสดีครับ กรุณาเลือกหมวดการทำงานดังนี้ 1 ตรวจจับวัตถุ 2 ระบุสี"
        tts = gTTS(text, lang="th")
        tts.save("welcome.mp3")
        play_audio("welcome.mp3")

        play_audio("sound.mp3")
        text = recognize_audio(source, recognizer)
        play_audio("sound.mp3")

        if text:
            if "ตรวจจับวัตถุ" in text or "1" in text:
                play_audio("speech1.mp3")
                return redirect(url_for('object_page'))

            elif "ระบุสี" in text or "3" in text:
                play_audio("speech3.mp3")
                return redirect(url_for('color_page'))

            else:
                text = "ขอโทษครับ ไม่เข้าใจคำสั่ง"

    tts = gTTS(text, lang="th")
    tts.save("answer.mp3")
    play_audio("answer.mp3")
    return redirect(url_for('index'))

@app.route('/object')
def object_page():
    process = subprocess.Popen(['python', 'object_main.py'])
    running_processes["object"] = process
    return render_template('object.html')


@app.route('/color')
def color_page():
    process = subprocess.Popen(['python', 'colordetection.py'])
    running_processes["ระบุสี"] = process
    return render_template('color.html')



@app.route('/message')
def message():
    return render_template('pp.html')

@app.route('/submit', methods=['POST'])
def submit():
    button_clicked = request.form['button']
    if button_clicked == 'ตรวจจับวัตถุ':
        play_audio("speech1.mp3")
        process = subprocess.Popen(['python', 'object_main.py'])
        running_processes[button_clicked] = process
        return render_template('object.html')
    

    
    elif button_clicked == 'ระบุสี':
        play_audio("speech3.mp3")
        process = subprocess.Popen(['python', 'colordetection.py'])
        running_processes[button_clicked] = process
        return render_template('color.html')
    
   
@app.route('/stop', methods=['POST'])
def stop():
    for key, process in running_processes.items():
        process.terminate()
    
    running_processes.clear()
    play_audio("speech8.mp3")
    return redirect('/message')

if __name__ == '__main__':
    app.run(debug=True)