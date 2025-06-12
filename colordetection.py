import cv2
import time
from gtts import gTTS
from IPython.display import Audio
import os

def text_to_speech(text, output_file='output.mp3'):
    tts = gTTS(text=text, lang='th', slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

def color_processing():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    first_iteration = True
    last_print_time = time.time()

    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]
        color = "Undefined"
        if hue_value < 5:
            color = "สีแดง"
        elif hue_value < 11:
            color = "สีแดงส้ม"
        elif hue_value < 22:
            color = "สีเหลืองส้ม"
        elif hue_value < 33:
            color = "สีเหลือง"
        elif hue_value < 45:
            color = "สีเหลืองเขียว"
        elif hue_value < 60:
            color = "สีเขียว"
        elif hue_value < 85:
            color = "สีเขียวอ่อน"
        elif hue_value < 100:
            color = "สีเขียว"
        elif hue_value < 115:
            color = "สีฟ้า"
        elif hue_value < 130:
            color = "สีน้ำเงิน"
        elif hue_value < 150:
            color = "สีน้ำเงิน"
        elif hue_value < 165:
            color = "สีคราม"
        elif hue_value < 170:
            color = "สีม่วง"
        elif hue_value < 190:
            color = "สีม่วงแดง"
        elif hue_value < 220:
            color = "สีแดงกุหลาบ"
        elif hue_value < 255:
            color = "สีม่วงแดง"
        else:
            color = "สีดำ"

        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
        cv2.rectangle(frame, (cx - 220, 10), (cx + 130, 120), (255, 255, 255), -1)
        cv2.putText(frame, "COLOR", (cx - 200, 100), 0, 3, (b, g, r), 5)
        cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
        cv2.imshow("Frame", frame)
        current_time = time.time()
        if first_iteration or (current_time - last_print_time >= 5):
            text_to_speech(color)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            last_print_time = current_time
            first_iteration = False
        key = cv2.waitKey(1)
        if key == 27:
            break

if __name__ == "__main__":
    color_processing()