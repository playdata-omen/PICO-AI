from flask import Flask, request
from flask_cors import CORS
from util import getServer
from service import Service



def create_app():
	app = Flask(__name__)
	CORS(app, resources={r'*': {'origins': getServer()}}) # 하위 경로 모두 허용
	

	@app.route('/labeling', methods = ['GET'])
	def labeling():
		if Service().labeling():
			result = '라벨링 성공'
		else:
			result = '라벨링 실패'

		return result


	@app.route('/search_image', methods = ['POST'])
	def search_image():
		# data = request.get_jason()
		# data = request.form["userfile"]

		# default_value = '0'
		# result_string = request.form.get('userfile', default_value)
		# if result_string == '0':
		#     result_file = request.files["userfile"]
				
		# result_string = request.form.get("userfile")
		import base64
		with open("./test_data/event.jpg", 'rb') as f:
			base64string = base64.b64encode(f.read())
		result = Service().search(base64string)

		return {"search_result":result}

	return app

if __name__ == "__main__":
	create_app().run()


