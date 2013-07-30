class DDRPowerEstimator:
	def __init__(self, ddrMem):
		self.ddrMem = ddrMem
	
	def parseLine(self, line):
		returnable = []
		returnable.append(float(line[0])) #RD%
		returnable.append(float(line[1])) #WR%
		returnable.append(float(line[2])) #PageHit%
		returnable.append(float(line[3])) #CKE_LO_PRE%
		returnable.append(float(line[4])) #CKE_LO_ACT
		returnable.append(float(line[5])) #BNK_PRE%

		return returnable

	def estimate(self, params):
		readPctg = params[0]
		writePctg = params[1]
		pageHitPctg = params[2]
		ckeLoPREPctg = params[3]
		ckeLoACTPctg = params[4]
		bnkPREPctg = params[5]
		tACT = self._calcTACT(self.ddrMem.bL, self.ddrMem.tCK, readPctg, writePctg, pageHitPctg)

		PRE_PDN = self._calcPRE_PDN(self.ddrMem.idd2p, self.ddrMem.vdd, bnkPREPctg, ckeLoPREPctg)
		PRE_STBY = self._calcPRE_STBY(self.ddrMem.idd2f, self.ddrMem.vdd, bnkPREPctg, ckeLoPREPctg)
		ACT_PDN = self._calcACT_PDN(self.ddrMem.idd3p, self.ddrMem.vdd, bnkPREPctg, ckeLoACTPctg)
		ACT_STBY = self._calcACT_STBY(self.ddrMem.idd3n, self.ddrMem.vdd, bnkPREPctg, ckeLoACTPctg)
		ACT = self._calcACT(self.ddrMem.idd0, self.ddrMem.idd3n, self.ddrMem.tRC, tACT, self.ddrMem.vdd)
		WR = self._calcWR(self.ddrMem.idd4w, self.ddrMem.idd3n, writePctg, self.ddrMem.vdd)
		RD = self._calcRD(self.ddrMem.idd4r, self.ddrMem.idd3n, readPctg, self.ddrMem.vdd)
		DQ = self._calcDQ(self.ddrMem.pPerDQ, self.ddrMem.numDQ, self.ddrMem.numDQS, readPctg)
		REF = self._calcREF(self.ddrMem.idd5a, self.ddrMem.idd2p, self.ddrMem.vdd)


		returnable = ''
		returnable += str(PRE_PDN) + ';'
		returnable += str(PRE_STBY) + ';'
		returnable += str(ACT_PDN) + ';'
		returnable += str(ACT_STBY) + ';'
		returnable += str(ACT) + ';'
		returnable += str(WR) + ';'
		returnable += str(RD) + ';'
		returnable += str(DQ) + ';'
		returnable += str(REF) + ';'
		returnable += str(PRE_PDN + PRE_STBY + ACT_PDN + ACT_STBY + ACT + WR + RD + DQ + REF) 


		return returnable

	def _calcTACT(self, bL, tCK, readPctg, writePctg, pageHitPctg):
		colToCol = ((bL/2.0) * tCK) / (readPctg + writePctg)
		tACT = colToCol / (1 - pageHitPctg)
		return tACT

	def _calcPRE_PDN(self, idd2p, vdd, bnkPREPctg, ckeLoPREPctg):
		PRE_PDN = idd2p * vdd * bnkPREPctg * ckeLoPREPctg
		return PRE_PDN

	def _calcPRE_STBY(self, idd2f, vdd, bnkPREPctg, ckeLoPREPctg):
		PRE_STBY = idd2f * vdd * bnkPREPctg * (1-ckeLoPREPctg)
		return PRE_STBY

	def _calcACT_PDN(self, idd3p, vdd, bnkPREPctg, ckeLoACTPctg):
		ACT_PDN = idd3p * vdd * (1-bnkPREPctg) * ckeLoACTPctg
		return ACT_PDN

	def _calcACT_STBY(self, idd3n, vdd, bnkPREPctg, ckeLoACTPctg):
		ACT_STBY = idd3n * vdd * (1-bnkPREPctg) * (1-ckeLoACTPctg)
		return ACT_STBY

	def _calcACT(self, idd0, idd3n, tRC, tACT, vdd):
		P_ACT = (idd0 - idd3n) * (tRC/tACT) * vdd
		return P_ACT

	def _calcWR(self, idd4w, idd3n, writePctg, vdd):
		P_WR = (idd4w - idd3n) * writePctg * vdd
		return P_WR

	def _calcRD(self, idd4r, idd3n, readPctg, vdd):
		P_RD = (idd4r - idd3n) * readPctg * vdd
		return P_RD

	def _calcDQ(self, pPerDQ, numDQ, numDQS, readPctg):
		P_DQ = pPerDQ * (numDQ + numDQS) * readPctg
		return P_DQ

	def _calcREF(self, idd5a, idd2p, vdd):
		P_REF = (idd5a - idd2p) * vdd
		return P_REF
	
	def getHeader(self):
		return 'PRE_PDN PRE_STBY ACT_PDN ACT_STBY ACT WR RD DQ REF TOT'
