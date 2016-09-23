int counter = 0;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(counter > 100){
    counter = 0;
  }
  
  Serial.println(counter);
  counter += 1;
}
