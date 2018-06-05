from __future__ import print_function

__author__ = 'shiyu'

import math
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from operator import itemgetter
from collections import OrderedDict
from pomegranate import *
import copy
import simplejson as json
from demjson import decode

app = Flask(__name__)
api = Api(app)

evidence = {}


class GoodStudent(Resource):
    def get(self):
        return {'hello': 'world'}


def inital_model(self):
    # initialize the Bayesnet

    highschool = DiscreteDistribution({'A': 0.2, 'B': 0.7, 'C': 0.1})
    college = DiscreteDistribution({'A': 0.2, 'B': 0.7, 'C': 0.1})
    onlinetrading = DiscreteDistribution({'A': 0.2, 'B': 0.7, 'C': 0.1})
    homeschool = DiscreteDistribution({'A': 0.05, 'B': 0.9, 'C': 0.05})
    deanlist = DiscreteDistribution({'A': 0.3, 'B': 0.6, 'C': 0.1})
    top20 = DiscreteDistribution({'A': 0.2, 'B': 0.7, 'C': 0.1})
    gpa3 = DiscreteDistribution({'A': 0.25, 'B': 0.65, 'C': 0.1})
    acttest = DiscreteDistribution({'A': 0.05, 'B': 0.65, 'C': 0.3})
    Age = DiscreteDistribution({'A': 0.2, 'B': 0.7, 'C': 0.1})

    traditionalfulltime = ConditionalProbabilityTable(gen_cpd_traditionalfulltime(),
                                                      [highschool, college, onlinetrading, homeschool])
    achievinghomeschool = ConditionalProbabilityTable(gen_cpd_achievinghomeschool(), [homeschool, acttest])
    achievingtraditionalschool = ConditionalProbabilityTable(gen_cpd_achievingtraditionalschool(),
                                                             [traditionalfulltime, deanlist, top20, gpa3])
    eligibility = ConditionalProbabilityTable(gen_eligibility(), [achievingtraditionalschool, achievinghomeschool, Age])

    s1 = Node(highschool, name="highschool")
    s2 = Node(college, name="college")
    s3 = Node(onlinetrading, name="onlinetrading")
    s4 = Node(homeschool, name="homeschool")
    s5 = Node(deanlist, name="deanlist")
    s6 = Node(top20, name="top20")
    s7 = Node(gpa3, name="gpa3")
    s8 = Node(acttest, name="acttest")
    s9 = Node(Age, name="Age")
    s10 = Node(traditionalfulltime, name="traditionalfulltime")
    s11 = Node(achievinghomeschool, name="achievinghomeschool")
    s12 = Node(achievingtraditionalschool, name="achievingtraditionalschool")
    s13 = Node(eligibility, name="eligibility")

    model = BayesianNetwork("Good Student Discount")
    model.add_states(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13)

    model.add_transition(s1, s10)
    model.add_transition(s2, s10)
    model.add_transition(s3, s10)
    model.add_transition(s4, s10)
    model.add_transition(s4, s11)
    model.add_transition(s8, s11)
    model.add_transition(s10, s12)
    model.add_transition(s5, s12)
    model.add_transition(s6, s12)
    model.add_transition(s7, s12)
    model.add_transition(s9, s13)
    model.add_transition(s11, s13)
    model.add_transition(s12, s13)
    model.bake()

    return save_model('good_student_prom.json', model)


def rule_traditionalfulltime(high, college, online, home):
    if ((high == 'A') | (college == 'A') | (online == 'A')):
        return 'A'
    elif (home == 'A'):  # all of them are no
        return 'B'
    else:
        return 'C'


def rule_achievinghomeschool(home, acttest):
    if ((home == 'A') & (acttest == 'A')):
        return 'A'
    elif ((home == 'B') | (acttest == 'B')):  # any of them are no
        return 'B'
    else:
        return 'C'


