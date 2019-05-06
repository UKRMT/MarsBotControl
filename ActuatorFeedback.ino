#define LeftDig A1
#define RightDig A6
int LeftDigPos=0;
int RightDigPos=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(LeftDig, OUTPUT);
  pinMode(RightDig, OUTPUT); 
}

void loop() {
  LeftDigPos=analogRead(LeftDig);
  RightDigPos=analogRead(RightDig);
  Serial.println("right: "+ String(RightDigPos)+"left: " + String(LeftDigPos));
}
