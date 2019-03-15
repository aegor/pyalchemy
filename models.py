from app import db
from marshmallow_sqlalchemy import ModelSchema
from safrs import SAFRSBase, jsonapi_rpc


class Dessert(SAFRSBase, db.Model):
    '''
        description: See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example for details on the column types.
    '''


    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A dessert has a name, a price and some calories:
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    calories = db.Column(db.Integer)
    # Following method is exposed through the REST API
    # This means it can be invoked with the argument http_methods
    @jsonapi_rpc(http_methods = ['GET'])
    def calories_per_dollar(self, **kwargs):
        """
            description : Calculate calories per dollar
            args:
                none:
                    type : string
                    example : any string
        """
        # check varargs arguments

        cost = 0.
        if self.calories:
            cost = self.calories / self.price
        # varargs argumentsw from request
        print(kwargs.get('varargs'))
        return { 'result' : 'cost %f' % cost}

    def get(self, *args, **kwargs):
        '''
            description: Return calories per dollar
            summary : same as description
            responses :
                429 :
                    description : Too many requests
        '''
        return self.http_methods['get'](self, *args, **kwargs)


class DessertSchema(ModelSchema):
    class Meta:
        model = Dessert


dessert_schema = DessertSchema()


class Menu(SAFRSBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class MenuSchema(ModelSchema):
    class Meta:
        model = Menu


def create_dessert(new_name, new_price, new_calories):
    # Create a dessert with the provided input.
    # At first, we will trust the user.

    # This line maps to line 16 above (the Dessert.__init__ method)
    dessert = Dessert(new_name, new_price, new_calories)

    # Actually add this dessert to the database
    db.session.add(dessert)

    # Save all pending changes to the database
    db.session.commit()

    return dessert


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print ("Done!")
