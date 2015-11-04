
#include <ros.h>
#include <ArduinoHardware.h>

#define ANGLE_MAX -78
#define ANGLE_MIN 78

/*
 * rosserial Service Client
 */


#include <std_msgs/Bool.h>
#include <lift_msgs/SimulateLift.h>
#include <std_msgs/Empty.h>
#include <sensor_msgs/JointState.h>

// #include <rosserial_arduino/Test.h>

int ticker = 0;
int min_output_volt = (int)(255/5*2.35);
int max_output_volt = (int)(255/5*3.55);
int analogPinAngle = 5;

ros::NodeHandle  nh;
using lift_msgs::SimulateLift;

void angleCb( const sensor_msgs::JointState& angleMsg){
  int angle = angleMsg.position[0]*100;
  int mappedAngle = map(angle,ANGLE_MAX, ANGLE_MIN, min_output_volt, max_output_volt);
  analogWrite(analogPinAngle, mappedAngle);

}

SimulateLift::Request req;
SimulateLift::Response res;

ros::ServiceClient<SimulateLift::Request, SimulateLift::Response> client("Simulate_Lift");
ros::Subscriber<sensor_msgs::JointState> sub("joint_states", &angleCb );

std_msgs::Bool bool_msg; //convert to bool

char up[3] = "up";
char down[5] = "down";
int inPin = 2;
int adcInput;
int enableLift;

void setup()
{
  pinMode(13, OUTPUT);
  nh.initNode();
  nh.subscribe(sub);
  nh.serviceClient(client);
  while(!nh.connected()) nh.spinOnce();
  nh.loginfo("Startup complete");
}

//We average the analog reading to elminate some of the noise
int averageAnalog(int pin){
  int v=0;
  for(int i=0; i<4; i++) v+= analogRead(pin);
  return v/4;
}

void loop()
{
  adcInput = map(averageAnalog(0),0,1023,0,500);
  enableLift = digitalRead(inPin);
  if(adcInput > 300 && enableLift == HIGH)
  //if(adcInput > 3)
  {
      req.directionToMove = up;
      client.call(req, res);
      bool_msg.data = res.status;
  }
  else if(adcInput <= 200 && enableLift == LOW){
  //else if(adcInput <= 2){
      req.directionToMove = down;
      client.call(req, res);
      bool_msg.data = res.status;
  }
  else{
    req.directionToMove = "";
  }
  
  nh.spinOnce();
  delay(10);
}
