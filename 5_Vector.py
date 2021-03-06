


#Unicode Characters from text file
import codecs
import json
import re 
from pprint import pprint
# Import graphviz
import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')

from pygraph.classes.digraph import digraph


gr = digraph()
count = 0

#Input
GraphInput = codecs.open('./Refined_GO_Nodes.txt', encoding='utf-8', mode='r')

EdgesInput = codecs.open('./GO_Children&Parents.txt', encoding='utf-8', mode='r')

with open('./GO_Children&Parents.txt') as json_file:
    json_data = json.load(json_file)
    #print(json_data, "\n")
    
    for key in json_data.keys():
            ##print ("key:", key, " parents:",json_data[key]['p'], " children:",json_data[key]['c'])#("key:",key,"\n")
            node = key.replace(":","")
            gr.add_node(node)
            print ("Added ",node)
            
    
    for key in json_data.keys():
            print (count)
            ##print ("key:", key, " parents:",json_data[key]['p'], " children:",json_data[key]['c'])#("key:",key,"\n")
            node = key.replace(":","")
            #gr.add_node(node)
            for parent in json_data[key]['p']:
                print("PARENT")
                pt = parent.replace(":","")
                #print(node, " - ", pt)
                if gr.has_node(node) and gr.has_node(pt):
                    if not gr.has_edge((pt,node)):
                        gr.add_edge((pt,node))
            for child in json_data[key]['c']:
                print("CHILD")
                cd = child.replace(":","")
                if gr.has_node(node) and gr.has_node(cd):
                    if not gr.has_edge((node,cd)):
                        gr.add_edge((node,cd))
            count +=1
#print(GraphInput)

counter = 0


count = 0
       
with open('./Refined_GO_Nodes.txt') as input:

            tempVec = []
            BinVec = []
            vec= []
            for line in input:
                tempVec.append(line.strip())
                BinVec.append(0)
            for item in tempVec:
                print("Item")
                print(item)
                tempItem = item.replace(":","")
                vec.append(tempItem)
                print(tempItem)
                

Missing = []

def Incidents(Up):
    i = 0
   
    for key in Up:
        #print(i)
        #print(key)
        if key not in Seen:
            tempy = []
            try:
                tempy.extend(gr.incidents(key))
                Seen.append(key)
            except (KeyError,ValueError): 
                OutMissing.write("Tempy Missing")
        #print(len(tempy))
            if  len(tempy) > 0:
                i = i+1
                if i > 0:
                    return False
                else:
                    return True
     
def Duplicates(Up):
    NewUp = []
    NodesSeen = []
    for node in Up:                   
        if node not in NodesSeen: # not a duplicate
            NewUp.append(node)
            NodesSeen.append(node)
    return NewUp           



debug = 0
#outputfile = open('/home/mint/git/prediction-of-Lethality-in-Fly-Mutants-using-Machine-Learning/Workspace/Lethality Extraction/Vector.txt')
#data = open('./Gene&GO_F.txt')#With IMP
data = open('./Gene&GO_F_No_IMP.txt')#Without IMP
outputfile = open('./BinVec.txt', mode = 'w')
OutMissing = open('./Missing.txt', mode = 'w')
OutParents = open('./Parents.txt', mode = 'w')
for line in data:
    debug = debug+1
    csv = line.split(",")
    Gene = csv[0]
    print(csv[0])

    Continue = True

    for t in range(1,len(csv)):
        if "GO" in csv [t]:
                print(csv[t])

                temp = csv[t]
                temp = temp.replace(":","")
               # print ("Ancestors")
                #print(gr.incidents(temp))
                Ancestors = []
                #Ancestors.append(temp)
                Seen = []
                Up = []
                Up.append(temp)

                try:
                    Up.extend(gr.incidents(temp))
                except (KeyError,ValueError):
                    print("Missing")
                    try:
                        Missing.index(gr.incidents(temp))
                        print("Already Missing")
                    except (KeyError,ValueError):
                            try:
                                Missing.append(gr.incidents(temp))
                            except (KeyError,ValueError):
                                Missing.append("Unable To Add Missing Value")


                #Ancestors.extend(Up)
                print("Up")

                Nodes = []
                while Continue == True:
                    l = 0
                    if  Incidents(Up) == False:
                        #print("GO in Incidents")

                        for node in Up:
                                if node not in Nodes:
                                    #if node != "GO0043089":
                                        try:
                                            Up.extend(gr.incidents(node))
                                            l = l+1
                                            if l == 1000000:
                                                Up = Duplicates(Up)
                                    #print("Parents Added")
                                        except (KeyError,ValueError):
                                            print("Error")
                                            Nodes.append(node)
                                    #print("Node Size")
                                    #print(len(Nodes))


                    else:
                        Continue = False
                        print("Root")



                Ancestors.extend(Up)
                print("Ancestors")
                #print(Ancestors)
                #print(vec)
                ModifiedAncestors = []
                NodesSeen = []
                for node in Ancestors:
                    if node not in NodesSeen: # not a duplicate
                        ModifiedAncestors.append(node)
                        NodesSeen.append(node)


                del Ancestors [:]
                for Node in ModifiedAncestors:

                    #OutParents.write(Node)
                    try:

                        print(vec.index(Node))
                        print("1233333333")
                        BinVec[vec.index(Node)] = 1
                    #Parents = gr.incidents(temp)

                    except (KeyError,ValueError):
                        print("Missing")
                        try:
                            Missing.index(Node)
                            print("Already Missing")
                        except (KeyError,ValueError):
                                Missing.append(Node)





    outputfile.write(Gene)
    outputfile.write(',')

    for key in BinVec:

        outputfile.write(str(key))
    outputfile.write('\n')


    print(Gene,BinVec)




    for t in range(0,len(BinVec)):
        BinVec[t] = 0
    print("Loop")
    try:
        del Seen[:]
        del Up[:]
        del Ancestors[:]
        del ModifiedAncestors[:]
        del Nodes[:]
    except NameError:
        print "Wups"
 
 
print("Missing")
print(len(Missing))
for key in Missing:
    OutMissing.write(str(Missing))
    OutMissing.write('\n')
    
#print(datetime.now()-startTime)