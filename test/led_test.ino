//デジタル出力のポート番号
const int led_out = 7;
//アナログ入力のポート番号
const int ana_in = 0;
//シリアルポート番号
const int Serialnumber = 9800;
//アナログ入力値のしきい値
const int put_border = 1010;
//乗っているかどうかの判定
bool put_flag = false;

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

  //置かれたことの判定
  if(put_flag==false && press < put_border){
    digitalWrite(led_out,HIGH);
    put_flag = true;
  }

  //取られたことの判定
  if(put_flag && press >= put_border){
    digitalWrite(led_out,LOW);
    put_flag = false;
  }
  
}
