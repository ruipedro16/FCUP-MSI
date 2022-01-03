#include <dirent.h>
#include <stdio.h>

int main(void) {
    int c;
    FILE *file;
    if ((file = fopen("flag.txt", "r"))) {
        while ((c = getc(file)) != EOF) {
            putchar(c);
        }
        fclose(file);
    }
    return (0);
}
