#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void print_flag() {
    char ch;
    FILE *fp = fopen("flag.txt", "r");
    while ((ch = fgetc(fp)) != EOF) {
        printf("%c", ch);
    }
    fclose(fp);
    fflush(stdout);
}

int main() {
    char buffer[50];
    printf("Segfault v. 1.0\nCopyright 2019, OOO \"TP\"\n\nWhat's your name?\n");
    fflush(stdout);
    gets(buffer);
    printf("Hello, ");
    printf(buffer);
    printf("\n");
    printf("Do you agree to collect your personal data?\n");
    fflush(stdout);
    gets(buffer);
    printf("It doesn't matter.\n");
    fflush(stdout);
    return 0;
}
