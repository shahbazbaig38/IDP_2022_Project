from maindash import server # import server created on Flask
import h5py
from flask import Flask, jsonify, request
import numpy as np

from database.database import Database


database = Database()


@server.route('/hello', methods=['GET'])
def test():
        return "hello"

@server.route('/spims/<int:id>', methods=['GET'])
def get_spims(id:list(int)):
        
        numpy_spim = database.get_spim_by_id(id)
        return numpy_spim

@server.route('/spim/<int:id>', methods=['GET'])
def get_spim(id:int):
        
        numpy_spim = database.get_spim_by_id(id)
        
        return numpy_spim



@server.route('/tissueclass', methods=['GET'])
def get_tissueclass():
        return {'hello': 'world'}

@server.route('/classfeature', methods=['GET'])
def get_classfeature():
        return {'hello': 'world'}