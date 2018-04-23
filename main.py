from __future__ import print_function
from sklearn import tree
import pandas as pd
import csv





def createFeatures(df):
    ret = []
    rows = df.shape[0]
    for x in range(rows):
        if x == 0:
            continue
        else:
            add = [int(df[0][x]),int(df[1][x]),int(df[2][x]),int(df[3][x]),int(df[4][x])]
            ret.append(add)
    return ret

def createLables(df):
    ret = []
    rows = df.shape[0]
    for x in range(rows):
        if x==0:
            continue
        else:
            add = int(df[5][x])
            ret.append(add)
    return ret

def createTrainingData(df):
    ret = []
    rows = df.shape[0]
    for x in range(rows):
        if x == 0:
            continue
        else:
            add = [int(df[0][x]),int(df[1][x]),int(df[2][x]),int(df[3][x]),int(df[4][x]),int(df[5][x])]
            ret.append(add)
    return ret







header = ["q1", "q2", "q3","q4","q5","label"]

#Unique Vals: Finds the unique values in a dataset.
def unique_vals(rows, col):
    return set([row[col] for row in rows])


#Class Counts: counts the number of each type in the data set
def class_counts(rows):
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

#Is Numeric: 0 - 9 vs a - z
def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

#Question:
#This shows all the types of quetions we can ask. Based on lables vs features.
class Question:
    #generate a list of questions
    def __init__(self,column,value):
        self.column = column
        self.value = value

    def match(self,example):
        #comp feature value in example to feature value in question
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))

#Patition: the data
def partition(rows,question):
    true_rows,false_rows = [], []
    for x in rows:
        if question.match(x):
            true_rows.append(x)
        else:
            false_rows.append(x)
    return true_rows,false_rows

#Gini:
#basically this tells us the chance of us being wrong in our guess. It depends how many different features there
#are vs  how many different type of labels there are.
def gini(rows):

    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

#Information gain:
#just a number to tell us what question to ask. We get a impurity, then try every possible combination of
#partitions that yield the lowest weighted average impurity on the child nodes. We then add it to the current
#uncertinty and that is the information we gained.

#Info Gain: Just a function to find the 'gain' in information.
def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

#Find Best Split: Finding the best split of the lables and features that yeilds the highest info gain
def find_best_split(rows):
    best_gain=0
    best_question= None
    current_uncertainty = gini(rows)
    n_features = len(rows[0])-1
    for col in range (n_features):
        values = set([row[col] for row in rows])
        for val in values:
            question = Question(col,val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows)==0 or len(false_rows)==0:
                continue
            gain = info_gain(true_rows,false_rows,current_uncertainty)
            if gain >= best_gain:
                best_gain,best_question = gain, question
    return best_gain,best_question


#Tree:
#This is the tree that will be used to model the decition tree :)

#Leaf: Leaf node class
class Leaf:
    def __init__(self,rows):
        self.predictions=class_counts(rows)

#Decition Node: Node that will be used to partition the data
class Decision_Node:
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

#Build Tree: Using all the helper methods and classes to finally build the tree
def build_tree(rows):
    gain,question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)

    true_rows,false_rows = partition(rows,question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question,true_branch,false_branch)




def classify(row, node):
    # if were at a leaf node
    if isinstance(node, Leaf):
        return node.predictions

    #which way to move? left or right?
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def return_response(input):
    df = pd.read_csv('BUS3 Phil Final Responses - New typeform.csv', sep=',', header=None)
    training_data = createTrainingData(df)
    my_tree = build_tree(training_data)
    return classify(input,my_tree)

def addtocsv(user_input):
    with open('BUS3 Phil Final Responses - New typeform.csv', 'a') as form:
        writer=csv.writer(form)
        writer.writerow([])
        writer.writerow(user_input)



