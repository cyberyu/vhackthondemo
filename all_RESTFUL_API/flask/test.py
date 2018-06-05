__author__ = 'shiyu'

import requests


r = requests.post('http://127.0.0.1:5000/clsfy', data = {'textinput':'I like to take risk.'})
print type(r)
print r.json()['y']