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

# Referans fotoðrafý yükle
ref_img = cv2.imread(x[2])
# Gri tonlamalý olarak referans fotoðrafý al
ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
# Referans fotoðrafýndaki dairelerin tespiti için Hough Daireleri Transformasyonu kullanýyoruz
# Burada kullanýlan parametreler, çaplarý 50 ile 80 piksel arasýnda olan daireleri tespit etmek için ayarlamak için min-maxRadius deðerlerini deðiþtirmemiz yeterli olacaktýr.
ref_circles = cv2.HoughCircles(ref_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
ref_num_circles = len(ref_circles[0])

# Kamera görüntüsünü yakala
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 793.7)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1133.85)
while True:
    # Kameradan görüntü al
    ret, frame = cap.read()

    # Görüntüyü gri tona dönüþtür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Daireleri bul
    # Görüntüdeki daireleri tespit etmek için Hough Daireleri Transformasyonu kullanýyoruz.
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # Dairelerin tespit edildiðinden emin olun
    if circles is not None:
        num_circles = len(circles[0])
    else:
        num_circles = 0

    # Referans fotoðraftaki ve kamera görüntüsündeki daire sayýsýný karþýlaþtýr
    if num_circles == ref_num_circles:
        text = "Daire sayisi: {} (Dogru)".format(num_circles)
    else:
        text = "Daire sayisi: {} (Yanlis)".format(num_circles)

    # Sonuçlarý ekrana yazdýr
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    # Çýkýþ yapmak için "q" tuþuna basýn
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
cap.release()
cv2.destroyAllWindows()
