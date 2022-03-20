#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned int max(unsigned int a, unsigned int b) { return a > b ? a : b; }

void finish_with_error(MYSQL *con) {
    fprintf(stderr, "%s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

void print_row(MYSQL_ROW row, const unsigned int *column_width, unsigned int num_fields,
               bool *is_numeric) {
    putchar('|');
    for (int i = 0; i < num_fields; i++) {
        if (is_numeric[i]) {  // right aligned
            for (int j = 0; j < column_width[i] - strlen(row[i]) - 1; j++) {
                putchar(' ');
            }
            printf("%s |", row[i] ? row[i] : "NULL");
        } else {  // left aligned
            putchar(' ');
            printf("%s", row[i] ? row[i] : "NULL");
            for (int j = 0; j < column_width[i] - strlen(row[i]) - 1; j++) {
                putchar(' ');
            }
            putchar('|');
        }
    }
    putchar('\n');
}

/*
 * Strings are left aligned and numeric values are right aligned
 */
void print_result_set(MYSQL_RES *result) {
    unsigned int num_fields = mysql_num_fields(result);
    bool is_numeric[num_fields];
    unsigned int column_width[num_fields];

    MYSQL_ROW row;
    MYSQL_FIELD *fields = mysql_fetch_fields(result);

    for (int i = 0; i < num_fields; i++) {
        is_numeric[i] = IS_NUM(fields[i].type);
        column_width[i] = max(fields[i].max_length / sizeof(char), strlen(fields[i].name)) + 2;
    }

    for (int i = 0; row = mysql_fetch_row(result); i++) {
        if (!i) {
            // top line
            putchar('+');
            for (int j = 0; j < num_fields; j++) {
                for (int k = 0; k < column_width[j]; k++) {
                    putchar('-');
                }
                putchar('+');
            }
            putchar('\n');

            // field names
            for (int k = 0; k < num_fields; k++) {
                printf("| %s", fields[k].name);
                for (int m = 0; m < column_width[k] - 1 - strlen(fields[k].name); m++) {
                    putchar(' ');
                }
            }
            puts("|");

            // bottom line
            putchar('+');
            for (int j = 0; j < num_fields; j++) {
                for (int k = 0; k < column_width[j]; k++) {
                    putchar('-');
                }
                putchar('+');
            }
            putchar('\n');

            // 1st row
            print_row(row, column_width, num_fields, is_numeric);
        } else {
            print_row(row, column_width, num_fields, is_numeric);
        }
    }

    // bottom line
    putchar('+');
    for (int j = 0; j < num_fields; j++) {
        for (int k = 0; k < column_width[j]; k++) {
            putchar('-');
        }
        putchar('+');
    }
    putchar('\n');
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

    print_result_set(result);

    mysql_free_result(result);

    mysql_close(con);

    return 0;
}
