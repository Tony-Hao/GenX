import csv
import re

Biological = "Biological"
Transgender = "Transgender"
Both = "Both"
Male = "Male"
Female = "Female"
rels1 = {'Not Biological Female':'Biological Male', 'Not Biological Male':'Biological Female', 'Not Transgender Female':'Transgender Male', 'Not Transgender Male':'Transgender Female'}
rels2 = {'Biological Male':'Biological Both', 'Biological Female':'Biological Both', 'Transgender Male':'Transgender Both', 'Transgender Female':'Transgender Both'}
rels3 = {'Biological Both':'Biological', 'Biological Male':'Biological', 'Biological Female':'Biological', 'Transgender Both':'Transgender', 'Transgender Male':'Transgender', 'Transgender Female':'Transgender'}

# the step of Text Pre-Processing.
def textPreProcessing(ori_text):
    ori_text = ori_text.lower()
    ori_text = ori_text.replace('(', ' ').replace(')', ' ')
    while '  ' in ori_text:
        ori_text = ori_text.replace('  ', ' ')
    sentences = re.split("[#.!?]\s", ori_text)
    return sentences

# 'rule.csv', 'genderDic.csv', 'cates.csv'
# load regular expression rule from file
def loadRule(ruleFile, genderDictionaryFile, catesFile):
    # read the regular expression file
    ruleCsvFile = open(ruleFile, 'rb')
    ruleReader = csv.reader(ruleCsvFile)
    # read the gender dictionary file
    genderDicCsvFile = open(genderDictionaryFile, 'rb')
    genderDicReader = csv.reader(genderDicCsvFile)
    rulePattern = []
    genderDicPattern = []
    for pattern in genderDicReader:
        genderDicPattern.append((pattern[0], pattern[1]))
    genderDicCsvFile.close()
    catesCsvFile = open(catesFile, 'rb')
    catesReader = csv.reader(catesCsvFile)
    patternCates = []
    for pattern in catesReader:
        patternCates.append((pattern[0], pattern[1]))
    catesCsvFile.close()
    # load the regular expression into the arry 'rulePattern'
    for pattern in ruleReader:
        pDic = pattern[0]
        pCates = pattern[1]
        for item in genderDicPattern:
            pDic = pDic.replace(item[0], item[1])
        for item in patternCates:
            pCates = pCates.replace(item[0], item[1])
        rulePattern.append((pDic, pCates))
    ruleCsvFile.close()
    return rulePattern

def genderAnnotator(sentences, rulePattern, pre_label=None):
    flag = False
    for sentence in sentences:
        if sentence.find('gender') > -1 or sentence.find('sex') > -1:
            flag = True
    tags, genderValuesList, gender = [], [], []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence == '':
            continue
        for rule in rulePattern:
            sentence = re.sub(r"" + rule[0] + "", r"" + rule[1] + "", sentence)
        vals = re.findall(r'<G=([^<>]+)>', sentence)
        contextGender = Biological  # set default value as "Biological"
        found = False
        for val in vals:
            if (val == Transgender) or (val == 'Not ' + Transgender):  # only contain transgender, e.g., "Transgender"
                contextGender = val  # set it for context analysis
        valIndex = len(genderValuesList)
        foundBiological = False
        foundTransgender = False
        for val in vals:
            if val == 'All':
                genderValuesList.append(Biological + ' ' + Both)
                genderValuesList.append(Transgender + ' ' + Both)
            elif Both in val or Male in val or Female in val:  # found a specific word, e.g., "Female"
                found = True
                if Transgender in val and not flag:  # continue if it is a clear transgender item
                    continue
                if val.startswith('Not ') and len(val.split()) == 2:
                    genderValuesList.append('Not ' + contextGender.replace('Not ', '') + ' ' + val.replace('Not ', ''))
                elif val.startswith('Not ') == False and len(val.split()) == 1:
                    genderValuesList.append(contextGender + ' ' + val)
                else:
                    genderValuesList.append(val)
        if not found and contextGender == Transgender:  # no specific gender found and not a biological gender, then add 'both'
            genderValuesList.append(contextGender + ' Both')
        while valIndex < len(genderValuesList):
            if Biological in genderValuesList[valIndex]:
                foundBiological = True
            if Transgender in genderValuesList[valIndex]:
                foundTransgender = True
            valIndex += 1
        if found and contextGender == Transgender and foundBiological and not foundTransgender:
            genderValuesList.append(contextGender + ' Both')
    found_Trans = False
    for val in genderValuesList:
        if Transgender in val:
            found_Trans = True
            break
    if not found_Trans and pre_label is not None and pre_label <> "":  # use pre-defined labels or not as one item for decision making
        genderValuesList.append(pre_label)
    return genderValuesList

