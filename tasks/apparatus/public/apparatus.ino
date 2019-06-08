int reg = 0;
int state = 0;

int REG[16] = {1, 11, 14, 7, 8, 3, 15, 9, 12, 2, 13, 10, 5, 4, 0, 6};

void setup() {
  pinMode(4, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  pinMode(13, INPUT_PULLUP);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A5, INPUT_PULLUP);
}

void loop() {
  int new_state = ((!digitalRead(2)) << 11) |
                  ((!digitalRead(6)) << 10) |
                  ((!digitalRead(7)) << 9) |
                  ((!digitalRead(9)) << 8) |
                  ((!digitalRead(12)) << 7) |
                  ((!digitalRead(13)) << 6) |
                  ((!digitalRead(A0)) << 5) |
                  ((!digitalRead(A1)) << 4) |
                  ((!digitalRead(A2)) << 3) |
                  ((!digitalRead(A3)) << 2) |
                  ((!digitalRead(A4)) << 1) |
                  ((!digitalRead(A5)));

  if (new_state != state) {
    int p2 = -1;
    for (int p = 0; p < 12; ++p) {
      if ((new_state >> p) == 1) {
        p2 = p;
      }
    }
    if (new_state && p2 != -1) {
      reg ^= REG[p2];
      digitalWrite(8, 1);
      digitalWrite(4, 1);
      digitalWrite(11, 1);
      digitalWrite(10, 1);
      delay(200);
      digitalWrite(8, reg & 1);
      digitalWrite(4, reg & 2);
      digitalWrite(11, reg & 4);
      digitalWrite(10, reg & 8);
      delay(500);
    } else {
      digitalWrite(8, 0);
      digitalWrite(4, 0);
      digitalWrite(11, 0);
      digitalWrite(10, 0);
    }
    state = new_state;
    delay(200);
  }
}
