#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>

void finish_with_error(MYSQL *con) {
    fprintf(stderr, "%s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

void print_datalog_fact(MYSQL_RES *result, const char *table_name) {
    unsigned int num_fields = mysql_num_fields(result);
    unsigned int num_rows = mysql_num_rows(result);
    bool is_string[num_fields];

    MYSQL_ROW row;
    MYSQL_FIELD *field;

    for (int i = 0; (row = mysql_fetch_row(result));) {
        printf("%s(%d, ", table_name, ++i);
        for (unsigned int j = 0; j < num_fields; j++) {
            if (!j) {  // headers
                int k = 0;
                while (field = mysql_fetch_field(result)) {
                    is_string[k++] = !IS_NUM(field->type);
                }
            } else {  // data
                if (is_string[j]) {
                    j == num_fields - 1 ? printf("'%s'", row[j] ? row[j] : "NULL")
                                        : printf("'%s', ", row[j] ? row[j] : "NULL");
                } else {
                    j == num_fields - 1 ? printf("%s", row[j] ? row[j] : "NULL")
                                        : printf("%s, ", row[j] ? row[j] : "NULL");
                }
            }
        }

        printf(").\n");
    }
}

/*
 * This code example generates datalog facts based on a MySQL table
 */
int main(int argc, char const *argv[]) {
    MYSQL *con = mysql_init(NULL);

    if (con == NULL) {
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

    print_datalog_fact(result, "cars");

    mysql_free_result(result);

    mysql_close(con);

    return 0;
}
