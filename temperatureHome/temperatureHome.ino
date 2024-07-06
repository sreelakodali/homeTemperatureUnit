/* Sreela Home Temperature Test 
*/

// Include the library:
#include <SparkFun_RHT03.h>
#include <EEPROM.h>

#define FSAMPLING 3600000
#define MAX_ADDR EEPROM.length()

const int RHT03_DATA_PIN = 4; // RHT03 data pin
RHT03 rht; // This creates a RTH03 object, which we'll use to interact with the sensor
int addr = 0;
bool COLLECT_DATA = true;
bool serialOn = !(COLLECT_DATA);
bool wEn = true;

void setup() {

  if (serialOn) Serial.begin(9600); // Serial is used to print sensor readings.
	rht.begin(RHT03_DATA_PIN);
  //clearEEPROM();
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if (addr < MAX_ADDR) {
    if (COLLECT_DATA) measureTemperatureWrite();
    else storedValuesRead();
    
  } else {
    blinkN(1,1000);
    if (serialOn) Serial.println("done");
  }
}


// additional functions

void clearEEPROM() {
  for (int i = 0 ; i < EEPROM.length() ; i++) {
    if (wEn) EEPROM.write(i, 0);
  }
}

void storedValuesRead() {
  unsigned long t;
  float f;

  if (wEn) EEPROM.get(addr, t);
  addr += sizeof(unsigned long);
  if (wEn) EEPROM.get(addr, f);
  addr += sizeof(float);

  if (serialOn) Serial.println(String(addr) + ", " + String(t) + ", " + String(f, 1));

  delay(500);
}

void blinkN(int n, int t_d) {
  for (int i = 0; i < n; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(t_d);
    digitalWrite(LED_BUILTIN, LOW);
    delay(t_d);
  }
}

void measureTemperatureWrite() {
    int updateRet = rht.update(); // gets new values from sensor
    int nMaxAttempts = 30;
    int nAttempts = 0;

    // if unsuccessful and haven't exceeded max attempts, try again
    while ( (updateRet != 1) and (nAttempts < nMaxAttempts)) {
      blinkN(2, 100);
      nAttempts = nAttempts + 1;
      delay(RHT_READ_INTERVAL_MS); // if failed, try delaying
      updateRet = rht.update();
    }

    // breaks out if successful or reached max attempts

    // if successful, get and write data in memory
    if (updateRet == 1) {    
      unsigned long t_elapsed = millis();
      float latestTempF = rht.tempF();
  
      if (wEn) EEPROM.put(addr, t_elapsed);
      addr += sizeof(unsigned long);
      if (wEn) EEPROM.put(addr, latestTempF);
      addr += sizeof(float);
      if (serialOn) Serial.println(String(addr) + ", " + String(t_elapsed) + ", " + String(latestTempF, 1));
      delay(FSAMPLING); 
    } 
}
