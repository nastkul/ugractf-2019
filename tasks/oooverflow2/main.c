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
    char buffer[10];
    printf("Segfault v. 1.0\nCopyright 2019, OOO \"TP\"\n\nPress enter to start.");
    gets(buffer);
    printf("Press enter again.\n");
    gets(buffer);
    return 0;
}
