from Constants import VARIABLES
import os
import subprocess

def generate_graphs(nodes, ipath):
    '''
    First delete all files from graph folder
    '''
    filenames = next(os.walk(ipath))[2]
    for file in filenames:
        filepath = ipath+file
        os.remove(filepath)

    '''
    crate all the graphs using all combinations of edges and nodes
    '''
    graphCount = 0
    edges = int((nodes * (nodes-1))/2)-1
    for i in range(1, edges):
        filename = ipath + 'node_' + str(nodes) + '_edge_' + str(i)
        f = open(filename, 'w')
        subprocess.call(["./randomgraph", str(nodes), str(i), str(5)], stdout=f)
        graphCount+=1

    return graphCount


def color_the_graphs(testParameter, graphFolder):

    # color the graph using different parameters
    #graphFile = 'tg.txt'
    MAXITER = 8
    '''
    TARGET = 10
    CWEIGHTS = 10
    VWEIGHTS = 10
    RLIMIT = 10
    TRILIMIT = 10
    SEED = 10
    '''
    parameterFile = 'parameters.txt'
    parameterOutFile = 'parameters_n.txt'
    graphOutFile = 'graph_out.txt'
    command = ['inp', 'int', 'max', 'tar', 'cwt', 'vwt', 'rev', 'tri', 'see']

    # initialize 2D arrays with 0 for max color and runtime.
    filenames = next(os.walk(graphFolder))[2] #all graph files
    l1 = len(filenames)
    l2 = MAXITER
    maxColor = [[0 for i in range(l2)] for j in range(l1)]
    coloringTime = [[0 for i in range(l2)] for j in range(l1)]

    if (testParameter == 1):  # test iteration
        for filename in filenames:      # for each file, find max color and time max times
            for i in range(MAXITER):
                fo = open(parameterOutFile, 'w')
                with open(parameterFile, 'r') as fi:
                    for rec in fi:
                        if ('max' in rec):
                            line = command[2] + ' ' + str(i+1) + '\n'
                            fo.write(line)
                        elif ('inp' in rec):
                            line = command[0] + ' ' + str(graphFolder+filename) + '\n'
                            fo.write(line)
                        else:
                            fo.write(rec)
                fi.close()
                fo.close()
                # call sig.c to color the graph
                param = "./sig" + " < " + VARIABLES.pfilepath + parameterOutFile + " >" + graphOutFile
                os.system(param)

                # get the max color and run time for each iteration
                mcolor, ctime = get_runtime_maxcolor(graphOutFile)
                t = filename.split('_')
                n = int(t[1])     #nodes
                m = int(t[3])     #edges
                j = m-1
                print ('Coloring the graph: ', filename, ' for iteration ', i, j)
                maxColor[j][i] = mcolor
                coloringTime[j][i] = ctime
        print (maxColor, coloringTime)


def get_runtime_maxcolor(graphOutFile):
    # get the runtime and max color for each iteration
    tempScore = []
    mcolor = 0
    ctime = 0
    with open(graphOutFile, 'r') as fin:
        for rec in fin:
            if ('Time spent' in rec):
                ctime = float(rec.split()[2])
            elif ('curcolors,score' in rec):
                tempScore.append(int(rec.split()[1]))
            else:
                continue
        try:
            mcolor = tempScore[len(tempScore)-1]
        except:
            mcolor = 0

    return mcolor, ctime



def main():
    # generate random graphs
    numOfNodes = 32
    graphCount = generate_graphs(numOfNodes, VARIABLES.ipath)
    print ('Generated ' + str(graphCount) + ' graphs')

    # color all the graphs created above using different parameters
    testParameter = 1   # which parameter should be tested
    color_the_graphs(testParameter, VARIABLES.ipath)


if __name__ == '__main__':
    main()
