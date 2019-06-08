import math
import sys
cachetype = sys.argv[4]		#checking whether cache is split or unified
associativity = int(sys.argv[3])	#checking for associativity if its direct mapped or 4-way
inputFL = open("/home/girija/CompArch/HW1/trace.din","r")
linecount = len(inputFL.readlines())
inputFL.close()
inputF = open("/home/girija/CompArch/HW1/trace.din","r")	#memory trace file - trace.din
########################################################################################
########################################################################################

if cachetype == 'U':		#for unified cache
	cachesize = int(sys.argv[1]) * 1024
	blocksize = int(sys.argv[2])
	numLines = cachesize / blocksize
	indices = numLines / associativity
	hit = 0
	miss = 0
	access = 0
	flag = 0
	cache = [0] * numLines
	validBit = [0] * numLines
	age = [0] * numLines
	previousInvalid = 0
	previousValid = 0

####################################################################################3
	if associativity == 1:		#for direct mapped
		for x in range(1,linecount):
			line = inputF.readline()
			access += 1
			temp = line.split(' ')[1]
			templength = len(temp)	#string length
			tempaddress = int(temp[0:templength-1],16)	#int
			address = bin(tempaddress)[2:]	#binary
			addressL = len(address)
			addressLength = int(addressL)
			#Extracting the offset, index and tag from memory address
			offsetBits = int(math.log(blocksize,2))
			indexBits = int(math.log(indices,2))
			offsetB = address[addressLength-offsetBits:addressLength]
			indexB = address[addressLength-offsetBits-indexBits:addressLength-offsetBits]
			tagB = address[:addressLength-offsetBits-indexBits]
			offset = int(offsetB,2)
			index = int(indexB,2)
			tag = int(tagB,2)

			if validBit[index] == 1:		#checking that if index in valid
				if cache[index] == tag:		#checking if index in cache has the required data	
					hit += 1		#if tag(data) is present then incrementing the hit count 
				else:
					miss += 1		#its a miss
					cache[index] = tag	#putting tag at that index in cache
			else:
				miss += 1			
				validBit[index] = 1		#setting the valid bit to 1 as data is taken into the cache at index
				cache[index] = tag

		print("miss: %d" %(miss))
		print("hit: %d" %(hit))	
		print("accesses: %d" %(access))	
		inputF.close()

#######################################################################################
	if associativity == 4:	#for 4-way assocaitive
		for x in range(1,linecount):
			line = inputF.readline()
			access += 1
			temp = line.split(' ')[1]
			templength = len(temp)	#string length
			tempaddress = int(temp[0:templength-1],16)	#int
			address = bin(tempaddress)[2:]	#binary
			addressL = len(address)
			addressLength = int(addressL)
			offsetBits = int(math.log(blocksize,2))
			indexBits = int(math.log(indices,2))
			offsetB = address[addressLength-offsetBits:addressLength]
			indexB = address[addressLength-offsetBits-indexBits:addressLength-offsetBits]
			tagB = address[:addressLength-offsetBits-indexBits]
			offset = int(offsetB,2)
			index = int(indexB,2)
			tag = int(tagB,2)

			for x in range(0, associativity):			#checking for all lines in given index of cache
				if validBit[index * associativity + x] == 1:
					if cache[index * associativity + x] == tag:
						hit += 1		#if at any location tag is present then incrementing the hit count
						flag = 1
						break
			if flag == 1:
				flag =0

			else:
				miss += 1
				for x in range(0, associativity):
					if validBit[index * associativity + x] == 0:
						cache[index * associativity + x] = tag	#putting the data at index where valid bit is 0
						validBit[index * associativity + x] = 1
						age[index * associativity + x] = 0	#making that index as most recently accessed index
						previousInvalid = 1
						break

				if previousInvalid == 1:	#incrementing the ages of other 3 lines in particular index
					previousInvalid = 0
					if x == 0:
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					elif x == 1:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					elif x == 2:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					else:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1

				for y in range(0, associativity):
					LRU = max(age[index * associativity + 0],age[index * associativity + 1],age[index * associativity + 2],age[index * associativity + 3])	#for application of LRU replacement policy. checking which line in index is least recently used
					if validBit[index * associativity + y] == 1:	
						if age[index * associativity + y] == LRU:
							cache[index * associativity + y] = tag	#putting data at location whose age is maximum
							#validBit[index * associativity + y] = 1
							age[index * associativity + y] = 0
							previousValid = 1
							break

				if previousValid == 1:	#modifying the ages of other 3
					previousValid = 0
					if y == 0:
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					elif y == 1:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					elif y == 2:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 3] < 3: age[index * associativity + 3] += 1
					else:
						if age[index * associativity + 0] < 3: age[index * associativity + 0] += 1
						if age[index * associativity + 1] < 3: age[index * associativity + 1] += 1
						if age[index * associativity + 2] < 3: age[index * associativity + 2] += 1

		print("miss: %d" %(miss))
		print("hit: %d" %(hit))	
		print("accesses: %d" %(access))	
		inputF.close()


