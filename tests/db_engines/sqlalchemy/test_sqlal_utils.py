# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on 2019-03-20 20:38:48
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: test_sqlal_utils.py
'''

import unittest

from spacetimegis.db_engines.sqlalchemy.sqlal_utils import *

class Test_SQLAl_Utils(unittest.TestCase):
    # def test_conn(self):
    #     engine = conn("localhost", 5432, "xujavy", "xzw9289:;", "postgis_test")
    #     # print(True)
    sqla = SQLAlchemyUtils('localhost', 5432, 'xujavy', 'xzw9289:;', 'postgis_test')

    def test_create(self):
        sql = 'CREATE TABLE users (\
            id INTEGER NOT NULL, \
            name VARCHAR, \
            fullname VARCHAR, \
            PRIMARY KEY (id))'
        self.sqla.executesql(sql)

    def test_insert(self):
        sql = "INSERT INTO users (id, name, fullname) VALUES (0, 'jack', 'Jack Jones')"
        self.sqla.executesql(sql)

    def test_select(self):
        sql = 'SELECT users.id, users.name, users.fullname FROM users'
        result = self.sqla.select(sql)
        print(result)

    def test_geo(self):
        rasttiff = self.sqla.select("SELECT st_astiff(rast, 'LZW') AS rasttiff FROM test WHERE rid=1;")

        # Write data to file
        # print(rasttiff[0][0])
        tiff_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../examples_data/postgis_test.tiff')
        if rasttiff is not None:
            open(tiff_path, 'wb').write(rasttiff[0][0])



if __name__ == "__main__":
    unittest.main()