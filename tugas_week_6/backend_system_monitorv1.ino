#include <Servo.h>

#define MA1 D1  // A+
#define MA2 D2  // A-
#define MB1 D5  // B+
#define MB2 D6  // B-

#define SERVO_PIN D4  // Pilih pin digital yang tidak dipakai untuk servo

Servo myServo;

void setup() {
  Serial.begin(9600);
  
  pinMode(MA1, OUTPUT);
  pinMode(MA2, OUTPUT);
  pinMode(MB1, OUTPUT);
  pinMode(MB2, OUTPUT);

  myServo.attach(SERVO_PIN);


  analogWrite(MA1, 200);
  digitalWrite(MA2, LOW);

  analogWrite(MB1, 200);
  digitalWrite(MB2, LOW);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    Serial.println("Diterima : " + input);

    if (input.startsWith("MB:")) {
      int pwm = input.substring(3).toInt();
      controlMotor(MB1, MB2, pwm);
    }
    else if (input.startsWith("MA:")) {
      int pwm = input.substring(3).toInt();
      controlMotor(MA1, MA2, pwm);
    }
    else if (input.startsWith("S:")) {
      int angle = input.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      myServo.write(angle);
    }
  }
}

void controlMotor(int pin1, int pin2, int pwm) {
  pwm = constrain(pwm, -255, 255); // Membatasi nilai PWM antara -255 dan 255
  if (pwm > 0) {
    analogWrite(pin1, pwm);  // arah maju
    digitalWrite(pin2, LOW);
  } else if (pwm < 0) {
    digitalWrite(pin1, LOW);
    analogWrite(pin2, -pwm);  // arah mundur
  } else {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);  // stop
  }
}