##########################################################################################
if cachetype == 'S':	#for split cache
	cachesize = int(sys.argv[1]) / 2
	datasize = cachesize * 1024
	instructionsize = cachesize * 1024
	blocksize = int(sys.argv[2])
	numLines = cachesize * 1024 / blocksize
	indices = numLines / associativity
	dhit = 0
	dmiss = 0
	ihit = 0
	imiss = 0
	access = 0
	dflag = 0
	iflag = 0
	dcache = [0] * numLines
	dvalidBit = [0] * numLines
	icache = [0] * numLines
	ivalidBit = [0] * numLines
	dage = [0] * numLines
	iage = [0] * numLines
	dpreviousInvalid = 0
	dpreviousValid = 0
	ipreviousInvalid = 0
	ipreviousValid = 0

##############################################################################################
	if associativity == 1:	#for direct mapped
		for x in range(1,linecount):
			line = inputF.readline()
			access += 1
			split = int(line.split(' ')[0])
			temp = line.split(' ')[1]
			templength = len(temp)	#string length
			tempaddress = int(temp[0:templength-1],16)	#int
			address = bin(tempaddress)[2:]	#binary
			addressL = len(address)
			addressLength = int(addressL)
			offsetBits = int(math.log(blocksize,2))
			indexBits = int(math.log(indices,2))
			offsetB = address[addressLength-offsetBits:addressLength]
			indexB = address[addressLength-offsetBits-indexBits:addressLength-offsetBits]
			tagB = address[:addressLength-offsetBits-indexBits]
			offset = int(offsetB,2)
			index = int(indexB,2)
			tag = int(tagB,2)

	
			if split == 2:	#checking if its a instruction address or data. 2 indiactes the instruction
				if ivalidBit[index] == 1:
					if icache[index] == tag:
						ihit += 1
					else:
						imiss += 1
						icache[index] = tag
				else:
					imiss += 1
					ivalidBit[index] = 1
					icache[index] = tag

			else:
				if dvalidBit[index] == 1:
					if dcache[index] == tag:
						dhit += 1
					else:
						dmiss += 1
						dcache[index] = tag
				else:
					dmiss += 1
					dvalidBit[index] = 1
					dcache[index] = tag

		print("Data miss: %d" %(dmiss))
		print("Data hit: %d" %(dhit))	
		print("Instruction miss: %d" %(imiss))
		print("Instruction hit: %d" %(ihit))
		print("accesses: %d" %(access))	
		inputF.close()


