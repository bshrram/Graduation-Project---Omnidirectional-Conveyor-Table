#include <Wire.h>
#include <cppQueue.h>
#define IMPLEMENTATION FIFO

Queue q(sizeof(int *), 100, IMPLEMENTATION);

void setup()
{
  for (int i = 2; i <= 53; i++)
  {
    if (i == 20 || i == 21)
      continue;
    pinMode(i, OUTPUT);
  }
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void receiveEvent(int howMany)
{
  int a[10], i = 0;
  while (Wire.available())
  {
    a[i++] = Wire.read();
  }
  int *b = a;
  q.push(&b);
}

/*handleMotor:
  Args: 
    a: array with pins & values
*/
void handleMotor(int a[])
{
  int code = a[0];
  /*code: int: 
      1: digital in slave, pwm in master
      2: digital & pwm in slave
      3: digital in master, pwm in slave
      4: digital & pwm in master
  */

  if (code == 1)
  {
    digitalWrite(a[1], a[2]);
    digitalWrite(a[1] - 1, !a[2]);
  }

  else if (code == 2)
  {
    digitalWrite(a[1], a[2]);
    digitalWrite(a[1] - 1, !a[2]);
    analogWrite(a[3], a[4]);
  }

  else if (code == 3)
  {
    analogWrite(a[1], a[2]);
  }
}

//*** loop
void loop()
{
  while (!q.isEmpty())
  {
    int *x;
    q.pop(&x);
    handleMotor(x);
  }
}
