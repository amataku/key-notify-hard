const int led_out = 7;
const int ana_in = 0;
bool flag=false;

void setup() {
  pinMode(led_out,OUTPUT);
  Serial.begin(9800);
}

void loop() {
  int press;

  press = analogRead(ana_in);

  Serial.println(press);
  
  if(press < 1010){
    flag=true;
  }

  if(flag){
    digitalWrite(led_out,HIGH);
    flag=false;
  }else{
    digitalWrite(led_out,LOW);
  }
  
}
