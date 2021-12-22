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


	@app.route('/searchImage', methods = ['POST'])
	def search_image():
		data = request.form.get("userFile")
		result = Service().search(data)

		return {"search_result":result}

	return app
	
if __name__ == "__main__":
	create_app().run(debug=True, host="0.0.0.0", port="5000")