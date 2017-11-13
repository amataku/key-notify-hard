const int led_out = 7;
const int ana_in = 0;
bool flag=false;

void setup() {
  pinMode(led_out,OUTPUT);
}

void loop() {
  int press;

  press = analogRead(ana_in);
  
  if(press <= 1000){
    flag=true;
  }

  if(flag){
    digitalWrite(led_out,HIGH);
  }
}
