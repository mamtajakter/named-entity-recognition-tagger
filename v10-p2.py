

def readFile(keyFileName):
    name = []
    namelist = []
    dict = {}
    keyFile = open(keyFileName, 'r')
    key = keyFile.readlines()
    keyWord = [""]
    keyFeature1 = [""]
    keyFeature2 = [""]
    keyFeature3 = [""]
    keyFeature4 = [""]
    keyFeature5 = [""]
    #FEATURE#
    # keyTag = [""]

# x=keyname[0]
# if x not in namelist:
#     namelist.append(x)

    for i in range(len(key)):
        key[i] = key[i].rstrip('\n').strip()
        if key[i] == "":
            keyWord.append("")
            keyFeature1.append("")
            keyFeature2.append("")
            keyFeature3.append("")
            keyFeature4.append("")
            keyFeature5.append("")
            #FEATURE#
            # keyTag.append("")
            continue
        else:
            keyFields = key[i].split('\t')
            keyWord.append(keyFields[0])
            keyFeature1.append(keyFields[1])
            keyFeature2.append(keyFields[0])
            if i==0:
                keyFeature3.append("")
            else:
                preKeyFields = key[i-1].split('\t')
                keyFeature3.append(preKeyFields[0])



            if i==(len(key)-1):
                keyFeature4.append("")
            else:
                nextKeyFields = key[i+1].split('\t')
                if (nextKeyFields[0]=="\n"):
                    keyFeature4.append("")
                else:
                    keyFeature4.append(nextKeyFields[0])
            keyFeature5.append("@@")
            #FEATURE#
            # keyTag.append(keyFields[3])
            # x=keyFields[1]
            # if x not in namelist:
            #     namelist.append(x)
    return keyWord, keyFeature1, keyFeature2,keyFeature3,keyFeature4,keyFeature5 #FEATURE#

trainFileName = "dev.pos-chunk"
# devFileName = "dev.pos-chunk"

keyWord,keyFeature1, keyFeature2,keyFeature3,keyFeature4,keyFeature5 = readFile(trainFileName)#FEATURE#
# keyTag2,keyname2 = readFile(devFileName)

outF = open("dev-input.txt", "w")

# print (keyTag)
# print (keyname)
# print (len(keyTag))
# print (len(keyname))
for i in range(len(keyWord)):
    # write line to output file
    word = keyWord[i]
    feature1 = keyFeature1[i]
    feature2 = keyFeature2[i]
    feature3 = keyFeature3[i]
    feature4 = keyFeature4[i]
    feature5 = keyFeature5[i]
    #FEATURE#
    # tag = keyTag[i]

    if (word==""):
        line=""
        if (i>0):
            outF.write("\n")
    else:
        line = str(word) + "\tpos-tag=" + str(feature1)+ "\tcur-tok=" + str(feature2)+ "\tpre-tok=" + str(feature3) + "\tnex-tok=" + str(feature4)+ "\tpre-tag=" + str(feature5) #FEATURE#
        outF.write(line)
        outF.write("\n")
outF.close()
# for x in keyname:
#     print(x)
