# Machine Learning Age Guesser
Check out a live version [here](https://sidpremkumar.com/MLAgeGuesser.html)
### How do I work? 
I use a decision tree to make decision on how I guess your age. 

To do this I first have to create a classifier. A classifier is a tool used to take an input, and convert it to an appropriate age. 
We first have to create a question method, this basically states all the possible questions that we can ask. For example if we have a question 
that could take on values from 1 - 10, all the question we could ask would be: is the question >=1, is the question >= 2.... is the question >= 10. 
```python
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
```

After we can evaluate all the possible question, we need to select the best possible question based on the ones were given. To do this 
we use something called a Gini. Basically this tells us the chance of us being wrong in our guess. It depends how many different features there
are vs  how many different type of labels there are.

```python
def gini(rows):

    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity
```

Once we know what kind of questions and how successful each question will be in partitioning the data we must select the best combination 
of questions. To do this we use a concept called 'Information Gain'. This method will evaluate all possible questions and all Gini's attached 
to the questions and then select the question that gets the most gain. After selecting the best question, we just create a tree based 
on all the questions we asked. 
```python
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
```

Once we have this tree that we've created we can use a classifier to move down the tree based on a series of inputs.

```python
def classify(row, node):
    # if were at a leaf node
    if isinstance(node, Leaf):
        return node.predictions

    #which way to move? left or right?
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
```

This code was modeled off of the Google Machine learning course found [here](https://www.youtube.com/watch?v=LDRbO9a6XPU).
