#include "stdio.h"
#include <unistd.h>

int counter = 0;

int simple_function(void){
  counter++;
  sleep(1);
  return counter;
}

int simple_timer(int x){
  sleep(x);
  counter++;
  return counter;
}

int main(void){
  while (1){
    simple_timer(3);
    printf("test %d \n", counter);
  }
  return 0;
}