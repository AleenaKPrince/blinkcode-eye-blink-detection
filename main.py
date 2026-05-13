import winsound
import threading
import cv2
import mediapipe as mp
import numpy as np
import time

from ear import calculate_EAR
from blink_logic import BlinkProcessor
from morse_decoder import decode_morse


# ---------- NON BLOCKING BEEP ----------
def beep(freq, dur):
    threading.Thread(target=winsound.Beep, args=(freq, dur)).start()


cap = cv2.VideoCapture(1)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

EAR_THRESHOLD = 0.25

blink = BlinkProcessor()

detecting = False

sentence = ""
full_morse = ""
last_blink_time = time.time()

ear = 0


while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face in results.multi_face_landmarks:

            landmarks = []

            h, w, _ = frame.shape

            for lm in face.landmark:
                landmarks.append((int(lm.x*w), int(lm.y*h)))

            left_eye = np.array([landmarks[i] for i in LEFT_EYE])
            right_eye = np.array([landmarks[i] for i in RIGHT_EYE])

            # draw eye landmarks
            for (x, y) in left_eye:
                cv2.circle(frame, (x, y), 2, (0,255,255), -1)

            for (x, y) in right_eye:
                cv2.circle(frame, (x, y), 2, (0,255,255), -1)

            leftEAR = calculate_EAR(left_eye)
            rightEAR = calculate_EAR(right_eye)

            ear = (leftEAR + rightEAR) / 2.0

            eye_closed = ear < EAR_THRESHOLD

            if detecting:

                previous_morse = blink.morse

                blink.detect(eye_closed)

                if previous_morse != blink.morse:

                    last_blink_time = time.time()

                    full_morse += blink.morse[-1]


    pause = time.time() - last_blink_time


    if detecting:

        # ---------- LETTER DETECTION ----------
        if pause > 2 and blink.morse != "":

            letter = decode_morse(blink.morse)

            if letter != "":
                sentence += letter
                print("Decoded Letter:", letter)

                # Letter beep
                beep(1200,150)

            full_morse += " "

            blink.reset_letter()
            last_blink_time = time.time()


        # ---------- WORD DETECTION ----------
        if pause > 4:

            if len(sentence) > 0 and sentence[-1] != " ":

                sentence += " "
                full_morse += " "

                # Word beep
                beep(800,300)

            last_blink_time = time.time()


    # ---------- UI ----------

    cv2.putText(frame,"Press S: Start | E: Stop",(30,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    cv2.putText(frame,"Press R: Reset | D: Delete Last | ESC: Exit",(30,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    status = "ON" if detecting else "OFF"

    cv2.putText(frame,"Detection:"+status,(30,100),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    display_morse = full_morse[-40:]
    display_text = sentence[-30:]

    cv2.putText(frame,"Morse:"+display_morse,(30,140),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    cv2.putText(frame,"Text:"+display_text,(30,180),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    cv2.putText(frame,f"EAR:{ear:.2f}",(30,220),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    cv2.imshow("Blink Morse System",frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    if key == ord('s'):
        detecting = True

    if key == ord('e'):
        detecting = False

    # reset everything
    if key == ord('r'):
        sentence = ""
        full_morse = ""
        blink.reset_letter()

    # delete last letter + morse
    if key == ord('d'):

        if len(sentence) > 0:
            sentence = sentence[:-1]

        full_morse = full_morse.rstrip()

        morse_parts = full_morse.split(" ")

        if len(morse_parts) > 0:
            morse_parts = morse_parts[:-1]

        full_morse = " ".join(morse_parts)

        print("Last letter removed")


cap.release()
cv2.destroyAllWindows()