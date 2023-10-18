int a=1;
int freq=15;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  freq=map(analogRead(3), 0, 1023, 10, 30);
  Serial1.print("^");
  Serial1.print(map(analogRead(A0), 0, 1023, 120, 160));
  Serial1.print("^");
  Serial1.print(map(analogRead(1), 0, 1023, 90,125));
  Serial1.print("^");
  Serial1.print(map(analogRead(2), 0, 1023, 0, 100));
  Serial1.println("^");
  

//  freq=map(analogRead(3), 0, 1023, 10, 30);
//  Serial.print("^");
//  Serial.print(map(analogRead(A0), 0, 1023, 120, 160));
//  Serial.print("^");
//  Serial.print(map(analogRead(1), 0, 1023, 90,125));
//  Serial.print("^");
//  Serial.print(map(analogRead(2), 0, 1023, 0, 100));
//  Serial.println("^");
//  a++;
  
  if (a==255){
    a=0;
  }
  delay(1000/freq);
}
