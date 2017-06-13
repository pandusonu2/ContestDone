import json,requests

def getProblems(contestID):
	retJSON = "\"" + contestID + "\":["
	try:
		req = requests.get(url="https://www.codechef.com/api/contests/" + contestID)
		data = json.loads(req.text)
		for problem in data["problems"]:
			retJSON += "\"" + str(problem) + "\","
	except Exception:
		print("Failure for contest: " + contestID)
	if retJSON.find("[") != len(retJSON) - 1:
		retJSON = retJSON[:-1]
	retJSON += "],\n"
	return retJSON

problemData = "{\n"
months = ['JAN', 'FEB', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
LTIME, COOK, month, year = 20,54,0,15
while year*12+month < 17*12+5:
	longContest = months[month] + str(year)
	cookoff = "COOK" + str(COOK)
	ltimeContest = "LTIME" + str(LTIME)
	problemData += getProblems(longContest) + getProblems(cookoff) + getProblems(ltimeContest)
	print(months[month] + str(year))
	LTIME += 1
	COOK += 1
	month += 1
	if (month == 12):
		month = 0
		year += 1
problemData = problemData[:-2] + "}"
file = open('probelms.txt','w')
file.write(problemData)
file.close()
