
############# Create Tables ##############
uuid_extension = "CREATE EXTENSION IF NOT EXISTS 'uuid-ossp';"

create_users_table = """CREATE SEQUENCE IF NOT EXISTS users_id_seq START 167992362910;
                        CREATE TABLE IF NOT EXISTS users(
                            id BIGINT PRIMARY KEY DEFAULT nextval('users_id_seq'),
                            name TEXT NOT NULL, 
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            photo TEXT,
                            verified BOOLEAN NOT NULL DEFAULT FALSE,
                            role TEXT NOT NULL DEFAULT 'user',
                            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
                            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
                    );
            """

create_link_table = """CREATE TABLE IF NOT EXISTS links(
                            id BIGINT REFERENCES users(id),
                            url text NOT NULL,
                            short_link VARCHAR(10) NOT NULL,
                            view INT DEFAULT 0
                    );
                    """

########### SELECT ##############
check_by_email = """select id from users where email = $1;"""


check_by_uid = """select id from users where id = $1;"""


get_user_info = """select * from users where email = $1;"""

get_user_links = """select * from links where id = $1;"""

get_user_link = """update links
                     set view = view + 1 
                     where  short_link = $1
                     returning url
                """

############ INSERT ##########
new_user = """insert into users 
                        (name, email, password, role, verified) 
               values ($1, $2, $3, $4, $5)
            """

        
add_new_link = """
               insert into links 
                    (id, url, short_link)
                values
                    ($1, $2, $3)
               """






