const topic = "/camera";
const broker = config.MQTT_IP;

window.addEventListener("load", (event) => {
  let img = document.getElementById("image");
  let msg = document.getElementById("msg");
  let frameCounter = 0;
  const options = {
    clean: true,
    connectTimeout: 4000,
    port: config.MQTT_PORT, // Secure websocket port
    username: config.MQTT_USER,
    password: config.MQTT_PASSWORD,
  };
  const client = mqtt.connect("mqtt://" + broker, options);

  client.on("connect", function () {
    msg.textContent = "Connected; Waiting for images...";
    client.subscribe(topic);
  });

  client.on("message", (topic, message) => {
    var topic = topic;
    var payload = message;
  
    if (payload != undefined && payload.length > 0) {
      $("img").attr("src", payload);
    }
    //const blob = new Blob([message], { type: "data:image/jpeg;base64" });
    //img.src = URL.createObjectURL(blob);
    //console.log(blob);
    frameCounter++;
    msg.textContent = `Frames: ${frameCounter}`;
  });
});
