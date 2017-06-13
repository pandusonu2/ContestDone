from django.http import HttpResponse
import json,requests

jsonData = ''

def index(request, user):
	global jsonData
	with open('probelms.txt', 'r') as file:
		jsonData = file.read().replace('\n','')
	jsonData = json.loads(jsonData)
	content = ""
	full, partial = getUserProgress(user)
	LTIME,COOK,month,year = 20,54,0,15
	months = ['JAN', 'FEB', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
	while month+year*12 < 5+17*12:
		ltime = "LTIME" + str(LTIME)
		cookoff = "COOK" + str(COOK)
		longContest = months[month] + str(year)
		content = getContestRow(ltime, full, partial) + content
		content = getContestRow(cookoff, full, partial) + content
		content = getContestRow(longContest, full, partial) + content
		LTIME = LTIME + 1
		COOK = COOK + 1
		month = month + 1
		if(month == 12):
			month=0
			year = year + 1
	content = "<table>" + content + "</table>"
	return HttpResponse(content)

def getUserProgress(userID):
	resp = requests.get(url="https://www.codechef.com/users/" + userID)
	resp = resp.text.split('\n')
	fully, partially = [], []
	for i in range(0,len(resp)):
		if "Fully Solved" in resp[i] or "Partially Solved" in resp[i]:
			if "Fully" in resp[i]:
				fully = getCodes(resp[i + 1], userID)
			if "Partially" in resp[i]:
				partially = getCodes(resp[i + 1], userID)
	return fully, partially

def getCodes(codeString, user):
	start = 0
	ret = []
	while True:
		ind = codeString.find(user, start)
		if ind == -1:
			break
		endInd = codeString.find("<", ind + 1)
		code = codeString[ind + len(user) + 2: endInd]
		ret.append(code)
		start = ind + 1
	return ret

def getContestRow(contestID, full, partial):
	try:
		ret=""
		if contestID in jsonData:
			ret += "<tr><td style=\"border:2px solid black\">" + contestID + "</td>"
			for problem in jsonData[contestID]:
				if problem in full:
					ret += "<td style=\"border:1px solid black; background: green;\">" + problem + "</td>"
				elif problem in partial:
					ret += "<td style=\"border:1px solid black; background: yellow;\">"
					ret += "<a href=\"https://www.codechef.com/problems/"+ problem + "\">" + problem + "</a></td>"
				else:
					ret += "<td style=\"border:1px solid black\">"
					ret += "<a href=\"https://www.codechef.com/problems/"+ problem + "\">" + problem + "</a></td>"
			ret += "</tr>"
		return ret
	except Exception:
		return ""
