from maindash import server # import server created on Flask
import h5py
from flask import Flask, jsonify, request
import numpy as np

from database.database import Database


database = Database()

@server.route('/hello/', methods=['GET'])
def test():
        return "hello world"

@server.route('/api/spims', methods=['GET'])
def get_spims():

        all_spim = database.get_all_spim()
        
        res = {"spims" : all_spim}
        
        return jsonify(res)

@server.route('/api/spim/<int:id>', methods=['GET'])
def get_spim(id:int):
                
        masks, spim_cube = database.get_spim_and_mask_by_id(id)
        
        # get all tissue & class
        res = {
                "spim_cube" : spim_cube,
                "masks" : masks
        }        
        return jsonify(res)



@server.route('/api/tissueclass', methods=['GET'])
def get_tissueclass():
        tissueclass = database.get_all_tissue_class()
        
        res = {
                "TissueClass" : tissueclass,
        }        
        
        return jsonify(res)


@server.route('/api/classfeature', methods=['GET'])
def get_classfeature():
        tissueclass = database.get_all_class_feature()
        
        res = {
                "ClassFeature" : tissueclass,
        }        
        
        return jsonify(res)