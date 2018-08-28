#include <ps2.h>

#define unsigned int DOUBLE_TAP_INTERVAL = 300;

struct mouse_data {
  int x;
  int y;
  int stat;
  int tap;
  int double_tap;
};

enum TapStatus
{ 
    untouched,
    first_tapped,
    first_tapped_released,
    double_tap_detected
};

PS2 mouse(12, 14);

TapStatus tapStatus = untouched;
unsigned long tapStartTime = 0;


/*
 * Initialize the mouse. Reset it, and place it into remote
 * mode, so we can get the encoder data on demand.
 */
void mouse_init()
{
  mouse.write(0xff);  // reset
  mouse.read();       // ack byte
  mouse.read();       // blank 
  mouse.read();       // blank 
  mouse.write(0xf0);  // remote mode
  mouse.read();       // ack
  delayMicroseconds(100);
}


int detect_taps(int stat)
{
    switch (tapStatus)
    {
        case untouched:
            if (stat == 9)
            {
                tapStatus = first_tapped;
                tapStartTime = millis();
            }
            break;

        case first_tapped:
            if (stat != 9)
                tapStatus = first_tapped_released;
            break;

        case first_tapped_released:
            if (stat != 9 && millis() - tapStartTime > DOUBLE_TAP_INTERVAL)
            {
                // Single tap detected
                tapStatus = untouched;
                return 1;
            }

            if (stat == 9 && millis() - tapStartTime < DOUBLE_TAP_INTERVAL)
            {
                // Double tap detected
                tapStatus = double_tap_detected;
                return 2;
            }
            
            break;

        case double_tap_detected:
            if (stat != 9)
                tapStatus = untouched;
            break;
    }
    return 0;
}

/*
 * Get a reading from the mouse, determine swiping directions and detect taps.
 */
struct mouse_data read_mouse_data()
{
    struct mouse_data m;

    // Get a reading from the mouse
    mouse.write(0xeb);  // give me data!
    mouse.read();      // ignore ack
    m.stat = mouse.read();
    m.x = int(mouse.read());
    m.y = int(mouse.read());

    // Detect taps and double taps
    int tap = detect_taps(m.stat);
    m.tap = tap == 1;
    m.double_tap = tap == 2;    

    // Determine directions:
    if (m.stat & 10000) // negative x
        m.x -= 255;

    if (m.stat & 100000) // negative y
        m.y -= 255;
    
    return m;
}
