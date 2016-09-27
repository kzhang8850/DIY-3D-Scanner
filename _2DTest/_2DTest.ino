
int degreelist[360];
int circle = 5;
String stuff;

int counter = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i =0;i < 360; i++){
    degreelist[i] = i;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(counter < 360){
    stuff = String(circle) + ", " + String(degreelist[counter]);
    Serial.println(stuff);
    
  }
  else{
    counter = 0;
    
  }
  counter++;
  delay(100);
}
