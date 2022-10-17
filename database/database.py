import sqlite3
import io
import numpy as np

class Database:
    def __init__(self) -> None:
        pass
         # connect to sqlite
        self.con = sqlite3.connect("database/hsi_database", detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()

    def adapt_array(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out,allow_pickle=True)


    def get_tiff(self):
        self.cur.execute("select spim from tiff_table")
        out = self.cur.fetchone()[0]
        out = io.BytesIO(out)
        out.seek(0)
        tiff_data = np.load(out)
        return tiff_data

    def get_mask(self):
        self.cur.execute("select mask from tiff_table")
        out = self.cur.fetchone()[0]
        out = io.BytesIO(out)
        out.seek(0)
        mask = np.load(out,allow_pickle=True)
        return mask

    def get_rgb(self):
        self.cur.execute("select rgb from tiff_table")
        out = self.cur.fetchone()[0]
        out = io.BytesIO(out)
        out.seek(0)
        rgb = np.load(out,allow_pickle=True)
        return rgb


    def get_id(self):
        self.cur.execute("select id from tiff_table")
        id = self.cur.fetchone()[0]
        return id