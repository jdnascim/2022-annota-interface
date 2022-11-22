import os
import utils as utils
import argparse
from datetime import datetime
from config import db
from models import Image, ImageSchema
from flask import abort
from werkzeug.exceptions import Conflict

def build_database(reset=True):
    annotadb = utils.read_config()["annotadb"]
    dtpath = utils.read_config()["dataset_path"]

    if reset is True:
        Image.query.delete()
    
    # Delete database file if it exists currently
    if os.path.exists(annotadb) is False or reset is True:
        # Create the database
        db.create_all()
        
        # iterate over the image dataset structure and populate the database
        for img in os.listdir(dtpath):
            i = Image(imagepath=img, related=False, annotated=False, 
                      timestamp=datetime.now())

            db.session.add(i)
        
        db.session.commit()
        
        image = Image.query.order_by(Image.imagepath).all()
        image_schema = ImageSchema(many=True)
        data = image_schema.dump(image)

        return data, 201

    # Otherwise, nope, person exists already
    elif os.path.exists(annotadb):
        abort(409, "database exists already")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--no-reset', dest='reset', action='store_false')

    args = parser.parse_args()

    try:
        build_database(args.reset)
    except Conflict:
        pass
        