#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Required libraries:
import cv2
import numpy as np
import mysql.connector
 

# Connection of database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="FlaskDb"
)

# Getting the informations from db
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM objects")

 # Creating some lists for incoming informations from db
myresult = mycursor.fetchall()
# Use incoming informations that from db with for loop
for x in myresult:
    print(x[2])
    print(x[1])

# Referans foto�raf� y�kle
ref_img = cv2.imread(x[2])
# Gri tonlamal� olarak referans foto�raf� al
ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
# Referans foto�raf�ndaki dairelerin tespiti i�in Hough Daireleri Transformasyonu kullan�yoruz
# Burada kullan�lan parametreler, �aplar� 50 ile 80 piksel aras�nda olan daireleri tespit etmek i�in ayarlamak i�in min-maxRadius de�erlerini de�i�tirmemiz yeterli olacakt�r.
ref_circles = cv2.HoughCircles(ref_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
ref_num_circles = len(ref_circles[0])

# Kamera g�r�nt�s�n� yakala
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 793.7)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1133.85)
while True:
    # Kameradan g�r�nt� al
    ret, frame = cap.read()

    # G�r�nt�y� gri tona d�n��t�r
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Daireleri bul
    # G�r�nt�deki daireleri tespit etmek i�in Hough Daireleri Transformasyonu kullan�yoruz.
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # Dairelerin tespit edildi�inden emin olun
    if circles is not None:
        num_circles = len(circles[0])
    else:
        num_circles = 0

    # Referans foto�raftaki ve kamera g�r�nt�s�ndeki daire say�s�n� kar��la�t�r
    if num_circles == ref_num_circles:
        text = "Daire sayisi: {} (Dogru)".format(num_circles)
    else:
        text = "Daire sayisi: {} (Yanlis)".format(num_circles)

    # Sonu�lar� ekrana yazd�r
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    # ��k�� yapmak i�in "q" tu�una bas�n
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
cap.release()
cv2.destroyAllWindows()
