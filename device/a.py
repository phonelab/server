import os 
Pwd = os.path.dirname(os.path.abspath(__file__))
Path = os.path.join(Pwd, 'Datalogger', '12345')
os.chdir(Path) #move to Path
for files in os.listdir("."):     #get list of files in the directory
	handle = open(files, 'r+')
	var = handle.read()
	print var;

