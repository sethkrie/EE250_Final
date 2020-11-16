from flask import Flask, render_template

def DataProcessing (myList):
	     ############# from properly formated list of strings
	users = dict()
	msgCont = []
	output = []
	for items in myList:
	    if ": " in items:
	        current = items.rsplit(":")[0]
	        msgCont.append((items.rsplit(":")[1]).strip())
	        users[current] = users.get(current,0) + 1

	output.append("Here are the users ")                              #"There are "+str(len(users))+" users dectected")
	output = output + list(users.keys())




	messageTotal = sum(users.values())
	output.append("There are "+str(messageTotal)+" messages")
	        
	aveLen = 0
	for j in msgCont:
	    aveLen = len(j)
	    
	aveLen = aveLen / len(msgCont)
	output.append("average message length = "+str(aveLen))

	return output

def Text2HTML():

	fileCont = []
	messageBuffer = []


	with open('MessageLog.txt', 'r') as LogReader:
		try:
			#This will take a file and read it into buffer
			for line in LogReader:
				messageBuffer.append(line)
				#print(type(line))
		finally:
		    LogReader.close()

	################################ Adding header
	headFormat = "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js\"></script>\n<!DOCTYPE html>\n<html>\n<body>\n"
	fileCont.append(headFormat)

	################################ Adding body
	bodyBuffer = []


	# Further file processing goes here
	title = "<h1>Chat history:</h1>\n"
	fileCont.append(title)
	messageDataStream = list()

	for line in messageBuffer: #this writes the file into HTML
		middle  = line.rstrip("\n")
		middle = "<p>"+"messege # "+middle+"</p>\n"
		bodyBuffer.append(middle)
		##HOLDING LIST FOR LATER USE in my list
		txt = line
		holderList = txt.split("\n")
		for i in holderList:
				if len(i)>2:
					messageDataStream.append(i)


	################################ Analyis
	# metricsBuffer = []
	# lengthOfHistory = len(bodyBuffer)
	# metricText = "There are " + str(lengthOfHistory) +" messages"
	# metricsBuffer.append(metricText)
	

	datametrics = DataProcessing(messageDataStream)
	for line in datametrics: #this writes the file into HTML
		middle = "<p>"+ line +"</p>\n"
		bodyBuffer.append(middle)
    #This will take a file and read it into buffer

	fileCont = fileCont + bodyBuffer
	############################## Adding footer
	title = "\n</body>\n</html>"
	fileCont.append(title)

	############################## Writing to file
	with open('templates/writeHTML.htm', 'w') as writer:
	    try:
	    	str1 = ""
	    	writer.write(str1.join(fileCont))
	    except:
	        print("something went wrong")
	    finally:
	    	writer.close()	


app = Flask(__name__)

@app.route('/')
def home():
    j = "hi"
    Text2HTML()
    return render_template('writeHTML.htm')


if __name__ == '__main__':
    app.run(debug=True)
    i = 0

'''
This function takes template text files and stiches them together into an HTML file the component files are 
1. MessageLog.txt
'''

"""
def DataProcessing ( myList)
	     ############# from properly formated list of strings
	users = dict()
	msgCont = []
	for items in myList:
	    if ":" in items:
	        current = items.rsplit(":")[0]
	        msgCont.append((items.rsplit(":")[1]).strip())
	        users[current] = users.get(current,0) + 1
	        print(current)
	print("There are ",len(users)," users dectected")
	messageTotal = sum(users.values())
	print("There are ",messageTotal," messages")
	        
	aveLen = 0
	for j in msgCont:
	    aveLen = len(j)
	    
	aveLen = aveLen / len(msgCont)
	print("average message length = ",aveLen)
"""