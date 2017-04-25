import requests 
import json

order = {
	'basket':{
		32768: 2,
		32885: 5
	},
	'name': "Dariya", #Елдан будет получать имя пользователя
	'address': "Толе би 59", #Елдан спросить адрес 
	'phone' : '+77757515542', #Елдан спросить адрес 
	'email' : '116dariya@gmail.com'

}
def make_order(order):

	session = requests.Session()
	r = session.get('http://manga-sushi.kz/menu')
	csrf = r.cookies['YII_CSRF_TOKEN']
	for item_id in order['basket']:
			amount = order['basket'][item_id]
			url = "http://manga-sushi.kz/basket/add/%d/%d" % (item_id, amount)
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' ,
				'X-Requested-With': 'XMLHttpRequest'
			}
			form_data = {
				'use_ajax':'true',
				'client_system': 'true',
				'YII_CSRF_TOKEN': csrf
			}
			r = session.post(url, data = form_data, headers = headers)
			response = r.json()
	form_data = {
		'use_ajax':'true',
		'client_system': 'true',
		'YII_CSRF_TOKEN': csrf,
		'OrderForm[delivery_type]': 'Курьер',
		'OrderForm[restraunt]': 167,
		'OrderForm[city]': 30,
		'OrderForm[name]': order['name'],
		'OrderForm[address]': order['address'],
		'OrderForm[phone]': order['phone'],
		'OrderForm[email]': order['email'],
		'OrderForm[prefered_time]':'',
		'OrderForm[sum]': '',
		'OrderForm[comments]': 'Это тестовый заказ не обращайте внимания',
		'OrderForm[save_data]': 0

	}
	headers = {
		'X-Requested-With':'XMLHttpRequest'
	}
	url = "http://manga-sushi.kz/basket/order"
	r = session.post(url, data = form_data, headers = headers)
	data = r.json()
	total_amount = None
	order_id = None
	result_order = None
	if "__commands" in data and "message" in data['__commands']:
		message_str = data['__commands']['message'][0]
		message = json.loads(message_str)
		total_amount = message["total"]
		order_id = message["order_id"]
		result_order = message["gtm_push"]
	return order_id, total_amount, result_order

#result = make_order(order)
#print(result)