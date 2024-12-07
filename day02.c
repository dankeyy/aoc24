#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


int is_safe(int *numbers, int length, int skip_n) {
    int first = (skip_n == 0) ? 1 : 0;
    int second = (first + 1 == skip_n) ? first + 2 : first + 1;

    bool initial_order = (numbers[first] < numbers[second]);

    for (int i = 0; i < length; i++) {
        if (i == skip_n) {
            continue;
        }

        int l, r;

        if (i + 1 == skip_n) {
           l = i;
           r = i + 2;
        } else {
           l = i;
           r = i + 1;
        }

        if (r >= length) {
            continue;
        }

        bool maintaining_order = (numbers[l] < numbers[r]) == initial_order;
        int gapsize = abs(numbers[r] - numbers[l]);
        bool valid_gapsize = gapsize >= 1 && gapsize <= 3;
        if (!maintaining_order || !valid_gapsize) {
            return 0;
        }
    }
    return 1;
}


int main(void)
{
    FILE *fp = fopen("day02.txt", "r");
    char line[1024];

    int safes = 0;
    int safes_with_tolerance = 0;
    while(fgets(line, sizeof line, fp))
    {
        int numbers[1024];
        int count = 0;
        char *save_ptr;
        char *token;

        token = strtok_r(line, " ", &save_ptr);
        while (token != NULL) {
            numbers[count++] = atoi(token);
            token = strtok_r(NULL, " ", &save_ptr);
        }

        // Check for safety without skipping
        bool safe = is_safe(numbers, count, -1);
        if (safe) {
            safes++;
            safes_with_tolerance++;
        } else {
            for(int i = 0; i < count; i++) {
                if (is_safe(numbers, count, i)) {
                    safes_with_tolerance++;  // It became safe by removing element i
                    break;
                }
            }
        }
    }

    printf("%d\n", safes); // p1
    printf("%d\n", safes_with_tolerance); // p2
    fclose(fp);
}
