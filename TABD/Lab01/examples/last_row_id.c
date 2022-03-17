#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>

void finish_with_error(MYSQL *con) {
    fprintf(stderr, "%s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

/*
 * This code example determine the last inserted row id by calling the mysql_insert_id() function.
 * The function only works if we have defined an AUTO_INCREMENT column in the table.
 */
int main(int argc, char **argv) {
    MYSQL *con = mysql_init(NULL);

    if (con == NULL) {
        fprintf(stderr, "mysql_init() failed\n");
        exit(1);
    }

    if (mysql_real_connect(con, "localhost", "root", "root_passwd", "testdb", 0, NULL, 0) == NULL) {
        finish_with_error(con);
    }

    if (mysql_query(con, "DROP TABLE IF EXISTS writers")) {
        finish_with_error(con);
    }

    char *sql = "CREATE TABLE writers(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))";

    if (mysql_query(con, sql)) {
        finish_with_error(con);
    }

    if (mysql_query(con, "INSERT INTO writers(name) VALUES('Leo Tolstoy')")) {
        finish_with_error(con);
    }

    if (mysql_query(con, "INSERT INTO writers(name) VALUES('Jack London')")) {
        finish_with_error(con);
    }

    if (mysql_query(con, "INSERT INTO writers(name) VALUES('Honore de Balzac')")) {
        finish_with_error(con);
    }

    int id =
        mysql_insert_id(con);  // mysql_insert_id() function returns the value generated for an
                               // AUTO_INCREMENT column by the previous INSERT or UPDATE statement.

    printf("The last inserted row id is: %d\n", id);

    mysql_close(con);
    exit(0);
}
