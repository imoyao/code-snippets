#coding=utf-8
import json

def city_info():
	with open('./cityinfo.json','r') as f:
		code_str = json.load(f)
	proviences = code_str['CityCode']
	county_dict = {}
	county_list = []
	for pro in proviences:
		cityList = pro['cityList']
		for city in cityList:
			countyList = city['countyList']
			for county in countyList:
				name = county['name']
				code = county['code']
				county_dict[name] = code
	return county_dict


def get_code(cityname):
	result = {}

	city = cityname.decode('utf-8')
	county_dict = city_info()
	if city in county_dict:
		code = county_dict[city]
		result['retcode'] = 1
		result['data'] = code
		result['msg'] = ''
	else:
		result['retcode'] = 0
		result['data'] = None
		result['msg'] = 'please check your enter.'
	return result

def main():
	data = get_code()
	code = data['retcode']
	citykey = data['data']
	print (code)
	if code and citykey:
		print (citykey)
	else:
		msg = data['msg']
		print (msg)

if __name__ == '__main__':
	main()