#ifndef touchpad_h
#define touchpad_h

struct mouse_data {
  int x;
  int y;
  int stat;
  int tap;
  int double_tap;
};

void mouse_init();
struct mouse_data read_mouse_data();

#endif