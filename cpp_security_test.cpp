#include <iostream>
#include <cstring>
#include <cstdlib>
#include <string>

#define BUFFER_SIZE 10

void bufferOverflowVuln(const char* input) {
    char buffer[BUFFER_SIZE];
    strcpy(buffer, input); 
    std::cout << "Vulnerable Buffer: " << buffer << std::endl;
}

void memoryLeakVuln() {
    int* data = new int[100];
    if (data == nullptr) return;

    data[0] = 1;
    std::cout << "Memory allocated and leaked." << std::endl;
}

int integerOverflowVuln(int a, int b) {
    return a + b; 
}

void formatStringVuln(const char* logMessage) {
    printf(logMessage); 
    printf("\n");
}

void bufferOverflowSafe(const char* input) {
    char buffer[BUFFER_SIZE];
    strncpy(buffer, input, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = '\0';
    std::cout << "Safe Buffer: " << buffer << std::endl;
}

int main_cwe_test(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_string>" << std::endl;
        return 1;
    }

    const char* user_input = argv[1];
    
    bufferOverflowVuln(user_input);
    memoryLeakVuln();
    int result = integerOverflowVuln(2147483647, 1); 
    formatStringVuln(user_input);

    bufferOverflowSafe(user_input);
    
    return 0;
}