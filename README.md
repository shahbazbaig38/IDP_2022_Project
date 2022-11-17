# IDP_2022_Project
This repository will be used for IDP project for Group 5


# Development Environment

python version 3.7

package managment system : pipenv


# Install guide

0. make sure you install  MySQL and Xampp and memorize password

1. install or confirm Python 3.7 on your machine

2. run `pip install pipenv` to install pipenv

3. run  `pipenv install` to create new environment based on Pipfile

4. you need download normal & mask tiff file from OneDrive and locate them in `/data` folder under this project.

5. run `pipenv shell` to activate env

6. modify data path in `database/convert_hdf5.py`

7. run `database/convert_hdf5.py` to generate hdf5 file

8. uncomment # self.insert_data() in `database/database.py` line 48. run insert_data() method to insert data into MySQL database. This is nesssasary only the first time. You can change content to be inserted by editing `database/database.py`.

9. make sure you use correct password and user in `maindash.py`

10. run `python app.py` to start app


# Others

if you install other package, run `pipenv install somepackage` after `pipenv shell`



pip install dash_bootstrap_components

exit()

pip install pipenv


## create db

cd database
python create_databse.py