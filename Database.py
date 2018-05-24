# Import Section
import MySQLdb
import MySQLdb.cursors

# Class Definition Section
class Database:
	# Constructor
	def __init__(self):
		# Initializing Database object's variables
		self.host = "localhost"
		self.user = "root"
		self.password = "kshitijpcmysql"
		self.database = "expense"

		# Connecting to MySQL Database Server
		self.link = MySQLdb.connect(self.host, self.user, self.password, self.database, cursorclass=MySQLdb.cursors.DictCursor)
		# Declaring Cursor
		self.cursor = self.link.cursor()
	# End __init__() Constructor

	# Query Executer
	def query(self, sql):
		self.cursor.execute(sql)
	# End query()

	# Fetching all the Result from the cursor.
	def fetchAll(self):
		return self.cursor.fetchall()
	# End fetchAll()

	# Select method to execute SELECT queries
	def select(self, columns, table, where = "", extras = ""):
		sql = "SELECT {} FROM {}".format(columns, table)
		if where != "":
			sql = sql + " WHERE {}".format(where)
		sql = sql + " {}".format(extras)
		self.query(sql)
		return self.fetchAll()
	# End select()

	# Insert method to execute INSERT statements
	def insert(self, table, data=dict()):
		sql = "INSERT INTO {} (".format(table)
		# Getting columns, first column without ',' symbol
		for column, value in data.iteritems():
			sql = sql + "`{}`".format(column)
			break
		# Getting columns, later columns with ',' symbol
		count = 0
		for column, value in data.iteritems():
			# skipping first key
			if count == 0:
				count = count + 1 
				continue
			sql = sql + ", `{}`".format(column)
		sql = sql + ") VALUES("
		# Getting values, first value without ',' symbol
		for column, value in data.iteritems():
			sql = sql + "'{}'".format(value)
			break
		# Getting values, later values with ',' symbol
		count = 0
		for column, value in data.iteritems():
			# skipping first value
			if count == 0:
				count = count + 1 
				continue
			sql = sql + ", '{}'".format(value)
		sql = sql + ")"

		try:
			self.cursor.execute(sql)
			self.link.commit()
			return True
		except:
			self.link.rollback()
			return False
	# End Insert()

	def getLastInsertId(self):
		return self.cursor.lastrowid

	# Update method
	def update(self, table, data=dict(), where="1=1"):
		sql = "UPDATE {} SET ".format(table)
		# Getting columns, first column without ',' symbol
		for column, value in data.iteritems():
			sql = sql + "`{}` = '{}'".format(column, value)
			break
		# Getting columns, later columns with ',' symbol
		count = 0
		for column, value in data.iteritems():
			# skipping first key
			if count == 0:
				count = count + 1 
				continue
			sql = sql + ", `{}` = '{}'".format(column, value)
		sql = sql + " WHERE {}".format(where)
		try:
			self.cursor.execute(sql)
			self.link.commit()
			return True
		except:
			self.link.rollback()
			return False
	# End Update

	# Delete Method
	def delete(self, table, where="1=1"):
		sql = "DELETE FROM {} WHERE {}".format(table, where)
		try:
			self.cursor.execute(sql)
			self.link.commit()
			return True
		except:
			self.link.rollback()
			return False
	# End Delete method

# End Class

# Creating Database object
db = Database()

# Performing Insert operation.
result = db.insert("user", {
	"name": "John Smith",
	"email": "john.smith@example.com",
})

# Print last insert id
print db.getLastInsertId()

# Performing Update Operation
result = db.update("user", { "name": "John Doe" }, "email = 'john.smith@example.com'")
print result

# Performing Delete Operation
result = db.delete("user", "email = 'john.smith@example.com'")
print result