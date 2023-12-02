bool SHORT = 0;
bool LONG = 1;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT); // LED

}

void blink(bool mode){
  digitalWrite(LED_BUILTIN, HIGH);
  if (mode == SHORT){
    delay(100);
  } else {
    delay(400);
  }
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  // HELLO WORLD = .... . .-.. .-.. --- / .. -- ..-
  // H
  blink(SHORT);
  blink(SHORT);
  blink(SHORT);
  blink(SHORT);
  delay(1000);
  // E
  blink(SHORT);
  delay(1000);
  // L
  blink(SHORT);
  blink(LONG);
  blink(SHORT);
  blink(SHORT);
  delay(1000);
  // L
  blink(SHORT);
  blink(LONG);
  blink(SHORT);
  blink(SHORT);
  delay(1000);
  // O
  blink(LONG);
  blink(LONG);
  blink(LONG);
  delay(1000);

  // I
  blink(SHORT);
  blink(SHORT);
  delay(1000);

  // M
  blink(LONG);
  blink(LONG);
  delay(1000);

  // U
  blink(SHORT);
  blink(SHORT);
  blink(LONG);
  delay(1000);
}
