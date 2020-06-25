#include <WiFi.h>
#include <HTTPClient.h>
  
const char* ssid = "Redmi";
const char* password =  "1234567@";
  
void setup() {
  
  Serial.begin(115200);
  delay(4000);   //Delay needed before calling the WiFi.begin
  
  WiFi.begin(ssid, password); 
  
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
  
}
  
void loop() {

  int tempvalue = analogRead(34);
  String tempvalue_send = String(tempvalue);
  
  Serial.print("temp ");
  Serial.println(tempvalue);
  
 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
  
   HTTPClient http;   
  
   http.begin("https://robot.findx.lk/temp_update.php");  //Specify destination for HTTP request
   http.addHeader("Content-Type", "application/x-www-form-urlencoded");        //Specify content-type header
  
   String httpRequestData = "temp=" + tempvalue_send + "";  // send data
    Serial.print("httpRequestData: ");
    Serial.println(httpRequestData);

    int httpResponseCode = http.POST(httpRequestData);
  
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
   
  
 }else{
  
    Serial.println("Error in WiFi connection");   
  
 }
  
  delay(100);  //Send a request every 10 seconds
  
}
