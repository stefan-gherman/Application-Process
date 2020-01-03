import database_common
from psycopg2 import sql


@database_common.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    cursor.execute(
        sql.SQL("select {col1}, {col2} from {table} where {col1}=(%s);"
                ).format(col1=sql.Identifier('first_name'), col2=sql.Identifier('last_name'),
                         table=sql.Identifier('mentors')), [first_name]
    )
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_mentors_names(cursor):
    cursor.execute(
        sql.SQL("SELECT {col1}, {col2} from {table};").format(col1=sql.Identifier('first_name'),
                                                               col2=sql.Identifier('last_name'),
                                                               table=sql.Identifier('mentors'))
    )
    mentor_names = cursor.fetchall()
    return mentor_names