##############################################################################################
	if associativity == 4:	#for 4-way associative
		for x in range(1,linecount):
			line = inputF.readline()
			access += 1
			split = int(line.split(' ')[0])
			temp = line.split(' ')[1]
			templength = len(temp)	#string length
			tempaddress = int(temp[0:templength-1],16)	#int
			address = bin(tempaddress)[2:]	#binary
			addressL = len(address)
			addressLength = int(addressL)
			offsetBits = int(math.log(blocksize,2))
			indexBits = int(math.log(indices,2))
			offsetB = address[addressLength-offsetBits:addressLength]
			indexB = address[addressLength-offsetBits-indexBits:addressLength-offsetBits]
			tagB = address[:addressLength-offsetBits-indexBits]
			offset = int(offsetB,2)
			index = int(indexB,2)
			tag = int(tagB,2)


			if split == 2:	#instruction
				for x in range(0, associativity):
					if ivalidBit[index * associativity + x] == 1:
						if icache[index * associativity + x] == tag:
							ihit += 1
							iflag = 1
							break
				if iflag == 1:
					iflag =0

				else:
					imiss += 1
					for x in range(0, associativity):
						if ivalidBit[index * associativity + x] == 0:
							icache[index * associativity + x] = tag
							ivalidBit[index * associativity + x] = 1
							iage[index * associativity + x] = 0
							ipreviousInvalid = 1
							break

					if ipreviousInvalid == 1:
						ipreviousInvalid = 0
						if x == 0:
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						elif x == 1:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						elif x == 2:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						else:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1

					for y in range(0, associativity):
						LRU = max(iage[index * associativity + 0],iage[index * associativity + 1],iage[index * associativity + 2],iage[index * associativity + 3])
						if ivalidBit[index * associativity + y] == 1:	
							if iage[index * associativity + y] == LRU:
								icache[index * associativity + y] = tag
								iage[index * associativity + y] = 0
								ipreviousValid = 1
								break

					if ipreviousValid == 1:
						ipreviousValid = 0
						if y == 0:
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						elif y == 1:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						elif y == 2:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 3] < 3: iage[index * associativity + 3] += 1
						else:
							if iage[index * associativity + 0] < 3: iage[index * associativity + 0] += 1
							if iage[index * associativity + 1] < 3: iage[index * associativity + 1] += 1
							if iage[index * associativity + 2] < 3: iage[index * associativity + 2] += 1
			
			else:			#data
				for x in range(0, associativity):
					if dvalidBit[index * associativity + x] == 1:
						if dcache[index * associativity + x] == tag:
							dhit += 1
							dflag = 1
							break
				if dflag == 1:
					dflag =0

				else:
					dmiss += 1
					for x in range(0, associativity):
						if dvalidBit[index * associativity + x] == 0:
							dcache[index * associativity + x] = tag
							dvalidBit[index * associativity + x] = 1
							dage[index * associativity + x] = 0
							dpreviousInvalid = 1
							break

					if dpreviousInvalid == 1:
						dpreviousInvalid = 0
						if x == 0:
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						elif x == 1:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						elif x == 2:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						else:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1

					for y in range(0, associativity):
						LRU = max(dage[index * associativity + 0],dage[index * associativity + 1],dage[index * associativity + 2],dage[index * associativity + 3])
						if dvalidBit[index * associativity + y] == 1:	
							if dage[index * associativity + y] == LRU:
								dcache[index * associativity + y] = tag
								dage[index * associativity + y] = 0
								dpreviousValid = 1
								break

					if dpreviousValid == 1:
						dpreviousValid = 0
						if y == 0:
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						elif y == 1:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						elif y == 2:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 3] < 3: dage[index * associativity + 3] += 1
						else:
							if dage[index * associativity + 0] < 3: dage[index * associativity + 0] += 1
							if dage[index * associativity + 1] < 3: dage[index * associativity + 1] += 1
							if dage[index * associativity + 2] < 3: dage[index * associativity + 2] += 1

		print("Data miss: %d" %(dmiss))
		print("Data hit: %d" %(dhit))	
		print("Instruction miss: %d" %(imiss))
		print("Instruction hit: %d" %(ihit))
		print("accesses: %d" %(access))	
		inputF.close()