def rule_achievingtraditionalschool(tradfulltime, deanlist, top20, gpa3):
    if ((tradfulltime == 'A') & ((deanlist == 'A') | (top20 == 'A') | (gpa3 == 'A'))):
        return 'A'
    elif ((tradfulltime == 'B') | ((deanlist == 'B') & (top20 == 'B') & (gpa3 == 'B'))):
        return 'B'
    else:
        return 'C'


def rule_eligibility(achievingtraditionalschool, achievinghomeschool, age):
    if (((achievingtraditionalschool == 'A') | (achievinghomeschool == 'A')) & (age == 'A')):
        return 'A'
    elif (((achievingtraditionalschool == 'B') & (achievinghomeschool == 'B')) | (age == 'B')):
        return 'B'
    else:
        return 'C'


def gen_cpd_traditionalfulltime():
    all_vec = []
    for high in ['A', 'B', 'C']:
        for college in ['A', 'B', 'C']:
            for online in ['A', 'B', 'C']:
                for home in ['A', 'B', 'C']:
                    p = rule_traditionalfulltime(str(high), str(college), str(online), str(home))
                    if p == 'A':
                        all_vec.append([str(high), str(college), str(online), str(home), 'A', 1])
                        all_vec.append([str(high), str(college), str(online), str(home), 'B', 0])
                        all_vec.append([str(high), str(college), str(online), str(home), 'C', 0])
                    elif p == 'B':
                        all_vec.append([str(high), str(college), str(online), str(home), 'A', 0])
                        all_vec.append([str(high), str(college), str(online), str(home), 'B', 1])
                        all_vec.append([str(high), str(college), str(online), str(home), 'C', 0])
                    else:
                        all_vec.append([str(high), str(college), str(online), str(home), 'A', 0])
                        all_vec.append([str(high), str(college), str(online), str(home), 'B', 0])
                        all_vec.append([str(high), str(college), str(online), str(home), 'C', 1])

    return all_vec


def gen_cpd_achievinghomeschool():
    all_vec = []
    for home in ['A', 'B', "C"]:
        for acttest in ['A', 'B', 'C']:
            p = rule_achievinghomeschool(home, acttest)
            if p == 'A':
                all_vec.append([str(home), str(acttest), 'A', 1])
                all_vec.append([str(home), str(acttest), 'B', 0])
                all_vec.append([str(home), str(acttest), 'C', 0])
            elif p == 'B':
                all_vec.append([str(home), str(acttest), 'A', 0])
                all_vec.append([str(home), str(acttest), 'B', 1])
                all_vec.append([str(home), str(acttest), 'C', 0])
            else:
                all_vec.append([str(home), str(acttest), 'A', 0])
                all_vec.append([str(home), str(acttest), 'B', 0])
                all_vec.append([str(home), str(acttest), 'C', 1])

    return all_vec


def gen_cpd_achievingtraditionalschool():
    all_vec = []
    for tradfulltime in ['A', 'B', 'C']:
        for deanlist in ['A', 'B', 'C']:
            for top20 in ['A', 'B', 'C']:
                for gpa3 in ['A', 'B', 'C']:
                    p = rule_achievingtraditionalschool(tradfulltime, deanlist, top20, gpa3)

                    if p == 'A':
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'A', 1])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'B', 0])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'C', 0])
                    elif p == 'B':
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'A', 0])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'B', 1])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'C', 0])
                    else:
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'A', 0])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'B', 0])
                        all_vec.append([str(tradfulltime), str(deanlist), str(top20), str(gpa3), 'C', 1])
    return all_vec


def gen_eligibility():
    all_vec = []
    for achievingtradition in ['A', 'B', 'C']:
        for achievinghome in ['A', 'B', 'C']:
            for age in ['A', 'B', 'C']:
                p = rule_eligibility(achievingtradition, achievinghome, age)

                if p == 'A':
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'A', 1])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'B', 0])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'C', 0])
                elif p == 'B':
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'A', 0])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'B', 1])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'C', 0])
                else:
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'A', 0])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'B', 0])
                    all_vec.append([str(achievingtradition), str(achievinghome), str(age), 'C', 1])
    return all_vec


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
    dis_fact = marginals[12].parameters[0]
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
        # return {'model_get':'built'}
        return jsonify(str(model))


