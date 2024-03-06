const topic = config.MQTT_TOPIC;
const broker = config.MQTT_IP;
let client;
let payload;

window.addEventListener("load", (event) => {
  let msg = document.getElementById("msg");
  let frameCounter = 0;
  const options = {
    clean: true,
    connectTimeout: 4000,
    port: config.MQTT_PORT,
    username: config.MQTT_USER,
    password: config.MQTT_PASSWORD,
  };
  client = mqtt.connect("ws://" + broker, options);
  client.on("connect", function () {
    msg.textContent = "Connected; Waiting for images...";
    client.subscribe(topic);
  });

  client.on("message", (topic, message) => {
    //var topic = topic;
    payload = message;

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



function send_to_database() {
  if (payload != undefined && payload.length > 0) {
    //console.log(client.connected);
    //console.log(client)
    let img = payload;
    // message = new Paho.MQTT.Message("Hello");
    // message.destinationName = "World";
    // client.send(message);
    client.publish
      ('db/image', img);
  }
}

function send_to_phone() {
  if (payload != undefined && payload.length > 0) {
    let img = payload;
    client.publish('phone/image', img);
  }
}

function detect_face(face) {
  if (payload != undefined && payload.length > 0) {
    console.log(face=="max_mustermann")
    if (face == "max_mustermann") {
      client.publish('face', "Max Mustermann");
      let img = payload;
      client.publish('phone/image', img);
    }
    else {
      client.publish('face', "unbekannte Person");
      let img = payload;
      client.publish('phone/image', img);
    }
  }
}