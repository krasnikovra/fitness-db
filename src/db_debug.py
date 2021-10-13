from db_utils import *

db_destroy()
db_init()
con = db_connect()
db_create_tables(con)
db_insert_constants(con)
#db_destroy()
