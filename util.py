import pymysql
import config

def getCORS():
	return config.server


def getConnect():
	conn = pymysql.connect(
		host=config.picoHost, 
		db=config.picoDb, 
		port=config.picoPort,
		user=config.picoUser,
		password=config.picoPassword
	)

	return conn
