#include <ps2.h>

PS2 mouse(12, 14);

struct mouse_data {
  int x;
  int y;
  int stat;
  int tap;
};

/*
 * initialize the mouse. Reset it, and place it into remote
 * mode, so we can get the encoder data on demand.
 */
void mouse_init()
{
  mouse.write(0xff);  // reset
  mouse.read();  // ack byte
  mouse.read();  // blank */
  mouse.read();  // blank */
  mouse.write(0xf0);  // remote mode
  mouse.read();  // ack
  delayMicroseconds(100);
}

/*
 * get a reading from the mouse and report it back to the
 * host via the serial line.
 */
struct mouse_data read_mouse_data()
{
    struct mouse_data m;

    /* get a reading from the mouse */
    mouse.write(0xeb);  // give me data!
    mouse.read();      // ignore ack
    m.stat = mouse.read();
    m.x = int(mouse.read());
    m.y = int(mouse.read());

    m.tap = 0; //detect_tap(m.stat);

    // get directions:

    if (m.stat & 10000) // negative x
        m.x -= 255;

    if (m.stat & 100000) // negative y
        m.y -= 255;


    /* send the data back up */
    /*
    Serial.print("Stat = ");
    Serial.print(m.stat);
    Serial.print("\tX = ");
    Serial.print(m.x);
    Serial.print("\tY = ");
    Serial.print(m.y);
    Serial.println();
    delay(20);  /* twiddle */
    
    return m;
}
