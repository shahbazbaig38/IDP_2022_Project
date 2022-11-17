import sqlite3
import io
import numpy as np
from maindash import server,db# import server created on Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import h5py


class SPM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hdf5_path = db.Column(db.String(400), primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

class MASK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hdf5_path = db.Column(db.String(400), primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


class RGB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hdf5_path = db.Column(db.String(400), primary_key=False)
    mask_id = db.Column(db.Integer, primary_key=False)
    spm_id = db.Column(db.Integer, primary_key=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

# class TISSUE(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(400), primary_key=False)

# class FEATURE(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(400), primary_key=False)


class Database():
    # instance for debug
    def __init__(self) -> None:
        
        self.infh = h5py.File('database/hsi.h5', 'r')
        
        # comment out to insert data
        # self.insert_data()
        
    # insert data to initialize
    def insert_data(self):
        with server.app_context():
            db.create_all()

            db.session.add(SPM(id=1111,hdf5_path="Set_1_lower_10_icg_spim"))
            db.session.add(SPM(id=1112,hdf5_path="Set_1_lower_2_icg_spim"))
            db.session.commit()
            
            db.session.add(MASK(id=3333,hdf5_path="Set_1_lower_10_icg_masks"))
            db.session.add(MASK(id=3334,hdf5_path="Set_1_lower_2_icg_masks"))
            db.session.commit()
            
            db.session.add(RGB(id=2222,
                               hdf5_path="Set_1_lower_10_icg_rgb",
                               mask_id=3333,
                               spm_id=1111,))
            
            db.session.add(RGB(id=2223,
                               hdf5_path="Set_1_lower_2_icg_rgb",
                               mask_id=3334,
                               spm_id=1112,))
            db.session.commit()
    # print all contents for debug
    def print_all_table(self):
        with server.app_context():
            spim = db.session.execute(db.select(SPM)).scalars()
            print(spim)    
            mask = db.session.execute(db.select(MASK)).scalars()
            print(mask)    
    
    # get all name to display
    def get_all_rgb_name(self):
        spims = RGB.query.all()
        names = []
        for item in spims:
            names.append(item.hdf5_path)
        return names
    
    # get spim data to return for frontend
    def get_spim_by_id(self,id:int):
        spim_id = SPM.query.filter(SPM.id == id).first()
        # print(spim_id)
        return np.array(self.infh[spim_id.hdf5_path])
    
    # get spim data to return for frontend
    def get_rgb_by_id(self,id:int):
        rgb_id = RGB.query.filter(RGB.id == id).first()
        # print(rgb_id)
        return np.array(self.infh[rgb_id.hdf5_path])

    # get spim data to return for frontend
    def get_mask_by_id(self,id:int):
        mask_id = MASK.query.filter(MASK.id == id).first()
        # print(mask_id)
        return np.array(self.infh[mask_id.hdf5_path])
    
    def get_all_data_by_rgb_name(self, name):
        rgb = RGB.query.filter(RGB.hdf5_path == name).first()
        
        rgb_np_data = self.get_rgb_by_id(rgb.id)
        spim_np_data = self.get_spim_by_id(rgb.spm_id)
        mask_np_data = self.get_mask_by_id(rgb.mask_id)
        
        # return numpy data
        return rgb_np_data, spim_np_data, mask_np_data
        


        
