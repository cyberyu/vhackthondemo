__author__ = 'shiyu'

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps, loads
import json
import calendar
import time

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

# e = create_engine('sqlite:///salaries.db')

app = Flask(__name__)
api = Api(app)

# def get_info_from_image(path):
#
#     import numpy as np
#
#     import pickle
#     from skimage import io
#
#     from skimage.color import rgb2gray
#     from skimage.transform import downscale_local_mean, resize
#     from sklearn.decomposition import PCA
#     from sklearn.svm import LinearSVC
#
#     objpath = "/home/ubuntu/rest/models_hack.obj"
#
#     loadfile = open(objpath,'r')
#     pca,classif=pickle.load(loadfile)
#     loadfile.close()
#     image = io.imread(path)
#     image = resize(image, (3024, 4032))
#     img_gray = rgb2gray(image)
#     red_img_gray=downscale_local_mean(img_gray, (20, 20))
#     vtemp=red_img_gray.flatten()
#     print("vtemp shape:{}".format(vtemp.shape))
#
#     x=pca.transform(vtemp);
#     pred=classif.predict(x);
#
#     return pred[0]
#
# class ClfImgTest(Resource):
#     def get(self):
# 	imgs = ["IMG_8739_0.JPG", "IMG_8768_1.JPG", "IMG_1191_2.JPG"]
# 	_id = int(request.args["id"])
# 	print(request.args)
# 	path = "/home/ubuntu/rest/images/{}".format(imgs[_id])
# 	print("path:{}".format(path));
# 	info = get_info_from_image(path)
#         print("info:{}".format(info))
#
# 	result = '{"y" : ' + str(info) + '}'
# 	print(result)
# 	print("JSON::: {}".format(json.loads(result)))
# 	return result
#
#
# class ClfImg(Resource):
#     def get(self):
# 	print("Get!");
#         return {'hey!': ['a', 'b']}
#
#     def post(self):
# 	print("POST");
# 	print("request.form: {}".format(request.form))
# 	print("request.files.keys: {}".format(request.files.keys()))
# 	print("request.files['image'] : {}".format(type(request.files['image'])))
# 	#print("request.data: {}".format(request.data))
# 	#print("request.get_json(): {}".format(request.get_json()))
#
#         sec = str(int(calendar.timegm(time.gmtime())))
# 	imgpath = "/home/ubuntu/rest/images/img_{}.jpg".format(sec)
# 	request.files['image'].save(imgpath)
#
# 	# j = request.get_json()
#
# 	print("Save IMG data to file")
#
# 	print("Classify file")
# 	info = get_info_from_image(imgpath)
#
# 	print("return val is {}".format(info))
#
# 	result = '{"y" : ' + str(info) + '}'
# 	return result
#
# api.add_resource(ClfImg, '/clf_img')
# api.add_resource(ClfImgTest, '/clf_img_test')


@app.route('/predict', methods=['POST'])
def predict():
     json_ = request.json
     query_df = pd.DataFrame(json_)
     query = pd.get_dummies(query_df)
     for col in model_columns:
          if col not in query.columns:
               query[col] = 0
     prediction = clf.predict(query)
     return jsonify({'prediction': list(prediction)})


if __name__ == '__main__':
     clf = joblib.load('model.pkl')
     model_columns = joblib.load('model_columns.pkl')
     app.run(port=8080)


# if __name__ == '__main__':
#      app.run(host="0.0.0.0")