#include <ctype.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include "token.h"

char* slice_string(const char* str, int start, int end) {
    if (str == NULL) {
        return NULL;
    }

    int str_len = strlen(str);

    if (start < 0) {
        start = str_len + start;
    }
    if (end < 0) {
        end = str_len + end;
    }

    start = (start < 0) ? 0 : start;
    end = (end > str_len) ? str_len : end;

    if (start >= end) {
        return strdup("");
    }

    int slice_len = end - start;
    char* slice = malloc(slice_len + 1);

    strncpy(slice, str + start, slice_len);
    slice[slice_len] = '\0';

    return slice;
}

bool ends_with(const char* str, const char* substr) {
    int strLen = strlen(str);
    int subStrLen = strlen(substr);
    if (strLen < subStrLen) {
        return false;
    }

    const char* suffixStart = str + (strLen - subStrLen);
    return strcmp(suffixStart, substr) == 0;
}

bool ends_with2(const char* str, const char* substr) {
    int str_len = strlen(str);
    int substr_len = strlen(substr);
    char* slice = slice_string(str, str_len - substr_len, str_len);
    return strcmp(slice, substr) == 0;
}

char** collect_matches(int argc, char* argv[], char* match, size_t* match_count) {
    char** matches = NULL;
    size_t count = 0;
    size_t capacity = 0;
    for (int i = 0; i < argc; i++) {
        const char* str = argv[i];
        if (ends_with2(str, match)) {
            if (count == capacity) {
                capacity = (capacity == 0) ? 4 : capacity * 2; 

                char** new_matches = realloc(matches, capacity * sizeof(char*));

                if (new_matches == NULL) {
                    perror("Failed to allocate new memory");
                    free(matches);
                    *match_count = 0;
                    return NULL;
                }
                matches = new_matches;
            }
            matches[count] = (char*)str;
            count++;
        }
    }
    *match_count = count;

    return matches;
}

int main(int argc, char* argv[]) {
    size_t match_count = 0;
    char** nuts_files = collect_matches(argc, argv, ".nuts", &match_count);
    for (int i = 0; i < match_count; i++) {
        printf("NUTS file: %s\n", nuts_files[i]);
    }
    free(nuts_files);

    FILE *fptr = fopen("../examples/hello.nuts", "r");
    char data[50];
    if (fptr == NULL) {
        printf("The file couldn't be opened.");
        return -1;
    }
    while(fgets(data, 50, fptr) != NULL) {
        printf("%s", data);
    }
    fclose(fptr);
    return 0;
}
