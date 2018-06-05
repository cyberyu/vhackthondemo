from __future__ import print_function

__author__ = 'shiyu'

import math
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from pathlib import Path
from operator import itemgetter
from collections import OrderedDict
from pgmpy.inference import VariableElimination
from pomegranate import *
import pickle
import copy
import simplejson as json
import ast
from demjson import decode


app = Flask(__name__)
api = Api(app)

evidence={}

class GoodStudent(Resource):
    def get(self):
        return {'hello': 'world'}

def parseJSON(obj):
    print ("DEBUG 4")
    if isinstance(obj, dict):
        newobj = {}
        for key, value in obj.iteritems():
            key = str(key)
            newobj[key] = self._parseJSON(value)
    elif isinstance(obj, list):
        newobj = []
        for value in obj:
            newobj.append(self._parseJSON(value))
    elif isinstance(obj, unicode):
        newobj = str(obj)
    else:
        newobj = obj
    return newobj

def inital_model(self):

    # initialize the Bayesnet

    schooltype = DiscreteDistribution({'A': 0.3, 'B': 0.3, 'C': 0.2, 'D': 0.15, 'E': 0.05})
    Age = DiscreteDistribution({'A': 0.5, 'B': 0.4, 'C': 0.1})

    ACTtest = ConditionalProbabilityTable(
        [['A', 'A', 0.6],
         ['A', 'B', 0.2],
         ['A', 'C', 0.2],
         ['B', 'A', 0.6],
         ['B', 'B', 0.2],
         ['B', 'C', 0.2],
         ['C', 'A', 0.6],
         ['C', 'B', 0.2],
         ['C', 'C', 0.2],
         ['D', 'A', 0.6],
         ['D', 'B', 0.2],
         ['D', 'C', 0.2],
         ['E', 'A', 0.2],
         ['E', 'B', 0.6],
         ['E', 'C', 0.2]], [schooltype])

    GPA = ConditionalProbabilityTable(
        [['A', 'A', 0.6],
         ['A', 'B', 0.2],
         ['A', 'C', 0.2],
         ['B', 'A', 0.6],
         ['B', 'B', 0.2],
         ['B', 'C', 0.2],
         ['C', 'A', 0.6],
         ['C', 'B', 0.2],
         ['C', 'C', 0.2],
         ['D', 'A', 0.6],
         ['D', 'B', 0.2],
         ['D', 'C', 0.2],
         ['E', 'A', 0.2],
         ['E', 'B', 0.6],
         ['E', 'C', 0.2]], [schooltype])

    top20 = ConditionalProbabilityTable(
        [['A', 'A', 0.6],
         ['A', 'B', 0.2],
         ['A', 'C', 0.2],
         ['B', 'A', 0.6],
         ['B', 'B', 0.2],
         ['B', 'C', 0.2],
         ['C', 'A', 0.6],
         ['C', 'B', 0.2],
         ['C', 'C', 0.2],
         ['D', 'A', 0.6],
         ['D', 'B', 0.2],
         ['D', 'C', 0.2],
         ['E', 'A', 0.2],
         ['E', 'B', 0.6],
         ['E', 'C', 0.2]], [schooltype])

    deanlist = ConditionalProbabilityTable(
        [['A', 'A', 0.6],
         ['A', 'B', 0.2],
         ['A', 'C', 0.2],
         ['B', 'A', 0.6],
         ['B', 'B', 0.2],
         ['B', 'C', 0.2],
         ['C', 'A', 0.6],
         ['C', 'B', 0.2],
         ['C', 'C', 0.2],
         ['D', 'A', 0.6],
         ['D', 'B', 0.2],
         ['D', 'C', 0.2],
         ['E', 'A', 0.2],
         ['E', 'B', 0.6],
         ['E', 'C', 0.2]], [schooltype])

    all_vec = []

    for dl in ['A', 'B', 'C']:  # 0 - Yes, on deanlist   1 - not on deanlist
        for t20 in ['A', 'B', 'C']:  # 0 - Yes, is top 20%,  1 - not in top 20%
            for gpa3 in ['A', 'B', 'C']:  # 0 - yes,  1 . -no
                for acttest in ['A', 'B', 'C']:  # 0 - yes,  1 - no
                    for age in ['A', 'B', 'C']:  # 0 below 25,  1 - above 25, 2- unknown
                        if rule_check_eligibility(rule_check_goodstudent(str(dl), str(t20), str(gpa3), str(acttest)),
                                                  str(age)) == 'yes':
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'yes', 1])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'no', 0.00])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'unknown', 0.00])
                        elif rule_check_eligibility(rule_check_goodstudent(str(dl), str(t20), str(gpa3), str(acttest)),
                                                    str(age)) == 'no':
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'yes', 0.00])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'no', 1])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'unknown', 0.00])
                        else:
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'yes', 0.00])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'no', 0.00])
                            all_vec.append([str(dl), str(t20), str(gpa3), str(acttest), str(age), 'unknown', 1])


    eligibility = ConditionalProbabilityTable(all_vec, [deanlist, top20, GPA, ACTtest, Age])

    s1 = Node(schooltype, name="schooltype")
    s2 = Node(deanlist, name="deanlist")
    s3 = Node(top20, name="top20")
    s4 = Node(GPA, name="GPA")
    s5 = Node(ACTtest, name="ACTtest")
    s6 = Node(Age, name="Age")
    s7 = Node(eligibility, name="eligibility")

    model = BayesianNetwork("Good Student Discount")
    model.add_states(s1, s2, s3, s4, s5, s6, s7)

    model.add_transition(s1, s2)
    model.add_transition(s1, s3)
    model.add_transition(s1, s4)
    model.add_transition(s1, s5)
    model.add_transition(s2, s7)
    model.add_transition(s3, s7)
    model.add_transition(s4, s7)
    model.add_transition(s5, s7)
    model.add_transition(s6, s7)
    model.bake()

    return save_model('good_student_prom.json', model)

