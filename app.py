# import necessary libraries
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float, inspect


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
engine = create_engine("sqlite:///Datasets/belly_button_biodiversity.sqlite")
conn = engine.connect()
inspector = inspect(engine)
inspector.get_table_names()
Base = automap_base()
Base.prepare(engine, reflect=True)
Otu = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata
session = Session(engine)


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/names')
def name():
    """List of Sample Names."""
    names = []
    columns = inspector.get_columns('samples')
    for c in columns:
        names.append(c['name'])
    del names[0]
    return jsonify(names)

@app.route('/otu')
def otu():
    """List of otu descriptions."""
    desc = session.query(Otu.lowest_taxonomic_unit_found).all()
    description = []
    for d in desc:
        description.append(d[0])
    return jsonify(description)

@app.route('/metadata/<sample>')
def metadata(sample):
    search_term = int(sample.replace("BB_", ""))
    x = 0
    SAMPLES = session.query(SamplesMetadata.SAMPLEID,SamplesMetadata.AGE, SamplesMetadata.BBTYPE,
        SamplesMetadata.ETHNICITY, SamplesMetadata.GENDER, SamplesMetadata.LOCATION).all()
    data = {}
    for samp in SAMPLES:
        if SAMPLES[x][0] == search_term:
            data["AGE"] = SAMPLES[x][1]
            data["BBTYPE"] = SAMPLES[x][2] 
            data["ETHNICITY"] = SAMPLES[x][3]
            data["GENDER"] = SAMPLES[x][4]
            data["LOCATION"] = SAMPLES[x][5]
            data["SAMPLEID"] = SAMPLES[x][0]
            return jsonify(data)
        x += 1
    return jsonify({"error": f"Sample with id {sample} not found."}), 404

@app.route('/wfreq/<sample>')
def wfreq(sample):
    search_term = int(sample.replace("BB_", ""))
    x = 0
    SAMPLES = session.query(SamplesMetadata.SAMPLEID,SamplesMetadata.WFREQ).all()
    for samp in SAMPLES:
        if SAMPLES[x][0] == search_term:
            wfreq = SAMPLES[x][1]
            return jsonify(wfreq)
        x += 1
    return jsonify({"error": f"Sample with id {sample} not found."}), 404

@app.route('/samples/<variable>')
def samples(variable):
    var = f'Samples.{variable}'
    SAMPLES = session.query(Samples.otu_id, var).order_by(var).all()
    x = len(SAMPLES) -1
    otu_ids = []
    sample_values = []
    for sample in SAMPLES:
        otu_ids.append(SAMPLES[x][0])
        sample_values.append(SAMPLES[x][1])
        x -=1
    dict = {}
    dict["otu_ids"] = otu_ids
    dict["sample_values"] = sample_values
    list = [dict]
    return jsonify(list)

if __name__ == "__main__":
    app.run()