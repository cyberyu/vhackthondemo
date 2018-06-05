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
import math
from operator import itemgetter
from collections import OrderedDict
import copy
import multiprocessing
from multiprocessing import Pool
from contextlib import closing


app = Flask(__name__)
api = Api(app)

evidence={}

class RiskTolerance(Resource):
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

def get_score_q1(ans):
    if ans=='A':
        return 4
    elif ans=='B':
        return 3
    elif ans=='C':
        return 2
    else:
        return 1
    
def get_score_q2(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4
    
def get_score_q3(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4

    
def get_score_q4(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3

def get_score_q5(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3

def get_score_q6(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3


def get_score_q7(ans):
    if ans=='A':
        return 2
    elif ans=='B':
        return 1
    elif ans=='C':
        return 3
    else:
        return 1

    
def get_score_q8(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4

def get_score_q9(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3

def get_score_q10(ans):
    if ans=='A':
        return 1
    else:
        return 3


def get_score_q11(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3

    
def get_score_q12(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4

def get_score_q13(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4
    
def get_score_q14(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4


def get_score_q15(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 2
    else:
        return 3

def get_score_q16(ans):
    if ans=='A':
        return 1
    else:
        return 3


def get_score_q17(ans):
    if ans=='A':
        return 1
    else:
        return 3


def get_score_q18(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4

def get_score_q19(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    else:
        return 3

def get_score_q20(ans):
    if ans=='A':
        return 1
    elif ans=='B':
        return 2
    elif ans=='C':
        return 3
    else:
        return 4


def rule_guaranteed_vs_probable(q1, q2, q11):
    # q1: 4, q2: 4, q11: 3
    # sum: 11
    # if the sum is larger or equal than 15, aggressive
    # if the sum is smaller than 10, conservative
    # other case moderate
    
    fs = get_score_q1(q1)+get_score_q2(q2)+get_score_q11(q11)
    
    if fs>=8:
        return 'A'
    elif fs<=5:
        return 'C'
    else:
        return 'B'
    
def gen_cpd_guaranteed_vs_probable():
    all_vec = []
    for q1 in ['A', 'B', 'C', 'D']:
        for q2 in ['A','B','C','D']:
            for q11 in ['A','B','C']:
                re = rule_guaranteed_vs_probable(q1, q2, q11)
                if re=='A':
                    all_vec.append([str(q1),str(q2),str(q11),'A',1])
                    all_vec.append([str(q1),str(q2),str(q11),'B',0])
                    all_vec.append([str(q1),str(q2),str(q11),'C',0])
                elif re=='B':
                    all_vec.append([str(q1),str(q2),str(q11),'A',0])
                    all_vec.append([str(q1),str(q2),str(q11),'B',1])
                    all_vec.append([str(q1),str(q2),str(q11),'C',0])                                    
                else:
                    all_vec.append([str(q1),str(q2),str(q11),'A',0])
                    all_vec.append([str(q1),str(q2),str(q11),'B',0])
                    all_vec.append([str(q1),str(q2),str(q11),'C',1])                                    
    return all_vec

    
def rule_risk_choice(q7, q13, q14):
    # q7: 4, q13: 4, q14: 4
    # sum: 12
    # if the sum is larger or equal than 10, aggressive
    # if the sum is smaller than 5, conservative
    # other case moderate
    fs = get_score_q7(q7)+get_score_q13(q13)+get_score_q14(q14)
    if fs>=8:
        return 'A'
    elif fs<=4:
        return 'C'
    else:
        return 'B'
    
def gen_cpd_risk_choice():
    all_vec=[]
    for q7 in ['A','B','C','D']:
        for q13 in ['A','B','C','D']:
            for q14 in ['A','B','C','D']:
                re=rule_risk_choice(q7,q13,q14)
                if re=='A':
                    all_vec.append([str(q7),str(q13),str(q14),'A',1])
                    all_vec.append([str(q7),str(q13),str(q14),'B',0])
                    all_vec.append([str(q7),str(q13),str(q14),'C',0])
                elif re=='B':
                    all_vec.append([str(q7),str(q13),str(q14),'A',0])
                    all_vec.append([str(q7),str(q13),str(q14),'B',1])
                    all_vec.append([str(q7),str(q13),str(q14),'C',0])                        
                else:
                    all_vec.append([str(q7),str(q13),str(q14),'A',0])
                    all_vec.append([str(q7),str(q13),str(q14),'B',0])
                    all_vec.append([str(q7),str(q13),str(q14),'C',1])                        
    return all_vec


def rule_risk_knowledge(q12, q15, q18):
    #q12:4, q15:4, q18:4
    #sum: 12
    fs = get_score_q12(q12)+get_score_q15(q15)+get_score_q18(q18)

    if fs>=8:
        return 'A'
    elif fs<=4:
        return 'C'
    else:
        return 'B'

def gen_cpd_risk_knowledge():
    all_vec=[]
    for q12 in ['A','B','C','D']:
        for q15 in ['A','B','C','D']:
            for q18 in ['A','B','C','D']:
                re=rule_risk_knowledge(q12, q15, q18)
                if re=='A':
                    all_vec.append([str(q12),str(q15),str(q18), 'A',1])
                    all_vec.append([str(q12),str(q15),str(q18), 'B',0])
                    all_vec.append([str(q12),str(q15),str(q18), 'C',0])
                elif re=='B':
                    all_vec.append([str(q12),str(q15),str(q18), 'A',0])
                    all_vec.append([str(q12),str(q15),str(q18), 'B',1])
                    all_vec.append([str(q12),str(q15),str(q18), 'C',0])
                else:
                    all_vec.append([str(q12),str(q15),str(q18), 'A',0])
                    all_vec.append([str(q12),str(q15),str(q18), 'B',1])
                    all_vec.append([str(q12),str(q15),str(q18), 'C',0])
    return all_vec
    
def rule_risk_comfortness(q1, q3, q4):
    # q1:4, q3:4, q4:3
    # sum: 11
    fs = get_score_q1(q1)+get_score_q3(q3)+get_score_q4(q4)
    if fs>=7:
        return 'A'
    elif fs<4:
        return 'C'
    else:
        return 'B'
    
def gen_cpd_risk_comfortness():
    all_vec=[]
    for q1 in ['A','B','C','D']:
        for q3 in ['A','B','C','D']:
            for q4 in ['A','B','C']:
                re=rule_risk_comfortness(q1,q3,q4)
                if re=='A':
                    all_vec.append([str(q1),str(q3),str(q4),'A',1])
                    all_vec.append([str(q1),str(q3),str(q4),'B',0]) 
                    all_vec.append([str(q1),str(q3),str(q4),'C',0])                                                     
                elif re=='B':
                    all_vec.append([str(q1),str(q3),str(q4), 'A',0])
                    all_vec.append([str(q1),str(q3),str(q4), 'B',1]) 
                    all_vec.append([str(q1),str(q3),str(q4), 'C',0])                                                 
                else:
                    all_vec.append([str(q1),str(q3),str(q4), 'A',0])
                    all_vec.append([str(q1),str(q3),str(q4), 'B',0]) 
                    all_vec.append([str(q1),str(q3),str(q4), 'C',1])                                                     
    return all_vec

def rule_risk_speculative(q12, q14, q20):
    # q12:4, q14:4, q20:4
    # sum: 12
    fs = get_score_q12(q12)+get_score_q14(q14)+get_score_q20(q20)
    
    if fs>=8:
        return 'A'
    elif fs<=4:
        return 'C'
    else:
        return 'B'

def gen_cpd_risk_speculative():
    all_vec=[]
    for q12 in ['A','B','C','D']:
        for q14 in ['A','B','C','D']:
            for q20 in ['A','B','C','D']:
                re=rule_risk_speculative(q12,q14,q20)
                if re=='A':
                    all_vec.append([str(q12),str(q14),str(q20),'A',1])
                    all_vec.append([str(q12),str(q14),str(q20),'B',0])
                    all_vec.append([str(q12),str(q14),str(q20),'C',0])
                elif re=='B':
                    all_vec.append([str(q12),str(q14),str(q20),'A',0])
                    all_vec.append([str(q12),str(q14),str(q20),'B',1])
                    all_vec.append([str(q12),str(q14),str(q20),'C',0])
                else:
                    all_vec.append([str(q12),str(q14),str(q20),'A',0])
                    all_vec.append([str(q12),str(q14),str(q20),'B',0])
                    all_vec.append([str(q12),str(q14),str(q20),'C',1])
    return all_vec 

def rule_risk_prospective(q16, q17, q19):
    # q16:2, q17:2, q19:3
    # sum: 7
    fs = get_score_q16(q16)+get_score_q17(q17)+get_score_q19(q19)
    
    if fs>=5:
        return 'A'
    elif fs<=3:
        return 'C'
    else:
        return 'B'
    
def gen_cpd_risk_prospective():
    all_vec=[]
    for q16 in ['A','B']:
        for q17 in ['A','B']:
            for q19 in ['A','B','C']:
                re=rule_risk_prospective(q16,q17,q19)
                if re=='A':
                    all_vec.append([str(q16),str(q17),str(q19),'A',1])
                    all_vec.append([str(q16),str(q17),str(q19),'B',0])
                    all_vec.append([str(q16),str(q17),str(q19),'C',0])
                elif re=='B':
                    all_vec.append([str(q16),str(q17),str(q19),'A',0])
                    all_vec.append([str(q16),str(q17),str(q19),'B',1])
                    all_vec.append([str(q16),str(q17),str(q19),'C',0])
                else:
                    all_vec.append([str(q16),str(q17),str(q19),'A',0])
                    all_vec.append([str(q16),str(q17),str(q19),'B',0])
                    all_vec.append([str(q16),str(q17),str(q19),'C',1])
    return all_vec
                    
    
def rule_risk_investment(q5, q6, q9):
    # q5:4, q6:3, q9:3
    # sum: 10
    fs = get_score_q5(q5)+get_score_q6(q6)+get_score_q9(q9)
    if fs>=7:
        return 'A'
    elif fs<=3:
        return 'C'
    else:
        return 'B'

def gen_cpd_risk_investment():
    all_vec=[]
    for q5 in ['A','B','C','D']:
        for q6 in ['A','B','C']:
            for q9 in ['A','B','C']:
                re=rule_risk_investment(q5,q6,q9)
                if re=='A':
                    all_vec.append([str(q5),str(q6),str(q9),'A',1])
                    all_vec.append([str(q5),str(q6),str(q9),'B',0])
                    all_vec.append([str(q5),str(q6),str(q9),'C',0])
                elif re=='B':
                    all_vec.append([str(q5),str(q6),str(q9),'A',0])
                    all_vec.append([str(q5),str(q6),str(q9),'B',1])
                    all_vec.append([str(q5),str(q6),str(q9),'C',0])
                else:
                    all_vec.append([str(q5),str(q6),str(q9),'A',0])
                    all_vec.append([str(q5),str(q6),str(q9),'B',0])
                    all_vec.append([str(q5),str(q6),str(q9),'C',1])
    return all_vec

def rule_risk_tol(guaranteed_vs_probable, risk_choice, risk_knowledge, risk_comfortness, risk_speculative, risk_prospective, risk_investment):
    options = {'A': 3, 'B': 2, 'C': 1}
    re = options[guaranteed_vs_probable]+options[risk_choice]+options[risk_knowledge]+options[risk_comfortness] \
         + options[risk_speculative]+ options[risk_investment]
    
    #print ('output', guaranteed_vs_probable, risk_choice, risk_knowledge, risk_comfortness, risk_speculative, risk_prospective, risk_investment)
    #re = 0
    if re >= 15:
        return 'A'
    elif re<=9:
        return 'C'
    else:
        return 'B'
    
def gen_cpd_risk_tol():
    all_vec=[]
    for guaranteed_vs_probable in ['A', 'B', 'C']:
        for risk_choice in ['A','B','C']:
            for risk_knowledge in ['A','B','C']:
                for risk_comfortness in ['A','B','C']:
                    for risk_speculative in ['A','B','C']:
                        for risk_prospective in ['A','B','C']:
                            for risk_investment in ['A','B','C']:
                                re=rule_risk_tol(guaranteed_vs_probable, risk_choice, risk_knowledge, risk_comfortness,risk_speculative, risk_prospective, risk_investment)
                                
                                if re=='A':
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'A',1])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge),  
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'B',0])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'C',0])
                                elif re=='B':
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'A',0])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'B',1])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'C',0])
                                else:
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'A',0])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'B',0])
                                    all_vec.append([str(guaranteed_vs_probable),str(risk_choice),str(risk_knowledge), 
                                                    str(risk_comfortness),str(risk_speculative), str(risk_prospective),
                                                    str(risk_investment),'C',1])
    
    return all_vec       

