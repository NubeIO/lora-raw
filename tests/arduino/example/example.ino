char* payloads[] = {
    "AAB296C4E5094228BA0000EC0000009A2D64",
    "CCB22E0BE8071D28C48E00EBA04F2FE03C64",
    "9BB2A166E9081C28373900EA21D0CEE03C61",
};
const int PAYLOADS_LENGTH = sizeof(payloads) / sizeof(payloads[0]);

const int DELAY_MS = 4000;

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    delay(2000);
}

void loop() {

    for(int i = 0; i < PAYLOADS_LENGTH; i++){
         Serial.println(payloads[i]);
         delay(DELAY_MS);
    }
}
