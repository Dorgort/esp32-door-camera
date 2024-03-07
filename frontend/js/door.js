const topic = config.MQTT_DOOR_TOPIC;
const broker = config.MQTT_IP;
const open_door_time = 10;
let remaining_door_open_time = open_door_time;
let is_door_open = false;

window.addEventListener("load", (event) => {
    let icon = document.getElementById("icon");
    let msg = document.getElementById("msg");


    const options = {
        clean: true,
        connectTimeout: 4000,
        port: config.MQTT_PORT,
        username: config.MQTT_USER,
        password: config.MQTT_PASSWORD,
    };
    const client = mqtt.connect("wss://" + broker, options);

    client.on("connect", function () {
        icon.setAttribute('class', 'fa-solid fa-door-closed');
        msg.textContent = "Tür verschlossen."
        client.subscribe(topic);
    });

    client.on("message", (topic, message) => {
        //var topic = topic;

        const decoder = new TextDecoder('utf-8'); // Specify the encoding, utf-8 is commonly used
        let payload = decoder.decode(message);
        console.log(payload);
        //console.log(payload== "Max Mustermann");
        if (payload == "offen" && !is_door_open) {
            is_door_open = true;
            icon.setAttribute('class', 'fa-solid fa-door-open');
            // Interval 1000ms Funktionsaufruf
            let interval = setInterval(reduce_remaining_door_open_time, 1000);
            //Ruft doorclose auf wenn 2. Variable (timeout) abläuft
            const timeout = setTimeout(door_close, (open_door_time+1)*1000, client, interval);
            
        }
        else {
            icon.setAttribute('class', 'fa-solid fa-door-closed');
            msg.textContent = "Tür verschlossen."
        }
    });
});

function door_close(client, interval){
    console.log("Türe zu!")
    msg.textContent = "Tür verschlossen.";
    client.publish('door', 'verschlossen');
    clearInterval(interval);
    is_door_open = false;
}

function reduce_remaining_door_open_time(){
    if (remaining_door_open_time < 0){
        return
    }
    console.log(remaining_door_open_time);
    msg.textContent = `Tür für ${remaining_door_open_time} Sekunden offen`;
    remaining_door_open_time--;
}