def rule_check_goodstudent(dl, t20, gpa3, acttest):
    if ((dl == 'A') | (t20 == 'A') | (gpa3 == 'A') | (acttest == 'A')):
        return 'yes'
    elif ((dl == 'B') & (t20 == 'B') & (gpa3 == 'B') & (acttest == 'B')):  # all of them are no
        return 'no'
    else:
        return 'unknown'

def rule_check_eligibility(gs, age):
    if ((gs == 'yes') & (age == 'A')):
        return 'yes'
    elif (age == 'B'):
        return 'no'
    elif ((gs == 'unknown') | (age == 'C')):

        return 'unknown'
    else:
        return 'no'



def save_model(file_path, model):
    with open(file_path, 'w') as outfile:
        json.dump(model.to_json(), outfile)
    outfile.close()
    return 'Model saved'


def load_model(file_path):
    mm = BayesianNetwork("Good Student Discount")

    with open(file_path) as json_data:
        d = json.load(json_data)

    json_data.close()
    return mm.from_json(d)



def conditional_entropy(variable, variable_list, my_evidence, model):
    cond_entropy = 0
    ind = variable_list.index(variable)
    marginals = model.predict_proba({})
    dis_fact = marginals[ind].parameters[0]

    # print (dis_fact)
    card = len(dis_fact)
    # print (card)
    temp_ev = copy.deepcopy(my_evidence)

    # print "length is "+str(card)
    for k, v in dis_fact.items():
        # update the variable value to v
        temp_ev[variable] = str(k)
        # print (temp_ev)
        #  H(Z|x_j)*p(x_j)
        cond_entropy = cond_entropy + v * evidence_entropy(temp_ev, model)
    return cond_entropy