class reset_evidence(Resource):
    def get(self):
        global evidence
        evidence = {}
        return "evidence reset"


class show_math(Resource):
    def get(self):
        global evidence
        
        var_list = ["highschool", "college", "onlinetrading", "homeschool", "deanlist", "Age", "top20", "gpa3",
                    "acttest", "Age"]

        mm = load_model("good_student_prom.json")
        
        ep = mm.predict_proba(evidence)[12].parameters[0]['A']
        
        question_order = rank_variable(evidence, var_list, mm)
        
        msg = "What we know about you: " + json.dumps(evidence)  +  "  Your current marginal probability being eligible for discount is " + str(ep) + "  And we are interested to ask you the following questions by order " + str(question_order)
        return msg
    
    
    

class get_eligibility(Resource):

    def get(self):
        global evidence

        var_list = ["highschool", "college", "onlinetrading", "homeschool", "deanlist", "Age", "top20", "gpa3",
                    "acttest", "Age"]

        mm = load_model("good_student_prom.json")
        print("Global evidence is " + json.dumps(evidence))

        ep = mm.predict_proba(evidence)[12].parameters[0]['A']

        print('EP is ' + str(ep))
        if float(ep) > 0.99:
            return "true"
        elif float(ep) < 0.01:
            return "false"
        else:
            return "unknown"


class next_question(Resource):

    def get(self):

        global evidence


        parser = reqparse.RequestParser()
        print("DEBUG 1")
        parser.add_argument('evidence', location='json', required=True)
        print("DEBUG 2")
        # parser.add_argument('evidence_name', type=str)
        # parser.add_argument('evidence_value', type=str)

        try:
            args = parser.parse_args()
            print("DEBUG 3")
            # ev_name = args['evidence_name']
            # print (ev_name)
            # ev_value = args['evidence_value']
            # print (ev_value)
            # if (ev_name==None) | (ev_value==None):
            #    evidence = evidence
            # else:
            #    evidence[ev_name] = ev_value

            new_evidence = args['evidence']

            print('Evidence Update')

            # print('Evidence output ' + evidence + " and the type is " + str(type(evidence)))
            # manually create a new dictionary to resolve the unicode issue

            # ne = ast.literal_eval(evidence)
            new_evidence = decode(new_evidence)
            # the json file is somehow damaged. At the request side it is double quoted, but flask restful API recieves it as a single quote one. So I use
            # demjson package to decode it and fix the problem
            # print("final evidence is " + ne)

            # print('Evidence output ' + ne)
            # ne = parseJSON(evidence)

            # for k,v in ne.iteritems():
            #    print (k,v)

        except TypeError as e:
            print(e)
            new_evidence = {}

        evidence = dict(evidence.items() + new_evidence.items())
        var_list = ["highschool", "college", "onlinetrading", "homeschool", "deanlist", "Age", "top20", "gpa3",
                    "acttest", "Age"]
        print("Global evidence is " + json.dumps(evidence))        
        mm = load_model("good_student_prom.json")

        # check the eligibility first

        ep = mm.predict_proba(evidence)[12].parameters[0]['A']
        
        print('EP is ' + str(ep))

        if float(ep) > 0.999:
            return "terminate_true"
        elif float(ep) < 0.001:
            return "terminate_false"
        else:
            question_order = rank_variable(evidence, var_list, mm)
            first_item = list(question_order)[0]
            print(first_item)
            return first_item


api.add_resource(build_model, '/build_model')
api.add_resource(next_question, '/next_question')
api.add_resource(GoodStudent, '/testing')
api.add_resource(reset_evidence, '/reset_evidence')
api.add_resource(get_eligibility, '/get_eligibility')
api.add_resource(show_math, '/show_math')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)