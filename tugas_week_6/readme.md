alat dan bahan:
- driver motor l298n
- motor DC n20
- Mikrokontroller ESP8266
- ESP8266 Motor Shield

  Wiring
  - Driver motor to ESP
    - ENA to D7
    - IN2 to D6
    - IN1 to D5
    - pin tersebut support PWM
    - GND to GND
    - VCC to VCC
   
menjalankan:
- upload file arduino dengan format .ino melalui Arduino IDE ke ESP8266
- jalankan program python
- masukkan nilai PWM dengan range(1-255)
