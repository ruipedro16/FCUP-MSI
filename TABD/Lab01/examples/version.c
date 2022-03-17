#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>

/*
 * This code example shows the MySQL client version 
 */
int main(int argc, char **argv) {
    printf("MySQL client version: %s\n", mysql_get_client_info());
    exit(0);
}
