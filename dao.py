from flask.json import jsonify
from util import getConnect
import sql
import error
from dto import PhotoDTO 
import json


class PhotoDAO:
	def findAllUnlabeled(self):  
		dtoList = []
		try:
			conn = getConnect()
			cur = conn.cursor()
			try:
				cur.execute(sql.findAllUnlabeled) 
				rows = cur.fetchall()  
				dtoList = [PhotoDTO(row[0],row[1],row[2],row[3]) for row in rows]
			except Exception as e:
				print(error.findAllUnlabeled)
				print(e) 
			finally:
				cur.close() 
				conn.close()
		except Exception as e:
			print(error.connection)
			print(e) 

		return dtoList

	def findAllLabeled(self):  
		dtoList = []
		try:
			conn = getConnect()
			cur = conn.cursor()
			try:
				cur.execute(sql.findAllLabeled) 
				rows = cur.fetchall()  
				dtoList = [PhotoDTO(row[0],row[1],row[2],json.loads(row[3])["data"]) for row in rows]
				print(dtoList)
			except Exception as e:
				print(error.findAllLabeled)
				print(e) 
			finally:
				cur.close() 
				conn.close()
		except Exception as e:
			print(error.connection)
			print(e) 

		return dtoList

	def updateLabel(self, data):  
		result = False
		try:
			conn = getConnect()
			cur = conn.cursor()
			try:
				cur.execute("update photo set label=%s where photo_idx=%s", data) 
				conn.commit()
				result = True
			except Exception as e:
				conn.rollback()
				print(error.updateLabel)
				print(e) 
			finally:
				cur.close() 
				conn.close()
		except Exception as e:
			print(error.connection)
			print(e) 

		return result


class PhotographerDAO:
	def findByWorkIdx(workIdx):
		try:
			conn = getConnect()
			cur = conn.cursor()
			try:
				cur.execute(sql.findAllUnlabeled, workIdx) 
				row = cur.fetchone()
				print(row)
				photographerIdx = row[0]
				print(photographerIdx)
			except Exception as e:
				print(error.findAllUnlabeled)
				print(e) 
			finally:
				cur.close() 
				conn.close()
		except Exception as e:
			print(error.connection)
			print(e) 

		return photographerIdx


if __name__ == "__main__":
    # PhotoDAO().findAllUnlabeled()
    PhotoDAO().findAllLabeled()