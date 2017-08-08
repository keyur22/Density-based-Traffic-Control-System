
int ledPin = 13;
void setup() {
  int inpins[] = {2, 3, 4, 5, 6, 7, 8};
  int first = 9, second = 10, third = 11;
  pinSetup(inpins, first, second, third);
  timerSetup();
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
}

void loop() {
 digitalWrite(ledPin, LOW);
 while(Serial.available()==0);
 if(Serial.readString() == "G")  {
   digitalWrite(ledPin, HIGH);
 }
 while(Serial.available()==0);
 int count = Serial.parseInt();
 counter(count);
}

