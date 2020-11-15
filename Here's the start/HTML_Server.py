from flask import Flask, render_template


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

	for line in messageBuffer: #this writes the file into HTML
		middle  = line.rstrip("\n")
		middle = "<p>"+"messege # "+middle+"</p>\n"
		bodyBuffer.append(middle)

	################################ Analyis
	metricsBuffer = []
	lengthOfHistory = len(bodyBuffer)
	metricText = "There are " + str(lengthOfHistory) +" messages"
	metricsBuffer.append(metricText)
	fileCont = fileCont + bodyBuffer+ metricsBuffer


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


""

'''