from random import shuffle

pathbase = './data/split-diogs/'

# Below three lines need changed based upon experiment
inpath = pathbase + 'zero-shot/multi-task/both-masked.jsonl'
outbase = pathbase + 'pcent-20/multi-task/'
train_size = 6
# pcent-20 = 6, pcent-50 = 15, pcent-80 = 24

allLines = []

with open(inpath, 'r') as f:
    for line in f:
        allLines.append(line)

def splitSet(allLines, train_size, outbase, run):
    shuffle(allLines)

    i = 0
    trainSet = []
    testSet = []
    for record in allLines:
        if i < train_size:
            trainSet.append(record)
            i = i + 1
        else:
            testSet.append(record)

    trainpath = outbase + 'run' + str(run) + '-train.jsonl'
    testpath = outbase + 'run' + str(run) + '-test.jsonl'
    with open(trainpath, 'w') as trof:
        for trainex in trainSet:
            trof.write(f"{trainex}")
            
    with open(testpath, 'w') as teof:
        for testex in testSet:
            teof.write(f"{testex}")

run = 1
while run < 6:
    splitSet(allLines, train_size, outbase, run)
    run = run + 1