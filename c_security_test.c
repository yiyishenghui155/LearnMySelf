#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_BUFFER 10

void buffer_overflow_vuln(char* user_input) {
    char buffer[MAX_BUFFER]; // 10 bytes buffer
    strcpy(buffer, user_input); 
    printf("Copied to buffer: %s\n", buffer);
}

void memory_leak_vuln() {
    int* data = (int*)malloc(10 * sizeof(int));
    if (data == NULL) {
        return;
    }
    printf("Memory block allocated and leaked.\n");
}

int integer_overflow_vuln(int count, int size) {
    int total_bytes = count * size; 
    return total_bytes;
}

void format_string_vuln(char* log_message) {
    printf(log_message); 
    printf("\n");
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input_string>\n", argv[0]);
        return 1;
    }

    buffer_overflow_vuln(argv[1]);

    memory_leak_vuln();

    int result = integer_overflow_vuln(INT_MAX, 2);
    printf("Integer overflow test result (should be negative): %d\n", result);

    format_string_vuln(argv[1]);

    return 0;
}