def inital_model(self):

    # initialize the Bayesnet

    q1 = DiscreteDistribution({'A': 0.20, 'B': 0.40, 'C': 0.30, 'D':0.10})  
    q2 = DiscreteDistribution({'A': 0.20, 'B': 0.40, 'C': 0.30, 'D':0.10})
    q3 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})  
    q4 = DiscreteDistribution({'A': 0.30, 'B': 0.44, 'C': 0.26})
    q5 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})  
    q6 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.46})
    q7 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})
    q8 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})
    q9 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.46})
    q10 = DiscreteDistribution({'A': 0.6, 'B': 0.4})
    q11 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.46})
    q12 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})
    q13 = DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})
    q14 =  DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20})
    q15 =  DiscreteDistribution({'A': 0.30, 'B': 0.24, 'C': 0.26, 'D':0.20}) 
    q16 =  DiscreteDistribution({'A': 0.30, 'B': 0.70})
    q17 =  DiscreteDistribution({'A': 0.30, 'B': 0.70})
    q18 = DiscreteDistribution({'A': 0.20, 'B': 0.30, 'C': 0.26, 'D':0.24})
    q19 = DiscreteDistribution({'A': 0.20, 'B': 0.54, 'C': 0.26})
    q20 = DiscreteDistribution({'A': 0.20, 'B': 0.30, 'C': 0.26, 'D':0.24})
    
    guaranteed_vs_probable = ConditionalProbabilityTable(gen_cpd_guaranteed_vs_probable(), [q1, q2, q11])
    risk_choice = ConditionalProbabilityTable(gen_cpd_risk_choice(), [q7, q13, q14])
    risk_knowledge = ConditionalProbabilityTable(gen_cpd_risk_knowledge(), [q12, q15, q18])
    risk_comfortness = ConditionalProbabilityTable(gen_cpd_risk_comfortness(), [q1, q3, q4])
    risk_speculative = ConditionalProbabilityTable(gen_cpd_risk_speculative(), [q12, q14, q20])
    risk_prospective = ConditionalProbabilityTable(gen_cpd_risk_prospective(), [q16, q17, q19])
    risk_investment =  ConditionalProbabilityTable(gen_cpd_risk_investment(), [q5, q6, q9])
    risk_tol = ConditionalProbabilityTable(gen_cpd_risk_tol(), [guaranteed_vs_probable, risk_choice, risk_knowledge, risk_comfortness, risk_speculative, risk_prospective, risk_investment])   

    s1 = Node(q1, name="q1")
    s2 = Node(q2, name="q2")
    s3 = Node(q3, name="q3")
    s4 = Node(q4, name="q4")
    s5 = Node(q5, name="q5")
    s6 = Node(q6, name="q6")
    s7 = Node(q7, name="q7")
    s8 = Node(q8, name="q8")
    s9 = Node(q9, name="q9")
    s10 = Node(q10, name="q10")
    s11 = Node(q11, name="q11")
    s12 = Node(q12, name="q12")
    s13 = Node(q13, name="q13")
    s14 = Node(q14, name="q14")
    s15 = Node(q15, name="q15")
    s16 = Node(q16, name="q16")
    s17 = Node(q17, name="q17")
    s18 = Node(q18, name="q18")
    s19 = Node(q19, name="q19")
    s20 = Node(q20, name="q20")
    s21 = Node(guaranteed_vs_probable, name="guaranteed_vs_probable")
    s22 = Node(risk_choice, name="risk_choice")
    s23 = Node(risk_knowledge, name="risk_knowledge")
    s24 = Node(risk_comfortness, name="risk_comfortness")
    s25 = Node(risk_speculative, name="risk_speculative")
    s26 = Node(risk_prospective, name="risk_prospective")
    s27 = Node(risk_investment, name="risk_investment")
    s28 = Node(risk_tol, name="risk_tol")

    model = BayesianNetwork("Risk Tolerance")
    #model2.add_states(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27)

    model.add_states(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28)

    model.add_transition(s1, s21)
    model.add_transition(s2, s21)
    model.add_transition(s11, s21)

    model.add_transition(s7, s22)
    model.add_transition(s13, s22)
    model.add_transition(s14, s22)

    model.add_transition(s12, s23)
    model.add_transition(s15, s23)
    model.add_transition(s18, s23)


    model.add_transition(s1, s24)
    model.add_transition(s3, s24)
    model.add_transition(s4, s24)

    model.add_transition(s12, s25)
    model.add_transition(s14, s25)
    model.add_transition(s20, s25)


    model.add_transition(s16, s26)
    model.add_transition(s17, s26)
    model.add_transition(s19, s26)

    model.add_transition(s5, s27)
    model.add_transition(s6, s27)
    model.add_transition(s9, s27)

    model.add_transition(s21, s28)
    model.add_transition(s22, s28)
    model.add_transition(s23, s28)
    model.add_transition(s24, s28)
    model.add_transition(s25, s28)
    model.add_transition(s26, s28)
    model.add_transition(s27, s28)

    model.bake()
    return save_model('risk_tolerance.json', model)

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
    #print (ind)
    marginals = model.predict_proba({})
    dis_fact = marginals[ind].parameters[0]
    
    #print (dis_fact)
    card = len(dis_fact)
    #print (card)
    temp_ev = copy.deepcopy(my_evidence)
    
    #print "length is "+str(card)
    for k, v in dis_fact.items():
        # update the variable value to v
        temp_ev[variable] = str(k)
        #print (temp_ev)
        #  H(Z|x_j)*p(x_j)
        cond_entropy = cond_entropy + v*evidence_entropy(temp_ev, model)
    return cond_entropy

