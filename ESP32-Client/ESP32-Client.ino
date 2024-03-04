#include <WiFi.h>
#include <WebSocketsClient.h>  // include before MQTTPubSubClient.h
#include <MQTTPubSubClient.h>
//#include "soc/soc.h"
#include "esp_camera.h"
#include "Base64.h"
#include "camera_pins.h"
#include "secrets.h"


WebSocketsClient client;
MQTTPubSubClient mqtt;

String image = "";


void setup() {
  Serial.begin(115200);

  initCamera();
  WiFi.begin(ssid, password);
  mqtt.begin(client);
  connect();
}

void loop() {
  mqtt.update(); //Should be called
  
  if (!mqtt.isConnected()) {
    connect();
  }
  static uint32_t prev_ms = millis();
  if (millis() > prev_ms + 1000) {
    prev_ms = millis();
    image = record_image();
    send_data(image);
  }

}


void connect() {
connect_to_wifi:
    Serial.print("connecting to wifi...");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println(" connected!");

connect_to_host:
    Serial.println("connecting to host...");
    client.disconnect();
    client.begin(mqtt_server, mqtt_port, "/", "mqtt");  // "mqtt" is required
    client.setReconnectInterval(2000);

    Serial.print("connecting to mqtt broker...");
    String client_ID = "ESP32-";
    client_ID += String(random(0xffff), HEX);
    while (!mqtt.connect(client_ID, MQTT_USER, MQTT_PASSWORD)) {
        Serial.print(".");
        delay(1000);
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("WiFi disconnected");
            goto connect_to_wifi;
        }
        if (!client.isConnected()) {
            Serial.println("WebSocketsClient disconnected");
            goto connect_to_host;
        }
    }
    Serial.println(" connected!");
}
