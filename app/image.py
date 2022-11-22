"""
This is the image module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Image, ImageSchema
from datetime import datetime

def read(related=None, annotated=None, qtde=-1):
    """
    This function responds to a request for /api/images
    with the complete lists of images
    :return:        json string of list of images
    """
    
    if qtde <= -1 or qtde is None:
        if related is None and annotated is None:
        # Create the list of people from our data
            image = Image.query.order_by(Image.imagepath).all()
        elif related is not None and annotated is None:
            image = Image.query.filter(Image.related.is_(related)).all()
        elif related is None and annotated is not None:
            image = Image.query.filter(Image.annotated.is_(annotated)).all()
        else:
            image = Image.query.filter(Image.related.is_(related),
                                    Image.annotated.is_(annotated)).all()
    else:
        if related is None and annotated is None:
        # Create the list of people from our data
            image = Image.query.order_by(Image.imagepath).limit(qtde).all()
        elif related is not None and annotated is None:
            image = Image.query.filter(Image.related.is_(related)).limit(qtde).all()
        elif related is None and annotated is not None:
            image = Image.query.filter(Image.annotated.is_(annotated)).limit(qtde).all()
        else:
            image = Image.query.filter(Image.related.is_(related),
                                    Image.annotated.is_(annotated)).limit(qtde).all()

    if image is not None:
        # Serialize the data for the response
        image_schema = ImageSchema(many=True)
        data = image_schema.dump(image)
        return data
    else:
        abort(404, f"Image not found for filter")


def annotate(imagepath, image):
    """
    This function annotates an existing image in the image structure
    :param imagepath:   Path of the image to annotate in the people structure
    :param related:     Annotation
    :return:            updated image structure
    """

    # Get the person requested from the db into session
    update_image = Image.query.filter(
        Image.imagepath == imagepath
    ).one_or_none()

    # Did we find an existing person?
    if update_image is not None:
        image["imagepath"] = imagepath
        image["annotated"] = True
        image["timestamp"] = str(datetime.now()) 

        # turn the passed in person into a db object
        schema = ImageSchema()
        update = schema.load(image, session=db.session)

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_image)

        return data, 200

    # Otherwise, nope, didn't find that Image
    else:
        abort(404, f"Image not found for path: {imagepath}")


def undo_last():
    """_summary_
    This function removes annotation flag from last annotated image
    :return:            updated image structure
    """

    last_image = Image.query.filter(
        Image.annotated.is_(True)
    ).order_by(Image.timestamp.desc()).first()

    if last_image is not None:
        last_image.annotated = False

        db.session.merge(last_image)
        db.session.commit()

        # Serialize the data for the response
        image_schema = ImageSchema(many=False)
        data = image_schema.dump(last_image)
        return data
    else:
        abort(404, f"No annotation found")
    
