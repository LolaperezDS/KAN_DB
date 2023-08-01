# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
#
# # Создание тестовой базы данных
# @pytest.fixture(scope='session')
# def db():
#     engine = create_engine('postgresql://username:password@localhost/test_db')
#     Base.metadata.create_all(engine)
#     yield engine
#     Base.metadata.drop_all(engine)
#
#
# # Создание сессии SQLAlchemy
# @pytest.fixture
# def session(db):
#     connection = db.connect()
#     transaction = connection.begin()
#     Session = sessionmaker(bind=connection)
#     session = Session()
#     yield session
#     session.close()
#     transaction.rollback()
#     connection.close()
