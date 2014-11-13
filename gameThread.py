import os,random
def get_random_line(file_name):
	total_bytes = os.stat(file_name).st_size 
	random_point = random.randint(0, total_bytes)
	file = open(file_name)
	file.seek(random_point)
	file.readline() # skip this line to clear the partial line
	print(file.readline())
	return file.readline()#variables

shortWord = open("shortWords.txt", "r")
count = 0
line = ""			
#print(l[2])
line = get_random_line("longWords.txt")
usrin = input("Your word is:" + line + " Please find words that are contained within!")
count = len(usrin)
if usrin + "\n" in shortWord:
	print("Hey!")
	for i in usrin:
		if i in line:
			count -= 1
			print("I'm over here now")

if count == 0:
	print("Good Job")
print(count)
