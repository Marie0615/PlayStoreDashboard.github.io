import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



#################################################
# Database Setup v2
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/playstore.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Appsdata = Base.classes.storedata
user_reviews = Base.classes.user_reviews



@app.route("/MyData")
def Mydata():
    """Return google playstore apps top 10"""

    stmt = db.session.query(Appsdata).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    print(df)
    data_list = list()
    for i, v in df.iterrows():
        data = {
            "App_Name": v['App_Name'],
            "Category": v['Category'],
            "Rating": v['Rating'],
            "Reviews": v['Reviews'],
            "Installs": v['Installs'],
            "Type": v['Type'],
            "Price": v['Price'],
            "Content_Rating": v['Content_Rating'],
        }
    
        data_list.append(data)
    # This is to remove the header when is duplicated
    data_list.pop(0)

    # return jsonify(df.to_dict())
    return jsonify(data_list)

   
if __name__ == '__main__':
    app.run(debug=True)
