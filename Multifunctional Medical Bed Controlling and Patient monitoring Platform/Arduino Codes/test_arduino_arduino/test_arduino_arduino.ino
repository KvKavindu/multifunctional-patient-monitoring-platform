int a = 1;
int freq_gui = 10;
int freq_iot = 1;

int interval_gui=1000/freq_gui;
int interval_iot=1000/freq_iot;


unsigned long currentMillis = millis();
unsigned long previousMillis_gui = currentMillis;
unsigned long previousMillis_iot = currentMillis;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  //freq = map(analogRead(3), 0, 1023, 0, 10);
  //Serial1.println(freq);
  //Serial.println(freq);
  if ((currentMillis - previousMillis_gui) > interval_gui) {
    if ()
    Serial1.print("^");
    Serial1.print(map(analogRead(A0), 0, 1023, 120, 160));
    Serial1.print("^");
    Serial1.print(map(analogRead(1), 0, 1023, 90, 125));
    Serial1.print("^");
    Serial1.print(map(analogRead(2), 0, 1023, 0, 100));
    Serial1.println("^");
    previousMillis_gui = currentMillis;
  }

  if ((currentMillis - previousMillis_iot) > interval_iot) {
    //  freq=map(analogRead(3), 0, 1023, 10, 30);
    Serial.print("^");
    Serial.print(map(analogRead(A0), 0, 1023, 120, 160));
    Serial.print("^");
    Serial.print(map(analogRead(1), 0, 1023, 90, 125));
    Serial.print("^");
    Serial.print(map(analogRead(2), 0, 1023, 0, 100));
    Serial.println("^");
    previousMillis_iot = currentMillis;
  }
  //delay(40);
}
