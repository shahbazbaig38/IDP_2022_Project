# IDP_2022_Project
This repository will be used for IDP project for Group 5


# Development Environment

python version 3.7

package managment system : pipenv


# Install guide

- clone IDP_2022_Project to your machine

- make sure you install  MySQL and Xampp and memorize password. And run MySQL. you can check running MySQL from this url  `http://localhost/phpmyadmin/index.php`

- install or confirm Python 3.7 on your machine

- run `pip install pipenv` to install pipenv

- run  `pipenv install` to create new environment based on Pipfile

- Also you need download tiff image and locate in `data` folder under this project There is database folder. 

- run `pipenv shell` to activate env

- modify data path in `database/convert_hdf5.py`

- run `database/convert_hdf5.py` to generate hdf5 file

- uncomment # self.insert_data() in `database/database.py` line 48. run `python create_databse.py` to execute insert_data() method to insert data into MySQL database. This is nesssasary only the first time. You can change content to be inserted by editing `database/database.py`.

- make sure you use correct password and user for `MySQL` in `maindash.py`

- run `python app.py` to start app


# Others

if you install other package, run `pipenv install somepackage` after `pipenv shell`
