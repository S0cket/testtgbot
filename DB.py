import mysql.connector


def isExists(id: int):
	query = "select id from users where id={0}".format(id)
	with mysql.connector.connect(
		host="127.0.0.1",
		user="test",
		password="12345671",
		database="tgbot"
	) as connection:
		with connection.cursor() as cursor:
			cursor.execute(query)
			users = cursor.fetchall()
			return len(users) != 0


def addUser(id: int, name: str, stat: int = 0):
	query = "insert into users values ({0}, \"{1}\", {2})".format(id, name, stat)
	with mysql.connector.connect(
			host="127.0.0.1",
			user="test",
			password="12345671",
			database="tgbot"
	) as connection:
		with connection.cursor() as cursor:
			cursor.execute(query)
			connection.commit()


def getStat(id: int) -> int:
	query = "select stat from users where id={0}".format(id)
	with mysql.connector.connect(
			host="127.0.0.1",
			user="test",
			password="12345671",
			database="tgbot"
	) as connection:
		with connection.cursor() as cursor:
			cursor.execute(query)
			users = cursor.fetchall()
			return users[0][0]


def setStat(id: int, stat: int):
	query = "update users set stat={0} where id={1}".format(stat, id)
	with mysql.connector.connect(
			host="127.0.0.1",
			user="test",
			password="12345671",
			database="tgbot"
	) as connection:
		with connection.cursor() as cursor:
			cursor.execute(query)
			connection.commit()


