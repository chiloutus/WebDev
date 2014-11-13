
longWords = "longWords.txt"
fn = "/usr/share/dict/words"
with open(fn) as words:
	for line in words:
		with open(longWords,'w') as lWord:
			for line in words:
				if "\'" in line:
					continue
				elif len(line) >= 8:
					lWord.write(line + '\n')
