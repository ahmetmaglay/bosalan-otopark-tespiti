import cv2
import pickle
import numpy as np

cap = cv2.VideoCapture("video.mp4")

def noktalari_kontrol_et(frame1):
    bos_alan_sayaci = 0
    for pos in liste:
        x, y = pos

        kiris = frame1[y:y+15, x:x+26]
        sayi = cv2.countNonZero(kiris)

        if sayi < 150:
            renk = (0, 255, 0)
            bos_alan_sayaci += 1
        else:
            renk = [0, 0, 255]

        cv2.rectangle(frame, pos, (pos[0]+26, pos[1]+15), renk, 2)

    cv2.putText(frame, f"Bos: {bos_alan_sayaci}/{len(liste)}", (10, 24), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

with open("noktalar", "rb") as f:
    liste = pickle.load(f)

while True: 
    _, frame = cap.read()
    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bulanik = cv2.GaussianBlur(gri, (3, 3), 1)
    esik = cv2.adaptiveThreshold(bulanik, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    ortanca = cv2.medianBlur(esik, 5)
    genisletilmis = cv2.dilate(ortanca, np.ones((3, 3)), iterations=1)

    noktalari_kontrol_et(genisletilmis)

    cv2.imshow("asd", frame)

    if cv2.waitKey(200) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()





