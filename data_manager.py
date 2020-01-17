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
def delete_applicant(cursor, mail):
    cursor.execute(
        sql.SQL("DELETE FROM {table} WHERE {col1} LIKE %s;").format(
            table=sql.Identifier('applicants'),
            col1=sql.Identifier('email')
        ), ['%' + mail]
    )


@database_common.connection_handler
def show_all_applicants(cursor):
    cursor.execute(
        sql.SQL("SELECT {col1}, {col2} FROM {table};").format(
            col1=sql.Identifier('id'),
            col2=sql.Identifier('first_name'),
            table=sql.Identifier('applicants')
        )
    )
    all_applicants = cursor.fetchall()
    return all_applicants


@database_common.connection_handler
def show_data_for_applicant(cursor, applicant_id):
    cursor.execute(
        sql.SQL("SELECT * from {table} WHERE {col1} = %s;")
            .format(
            table=sql.Identifier('applicants'),
            col1=sql.Identifier('id')
        ), [applicant_id]
    )
    applicant_data = cursor.fetchall()
    return applicant_data


@database_common.connection_handler
def show_mentors_and_schools(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, {table1}.{col2}, {table2}.{col3}, {table2}.{col4} FROM {table1} JOIN {table2} ON {table1}.{col5} = {table2}.{col6} ORDER BY {table1}.{col7} ASC;")
            .format(
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('last_name'),
            col3=sql.Identifier('name'),
            col4=sql.Identifier('country'),
            table1=sql.Identifier('mentors'),
            table2=sql.Identifier('schools'),
            col5=sql.Identifier('city'),
            col6=sql.Identifier('city'),
            col7=sql.Identifier('id')
        )
    )

    mentors_and_schools = cursor.fetchall()
    return mentors_and_schools


@database_common.connection_handler
def show_mentors_and_schools_with_null_vals(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, {table1}.{col2}, {table2}.{col3}, {table2}.{col4} FROM {table1} RIGHT JOIN {table2} ON {table1}.{col5} = {table2}.{col6} ORDER BY {table1}.{col7} ASC;")
            .format(
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('last_name'),
            col3=sql.Identifier('name'),
            col4=sql.Identifier('country'),
            table1=sql.Identifier('mentors'),
            table2=sql.Identifier('schools'),
            col5=sql.Identifier('city'),
            col6=sql.Identifier('city'),
            col7=sql.Identifier('id')
        )
    )

    mentors_and_schools = cursor.fetchall()
    for mentor in mentors_and_schools:
        for key in mentor.keys():
            if mentor[key] is None:
                mentor[key] = "No Data"
    return mentors_and_schools


@database_common.connection_handler
def show_mentors_per_country(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, count(*) as number FROM {table1} JOIN {table2} ON {table1}.{col2} = {table2}.{col2} GROUP BY {table1}.{col1};")
            .format(
            table1=sql.Identifier('schools'),
            col1=sql.Identifier('country'),
            table2=sql.Identifier('mentors'),
            col2=sql.Identifier('city'),

        )
    )
    mentors_per_country = cursor.fetchall()
    return mentors_per_country


@database_common.connection_handler
def show_contacts(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, {table2}.{col2}, {table2}.{col3} FROM {table1} LEFT JOIN {table2} ON {table1}.{col4} = {table2}.{col5} ORDER BY {table1}.{col1} ASC;"
        ).format(
            table1=sql.Identifier('schools'),
            col1=sql.Identifier('name'),
            table2=sql.Identifier('mentors'),
            col2=sql.Identifier('first_name'),
            col3=sql.Identifier('last_name'),
            col4=sql.Identifier('contact_person'),
            col5=sql.Identifier('id')
        )
    )
    contacts = cursor.fetchall()
    for contact in contacts:
        for key in contact.keys():
            if contact[key] is None:
                contact[key] = "No Data"
    return contacts


@database_common.connection_handler
def show_applicants_later_than(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, {table1}.{col2}, {table2}.{col3} FROM {table1} JOIN {table2} ON {table1}.{col4} = {table2}.{col5} WHERE {table2}.{col3} > '2016-01-01' :: DATE ORDER BY {table2}.{col3} DESC;"
        ).format(
            table1=sql.Identifier('applicants'),
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('application_code'),
            table2=sql.Identifier('applicants_mentors'),
            col3=sql.Identifier('creation_date'),
            col4=sql.Identifier('id'),
            col5=sql.Identifier('applicant_id')
        )
    )
    applicants = cursor.fetchall()
    return applicants


@database_common.connection_handler
def show_applicants_mentors(cursor):
    cursor.execute(
        sql.SQL(
            "SELECT {table1}.{col1}, {table1}.{col2}, {table2}.{col1} as mntr_frst_nm, {table2}.{col4} FROM {table1} LEFT JOIN {table3} ON {table1}.{col5} = {table3}.{col6} LEFT JOIN {table2} ON {table2}.{col5} = {table3}.{col7} ORDER BY {table1}.{col5};"
            ).format(
            table1=sql.Identifier('applicants'),
            col1=sql.Identifier('first_name'),
            col2=sql.Identifier('application_code'),
            table2=sql.Identifier('mentors'),
            col4=sql.Identifier('last_name'),
            table3=sql.Identifier('applicants_mentors'),
            col5=sql.Identifier('id'),
            col6=sql.Identifier('applicant_id'),
            col7=sql.Identifier('mentor_id')

        )
    )
    applicants_mentors = cursor.fetchall()
    for applicant in applicants_mentors:
        for key in applicant.keys():
            if applicant[key] is None:
                applicant[key] = "No Data"
    return applicants_mentors
