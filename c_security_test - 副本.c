
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_BUFFER 10

void buffer_overflow_vuln(char* user_input) {
    char buffer[MAX_BUFFER];
    strcpy(buffer, user_input); 
}
