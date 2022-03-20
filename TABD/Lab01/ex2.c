#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>

void finish_with_error(MYSQL *con) {
    fprintf(stderr, "%s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

void my_dump(MYSQL_RES *result, int create_table) {
    MYSQL_FIELD *fields = mysql_fetch_fields(result);
    unsigned int num_fields = mysql_num_fields(result);
    const char *field_names[num_fields];
    bool is_numeric[num_fields];
    const char *table_name = (*fields).table;

    for (unsigned int i = 0; i < num_fields; i++) {
        field_names[i] = fields[i].name;
        is_numeric[i] = IS_NUM(fields[i].type);
    }

    if (create_table) {
        printf("CREATE TABLE %s(", table_name);
        for (unsigned int i = 0; i < num_fields; i++) {
            if (!i) {  // 1st column is the key
                is_numeric[i]
                    ? printf("%s INT PRIMARY KEY AUTO_INCREMENT, ", field_names[i])
                    : printf("%s VARCHAR(255) PRIMARY KEY AUTO_INCREMENT, ", field_names[i]);
            } else {
                if (is_numeric[i]) {
                    i == num_fields - 1 ? printf("%s INT", field_names[i])
                                        : printf("%s INT, ", field_names[i]);
                } else {
                    i == num_fields - 1 ? printf("%s VARCHAR(255)", field_names[i])
                                        : printf("%s VARCHAR(255), ", field_names[i]);
                }
            }
        }
        printf(")\n");
    }

    MYSQL_ROW row;
    while (row = mysql_fetch_row(result)) {
        printf("INSERT INTO %s VALUES(", table_name);
        for (unsigned int i = 0; i < num_fields; i++) {
            if (is_numeric[i]) {
                i == num_fields - 1 ? printf("%s)\n", row[i] ? row[i] : "NULL")
                                    : printf("%s, ", row[i] ? row[i] : "NULL");
            } else {
                i == num_fields - 1 ? printf("'%s')\n", row[i] ? row[i] : "NULL")
                                    : printf("'%s', ", row[i] ? row[i] : "NULL");
            }
        }
    }
}

/*
 * Uses the testdb database from the previous examples
 */
int main(int argc, char const *argv[]) {
    MYSQL *con = mysql_init(NULL);

    if (!con) {
        fprintf(stderr, "%s\n", mysql_error(con));
        exit(1);
    }

    if (mysql_real_connect(con, "localhost", "root", "root_passwd", "testdb", 0, NULL, 0) == NULL) {
        finish_with_error(con);
    }

    if (mysql_query(con, "SELECT * FROM cars")) {
        finish_with_error(con);
    }

    MYSQL_RES *result = mysql_store_result(con);

    if (!result) {
        finish_with_error(con);
    }

    my_dump(result, 1);

    mysql_free_result(result);

    mysql_close(con);

    return 0;
}
