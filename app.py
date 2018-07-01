# import necessary libraries
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)

from .models import Otu, Samples, SamplesMetadata

##################################################
# Routes
##################################################

# create home route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#List of sample names
@app.route('/names')
def samples():
    results = db.session.query(SamplesMetadata.SAMPLEID).all()
    samples_list = [('BB_' + str(id)) for (id,) in results]
    return jsonify(samples_list)

#List of OTU descriptions.
@app.route('/otu')
def otuDesc():
    results = db.session.query(Otu.LOWEST_TAXONOMIC_UNIT_FOUND).all()
    name_list = [name for (name,) in results]
    return jsonify(name_list)

#Returns a json dictionary of sample metadata
@app.route('/metadata/<sample>')
def metadataFor(sample):
    sample_id = sample.split('_')
    results = db.session.query(SamplesMetadata.AGE,
                               SamplesMetadata.BBTYPE,
                               SamplesMetadata.ETHNICITY,
                               SamplesMetadata.GENDER,
                               SamplesMetadata.LOCATION,
                               SamplesMetadata.SAMPLEID)\
                        .filter(SamplesMetadata.SAMPLEID == int(sample_id))\
                        .all()

    for result in results:
        sample_data = [{
            "AGE": result[0],
            "BBTYPE": result[1],
            "ETHNICITY": result[2],
            "GENDER": result[3],
            "LOCATION": result[4],
            "SAMPLEID": result[5]
        }]

    return jsonify(sample_data)


#Returns an integer value for the weekly washing frequency for sample
@app.route('/wfreq/<sample>')
def wfreqFor(sample):
    sample_id = sample.split('_')
    results = db.session.query(SamplesMetadata.WFREQ,)\
                        .filter(SamplesMetadata.SAMPLEID == int(sample_id))\
                        .all()

    for result in results:
        sample_data = [{
            "WFREQ": result[0],
        }]

    return jsonify(sample_data)

#OTU IDs and Sample Values for a given sample.
@app.route('/samples/<sample>')
def sampleValues(sample):
    otu_id_list = []
    sample_value_list = []
    sample_col = f'Samples.{sample}'
    results = db.session.query(Samples.OTU_ID,
                               sample_col)\
                .order_by(sample_col)\
                .all()

    for result in results:
        otu_id_list.append(result[0])
        sample_value_list.append(result[1])

    sample_data = [{
        "otu_ids": otu_id_list,
        "sample_values": sample_value_list
    }]

    return jsonify(sample_data)


if __name__ == "__main__":
    app.run()
