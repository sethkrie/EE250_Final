
global fileCont
global messageBuffer
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

# with open('header.txt', 'r') as headReader:
# 	try:

# 	    # Further file processing goes here
# 	    fileCont = fileCont + list(headReader)
# 	    #print("1 ",fileCont)
# 	finally:
# 	    headReader.close()

## adding header
headFormat = "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js\"></script>\n<!DOCTYPE html>\n<html>\n<body>\n"
fileCont.append(headFormat)

with open('body.txt', 'r') as contReader:
	try:
	    bodyBuffer = []
	    # Further file processing goes here
	    bodyBuffer = bodyBuffer + list(contReader)


	    for line in messageBuffer: #this writes the file into HTML
	    	middle  = line
	    	middle = "<p>"+"messge #"+middle+".</p>\n"
	    	bodyBuffer.append(middle)

	    #analyis
	    metricsBuffer = []
	    lengthOfHistory = len(bodyBuffer) - 1
	    metricText = "There are " + str(lengthOfHistory) +" messages"

	    metricsBuffer.append(metricText)


	    fileCont = fileCont + bodyBuffer + metricsBuffer
	    print(len(bodyBuffer))
	    #print("2 ", fileCont)
	finally:
	    contReader.close()

with open('footer.txt', 'r') as footReader:
	try:

	    # Further file processing goes here
	    fileCont = fileCont + list(footReader)
	    #print("3 ",fileCont)
	finally:
	    footReader.close()
	    
with open('templates/writeHTML.html', 'w') as writer:
    try:
    	str1 = ""
    	print(str1.join(fileCont))
    	writer.write(str1.join(fileCont))
    finally:
    	writer.close()	
	# except:
	#     print("something went wrong")


