from db_utils import db_connect
from random import *
import time


def db_drop_benchmark_table(connection) -> None:
    cur = connection.cursor()
    cur.execute('DROP TABLE benchmark')


def db_init_benchmark_table(connection) -> None:
    cur = connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS benchmark '
                '('
                'benchmark_id INT PRIMARY KEY AUTO_INCREMENT, '
                'benchmark_text NVARCHAR(64) NOT NULL, '
                'benchmark_num INT'
                ')')


def db_initial_insert_rows(connection, count: int, text: str) -> float:
    cur = connection.cursor()
    query = 'INSERT INTO benchmark (benchmark_text, benchmark_num) VALUES '
    for i in range(count - 1):
        split_begin = randint(0, int(len(text) / 2))
        split_end = randint(int(len(text) / 2), len(text) - 1)
        query += '("{}", {}), '.format(text[split_begin:split_end], i + 7)
    query += '("{}", {});'.format(text, count + 6)
    start = time.perf_counter_ns()
    cur.execute(query)
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_search_key_column(connection, key: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('SELECT * FROM benchmark WHERE benchmark_id = {};'.format(key))
    end = time.perf_counter_ns()
    return (end - start) / 1e6


def db_search_nonkey_column(connection, num: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('SELECT * FROM benchmark WHERE benchmark_num = {};'.format(num))
    end = time.perf_counter_ns()
    return (end - start) / 1e6


def db_search_by_mask(connection, mask: str) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('SELECT * FROM benchmark WHERE benchmark_text LIKE "{}";'.format(mask))
    end = time.perf_counter_ns()
    return (end - start) / 1e6


def db_insert_row(connection, text: str, num: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('INSERT INTO benchmark (benchmark_text, benchmark_num) VALUES '
                '("{}", {});'.format(text, num))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_insert_some_rows(connection, text: str, num: int, count: int) -> float:
    cur = connection.cursor()
    query = 'INSERT INTO benchmark (benchmark_text, benchmark_num) VALUES '
    for i in range(count - 1):
        query += '("{}", {}), '.format(text, num)
    query += '("{}", {});'.format(text, num)
    start = time.perf_counter_ns()
    cur.execute(query)
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_update_by_key_column(connection, key: int, text: str, num: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('UPDATE benchmark SET benchmark_text = "{}", '
                'benchmark_num = {} WHERE benchmark_id = {};'.format(text, num, key))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_update_by_num_column(connection, text: str, num: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('UPDATE benchmark SET benchmark_text = "{}" '
                'WHERE benchmark_num = {};'.format(text, num))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_delete_by_key_column(connection, key: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('DELETE FROM benchmark WHERE benchmark_id = {};'.format(key))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_delete_by_num_column(connection, num: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('DELETE FROM benchmark WHERE benchmark_num = {};'.format(num))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_delete_some_rows(connection, count: int) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('DELETE FROM benchmark LIMIT {};'.format(count))
    end = time.perf_counter_ns()
    connection.commit()
    return (end - start) / 1e6


def db_compress(connection) -> float:
    cur = connection.cursor()
    start = time.perf_counter_ns()
    cur.execute('ALTER TABLE benchmark ROW_FORMAT=COMPRESSED;')
    end = time.perf_counter_ns()
    return (end - start) / 1e6


def db_return_to_the_initial_state(connection, count: int, text: str) -> None:
    db_drop_benchmark_table(connection)
    db_init_benchmark_table(connection)
    db_initial_insert_rows(connection, count, text)


if __name__ == '__main__':
    some_key = 672
    some_num = 34
    some_text = 'keklolxd'
    some_mask = 'k%'
    rows_count = 100000
    rows_group_count = 200
    con = db_connect()
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Search key column {} rows: {:.4f} ms'.format(rows_count, db_search_key_column(con, some_key)))
    print('Search non-key column {} rows: {:.4f} ms'.format(rows_count, db_search_nonkey_column(con, some_num)))
    print('Search by mask {} rows: {:.4f} ms'.format(rows_count, db_search_by_mask(con, some_mask)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Insert one row {} rows: {:.4f} ms'.format(rows_count, db_insert_row(con, some_text, some_num)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Insert group of rows {} rows: {:.4f} ms'.format(rows_count, db_insert_some_rows(con, some_text, some_num,
                                                                                           rows_group_count)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Update key column {} rows: {:.4f} ms'.format(rows_count, db_update_by_key_column(con, some_key, some_text,
                                                                                            some_num)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Update num (non-key) column {} rows: {:.4f} ms'.format(rows_count, db_update_by_num_column(con, some_text,
                                                                                                      some_num)))
    print('Delete key column {} rows: {:.4f} ms'.format(rows_count, db_delete_by_key_column(con, some_key)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Delete num (non-key) column {} rows: {:.4f} ms'.format(rows_count, db_delete_by_num_column(con, some_num)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    print('Delete group of rows {} rows: {:.4f} ms'.format(rows_count, db_delete_some_rows(con, rows_group_count)))
    db_return_to_the_initial_state(con, rows_count, some_text)
    db_delete_some_rows(con, rows_group_count)
    print('Compress db after 200 rows deletion {} rows: {} ms'.format(rows_count, db_compress(con)))
    db_return_to_the_initial_state(con, rows_group_count, some_text)
    print('Compress db with 200 rows left {} rows: {} ms'.format(rows_count, db_compress(con)))
    db_return_to_the_initial_state(con, rows_count, some_text)
