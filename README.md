# ZPHS01_WINSEN_SCRIPT
ZPHS01_WINSEN procedimiento para hacer funcionar el sensor.  
Se adjunta script en python para el funcionamiento del sensor Winsen ZPHS01  
Espero que los ayude, cualquier apoyo pueden escribir al Github  
1.- Primero paso conectar los puerto UART, segun el datasheet de winsen ZPHS01, en mi caso tuve que conectar los puertos desde mi raspberry TX uart al rx ZPHS01 sensor, rx raspberry al tx ZPHS01.  
**2.- Una vez tengas el codigo listo, debes activar el sensor mandando la señal  [ start dust measurement,Respond： 16 02 0C 02 DA //the module is in “on-state dust measurement” ] en el codigo lo usas solo 1 vez para activar el sensor, despues de eso usas la señal [Send： 11 02 01 00 EC measurement]  que esta en el codigo.**  
3.- Deberias obtener un codigo similar a este:  
root@raspberrypi2:/home/raspberrypi2/16_ZPHS01_v1# python3 2_ZPHS01_v2.py   
Co2= 400 TVOC= 3 Humidity= 590 Tempe= 28.4 PM 2.5= 11  
Co2= 400 TVOC= 3 Humidity= 590 Tempe= 28.4 PM 2.5= 11  
Co2= 400 TVOC= 3 Humidity= 590 Tempe= 28.3 PM 2.5= 11  
Co2= 400 TVOC= 3 Humidity= 590 Tempe= 28.4 PM 2.5= 11  


![zphs01-voc-02](https://github.com/user-attachments/assets/acb99174-a265-4260-9f81-0ed60772d181)
![zphs01-__](https://github.com/user-attachments/assets/ecfa24fa-7e8b-44ff-b61f-ff19e8168644)
