class FileDB(object):
	"""A file based database.

    A file based database, read and write arguements in the specific file.
    """
	DIR = "/home/pi/.picar-4wd/"
	def __init__(self, db=None):
		'''Init the db_file is a file to save the datas.'''

		# Check if db_file is defined
		if db != None:
			self.db = db
		else:
			self.db = "config"

	def get(self, name, default_value=None):
		"""Get value by data's name. Default value is for the arguemants do not exist"""
		try:
			conf = open(self.DIR+self.db,'r')
			lines=conf.readlines()
			conf.close()
			flag = False
			# Find the arguement and set the value
			for line in lines:
				# print(line)
				if line.startswith('#'):
					continue
				# print("no#")
				if line.split('=')[0].strip() == name:
					# print(name)
					value = line.split('=')[1].replace(' ', '').strip()
					break
			else:
				# print("flag_error")
				return default_value

			return eval(value)

		except:
			# print("error")
			return default_value
	
	def set(self, name, value):
		"""Set value by data's name. Or create one if the arguement does not exist"""

		# Read the file
		conf = open(self.DIR+self.db,'r')
		lines=conf.readlines()
		conf.close()
		flag = False
		# Find the arguement and set the value
		for i, line in enumerate(lines):
			if line.startswith('#'):
				continue
			if line.split('=')[0].strip() == name:
				lines[i] = '%s = %s\n' % (name, value)
				break
		# If arguement does not exist, create one
		else:
			lines.append('%s = %s\n\n' % (name, value))

		# Save the file
		conf = open(self.DIR+self.db,'w')
		conf.writelines(lines)
		conf.close()

def test():
	name = "hhh"
	db = FileDB()
	print("Get not exist: %s" % db.get(name, 0))
	print("Set not exist: %s" % db.set(name, 10))
	print("Get exist: %s" % db.get(name, 0))
	print("Set exist: %s" % db.set(name, 20))
	print("Get exist: %s" % db.get(name, 0))

if __name__ == "__main__":
	test()