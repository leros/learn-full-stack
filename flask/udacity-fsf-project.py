from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant = session.query(Restaurant).first()
    try:
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        output = ''
        for i in items:
            output += i.name
            output += '</br>'
        return output
    except:
        return "no results"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)