// Motor pins
int ENA = 5;  
int IN1 = 3;
int IN2 = 4;

int ENB = 6;
int IN3 = 7;
int IN4 = 8;

// Sensors
int LDR_Left = A0;
int LDR_Right = A1;

// LEDs
int LED_Green = 9;  // Idle / line-following
int LED_Red   = 10; // Obstacle detected

// Ultrasonic sensor pins
int TRIG_PIN = 11;
int ECHO_PIN = 13;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  pinMode(LED_Green, OUTPUT);
  pinMode(LED_Red, OUTPUT);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.begin(9600);
}

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  long distance = duration * 0.034 / 2; // in cm
  return distance;
}

void loop() {
  int leftValue = analogRead(LDR_Left);
  int rightValue = analogRead(LDR_Right);
  long distance = getDistance();

  Serial.print("Left LDR: "); Serial.print(leftValue);
  Serial.print("  Right LDR: "); Serial.print(rightValue);
  Serial.print("  Distance: "); Serial.println(distance);

  // 🚧 Obstacle detection
  if (distance < 100 && distance > 0) {
    stopMotors();
    digitalWrite(LED_Green, LOW);
    digitalWrite(LED_Red, HIGH);  // Obstacle → RED ON
    return;
  }

  // ✅ Line following logic
  digitalWrite(LED_Red, LOW);

  if (leftValue > 500 && rightValue > 500) { // both dark → forward
    moveForward();
    digitalWrite(LED_Green, HIGH); // show ACTIVE
  } 
  else if (leftValue > 500) { // left dark
    turnLeft();
    blinkGreen();
  } 
  else if (rightValue > 500) { // right dark
    turnRight();
    blinkGreen();
  } 
  else { // lost track
    stopMotors();
    digitalWrite(LED_Green, LOW);
  }
}

// ---- Motor functions ----
void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

// ---- LED blink for turns ----
void blinkGreen() {
  digitalWrite(LED_Green, HIGH);
  delay(100);
  digitalWrite(LED_Green, LOW);
  delay(100);
}
