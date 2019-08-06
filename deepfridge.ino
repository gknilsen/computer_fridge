/* 
 * Python deep fridge backend
 * Author: Geir K. Nilsen <geir.kjetil.nilsen@gmail.com>
 */

// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include "DHT.h"

#define DHTPIN 7     // Digital pin connected to the DHT sensor
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
// Pin 15 can work but DHT must be disconnected during program upload.

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht(DHTPIN, DHTTYPE);
float t, h;
const int motor_input = A0;
const int motor_eject_in = 2;
const int motor_eject_out = 4;
int rack_eject_no_pulses = 1600;//385;
int count = 0;
int prev_val = 0;
int val = 0;
int progress = 0;
int prev_progress = -1;
int pulse = 0;

void setup() {
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(motor_input, INPUT);
  pinMode(motor_eject_in, OUTPUT);
  pinMode(motor_eject_out, OUTPUT);  
  Serial.begin(9600);

  dht.begin();
}

void loop() 
{

  while(!Serial.available()){}
  
  while(Serial.available())
  { 
    switch(Serial.read())
    {
      case 't':
        // Read temperature as Celsius (the default)
        t = dht.readTemperature();

        // Check if any reads failed and exit early (to try again).
        if (isnan(t)) 
        {
          Serial.println(F("E"));
          return;
        }
        Serial.println(t);
        break;

     case 'h':
       // Reading temperature or humidity takes about 250 milliseconds!
       // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
       h = dht.readHumidity();

        if (isnan(h)) 
        {
          Serial.println(F("E"));
          return;
        }
       Serial.println(h);
       break;

     // set comp off
     case '0':
       digitalWrite(13, LOW);
     break;

     // set comp on
     case '1':
       digitalWrite(13, HIGH);
     break;

     // set light on
     case '2':
       digitalWrite(12, LOW);
     break;

     // set light off
     case '3':
       digitalWrite(12, HIGH);
     break;

     case '4': // eject rack out
      digitalWrite(motor_eject_in, LOW); 
      digitalWrite(motor_eject_out, HIGH); // activate motor eject out
      
      pulse = 0;
      progress = 0;
      prev_progress = -1;
      prev_val = analogRead(motor_input);
      while(1)
      {
        val = analogRead(motor_input);

        if(abs(val - prev_val) > 75)
          pulse++;

        prev_val = val;
        delay(10); // Delay for stability.

        progress = (int) ((float)pulse * 10.0f) / (float)rack_eject_no_pulses;

        if(progress != prev_progress)
           Serial.println(progress);

        prev_progress = progress;
        
        if(pulse >= rack_eject_no_pulses)
        {
          digitalWrite(motor_eject_out, LOW); // deactivate motor eject out
          digitalWrite(motor_eject_in, LOW);           
          break;
        }
        
      }
      break;

    case '5': // eject rack in
      digitalWrite(motor_eject_out, LOW); // activate motor eject in
      digitalWrite(motor_eject_in, HIGH); 
      
      pulse = 0;
      progress = 0;
      prev_progress = -1;
      prev_val = analogRead(motor_input);
      while(1)
      {
        val = analogRead(motor_input);

        if(abs(val - prev_val) > 75)
          pulse++;

        prev_val = val;
        delay(10); // Delay for stability.

        progress = (int) ((float)pulse * 10.0f) / (float)rack_eject_no_pulses;       

        if(progress != prev_progress)
          Serial.println(progress);

        prev_progress = progress;

       
        if(pulse >= rack_eject_no_pulses)
        {
          digitalWrite(motor_eject_out, LOW); // deactivate motor eject in
          digitalWrite(motor_eject_in, LOW);           
          break;
        }
      }
      break;

      //////


    case '9': // eject rack in just a bit
      digitalWrite(motor_eject_out, LOW); // activate motor eject in
      digitalWrite(motor_eject_in, HIGH); 
      
      pulse = 0;
      progress = 0;
      prev_progress = -1;
      prev_val = analogRead(motor_input);
      while(1)
      {
        val = analogRead(motor_input);

        if(abs(val - prev_val) > 75)
          pulse++;

        prev_val = val;
        delay(10); // Delay for stability.

        progress = (int) ((float)pulse * 10.0f) / (float)10.0;       

        if(progress != prev_progress)
          Serial.println(progress);

        prev_progress = progress;

       
        if(pulse >= rack_eject_no_pulses)
        {
          digitalWrite(motor_eject_out, LOW); // deactivate motor eject in
          digitalWrite(motor_eject_in, LOW);           
          break;
        }
      }
      break;


      case '6':
        digitalWrite(motor_eject_out, LOW);
        digitalWrite(motor_eject_in, HIGH);
      break;
      
      case '7':
        digitalWrite(motor_eject_in, LOW);
        digitalWrite(motor_eject_out, HIGH);
      break;

      case '8':
        digitalWrite(motor_eject_in, LOW);
        digitalWrite(motor_eject_out, LOW);
      break;

     default:
     break;
         
    }
  
 }
}