def evidence_entropy(my_evidence, model):
    marginals = model.predict_proba(my_evidence)
    dis_fact = marginals[27].parameters[0]
    #print(dis_fact)
    entropy = 0
    for k,v in dis_fact.items():
        #print (k,v)
        entropy =entropy - float(v)*math.log(float(v)+1E-10)
    return entropy

def calculate_gain(variable, variable_list, my_evidence, model):
    
    H_z= evidence_entropy(my_evidence, model)
    H_z_x = conditional_entropy(variable, variable_list, my_evidence, model)
#     print('old entropy' + str(H_z))
#     print('new entropy' + str(H_z_x))
    gain = H_z - H_z_x
    return gain

def calculate_gain_par(var):
    global model
    global evidence
    global variable_list
    H_z= evidence_entropy(evidence, model)
    H_z_x = conditional_entropy(var, variable_list, evidence, model)
    gain = H_z - H_z_x
    return var, gain
    
def parse_parallel_result(l):
    dd = {}
    for e in l:
        dd[e[0]]=e[1]
    return OrderedDict(sorted(dd.items(), key=itemgetter(1),reverse=True))
    
def rank_variable_par():
    global model, evidence, variable_list
    #print ('variable_list  is ' + str(variable_list))
    #print ('evidence  is ' + str(evidence.keys()))
    
    num_cores = multiprocessing.cpu_count()
    ranked_q = {}
    p = Pool(num_cores)

    cand_v =list(set(variable_list) - set(evidence.keys()))
    chunksize = 1
    
    with closing(Pool(processes=num_cores)) as pool:
        x = pool.map(calculate_gain_par, cand_v, chunksize)
        pool.terminate()
        
    #with Pool(processes=num_cores) as pool:
    #    x = pool.map(calculate_gain_par, cand_v, chunksize)

    return parse_parallel_result(x)

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
        global evidence, variable_list

        variable_list =["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8","q9", "q10", "q11", "q12", "q13", "q14", "q15","q16", "q17", "q18", "q19", "q20"]
        mm = load_model("risk_tolerance.json")
        print ("Global evidence is "+ json.dumps(evidence))
        
        ep = mm.predict_proba(evidence)[27].parameters[0]
        epa = ep['A']
        epb = ep['B']
        epc = ep['C']
        
        print ('EPA is ' + str(epa) + 'EPB is ' + str(epb) + ' EPC is' + str(epc))
        if (float(epa)>0.5 | float(epb)>0.5 | float(epc)>0.5):
            return "true"
        else:
            return "false"
    
class next_question(Resource):

    def get(self):
        
        global evidence, var, model, variable_list
        
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
        variable_list =["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15","q16", "q17", "q18", "q19", "q20"]
        model = load_model("risk_tolerance.json")
        question_order = rank_variable_par()
        first_item = list(question_order)[0]
        print (first_item)
        return first_item


api.add_resource(build_model, '/build_model')
api.add_resource(next_question, '/next_question')
api.add_resource(RiskTolerance, '/testing')
api.add_resource(reset_evidence, '/reset_evidence')
api.add_resource(get_eligibility, '/get_eligibility')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)