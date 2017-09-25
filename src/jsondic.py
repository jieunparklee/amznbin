import json
from pathlib import Path

FILE_NUM = 535235
TV_INIT = 0

#for file name
def ntostr(n):
	if(n<10):
		 return "0000" + str(n)
	elif(n < 100):
		 return "000" + str(n)
	elif(n < 1000):
		 return "00" + str(n)
	elif(n < 10000):
		 return "0" + str(n)
	else:
		 return "" + str(n)

pct = 10
asin_index_dic = {}
asin_index_dic_r = {}
asin_name_dic = {}

#make dic and save to json
def make_dic():
	cnt = 0
	for i in range(1,FILE_NUM):
		jsdata = open("./metadata/"+ntostr(i)+".json").read()
		data = json.loads(jsdata)	
		#if(i*100/FILENUM > pct):
		#	print(str(pct)+"%")
		#	pct += 10
	
		for asin in data['BIN_FCSKU_DATA'].keys():
			if(asin not in asin_index_dic.keys()):
				asin_index_dic[asin] = cnt
				asin_name_dic[asin] = data['BIN_FCSKU_DATA'][asin]['normalizedName']
				asin_index_dic_r[str(cnt)] = asin
				cnt += 1

	aidfw = open("./jsondic/asin_index_dic.json", 'w')
	aidrfw = open("./jsondic/asin_index_dic_r.json", 'w')
	andfw = open("./jsondic/asin_name_dic.json", 'w')

	js_asin_index_dic = json.dumps(asin_index_dic, sort_keys=True, indent=4, separators=(',', ':'))
	js_asin_index_dic_r = json.dumps(asin_index_dic_r, sort_keys=True, indent=4, separators=(',', ':'))
	js_asin_name_dic = json.dumps(asin_name_dic, sort_keys=True, indent=4, separators=(',', ':'))

	aidfw.write(js_asin_index_dic)
	aidrfw.write(js_asin_index_dic_r)
	andfw.write(js_asin_name_dic)

	aidfw.close()
	aidrfw.close()
	andfw.close()

def json2tv(n):
	jsdata = open("./metadata/"+ntostr(n)+".json").read()
	data = json.loads(jsdata)

	tvlen = len(asin_index_dic.keys())
	tv = []
	for _ in range(0, tvlen):
		tv += [TV_INIT]

	for asin in data['BIN_FCSKU_DATA'].keys():
		tv[asin_index_dic[asin]] = data['BIN_FCSKU_DATA'][asin]['quantity']

	return tv

def tv2res(tv):
	res = {}
	l = len(tv)
	
	for i in range(0, l):
		if(tv[i] != TV_INIT):
			asin = asin_index_dic_r[str(i)]
			res[asin] = {}	
			res[asin]['name'] = asin_name_dic[asin]
			res[asin]['quantity'] = tv[i]
	return res


if __name__ == '__main__':
	make_dic()
else:
	jsonfile = Path("./jsondic/asin_index_dic.json")
	
	#already exist
	if jsonfile.is_file():
		jsdata = open("./jsondic/asin_index_dic.json").read()
		asin_index_dic = json.loads(jsdata)		

		jsdata = open("./jsondic/asin_index_dic_r.json").read()
		asin_index_dic_r = json.loads(jsdata)

		jsdata = open("./jsondic/asin_name_dic.json").read()
		asin_name_dic = json.loads(jsdata)
	else:
		make_dic()
