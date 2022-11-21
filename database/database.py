import sqlite3
import io
import numpy as np
from maindash import server,db# import server created on Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import h5py

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship,joinedload,lazyload,subqueryload
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
    
    # relation
    tissue_id = Column(Integer, ForeignKey("tissue_table.id"))
    tissue = relationship("TISSUE", back_populates="mask")
    
    class_id = Column(Integer, ForeignKey("class_table.id"))
    class_f = relationship("CLASS", back_populates="mask")


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


class TISSUE(db.Model):
    __tablename__ = "tissue_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)

    # mask_id = Column(Integer, ForeignKey("mask_table.id"))
    mask = relationship("MASK", back_populates="tissue")

    class_id = Column(Integer, ForeignKey("class_table.id"))
    class_f = relationship("CLASS", back_populates="tissue")

class CLASS(db.Model):
    __tablename__ = "class_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), primary_key=False)

    # mask_id = Column(Integer, ForeignKey("mask_table.id"))
    mask = relationship("MASK", back_populates="class_f")
    
    tissue = relationship("TISSUE", back_populates="class_f")



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
            
            
            tissue1 = TISSUE(id=5555,name="tissue1",mask=[mask1])
            tissue2 = TISSUE(id=5556,name="tissue2",mask=[mask2])
            tissue3 = TISSUE(id=5557,name="tissue3",mask=[mask3])
            tissue4 = TISSUE(id=5558,name="tissue4",mask=[mask4])

            tissue5 = TISSUE(id=5559,name="tissue5",mask=[mask5])
            tissue6 = TISSUE(id=5560,name="tissue6",mask=[mask6])
            tissue7 = TISSUE(id=5561,name="tissue7",mask=[mask7])
            tissue8 = TISSUE(id=5562,name="tissue8",mask=[mask8])
            
            db.session.add(tissue1)
            db.session.add(tissue2)
            db.session.add(tissue3)
            db.session.add(tissue4)
            db.session.add(tissue5)
            db.session.add(tissue6)
            db.session.add(tissue7)
            db.session.add(tissue8)

            class1 = CLASS(id=6666,name="class1",mask=[mask1],tissue=[tissue1])
            class2 = CLASS(id=6667,name="class2",mask=[mask2],tissue=[tissue2])
            class3 = CLASS(id=6668,name="class3",mask=[mask3],tissue=[tissue3])
            class4 = CLASS(id=6669,name="class4",mask=[mask4],tissue=[tissue4])

            class5 = CLASS(id=6670,name="class5",mask=[mask5],tissue=[tissue5])
            class6 = CLASS(id=6671,name="class6",mask=[mask6],tissue=[tissue6])
            class7 = CLASS(id=6672,name="class7",mask=[mask7],tissue=[tissue7])
            class8 = CLASS(id=6673,name="class8",mask=[mask8],tissue=[tissue8])
            
            db.session.add(class1)
            db.session.add(class2)
            db.session.add(class3)
            db.session.add(class4)
            db.session.add(class5)
            db.session.add(class6)
            db.session.add(class7)
            db.session.add(class8)            
        
        
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
    
    def get_mask_cubic_by_name(self,name:str):
        spim_by_id = SPIM.query.filter(SPIM.hdf5_name == name).first()
        # print(mask_id)
        
        infh = self.open_hdf5(spim_by_id.hdf5_name)
        return np.array(infh["mask"])
    
    
    # get spim data to return for frontend
    def get_mask_by_id(self,id:int):
        mask_id = MASK.query.filter(MASK.id == id).first()
        # print(mask_id)
        
        infh = self.open_hdf5(mask_id.hdf5_name)
        return np.array(infh["mask"])  
      
    
    def get_all_data_by_rgb_name(self, name):
        rgb = RGB.query.filter(RGB.hdf5_name == name).first()
        
        rgb_np_data = self.get_rgb_by_id(rgb.id)
        spim_np_data = self.get_spim_by_id(rgb.spim_id)
        mask_np_data = self.get_mask_cubic_by_name(name)
        
        # return numpy data
        return rgb_np_data, spim_np_data, mask_np_data
        
    '''
        for API implementation
    '''
    
    def get_all_spim(self):
        spims = SPIM.query.options(subqueryload(SPIM.rgb)).all()
        # print(dump(spims))
        print(spims[0].rgb)
        res = []
        
        for item in spims:
            rgb = RGB.query.filter(RGB.spim_id == item.id).first()

            res.append({
                "name":item.hdf5_name,
                "pk":item.id,
                "rgb":rgb.hdf5_name,
            })
            
            # names.append(item.hdf5_name)
            # pks.append(item.id)
            # rgbs.append(item.rgb.hdf5_name)

        return res
    
    def get_spim_and_mask_by_id(self,id):
        
        # get one spim
        spim = SPIM.query.filter(SPIM.id == id).first()
        
        print()
        
        # get all mask
        anntn = ANNOTATION.query.filter(ANNOTATION.spim_id == spim.id).first()
        
        masks = MASK.query.filter(MASK.annotation_id == anntn.id)
        
        # each mask
        res = []

        for item in masks:
            res.append({
                "bitmap":item.hdf5_name,
                "tissueId":item.tissue_id,
                "classId":item.class_id,
            })
        
        return res, spim.hdf5_name + ".hdf5"
    
    
    def get_all_tissue_class(self):
        tissues = TISSUE.query.options().all()
        res = []
        
        for item in tissues:
            res.append({
                "tissue_type":item.name,
                "class_id":item.class_id,
                "pk":item.id,
            })
            
        return res


    def get_all_class_feature(self):
        classes = CLASS.query.options().all()
        res = []
        
        for item in classes:
            res.append({
                "class_feature":item.name,
                "pk":item.id,
            })
            
        return res

        
