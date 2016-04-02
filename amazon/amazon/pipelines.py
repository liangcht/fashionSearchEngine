# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os
con = None

class AmazonPipeline(object):
	def __init__(self):
		self.setupDBCon()
		self.createTables()

	def setupDBCon(self):
		self.con = sqlite3.connect('./test.db') #Change this to your own directory
		self.cur = self.con.cursor()

	def createTables(self):
		self.dropAmazonTable()
		self.createAmazonTable()

	def dropAmazonTable(self):
		#drop amazon table if it exists
		self.cur.execute("DROP TABLE IF EXISTS Amazon")

	def createAmazonTable(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Amazon(id INTEGER PRIMARY KEY NOT NULL, \
		    name TEXT, \
		    path TEXT, \
		    gender TEXT, \
		    type TEXT, \
		    source TEXT \
		    )")

	def storeInDb(self,item):
		self.cur.execute("INSERT INTO Amazon(\
		    name, \
		    path, \
		    gender, \
		    type, \
		    source \
		    ) \
		VALUES( ?, ?, ?, ?, ?)", \
		( \
		    item.get('Name',''),
		    item.get('Path',''),
		    item.get('Gender',''),
		    item.get('Type',''),
		    item.get('Source','')
		))
		print '------------------------'
		print 'Data Stored in Database'
		print '------------------------'
		self.con.commit()

	def process_item(self, item, spider):
		self.storeInDb(item)
		return item

	def closeDB(self):
		self.con.close()

	def __del__(self):
		self.closeDB()
