"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def read_all():

    # Create the list of people from our data
    people = Directors.query.order_by(Directors.id).all()

    # Serialize the data for the response
    person_schema = DirectorsSchema(many=True)
    data = person_schema.dump(people)
    return data

def gender_l(gender):

    
    if gender > 0 and gender < 3:
        
        # Create the list of people from our data
        people = (
            Directors.query.filter(Directors.gender == gender)
            .outerjoin(Movies)
            .all()
        )
        if people is not None:
            
        # Serialize the data for the response
            person_schema = DirectorsSchema(many=True)
            data = person_schema.dump(people)
            return data
        else:
            abort(404, f"Tidak di temukan")
    else:
        abort(409, f"Salah input gender 1/2 saja 1 untuk laki laki 2 untuk perempuan")
        
def read_one(director_id):

    # Build the initial query
    person = (
        Directors.query.filter(Directors.id == director_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = DirectorsSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {director_id}")
        



def create(person):

    name = person.get("name")
    gender = person.get("gender")
    uid = person.get("uid")
    department = person.get("department")

    existing_person = (
        Directors.query.filter(Directors.uid == uid)
        .filter(Directors.uid == uid)
        .one_or_none()
    )

    if gender <= 2 and gender > 0:
    # Can we insert this person?
        if existing_person is None:

            # Create a person instance using the schema and the passed in person
            schema = DirectorsSchema()
            new_person = schema.load(person, session=db.session)

            # Add the person to the database
            db.session.add(new_person)
            db.session.commit()

            # Serialize and return the newly created person in the response
            data = schema.dump(new_person)

            return data, 201

        # Otherwise, nope, person exists already
        else:
            abort(409, f" {name} exists already")
    else:
        abort(409, f"Gender Salah!")


def update(director_id, person):

    # Get the person requested from the db into session
    update_person = Directors.query.filter(
        Directors.id == director_id
    ).one_or_none()
    
    gender = person.get("gender")
    if gender > 0 and gender < 3:    
    # Did we find an existing person?
        if update_person is not None:

            # turn the passed in person into a db object
            schema = DirectorsSchema()
            update = schema.load(person, session=db.session)

            # Set the id to the person we want to update
            update.id = update_person.id

            # merge the new object into the old and commit it to the db
            db.session.merge(update)
            db.session.commit()

            # return updated person in the response
            data = schema.dump(update_person)

            return data, 200

        # Otherwise, nope, didn't find that person
        else:
            abort(404, f"Directors not found for Id: {director_id}")
    else:
        abort(409, f"Salah Input! Gender 1 / 2 ")


def delete(director_id):
   
    # Get the person requested
    person = Directors.query.filter(Directors.id == director_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(f"Person {director_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {director_id}")