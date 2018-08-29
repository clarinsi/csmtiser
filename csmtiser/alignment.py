#! /usr/bin/python
# -*- coding: utf-8 -*-


import codecs, math, sys, os, re

verbatim=False

# from http://hetland.org/coding/python/levenshtein.py
def levenshtein(a, b):
	"Calculates the Levenshtein distance between a and b."
	n = len(a)
	m = len(b)
	if n > m:
		# Make sure n <= m, to use O(min(n,m)) space
		a,b = b,a
		n,m = m,n   
	current = range(n+1)
	for i in range(1,m+1):
		previous, current = current, [i]+[0]*n
		for j in range(1,n+1):
			add = previous[j]+1
			delete = current[j-1]+1
			change = previous[j-1]
			if a[j-1] != b[i-1]:
				change = change + 1
			current[j] = min(add, delete, change)
	return current[n]


# normalised Levenshtein distance
def normLevenshtein(a, b):
	if a == b:
		return 0.0
	else:
		l = levenshtein([x.lower() for x in a], [x.lower() for x in b])
		return l / float(max(len(a), len(b)))


def getUnderscoreAlignments(oChars, tChars, alignments, SEP="_"):
	underscorePairs = []
	for alignment in alignments:
		oUnderscoreIndices = [i for i in range(alignment[0], alignment[1]) if oChars[i] == SEP]
		tUnderscoreIndices = [i for i in range(alignment[2], alignment[3]) if tChars[i] == SEP]
		
		# assume monotone underscore alignment in case of identical counts
		if len(oUnderscoreIndices) == len(tUnderscoreIndices):
			alignedUnderscoreIndices = zip(oUnderscoreIndices, tUnderscoreIndices)
			underscorePairs.extend(alignedUnderscoreIndices)
		
		else:
			# if there are more source than target underscores, just display a message
			# this is taken care of by None alignments and the splitByUnderscoreAlignment procedure
			if len(oUnderscoreIndices) > len(tUnderscoreIndices):
				if verbatim:
					print "** More oUnderscores than tUnderscores:", oUnderscoreIndices, ("".join(oChars[alignment[0]:alignment[1]])).encode('utf-8'), tUnderscoreIndices, ("".join(tChars[alignment[2]:alignment[3]])).encode('utf-8')
		
			# match every element of oUnderscoreIndices with one element of tUnderscoreIndices - there may be unmatched tUnderscoreIndices elements but no unmatched oUnderscoreIndices elements
			#print ">>>", "".join(oChars[alignment[0]:alignment[1]]), "<<>>", "".join(tChars[alignment[2]:alignment[3]])
			for ou in oUnderscoreIndices:
				# first approach: select the tu that splits the phrase into two chunks that are most equally sized to the two chunks obtained by the ou
				ouRelPrefixLen = len(oChars[alignment[0]:ou]) / float(len(oChars[alignment[0]:alignment[1]]))
				ouRelSuffixLen = len(oChars[ou+1:alignment[1]]) / float(len(oChars[alignment[0]:alignment[1]]))
				tuRelPrefixLens = [len(tChars[alignment[2]:tu]) / float(len(tChars[alignment[2]:alignment[3]])) for tu in tUnderscoreIndices]
				tuRelSuffixLens = [len(tChars[tu+1:alignment[3]]) / float(len(tChars[alignment[2]:alignment[3]])) for tu in tUnderscoreIndices]
				differences = [math.sqrt((ouRelPrefixLen-tuRelPrefixLens[i])**2 + (ouRelSuffixLen-tuRelSuffixLens[i])**2) for i in range(len(tUnderscoreIndices))]
				minDifferences = [x for x in differences if x == min(differences)]
				#print ">>", ("".join(oChars[alignment[0]:alignment[1]])).encode('utf-8'), ("".join(tChars[alignment[2]:alignment[3]])).encode('utf-8'), ou, differences, minDifferences
				
				if len(differences) == 0:
					if verbatim:
						print "** No candidates for oUnderscore, add empty alignment"
					underscorePairs.append((ou, None))
				
				elif (len(differences) == 1) and (differences[0] == 0):
					if verbatim:
						print "** Only candidate has zero value, add empty alignment"
					underscorePairs.append((ou, None))
					
				# unambiguous solution (most cases)
				elif len(minDifferences) == 1:
					underscorePairs.append((ou, tUnderscoreIndices[differences.index(minDifferences[0])]))
				
				# ties (very few cases)
				# second approach: compare the preceding character and the following character of the tu with the preceding and following character of the ou and select closest one
				else:
					ouPrefixChar = oChars[ou-1]
					ouSuffixChar = oChars[ou+1]
					tuPrefixChars = [tChars[tu-1] if tu-1 >= 0 else "" for tu in tUnderscoreIndices]
					tuSuffixChars = [tChars[tu+1] if tu+1 < len(tChars) else "" for tu in tUnderscoreIndices]
					if verbatim:
						print "** Ambiguous alignment - checking surrounding characters:", ouPrefixChar+"__"+ouSuffixChar, "".join(tuPrefixChars)+"__"+"".join(tuSuffixChars)
					differences = [math.sqrt(int(ouPrefixChar!=tuPrefixChars[i])**2 + int(ouSuffixChar!=tuSuffixChars[i])**2) for i in range(len(tUnderscoreIndices))]
					minDifferences = [x for x in differences if x == min(differences)]
					
					# there could be ties here as well but we don't bother
					if len(minDifferences) > 1:
						if verbatim:
							print "** Tie after two difference calculations - taking first:", "".join(oChars[alignment[0]:alignment[1]]), "<<>>", "".join(tChars[alignment[2]:alignment[3]]), ou, tUnderscoreIndices, differences
					underscorePairs.append((ou, tUnderscoreIndices[differences.index(minDifferences[0])]))
	return underscorePairs


