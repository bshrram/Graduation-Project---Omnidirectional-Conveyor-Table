#include <Wire.h>
#include <cppQueue.h>
#define  IMPLEMENTATION  FIFO

Queue q(sizeof(int *), 100, IMPLEMENTATION);

void setup()
{
  pinMode (2 , OUTPUT);
  pinMode (3 , OUTPUT);
  pinMode (4 , OUTPUT);
  //-----4th
  pinMode (7 , OUTPUT);
  pinMode (6 , OUTPUT);
  pinMode (5 , OUTPUT);
  //-----5 th
  pinMode (10 , OUTPUT);
  pinMode (9 , OUTPUT);
  pinMode (8 , OUTPUT);
  //--- 6 th
  pinMode (13 , OUTPUT);
  pinMode (12 , OUTPUT);
  pinMode (11 , OUTPUT);
  //---------------------digital
  //-----first
  pinMode (48 , OUTPUT);
  pinMode (49 , OUTPUT);
  pinMode (50 , OUTPUT);
  pinMode (51 , OUTPUT);
  pinMode (52 , OUTPUT);
  pinMode (53 , OUTPUT);
  //-----secand
  pinMode (34 , OUTPUT);
  pinMode (35 , OUTPUT);
  pinMode (36 , OUTPUT);
  pinMode (37 , OUTPUT);
  pinMode (38 , OUTPUT);
  pinMode (47 , OUTPUT);
  //-----3th
  pinMode (28 , OUTPUT);
  pinMode (29 , OUTPUT);
  pinMode (30 , OUTPUT);
  pinMode (31 , OUTPUT);
  pinMode (32 , OUTPUT);
  pinMode (33 , OUTPUT);
  //-----4th
  pinMode (22 , OUTPUT);
  pinMode (23 , OUTPUT);
  pinMode (24 , OUTPUT);
  pinMode (25 , OUTPUT);
  pinMode (26 , OUTPUT);
  pinMode (27 , OUTPUT);
  Wire.begin(8); // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void receiveEvent(int howMany)
{
  int a[10], i = 0;
  while (Wire.available()) {
    a[i++] = Wire.read();
  }
  int *b = a;
  q.push(&b);
}

//*** cell handle
// @param x: array with 7 items [cellId, dig1, dig2, dig3, pwm1, pwm2, pwm3]
void handleCell(int a[]) {
  int Code = a[0];

  if (a[0] == 1)
  { digitalWrite(a[1], a[2]);
    digitalWrite(a[1] + 1, !a[2]);
  }

  else if (a[0] == 2)
  { analogWrite(a[1], a[2]);
    analogWrite(a[1] + 1, !a[2]);
  }
  else if (a[0] == 3)
  { digitalWrite(a[1], a[2]);
    digitalWrite(a[1] + 1, !a[2]);
    analogWrite(a[3], a[4]);
  }

}


//*** loop
void loop() {
  while (!q.isEmpty()) {
    int *x;
    q.pop(&x);
    handleCell(x);
  }
}
