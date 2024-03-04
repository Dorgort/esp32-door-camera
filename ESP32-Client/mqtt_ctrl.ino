void send_data(String text) {
  if (mqtt.isConnected()) {
    mqtt.publish(MQTT_PUBLISH_TOPIC, text.c_str());
  } else {
    Serial.print("failed, not connected, while trying to publish");
  }
}
