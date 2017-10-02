from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

#  Create a database that stores data in the local directory's data.db file
engine = create_engine('sqlite:///person_alchemy.db')
Base = declarative_base()


#  Define classes for each table in the database.
#  Define attributes in each class to correspond to columns in table
class Person(Base):
    __tablename__ = 'person'
    #  Here we define columns for the table person
    #  Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    #  Here we define columns for the table address.
    #  Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)


#  Create all tables in the engine. This is equivalent to "Create Table"
#  statements in raw SQL.
try:
    Base.metadata.create_all(engine)
except:
    print("Table already there.")


# ********************** Inserting Records ************************
# Create a session to connect to the database created above
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert records to the Person and Addresses table
# Record 1 in Person
new_person = Person(name='Mary Poppins')
session.add(new_person)

new_address = Address(
        street_name='Magic Lane', street_number=22,
        post_code='12000', person=new_person)
session.add(new_address)

#  Insert a Person in the person table
#  Record 2 in Person
new_person = Person(name='Roald Dahl')
session.add(new_person)

#  Insert an Address in the address table
new_address = Address(
        street_name='Kids Pde', street_number=26,
        post_code='26000', person=new_person)
session.add(new_address)

session.commit()


# ***************** Building Queries ***********************
# Create queries to fetch data from the tables
# Return the first Person from all persons in the database
person = session.query(Person).first()
print(person.name)
addr = session.query(Address).filter(Address.person == person).one()
print(addr.post_code)

# Make a query to find all Persons in the database
rowset = session.query(Person).all()
for record in rowset:
    print(record.name)
    addr = session.query(Address).filter(Address.person == record).one()
    print(
        record.name + "lives at " + addr.street_number + " " +
        addr.street_name + " " + addr.post_code
    )