# threshold is minimum number of difference
def genderTypeConclusion(genderValuesList, threshold):
    cates1 = ["Biological", "Transgender"]
    cates2 = ["Both", "Male", "Female"]
    if len(genderValuesList) == 0:
        types = set(genderValuesList)
        types = list(types)
    else:
        # create category list
        catelist = {}
        for i in xrange(0, len(cates1)):
            for j in xrange(1, len(cates2)):  # without 'both'
                catelist[cates1[i] + ' ' + cates2[j]] = 0
        # get all values and normalized into catelist
        types = genderValuesList
        for type in types:
            if type.endswith('Both') and not type.startswith('Not '):
                catelist[type.replace('Both', 'Male')] += 1
                catelist[type.replace('Both', 'Female')] += 1
            elif type in catelist:
                catelist[type] += 1
            elif type.startswith('Not '):
                if type[4:] in catelist:
                    catelist[type[4:]] = -1
        # process if value is lower than 1 (negtive cases)
        for cate, value in catelist.iteritems():
            if value < 0:
                if 'Not ' + cate in rels1:
                    catelist[rels1['Not ' + cate]] += 1
        # detect special gender (not bio); add effective genders into types
        types = set()
        sp_gender = False
        for cate, value in catelist.iteritems():
            if value > 0:
                types.add(cate)
                if not cate.startswith(cates1[0]):
                    sp_gender = True

        finalGender = []
        # value judge to get result by comparing with threshold
        if len(types) > 1:
            sort_cates = sorted([(value, key) for (key, value) in catelist.items()])
            for i in range(len(types)):
                finalGender.append(sort_cates[-1*(i+1)][1])
                if i != len(types)-1:
                    if int(sort_cates[-1*(i+1)][0]) >= threshold * int(sort_cates[-1*(i+2)][0]):
                        break
            finalGender = set(finalGender)
        else:
            finalGender = types
        # print finalGender
        # if have special gender, then remove bio gender.
        types2 = list(finalGender)
        for type in types2:
            if (type in rels2 and rels2[type] in finalGender):
                finalGender.remove(type)  # merge if there is high coverage gender

        # combine genders 'bilogical male' +'biological female' = 'biological both'
        if (Biological + ' ' + Male in finalGender and Biological + ' ' + Female in finalGender):
            finalGender.add(Biological + ' ' + Both)
            finalGender.remove(Biological + ' ' + Male)
            finalGender.remove(Biological + ' ' + Female)
        if (Transgender + ' ' + Male in finalGender and Transgender + ' ' + Female in finalGender):
            finalGender.add(Transgender + ' ' + Both)
            finalGender.remove(Transgender + ' ' + Male)
            finalGender.remove(Transgender + ' ' + Female)
    finalGender = list(finalGender)
    finalGender = str(finalGender)
    return finalGender

def genderOutputNormalization(gender):
    norGender = "["
    if "Transgender" in gender and "Biological" in gender:
        if "Transgender Both" in gender:
            norGender = norGender + "'Transgender Both', "
        elif "Transgender Female" in gender:
            norGender = norGender + "'Transgender Female', "
        else:
            norGender = norGender + "'Transgender Male', "
        if "Biological Both" in gender:
            norGender = norGender + "'Biological Both']"
        elif "Biological Female" in gender:
            norGender = norGender + "'Biological Female']"
        else:
            norGender = norGender + "'Biological Male']"
    elif "Transgender" in gender and "Biological" not in gender:
        if "Transgender Both" in gender:
            norGender = norGender + "'Transgender Both']"
        elif "Transgender Female" in gender:
            norGender = norGender + "'Transgender Female']"
        else:
            norGender = norGender + "'Transgender Male']"
    elif "Transgender" not in gender and "Biological" in gender:
        norGender = norGender + "'Biological']"
    return norGender

