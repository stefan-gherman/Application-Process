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


@database_common.connection_handler
def get_mentor_nicknames_city(cursor, city):
    cursor.execute(
        sql.SQL("SELECT {nickname},{city} FROM {table} WHERE {city}=(%s)").format(
            nickname=sql.Identifier('nick_name'),
            city=sql.Identifier('city'),
            table=sql.Identifier('mentors')), [city]
    )
    mentor_nicks = cursor.fetchall()
    return mentor_nicks


@database_common.connection_handler
def get_info_by_name(cursor, name):
    cursor.execute(
        sql.SQL("SELECT (({col1}||' ') || {col2}) AS full_name, {col3}  FROM {table} WHERE {col1}=(%s);").format(
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('last_name'),
            col3=sql.Identifier('phone_number'),
            table=sql.Identifier('applicants')
        ), [name]
    )
    info = cursor.fetchall()
    return info


@database_common.connection_handler
def get_info_mailprovider(cursor, provider):
    cursor.execute(
        sql.SQL("SELECT (({col1}||' ') || {col2}) AS full_name, {col3}  FROM {table} WHERE {col4} LIKE %s;").format(
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('last_name'),
            col3=sql.Identifier('phone_number'),
            col4=sql.Identifier('email'),
            table=sql.Identifier('applicants')
        ), ['%' + provider]
    )
    info = cursor.fetchall()
    return info


@database_common.connection_handler
def insert_applicant(cursor, first_name, last_name, phone_number, email, application_code):
    cursor.execute(
        sql.SQL(
            "INSERT INTO {table} ({f_n},{l_n},{p_n},{email},{a_c}) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;").format(
            f_n=sql.Identifier('first_name'),
            l_n=sql.Identifier('last_name'),
            p_n=sql.Identifier('phone_number'),
            email=sql.Identifier('email'),
            a_c=sql.Identifier('application_code'),
            table=sql.Identifier('applicants')
        ), [first_name, last_name, phone_number, email, application_code]
    )
    cursor.execute(
        sql.SQL("SELECT * FROM {table} WHERE {col1} = (%s);").format(
            col1=sql.Identifier('application_code'),
            table=sql.Identifier('applicants')
        ), [application_code]
    )

    query_result = cursor.fetchall()
    return query_result


@database_common.connection_handler
def update_applicant(cursor, first_name, last_name, phone_number):
    cursor.execute(
        sql.SQL("UPDATE {table} SET {col1}=%s WHERE {col2} = %s and {col3} = %s;"

                ).format(
            table=sql.Identifier('applicants'),
            col1=sql.Identifier('phone_number'),
            col2=sql.Identifier('first_name'),
            col3=sql.Identifier('last_name')
        ), [phone_number, first_name, last_name]
    )

    cursor.execute(
        sql.SQL("SELECT * FROM {table} WHERE {col2} = %s AND {col3} = %s").format(
            table=sql.Identifier('applicants'),
            col2=sql.Identifier('first_name'),
            col3=sql.Identifier('last_name')
        ), [first_name, last_name]
    )

    query_result = cursor.fetchall()
    return query_result
@database_common.connection_handler
def delete_applicant(cursor,mail):
    cursor.execute(
        sql.SQL("DELETE FROM {table} WHERE {col1} LIKE %s;").format(
        table=sql.Identifier('applicants'),
        col1=sql.Identifier('email')
    ),['%'+mail]
    )

