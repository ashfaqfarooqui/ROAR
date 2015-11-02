
#include <ros.h>
#include <ArduinoHardware.h>


/*
 * rosserial Service Client
 */


#include <std_msgs/Bool.h>
#include <lift_msgs/SimulateLift.h>
// #include <rosserial_arduino/Test.h>

ros::NodeHandle  nh;
using lift_msgs::SimulateLift;

ros::ServiceClient<SimulateLift::Request, SimulateLift::Response> client("Simulate_Lift");

std_msgs::Bool bool_msg; //convert to bool

char up[3] = "up";
char down[5] = "down";
int inPin = 2;

void setup()
{
  nh.initNode();
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
  int adcInput;
  adcInput = map(averageAnalog(0),0,1024,0,5);
  int enableLift = digitalRead(inPin);
  if(adcInput > 3 && enableLift == HIGH)
  {
      SimulateLift::Request req;
      SimulateLift::Response res;
      req.directionToMove = up;
      client.call(req, res);
      bool_msg.data = res.status;
  }
  else if(adcInput <= 2 && enableLift == LOW){
      SimulateLift::Request req;
      SimulateLift::Response res;
      req.directionToMove = down;
      client.call(req, res);
      bool_msg.data = res.status;
  }
  
  nh.spinOnce();
  delay(100);
}