# the whole process of GenX
def GenX(ori_text, threshold, pre_label=None):
    sentences = textPreProcessing(ori_text)
    rulePattern = loadRule('rules/rule.csv', 'rules/genderDic.csv', 'rules/cates.csv')
    genderValuesList = genderAnnotator(sentences, rulePattern, pre_label)
    gender = genderTypeConclusion(genderValuesList, threshold)
    gender = genderOutputNormalization(gender)
    return gender

# utilize the GenX to process the clinical trials
def processByGenX(fileIn, fileOut, threshold):
    fileIn = 'clinicaltrial/'+ fileIn
    fileOut = 'clinicaltrial/'+ fileOut
    clincailTrialCsvFile = open(fileIn, 'rb')
    clinicalTrialReader = csv.reader(clincailTrialCsvFile)
    # read the clinical trials file
    cnt = 0
    GenXOutFile = file(fileOut, 'wb')
    writer = csv.writer(GenXOutFile)
    GenXOut = []

    for trial in clinicalTrialReader:
        if cnt % 1000 == 0:
            print 'processing ' + str(cnt)

        cnt += 1
        NCT = trial[0]
        NCT = NCT.replace('"', '')
        NCT = str(NCT)

        inclusive = trial[5].lower()
        inclusive = inclusive[0:inclusive.find('exclusi')]
        combine_texts = trial[3].lower() + ". " + trial[4].lower() + ". " + inclusive
        if trial[1].lower() == 'all':
            pre_label = 'Biological Both'
        else:
            pre_label = 'Biological ' + trial[1][0].upper() + trial[1][1:]

        result = GenX(combine_texts, threshold, pre_label)
        GenXOut.append((NCT, trial[1], result))
        # print result

    writer.writerows(GenXOut)
    clincailTrialCsvFile.close()
    GenXOutFile.close()

if __name__ == '__main__' :
    threshold = 7
    processByGenX('144_clinical_trails_data.csv', '144_clinical_trails_data_threshold' + str(threshold) + '.csv',threshold)

    # ori_text = 'antiretroviral pre-exposure with Truvada versus placebo, associated with overall prevention (counselling, condoms, sexually transmitted diseases (STD) screening, HBV and HAV vaccinations and post-exposure treatment of HIV infection) in men who have sex with men (MSM), exposed to the risk of HIV infection. Indeed recent studies have reported a higher incidence of new HIV infection in MSM as compared to the general population, new approaches to the prevention of HIV infection are, therefore, necessary in order to consider the limits of current strategies..Inclusion Criteria:# - Age >= 18 years old# - Male (or transgender) having sex with men# - Not infected with HIV-1 or HIV-2# - Elevated risk of HIV contamination : anal sexual relations with at least 2 different sexual partners within the past 6 months without the systematic use of a condom# - Satisfactory kidney function with a clearance of more than 60 mL/min (Cockcroft formula)# - ALT < 2.5 ULN,# - Neutrophil granulocytes >= 1 000/mm3, haemoglobin >= 10 g/dL, platelets >= 150 000/mm3# - Negative HBs antigen and negative HCV serology (or negative HCV PCR if positive serology)# - Agrees to be contacted personally, if possible by telephone, SMS or e-mail# - Agrees to the constraints imposed by the trial (visits every 2 months)# - Subjects enrolled in or a beneficiary of a Social '
    # test = 'male. male. male. male. male.female.female.female.transgender female.transgender male.transgender male.transgender male.'
    # sentences = textPreProcessing('Inclusion Criteria:# - Age >= 18 years old# - Male (or transgender) having sex with men# - Not infected with HIV-1 or HIV-2# - Elevated risk of HIV contamination : anal sexual relations with at least 2 different sexual partners within the past 6 months without the systematic use of a condom# - Satisfactory kidney function with a clearance of more than 60 mL/min (Cockcroft formula)# - ALT < 2.5 ULN,# - Neutrophil granulocytes >= 1 000/mm3, haemoglobin >= 10 g/dL, platelets >= 150 000/mm3# - Negative HBs antigen and negative HCV serology (or negative HCV PCR if positive serology)# - Agrees to be contacted personally, if possible by telephone, SMS or e-mail# - Agrees to the constraints imposed by the trial (visits every 2 months)# - Subjects enrolled in or a beneficiary of a Social ')
    # sentences = loadRule('rule.csv', 'genderDic.csv', 'cates.csv')
    # gender = GenX(test,3)
    # print gender
    # vals = GenX(ori_text)
    # for i in vals:
    #     print i