import numpy as np 
import cv2
import time
from gtts import gTTS
from IPython.display import Audio
import os

def text_to_speech(text, output_file='output.mp3'):
    tts = gTTS(text=text, lang='th', slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

def object_processing():
    CLASSES = ["พื้นหลัง", "เครื่องบิน", "จักรยาน", "นก", "เรือ",
        "ขวด", "รถบัส", "รถ", "แมว", "เก้าอี้", "วัว", "โต๊ะ",
        "หมา", "ม้า", "จักรยานยนต์", "คน", "กระถางต้นไม้", "แกะ",
        "โซฟา", "รถไฟ", "หน้าจอ"]

    COLORS = np.random.uniform(0, 100, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("./MobileNetSSD/MobileNetSSD.prototxt", "./MobileNetSSD/MobileNetSSD.caffemodel")
    cap = cv2.VideoCapture(0)
    

    first_iteration = True
    last_print_time = time.time()

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 540))
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            for i in np.arange(0, detections.shape[2]):
                percent = detections[0, 0, i, 2]
                if percent > 0.5:
                    class_index = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    center_x = int((startX + endX) / 2)
                    center_y = int((startY + endY) / 2)
                    # cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), -1)

                    object_position = ""
                    if center_x < 210 and center_x > 180:
                        object_position = "ด้านหน้า"
                    elif center_x < 180:
                        object_position = "ด้านซ้าย"
                    elif center_x > 210:
                        object_position = "ด้านขวา"
            

                    label = "{} อยู่ {} ของคุณ".format(CLASSES[class_index],object_position)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[class_index], 2)
                    cv2.rectangle(frame, (startX-1, startY-1), (endX+1, startY), COLORS[class_index], cv2.FILLED)

                    current_time = time.time()
                    if first_iteration or (current_time - last_print_time >= 5):
                        print(CLASSES[class_index])

                        text_to_speech(label)

                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                        last_print_time = current_time
                        first_iteration = False

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    object_processing()