def evidence_entropy(my_evidence, model):
    marginals = model.predict_proba(my_evidence)
    dis_fact = marginals[6].parameters[0]
    # print(dis_fact)
    entropy = 0
    for k, v in dis_fact.items():
        entropy = entropy - float(v) * math.log(float(v) + 1E-10)
    return entropy


def calculate_gain(variable, variable_list, my_evidence, model):
    H_z = evidence_entropy(my_evidence, model)
    H_z_x = conditional_entropy(variable, variable_list, my_evidence, model)
    #     print('old entropy' + str(H_z))
    #     print('new entropy' + str(H_z_x))
    gain = H_z - H_z_x
    return gain


def rank_variable(my_evidence, variable_list, model):
    ranked_q = {}
    for var in variable_list:
        if var not in my_evidence:
            # print(var)
            # print(calculate_gain(var,my_evidence))
            ranked_q[var] = calculate_gain(var, variable_list, my_evidence, model)
    return OrderedDict(sorted(ranked_q.items(), key=itemgetter(1), reverse=True))


class build_model(Resource):
	# def post(self):
	# 	#model2 = inital_model()
	# 	return {'model':'built'}
	# 	#return jsonify(model2)

	def get(self):
		model = inital_model(self)
		#return {'model_get':'built'}
		return jsonify(str(model))

class reset_evidence(Resource):
	def get(self):
		global evidence
		evidence = {}
		return "evidence reset"

    
class get_eligibility(Resource):
    
    def get(self):
        global evidence

        var_list = ["schooltype", "deanlist", "top20", "GPA", "ACTtest", "Age"]
        mm = load_model("good_student_prom.json")
        print ("Global evidence is "+ json.dumps(evidence))
        
        ep = mm.predict_proba(evidence)[6].parameters[0]['yes']
        
        print ('EP is ' + str(ep))
        if float(ep)>0.99:
            return "true"
        elif float(ep)<0.02:
            return "false"
        else:
            return "unknown"
    
class next_question(Resource):

    def get(self):
        
        global evidence
        
        print ("Global evidence is "+ json.dumps(evidence))
        parser = reqparse.RequestParser()
        print ("DEBUG 1")
        parser.add_argument('evidence', location='json', required=True)
        print ("DEBUG 2")
        #parser.add_argument('evidence_name', type=str)
        #parser.add_argument('evidence_value', type=str)

        try:
            args = parser.parse_args()
            print ("DEBUG 3")
            #ev_name = args['evidence_name']
            # print (ev_name)
            # ev_value = args['evidence_value']
            # print (ev_value)
            # if (ev_name==None) | (ev_value==None):
            #    evidence = evidence
            # else:
            #    evidence[ev_name] = ev_value

            new_evidence=args['evidence']

            print('Evidence Update')
            
            #print('Evidence output ' + evidence + " and the type is " + str(type(evidence)))
            # manually create a new dictionary to resolve the unicode issue
            
            #ne = ast.literal_eval(evidence)
            new_evidence = decode(new_evidence)  
            # the json file is somehow damaged. At the request side it is double quoted, but flask restful API recieves it as a single quote one. So I use 
            # demjson package to decode it and fix the problem
            #print("final evidence is " + ne)
            
            #print('Evidence output ' + ne)
            #ne = parseJSON(evidence)
            
            #for k,v in ne.iteritems():
            #    print (k,v)

        except TypeError as e:
            print (e)
            new_evidence = {}

        evidence = dict(evidence.items() + new_evidence.items())
        var_list = ["schooltype", "deanlist", "top20", "GPA", "ACTtest", "Age"]
        mm = load_model("good_student_prom.json")
        question_order = rank_variable(evidence, var_list, mm)
        first_item = list(question_order)[0]
        print (first_item)
        return first_item


api.add_resource(build_model, '/build_model')
api.add_resource(next_question, '/next_question')
api.add_resource(GoodStudent, '/testing')
api.add_resource(reset_evidence, '/reset_evidence')
api.add_resource(get_eligibility, '/get_eligibility')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)