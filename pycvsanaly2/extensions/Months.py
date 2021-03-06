# Copyright (C) 2012 LibreSoft
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Jesus M. Gonzalez-Barahona <jgb@gsyc.es>

"""Produces a table with the list of months for the life of the repository

Very simple code just to produce, for convenience, a table with one
month per row, starting with the month of the first commit, and ending
with the month of the last commit found in the repository.

This table can be used to select "solid" sets of months. GROUP BY would
not produce entries for months with no results in the select (eg., months
with no commits at all). But in many cases, you need a row with some
parameter for all the months, including a 0 when no activity is found. That
can be easily done using this auxiliary table.
"""

from pycvsanaly2.extensions import Extension, register_extension, ExtensionRunError
from pycvsanaly2.extensions.DBTable import DBTable

class MonthsTable (DBTable):
    """Class for managing the months table

    Each record in the table has two fields:
      - id: an integer with a month identifier (year * 12 + month)
      - year: an integer with the numeral of the year (eg. 2012)
      - month: an integer with the numeral of the month (eg. 1 for January)
      - date: a date for the beginning of the month, eg. 2012-01-01
         for Jan 2012
    """

    # SQL string for creating the table, specialized for SQLite
    _sql_create_table_sqlite = "CREATE TABLE months (" + \
        "id integer primary key," + \
        "year integer," + \
        "month integer," + \
        "date datetime" + \
        ")"

    # SQL string for creating the table, specialized for MySQL
    _sql_create_table_mysql = "CREATE TABLE months (" + \
        "id INTEGER PRIMARY KEY," + \
        "year INTEGER," + \
        "month INTEGER," + \
        "date DATETIME" + \
        ") ENGINE=MyISAM" + \
        " CHARACTER SET=utf8"

    # SQL string for getting the max id in table
    _sql_max_id = "SELECT max(id) FROM months"

    # SQL string for inserting a row in table
    _sql_row_insert = "INSERT INTO months " + \
        "(id, year, month, date) VALUES (%s, %s, %s, %s)"

    # SQL string for selecting all rows to fill self.table
    # (rows already in table), corresponding to repository_id
    # Should return a unique identifier which will be key in self.table
    # In this case, this is the commit id (for commits in repository_id)
    _sql_select_rows = "SELECT id FROM months # %s"


class Months (Extension):
    """Extension to produce a table the list of months.

    Includes a list with the list of months for the life of the repository,
    with no holes in it (all months, have they commits or not, from first
    to last date in repository.
    """

    def run (self, repo, uri, db):
        """Extract first and laste commits from scmlog and create the months table.
        """

        cnn = db.connect ()
        # Cursor for reading from the database
        cursor = cnn.cursor ()
        # Cursor for writing to the database
        write_cursor = cnn.cursor ()

        cursor.execute ("SELECT MIN(date) FROM scmlog")
        minDate = cursor.fetchone ()[0]
        cursor.execute ("SELECT MAX(date) FROM scmlog")
        maxDate = cursor.fetchone ()[0]
        cursor.execute ("DROP TABLE IF EXISTS months")

        theMonthsTable = MonthsTable(db, cnn, repo)

        firstMonth = minDate.year * 12 + minDate.month
        lastMonth = maxDate.year * 12 + maxDate.month

        for period in range (firstMonth, lastMonth+1):
            month = (period -1 ) % 12 + 1 
            year = (period - 1)// 12
            date = str(year) + "-" + str(month) + "-01"
            theMonthsTable.add_pending_row ((period, year, month, date))
        theMonthsTable.insert_rows (write_cursor)
        cnn.commit ()
        write_cursor.close ()
        cursor.close ()
        cnn.close ()

# Register in the CVSAnalY extension system
register_extension ("Months", Months)
