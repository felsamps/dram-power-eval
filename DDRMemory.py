class DDRMemory:
	def __init__(self, fileName):
		self.fp = open(fileName, 'r')
		self.__parseFile()
		self.fp.close()
	
	def __parseFile(self):
		buff = self.fp.readlines()
		self.reportList = []
		for line in buff:
			tokens = line.split()
			if tokens[0] == 'VDD':
				self.vdd = float(tokens[2])
			elif tokens[0] == 'tCK':
				self.tCK = float(tokens[2]) * 0.000000001
			elif tokens[0] == 'tRC':
				self.tRC = float(tokens[2]) * 0.000000001
			elif tokens[0] == 'P_DQ':
				self.pPerDQ = float(tokens[2]) * 0.001
			elif tokens[0] == 'WORD_SIZE':
				self.wordSize = int(tokens[2])
			elif tokens[0] == 'PAGE_SIZE':
				self.pageSize = int(tokens[2])
			elif tokens[0] == 'IDD2P':
				self.idd2p = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD2F':
				self.idd2f = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD3P':
				self.idd3p = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD3N':
				self.idd3n = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD0':
				self.idd0 = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD4W':
				self.idd4w = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD4R':
				self.idd4r = float(tokens[2]) * 0.001
			elif tokens[0] == 'IDD5A':
				self.idd5a = float(tokens[2]) * 0.001
			elif tokens[0] == 'BL':
				self.bL = int(tokens[2])
			elif tokens[0] == 'NUM_DQ':
				self.numDQ = int(tokens[2])
			elif tokens[0] == 'NUM_DQS':
				self.numDQS = int(tokens[2])

			self.reportList.append([tokens[0], tokens[2]]);


	def reportDDRParams(self):
		print self.reportList




			