def splitByUnderscoreAlignment(oChars, tChars, uAlignments):
	wordpairs = []
	uAlignments.insert(0, (-1, -1))
	uAlignments.append((len(oChars), len(tChars)))
	
	for i in range(1, len(uAlignments)):
		ou = uAlignments[i][0]
		prevou = uAlignments[i-1][0]
		oword = oChars[prevou+1:ou]
		
		tu = uAlignments[i][1]
		prevtu = uAlignments[i-1][1]
		if prevtu is None:
			tword = []
		elif tu is None:
			j = i+1
			while uAlignments[j][1] is None:
				j += 1
			nexttu = uAlignments[j][1]
			tword = tChars[prevtu+1:nexttu]
		else:
			tword = tChars[prevtu+1:tu]
		
		if (len(oword) > 0) or (len(tword) > 0):
			#print "".join(oword).encode('utf-8'), "".join(tword).encode('utf-8')
			wordpairs.append((oword, tword))
	
	for i in range(len(wordpairs)):
		o, t = wordpairs[i]
		if t == []:
			j = i - 1
			while wordpairs[j][1] == "":
				j -= 1
			prevDistance = normLevenshtein(wordpairs[j][0], wordpairs[j][1])
			distance = normLevenshtein(o, wordpairs[j][1])
			if distance < prevDistance:
				if verbatim:
					print "** Reattach {} from {} to {}".format("".join(wordpairs[j][1]).encode('utf-8'), "".join(wordpairs[j][0]).encode('utf-8'), "".join(o).encode('utf-8'))
				wordpairs[i] = (wordpairs[i][0], wordpairs[j][1])
				wordpairs[j] = (wordpairs[j][0], "")
	return wordpairs


def rebalanceAlignments(oChars, tChars, alignments, SEP="_"):
	previousCounts = (0, 0)
	previousSequence = ("", "")
	alignments2 = []
	for i, alignment in enumerate(alignments):
		oSequence = oChars[alignment[0]:alignment[1]]
		tSequence = tChars[alignment[2]:alignment[3]]
		currentCounts = (oSequence.count(SEP), tSequence.count(SEP))
		if (currentCounts[0] != currentCounts[1]) and (currentCounts[0]+previousCounts[0] == currentCounts[1]+previousCounts[1]):
			if verbatim:
				print "** Merge alignments:", "".join(previousSequence[0]), "".join(previousSequence[1]), "".join(oSequence), "".join(tSequence)
			mergedAlignment = (alignments[i-1][0], alignment[1], alignments[i-1][2], alignment[3])
			alignments2.append(mergedAlignment)
			try:
				alignments2.remove(alignments[i-1])
			except ValueError:
				print "Cannot remove alignment point:", alignments[i-1]
		else:
			alignments2.append(alignment)
		previousCounts = currentCounts
		previousSequence = (oSequence, tSequence)
	return alignments2


def extractAlignments(transElements):
	transChars = []
	transAlignments = []
	previousAlignmentStart = 0
	for i, c in enumerate(transElements):
		if c.startswith("|"):
			srcIndices = c.strip("|").split("-")
			srcIndicesInt = (int(srcIndices[0]), int(srcIndices[1])+1)	# convert to Python indices
			tgtIndicesInt = (previousAlignmentStart, len(transChars))
			previousAlignmentStart = len(transChars)
			transAlignments.append((srcIndicesInt[0], srcIndicesInt[1], tgtIndicesInt[0], tgtIndicesInt[1]))
		else:
			transChars.append(c)
	return transChars, transAlignments
	
def case(orig,trans):
	if orig.isupper():
		trans=trans.upper()
	if orig.istitle():
		trans=trans[:1].upper()+trans[1:]
	return trans

def retokenize(orig_segm, trans_segm, verticalized, casing=False, SEP="_", DELETED="DELETED", encoding='utf-8'):
	orig_segm_file = codecs.open(orig_segm, 'r', encoding)
	trans_segm_file = codecs.open(trans_segm, 'r', encoding)
	verticalized_file = codecs.open(verticalized, 'w', encoding)
	
	for origsentence, transsentence in zip(orig_segm_file, trans_segm_file):
		origsentence = re.sub(r'<.+?>', '', origsentence)		# get rid of xml constraint annotation
		origchars = origsentence.strip().split(" ")
		transelements = transsentence.strip().split(" ")
		transchars, transalignments = extractAlignments(transelements)
		transalignments = rebalanceAlignments(origchars, transchars, transalignments, SEP)
		underscorealignments = getUnderscoreAlignments(origchars, transchars, transalignments, SEP)
		wordpairs = splitByUnderscoreAlignment(origchars, transchars, underscorealignments)
		first=True
		for origword, transword in wordpairs:
			origword="".join(origword)
			transword="".join(transword)
			if casing:
				if first:
					first=False
					if origword.islower():
						origword=origword[:1].upper()+origword[1:]
						transword=transword[:1].upper()+transword[1:]
					elif origword.istitle():
						transword=transword[:1].upper()+transword[1:]
				else:
					transword=case(origword,transword)
			if len(transword)==0:
				transword=DELETED
			verticalized_file.write(origword + "\t" + transword.replace(SEP, " ") + "\n")
		verticalized_file.write("\n")
	orig_segm_file.close()
	trans_segm_file.close()
	verticalized_file.close()

if __name__ == "__main__":
	#retokenize("test.orig", "test.translated", "test.retok.orig", "test.retok.translated")
	#retokenize(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	verbatim=True
	retokenize(sys.argv[1],sys.argv[1]+'.norm',sys.argv[1]+'.norm.align')
