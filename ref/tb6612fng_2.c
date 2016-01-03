//Configure these to fit your design...
#define out_STBY 5
#define out_B_PWM 3
#define out_A_PWM 11
#define out_A_IN2 9
#define out_A_IN1 10
#define out_B_IN1 8
#define out_B_IN2 7
#define motor_A 0
#define motor_B 1
#define motor_AB 2

void setup()
{
 pinMode(out_STBY,OUTPUT);
 pinMode(out_A_PWM,OUTPUT);
 pinMode(out_A_IN1,OUTPUT);
 pinMode(out_A_IN2,OUTPUT);
 pinMode(out_B_PWM,OUTPUT);
 pinMode(out_B_IN1,OUTPUT);
 pinMode(out_B_IN2,OUTPUT);

 motor_standby(false);
 motor_speed2(motor_A,-100);
 motor_speed2(motor_B,-100);
 delay(2000);
 for (int i=-100; i<100; i++) {
   motor_speed2(motor_A,i);
   motor_speed2(motor_B,i);
   delay(50);
 }
 delay(2000);
 motor_standby(true);
}

void loop()
{
 byte data, length, motor, command; //0-255
 char speed; //-128-128
 data = Serial.available();
 if (data > 0) {
   length = Serial.read();
   while (data < length-1) { //wait until we got everything
     data = Serial.available(); delay(20); //todo: add timeout
   }
   command = Serial.read();
   switch (command) {
     case 0: //speed
       motor = Serial.read();
       speed = Serial.read();
       if (motor == motor_AB) {
         motor_speed2(motor_A,speed);
         motor_speed2(motor_B,speed);
       } else {
         motor_speed2(motor,speed);
       }
       break;
     case 1: //brake
       motor = Serial.read();
       if (motor == motor_AB) {
         motor_brake(motor_A);
         motor_brake(motor_B);
       } else {
         motor_brake(motor);
       }
       break;
     case 2: //coast
       motor = Serial.read();
       if (motor == motor_AB) {
         motor_coast(motor_A);
         motor_coast(motor_B);
       } else {
         motor_coast(motor);
       }
       break;
     case 3: //standby
       motor_standby(Serial.read());
       break;
   }
 }
}

void motor_speed2(boolean motor, char speed) { //speed from -100 to 100
 byte PWMvalue=0;
 PWMvalue = map(abs(speed),0,100,50,255); //anything below 50 is very weak
 if (speed > 0)
   motor_speed(motor,0,PWMvalue);
 else if (speed < 0)
   motor_speed(motor,1,PWMvalue);
 else {
   motor_coast(motor);
 }
}
void motor_speed(boolean motor, boolean direction, byte speed) { //speed from 0 to 255
 if (motor == motor_A) {
   if (direction == 0) {
     digitalWrite(out_A_IN1,HIGH);
     digitalWrite(out_A_IN2,LOW);
   } else {
     digitalWrite(out_A_IN1,LOW);
     digitalWrite(out_A_IN2,HIGH);
   }
   analogWrite(out_A_PWM,speed);
 } else {
   if (direction == 0) {
     digitalWrite(out_B_IN1,HIGH);
     digitalWrite(out_B_IN2,LOW);
   } else {
     digitalWrite(out_B_IN1,LOW);
     digitalWrite(out_B_IN2,HIGH);
   }
   analogWrite(out_B_PWM,speed);
 }
}
void motor_standby(boolean state) { //low power mode
 if (state == true)
   digitalWrite(out_STBY,LOW);
 else
   digitalWrite(out_STBY,HIGH);
}
void motor_brake(boolean motor) {
 if (motor == motor_A) {
   digitalWrite(out_A_IN1,HIGH);
   digitalWrite(out_A_IN2,HIGH);
 } else {
   digitalWrite(out_B_IN1,HIGH);
   digitalWrite(out_B_IN2,HIGH);
 }
}
void motor_coast(boolean motor) {
 if (motor == motor_A) {
   digitalWrite(out_A_IN1,LOW);
   digitalWrite(out_A_IN2,LOW);
   digitalWrite(out_A_PWM,HIGH);
 } else {
   digitalWrite(out_B_IN1,LOW);
   digitalWrite(out_B_IN2,LOW);
   digitalWrite(out_B_PWM,HIGH);
 }
}