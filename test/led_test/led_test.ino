//デジタル出力のポート番号
const int led_out = 7;
//アナログ入力のポート番号
const int ana_in = 0;
//シリアルポート番号
const int Serialnumber = 9800;
//アナログ入力値のしきい値
const int on_border = 1010;


void setup() {
  //アウトプットのピン設定
  pinMode(led_out,OUTPUT);
  //コンソール出力設定
  Serial.begin(Serialnumber);
}

void loop() {
  int press;

  //アナログ値を取得
  press = analogRead(ana_in);

  //コンソールに出力
  Serial.println(press);

  //アウトプットの設定
  if(press < on_border){
    digitalWrite(led_out,HIGH);
  }else{
    digitalWrite(led_out,LOW);
  }

}
