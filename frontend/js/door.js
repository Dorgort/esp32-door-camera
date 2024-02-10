const topic = config.MQTT_DOOR_TOPIC;
const broker = config.MQTT_IP;



window.addEventListener("load", (event) => {
    let icon = document.getElementById("icon");
    let msg = document.getElementById("msg");

    const options = {
        clean: true,
        connectTimeout: 4000,
        port: config.MQTT_PORT, // Secure websocket port
        username: config.MQTT_USER,
        password: config.MQTT_PASSWORD,
    };
    const client = mqtt.connect("mqtt://" + broker, options);

    client.on("connect", function () {
        icon.setAttribute('class', 'fa-solid fa-door-closed');
        msg.textContent = "Door locked."
        client.subscribe(topic);
    });

    client.on("message", (topic, message) => {
        //var topic = topic;

        const decoder = new TextDecoder('utf-8'); // Specify the encoding, utf-8 is commonly used
        let payload = decoder.decode(message);
        console.log(payload== "true")
        if (payload == "true") {
            icon.setAttribute('class', 'fa-solid fa-door-open');
            timer = 20
            while (timer > 0) {
                console.log(timer)
                msg.textContent = `Door open for  ${timer} seconds`;
                timer--;
            }
            client.publish('face', 'false');
            
        }
        else {
            icon.setAttribute('class', 'fa-solid fa-door-closed');
            msg.textContent = "Door locked."
        }
    });
});
