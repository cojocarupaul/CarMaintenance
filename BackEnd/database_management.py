import logging
import sqlalchemy
import mysql.connector

from sqlalchemy.orm import scoped_session, sessionmaker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

database_session = None


def create_dependent_tables(engine):
    from src.models.base import Base
    from src.models.user import User
    Base.metadata.create_all(engine)


def create_database(host_name, user_name, password, database_name):
    mydb = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=password,
    )
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS "+database_name)
    my_cursor.close()
    mydb.close()


def init_database_connection(host_name, user_name, password, database_name):
    global database_session
    create_database(host_name, user_name, password, database_name)

    engine = sqlalchemy.create_engine(
        'mysql+pymysql://%s:%s@%s/%s' % (user_name, password, host_name, database_name))
    database_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    create_dependent_tables(engine)

    logger.info('Successful initiated the database')
    return engine, database_session


def get_database_session():
    return database_session()
