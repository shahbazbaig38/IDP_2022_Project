import sqlite3
import io
import numpy as np
from maindash import server,db# import server created on Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class SPIM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)
    hdf5_path = db.Column(db.String(400), primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
class MASK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)
    hdf5_path = db.Column(db.String(400), primary_key=False)

class RGB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)
    hdf5_path = db.Column(db.String(400), primary_key=False)

class TISSUE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)

class FEATURE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)


class Database():
    def __init__(self) -> None:
        self.test_connection()
        
    def test_connection(self):
        with server.app_context():
            db.create_all()

            db.session.add(SPIM(id=1234,name="example",hsi="hsi_example"))
            db.session.commit()

            spim = db.session.execute(db.select(SPIM)).scalars()
            print(spim)
        
    def get_spim_hdf5_path(self,id:int):
        # return path to hdf5
        spim = db.session.execute(db.select(SPIM)).scalars()
        return spim[""]
    
    def get_rgb_hdf5_path(self,id:int):
        # return path to hdf5
        path_to_hdf5 = db.session.execute(db.select(SPIM)).scalars()
        return path_to_hdf5

    def adapt_array(self,arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(self,text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out,allow_pickle=True)

    # def get_rgb(self):
    #     self.cur.execute("select rgb from tiff_table")
    #     out = self.cur.fetchone()[0]
    #     out = io.BytesIO(out)
    #     out.seek(0)
    #     rgb = np.load(out,allow_pickle=True)
    #     return rgb


    # def get_id(self):
    #     self.cur.execute("select id from tiff_table")
    #     id = self.cur.fetchone()[0]
    #     return id