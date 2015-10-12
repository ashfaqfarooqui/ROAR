/*
 * rosserial Service Client
 */

#include <ros.h>
#include <std_msgs/Bool.h>
#include <lift_msgs/SimulateLift.h>
// #include <rosserial_arduino/Test.h>

ros::NodeHandle  nh;
using lift_msgs::SimulateLift;

ros::ServiceClient<SimulateLift::Request, SimulateLift::Response> client("Simulate_Lift");

std_msgs::Bool bool_msg; //convert to bool
// ros::Publisher chatter("chatter", &str_msg);

char up[3] = "up";
char down[5] = "down";

void setup()
{
  nh.initNode();
  nh.serviceClient(client);
  // nh.advertise(chatter);
  while(!nh.connected()) nh.spinOnce();
  nh.loginfo("Startup complete");
}

void loop()
{
  SimulateLift::Request req;
  SimulateLift::Response res;
  req.directionToMove = up;
  client.call(req, res);
  bool_msg.data = res.status;
  // chatter.publish( &str_msg );
  nh.spinOnce();
  delay(100);
}