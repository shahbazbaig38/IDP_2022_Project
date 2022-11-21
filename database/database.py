import sqlite3
import io
import numpy as np
from maindash import server,db# import server created on Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import h5py

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

class SPIM(db.Model):
    __tablename__ = "spim_table"
    id = db.Column(db.Integer, primary_key=True)
    hdf5_name = db.Column(db.String(400), primary_key=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    anntn = relationship("ANNOTATION", back_populates="spim")
    rgb = relationship("RGB", back_populates="spim")
    
    # rgb_id = Column(Integer, ForeignKey("rgb_table.id"))
    # anntn_id = Column(Integer, ForeignKey("annotation_table.id"))

class ANNOTATION(db.Model):
    __tablename__ = "annotation_table"
    id = db.Column(db.Integer, primary_key=True)
    
    # relation to spim
    # one to one relation
    spim_id = Column(Integer, ForeignKey("spim_table.id"))
    spim = relationship("SPIM", back_populates="anntn")

    # relation to masks
    # one to Many relation
    mask_list = relationship("MASK")

class MASK(db.Model):
    __tablename__ = "mask_table"
    id = db.Column(db.Integer, primary_key=True)
    hdf5_name = db.Column(db.String(400), primary_key=False)
    mask_name = db.Column(db.String(400))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    # relation to annotation
    # many to one
    annotation_id = Column(Integer, ForeignKey("annotation_table.id"))
    

class RGB(db.Model):
    __tablename__ = "rgb_table"
    id = db.Column(db.Integer, primary_key=True)
    hdf5_name = db.Column(db.String(400), primary_key=False)
    
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    # relation to spim
    # one to one relation
    spim_id = Column(Integer, ForeignKey("spim_table.id"))
    spim = relationship("SPIM", back_populates="rgb")


# class TISSUE(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(400), primary_key=False)

# class FEATURE(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(400), primary_key=False)


class Database():
    # instance for debug
    def __init__(self) -> None:
        
        # self.infh = h5py.File('hdf5_datafiles/hsi.h5', 'r')
        
        # comment out to insert data
        # self.insert_data()
        pass
        
    def open_hdf5(self,name):
        infh =h5py.File(f'hdf5_files/{name}.h5', 'r')
        return infh
        
    # insert data to initialize
    def insert_data(self):
        with server.app_context():
            db.create_all()
            
            mask1 = MASK(id=3333,hdf5_name="Set_1_lower_10_icg", mask_name = "Specular reflection")
            mask2 = MASK(id=3334,hdf5_name="Set_1_lower_10_icg", mask_name = "Artery")
            mask3 = MASK(id=3335,hdf5_name="Set_1_lower_10_icg", mask_name = "Vein")
            mask4 = MASK(id=3336,hdf5_name="Set_1_lower_10_icg", mask_name = "Stroma, ICG")

            mask5 = MASK(id=3337,hdf5_name="Set_1_lower_2_icg", mask_name = "Specular reflection")
            mask6 = MASK(id=3338,hdf5_name="Set_1_lower_2_icg", mask_name = "Artery")
            mask7 = MASK(id=3339,hdf5_name="Set_1_lower_2_icg", mask_name = "Vein")
            mask8 = MASK(id=3340,hdf5_name="Set_1_lower_2_icg", mask_name = "Stroma, ICG")
            
            db.session.add(mask1)
            db.session.add(mask2)
            db.session.add(mask3)
            db.session.add(mask4)
            db.session.add(mask5)
            db.session.add(mask6)
            db.session.add(mask7)
            db.session.add(mask8)
            # db.session.commit()

            anntn1 = ANNOTATION(id=1111,mask_list=[mask1,mask2,mask3,mask4])
            anntn2 = ANNOTATION(id=1112,mask_list=[mask5,mask6,mask7,mask8])
            
            db.session.add(anntn1)
            db.session.add(anntn2)
            # db.session.commit()
            
            rgb1 = RGB(id=2222,hdf5_name="Set_1_lower_10_icg")
            rgb2 = RGB(id=2223,hdf5_name="Set_1_lower_2_icg")
            
            db.session.add(rgb1)
            db.session.add(rgb2)
            # db.session.commit()

            db.session.add(SPIM(id=4444,hdf5_name="Set_1_lower_10_icg",anntn = [anntn1],rgb = [rgb1]))
            db.session.add(SPIM(id=4445,hdf5_name="Set_1_lower_2_icg",anntn = [anntn2],rgb = [rgb2]))
            db.session.commit()
                
    # print all contents for debug
    def print_all_table(self):
        with server.app_context():
            spim = db.session.execute(db.select(SPIM)).scalars()
            print(spim)
            mask = db.session.execute(db.select(MASK)).scalars()
            print(mask)
    
    # get all name to display
    def get_all_rgb_name(self):
        spims = RGB.query.all()
        names = []
        for item in spims:
            names.append(item.hdf5_name)
        return names
    
    # get spim data to return for frontend
    def get_spim_by_id(self,id:int):
        spim_id = SPIM.query.filter(SPIM.id == id).first()
        # print(spim_id)
        infh = self.open_hdf5(spim_id.hdf5_name)
        return np.array(infh["spim"])
    
    # get spim data to return for frontend
    def get_rgb_by_id(self,id:int):
        rgb_id = RGB.query.filter(RGB.id == id).first()
        # print(rgb_id)
        infh = self.open_hdf5(rgb_id.hdf5_name)
        return np.array(infh["rgb"])
    
    # get spim data to return for frontend
    def get_mask_by_id(self,id:int):
        mask_id = MASK.query.filter(MASK.id == id).first()
        # print(mask_id)
        
        infh = self.open_hdf5(mask_id.hdf5_name)
        return np.array(infh["mask"])  
      
    def get_all_data_by_rgb_name(self, name):
        rgb = RGB.query.filter(RGB.hdf5_name == name).first()
        
        rgb_np_data = self.get_rgb_by_id(rgb.id)
        spim_np_data = self.get_spim_by_id(rgb.spm_id)
        mask_np_data = self.get_mask_by_id(rgb.mask_id)
        
        # return numpy data
        return rgb_np_data, spim_np_data, mask_np_data
        


        
