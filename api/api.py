from maindash import server # import server created on Flask
from maindash import server,db# import server created on Flask
import h5py
from flask import Flask, jsonify, request
import numpy as np

from database.database import Database
database = Database()


@server.route('/spims/<int:id>', methods=['GET'])
def get_spims(id:int):
        # id to path
        path = database.get_spim(id)
        with h5py.File(path,"r") as f:
                numpy_spim = np.array(f["spim"])
                return numpy_spim

@server.route('/tissueclass', methods=['GET'])
def get_tissueclass():
        return {'hello': 'world'}

@server.route('/classfeature', methods=['GET'])
def get_classfeature():
        return {'hello': 'world'}