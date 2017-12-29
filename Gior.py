# extracting gender and age information from natural language texts
# Authored by Tony HAO, th2510@columbia.edu

from kernel.NLP import sentence as NLP_sent
import W_utility.file as ufile
from W_utility.log import ext_print
import sys, os
import re
import unicodedata
import random

def GAXer_wrapper (fdin, fout = None):
    
    #----------------------------------initialize and load supporting data
    # read input data
    all_texts = []
    if fdin is None or fdin =="":
        return False
    
    elif fdin.endswith(".txt"):
        all_texts = ufile.load_files (fdin)
        if all_texts is None or len(all_texts) <= 0:
            print ext_print ('input data error, please check either no such file or no data --- interrupting')
            return
        print ext_print ('found a total of %d data items' % len(all_texts))
    
        output =[]
        for text in all_texts:
            text = text.lower()
            result = GAXer_Ggender(text)
            output.append(result)

        # output result
        if (fout is None) or (fout == ""):
            fout = os.path.splitext(fdin)[0] + "_gender.txt"
    
        ufile.write_file (fout, output, False)
        
    elif fdin.endswith(".csv"):
        all_texts = ufile.load_files (fdin) # a specific file or a directory
        if all_texts is None or len(all_texts) <= 0:
            print ext_print ('input data error, please check either no such file or no data --- interrupting')
            return
        print ext_print ('found a total of %d data items' % len(all_texts))
    
        output =[]
        i = 0
        for texts in all_texts:
            if i%1000 ==0:
                print ext_print ('processing %d' % i)
            i += 1
            
#             if str(texts[0])<>'NCT00002967':
#                 continue
            inclusive = texts[5].lower()
            inclusive = inclusive[0:inclusive.find('exclusi')]
#            combine_texts = texts[2].lower() + ". " + texts[3].lower() + ". " + texts[4].lower() + ". " + inclusive
            combine_texts =texts[3].lower() + ". " + texts[4].lower() + ". " + inclusive
            pre_label = 'Biological '+texts[1][0].upper()+texts[1][1:]
            result = GAXer_Ggender(combine_texts, pre_label)
#            print result
#            if len(result)==0 or (len(texts[1])>0 and len(result)==1 and pre_label in result):
            if len(result)==0:
                continue
            else:
                t=texts[0]
                t = t.replace('"','')
                t=str(t)
                output.append((t, texts[1], str(result)))

        # output result
        if (fout is None) or (fout == ""):
            fout = os.path.splitext(fdin)[0] + "_gender.csv"
    
        ufile.write_csv (fout, output)

    print ext_print ('saved processed results into: %s' % fout)

    print ext_print ('all tasks completed\n')
    return True

def Extract_nonGT(fdin, fout,fin_,fout_,c):

    #----------------------------------initialize and load supporting data
    # read input data
    all_texts = []
    if fdin is None or fdin =="":
        return False

    elif fdin.endswith(".txt"):
        all_texts = ufile.load_files (fdin)
        if all_texts is None or len(all_texts) <= 0:
            print ext_print ('input data error, please check either no such file or no data --- interrupting')
            return
        print ext_print ('found a total of %d data items' % len(all_texts))

        output =[]
        for text in all_texts:
            text = text.lower()
            result = GAXer_Ggender(text)
            output.append(result)

        # output result
        if (fout is None) or (fout == ""):
            fout = os.path.splitext(fdin)[0] + "_gender.txt"

        ufile.write_file (fout, output, False)

    elif fdin.endswith(".csv"):
        all_texts = ufile.load_files (fdin) # a specific file or a directory
        all_texts_ = ufile.load_files (fin_) # a specific file or a directory
        if all_texts is None or len(all_texts) <= 0:
            print ext_print ('input data error, please check either no such file or no data --- interrupting')
            return
        print ext_print ('found a total of %d data items' % len(all_texts))

        output =[]
        output_ =[]
        i = 0
        cnt=0
        cho=0
        j=100
        jump=int(j*random.random())+2
        goadList={}
        for t in all_texts_:
            goadList[t[0]]=1

        for texts in all_texts:
            if i%1000 ==0:
                print ext_print ('processing %d' % i)
            i += 1

#             if str(texts[0])<>'NCT00002967':
#                 continue
            cop=texts
            inclusive = texts[5].lower()
            inclusive = inclusive[0:inclusive.find('exclusi')]
            combine_texts = texts[2].lower() + ". " + texts[3].lower() + ". " + texts[4].lower() + ". " + inclusive
            pre_label = 'Biological '+texts[1][0].upper()+texts[1][1:]
            result = GAXer_Ggender(combine_texts, pre_label)
            '''
            if 'Transgender' not in str(result):
                FindSame = texts[0] in goadList.keys()
                if not FindSame:
                    if cho==jump:
                        output_.append((cop[0],cop[1],cop[2],cop[3],cop[4],cop[5]))
                        cnt+=1
                        jump=int(j*random.random())+2
                        cho=0
                    cho+=1
            '''
            if 'Transgender' not in str(result):
                FindSame = texts[0] in goadList.keys()
                if not FindSame:
                    output_.append((cop[0],cop[1],cop[2],cop[3],cop[4],cop[5]))
                    cnt+=1
            if cnt==c:
                break

            if len(result)==0 or (len(texts[1])>0 and len(result)==1 and pre_label in result):
                continue
            else:
                t=texts[0]
                t = t.replace('"','')
                t=str(t)
                output.append((t, texts[1], str(result)))

        # output result
        if (fout is None) or (fout == ""):
            fout = os.path.splitext(fdin)[0] + "_gender.csv"

        ufile.write_csv (fout, output)
        ufile.write_csv (fout_, output_)

    print ext_print ('saved processed results into: %s' % fout)

    print ext_print ('all tasks completed\n')
    return True


# from nltk import word_tokenize
# def GAXer_Ggender (text):
#     text = text.lower();
#     
#     #---------------detect gender
#     splis = ["exclusion", "exclusive"]
#     for spli in splis:
#         if text.contains(spli):
#             text_in = text.split(spli)[0]
#             text_ex = text.split(spli)[1:]
#             break
# 
#     if text_in is None:
#         text_in = text

cates1 = ["Biological", "Transgender"]
cates2 = ["Both", "Male", "Female"]
rels1 = {'Not Biological Female':'Biological Male', 'Not Biological Male':'Biological Female', 'Not Transgender Female':'Transgender Male', 'Not Transgender Male':'Transgender Female'}
rels2 = {'Biological Male':'Biological Both', 'Biological Female':'Biological Both', 'Transgender Male':'Transgender Both', 'Transgender Female':'Transgender Both'}
rels3 = {'Biological Both':'Biological', 'Biological Male':'Biological', 'Biological Female':'Biological', 'Transgender Both':'Transgender', 'Transgender Male':'Transgender', 'Transgender Female':'Transgender'}

# male = "males|male|man|men|father|fathers|boy|boys|gentleman|he"
# female = "females|female|woman|women|mother|mothers|pregnant|pregnancy|girl|girls|lady|ladies|lassie|she"
all_gender = "lgbt|any sex/gender, including transgender|any gender/sex, including transgender|men and women, transgender|men or women, transgender"
male = "m|males|male|man|men|msm|msw|msm/w|msw/m|gay|gays"
female = "f|females|female|woman|women|wsw|wsm|wsm/w|wsw/m|lesbian|lesbian|les"
both = "m/f|m&f|both genders|two genders|two-gender|all genders|all-gender|male and female|male&female|male & female|any gender|genderqueer"
un_both = "person|individual|persons|individuals"
bio = "biologically|biological|birth sex"
trans = "trans|transgender|transsexual|transsexuals|transsexualism|change sex|changed sex|sex changed|change gender|changed gender|gender changed|Self-identified|sr surgery performed|sr surgery|sex reassignment surgery|sex reassignment"



Tboth = "female-to-male and male-to-female|male-to-female and female-to-male|mft and fmt|fmt and mft|male to female and female to male|female to male and male to female|m to f and f to m|f to m and m to f"
MFT = "mft|female from male|male at birth and currently identify as female|male-to-female transgender women|men transitioning into women|male sex at birth and now self-identifies as a woman"
MFT_un = "male-to-female|mtf|male-female|male - female|male to female|m to f"
FMT = "fmt|male from female|female at birth and currently identify as male|female-to-male transgender men|women transitioning into men|female sex at birth and now self-identifies as a man"
FMT_un = "female-to-male|ftm|female-male|female - male|female to male|f to m"

sex = "hemeosexual|Heterosexual"
mult_c = "couple|couples|man+woman|male+female|male&female|male & female|husband and wife"

partner = "partner|partners|sexual partner|sexual partners|wife|husband"
# expt = "with|who|which|of"
# mult_m = "families|family"

neg = "no|not|except|besides|rather|rather than|neither|not identify as|not identified as"

def GAXer_Ggender (ori_text, pre_label=None):
    ori_text = ori_text.lower()
    flag = ori_text.find('gender')>-1 or ori_text.find('sex')>-1
    tags, values, gender = [], [], []
    sentences = re.split("[#.!?]\s", ori_text)
    exclusionCriteria=False;
    for text in sentences:
        text = text.strip()
        if text == '':
            continue
        #!!text = text.replace('(', '').replace(')','')
        text = text.replace('(', ' ').replace(')',' ')
        while '  ' in text:
            text = text.replace('  ',' ')
        if text.find('exclusion criteria')>-1:
            exclusionCriteria = True;
        #=======================detect gender feature by regular expressions
    #     text = re.sub(r"(?<!(\w|\d|<|>|-))(("+sex+") ("+mult_c+"))(?!(\w|\d|<|>))", r'<G=Couple \3>\2</G>', text) #
    #     text = re.sub(r"(?<!(\w|\d|<|>|-))("+mult_c+")(?!(\w|\d|<|>))", r'<G=Couple>\2</G>', text) #


        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") (from ("+female+") ((into|to) ("+male+"))?|(from ("+female+") )?(into|to) ("+male+")))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") (from ("+male+") ((into|to) ("+female+"))?|(from ("+male+") )?(into|to) ("+female+")))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))((("+trans+") )?("+FMT+")( ("+trans+"))?)(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))((("+trans+") )?("+MFT+")( ("+trans+"))?)(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))((("+trans+") )?("+Tboth+")( ("+trans+"))?)(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[0]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))((("+trans+") )?("+FMT_un+")( ("+trans+"))?)(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))((("+trans+") )?("+MFT_un+")( ("+trans+"))?)(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)


        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+"|gender"+") ("+FMT_un+")|("+FMT_un+") ("+trans+"|gender"+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+"|gender"+") ("+MFT_un+")|("+MFT_un+") ("+trans+"|gender"+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") ("+male+")|("+male+") ("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") ("+female+")|("+female+") ("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+")/("+male+")|("+male+")/("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+")/("+female+")|("+female+")/("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[2]+r'>\2</G>', text)


        text = re.sub(r"(?<!(\w|\d|<|>|-))("+all_gender+")(?!(\w|\d|<|>))", '<G='+'All'+r'>\2</G>', text) #

        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") ("+both+")|("+both+") ("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[0]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+trans+") ("+un_both+")|("+both+") ("+trans+"))(?!(\w|\d|<|>))", '<G='+cates1[1]+' '+cates2[0]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+bio+") ("+both+")|("+both+") ("+bio+"))(?!(\w|\d|<|>))", '<G='+cates1[0]+' '+cates2[0]+r'>\2</G>', text)


        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+bio+"|gender|sex"+") ("+male+")|("+male+") ("+bio+"|gender|sex"+"))(?!(\w|\d|<|>))", '<G='+cates1[0]+' '+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))(("+bio+"|gender|sex"+") ("+female+")|("+female+") ("+bio+"|gender|sex"+"))(?!(\w|\d|<|>))", '<G='+cates1[0]+' '+cates2[2]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))("+bio+")(?!(\w|\d|<|>))", '<G='+cates1[0]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+trans+")(?!(\w|\d|<|>))", '<G='+cates1[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+both+")(?!(\w|\d|<|>))", '<G='+cates2[0]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+male+")(?!(\w|\d|<|>))", '<G='+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+female+")(?!(\w|\d|<|>))", '<G='+cates2[2]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+male+")(?!(\w|\d|<|>))", '<G='+cates2[1]+r'>\2</G>', text)
        text = re.sub(r"(?<!(\w|\d|<|>|-))("+female+")(?!(\w|\d|<|>))", '<G='+cates2[2]+r'>\2</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))("+neg+") <G=([^<>]+)>([^<>]+)</G>", r'<G=Not \3>\2 \3</G>', text)

        text = re.sub(r"(?<!(\w|\d|<|>|-))("+neg+") (\w+ ){0,3}<G=([^<>]+)>([^<>]+)</G>", r'<G=Not \4>\2 \4</G>', text)

        text = re.sub(r'<G=Not [^<>]+>([^<>]+)</G> [^.<>?!]*(who|which|that|having|with|of|after|before)', r'\1 \2', text)

        text = re.sub(r'(?<!(\w|\d|<|>|-))('+partner+'|with|with a'+') <G=[^<>]+>([^<>]+)</G>', r'\2 \3', text)
        text = re.sub(r'<G=[^<>]+>([^<>]+)</G> ('+partner+'condom|condoms'+')', r'\1 \2', text)
        text = re.sub(r'<G=[^<>]+>([^<>]+)</G>(\@|\#|\%|\&|\*|\+|\-|\=|\_|\/|\\)', r'\1\2', text)
        text = re.sub(r'<G=[^<>]+>(f|m)</G>', r'\1', text)

        text = re.sub('(<G=[^<>]+>[^<>]+)<G=[^<>]+>', r'\1', text)
        text = re.sub('</G>([^<>]+</G>)', r'\1', text)



        # output
#!!        tag =re.findall(r'<G=[^<>]+>([^<>]+)</G>', text)
#!!       if len(tag) > 0:
#!!           tags += tag

        vals = re.findall(r'<G=([^<>]+)>', text)

        w_cate1 = cates1[0] # set default value as "Biological"
        found = False
        for val in vals:
            if (val == cates1[1]) or (val == 'Not '+cates1[1]): # only contain transgender, e.g., "Transgender"
                w_cate1 = val # set it for context analysis

        valIndex = len(values)
        foundBio = False
        foundTran = False
        for val in vals:
            if val=='All':
                values.append(cates1[0]+' '+cates2[0])
                values.append(cates1[1]+' '+cates2[0])
            elif cates2[0] in val or cates2[1] in val or cates2[2] in val: # found a specific word, e.g., "Female"
                found = True
                if cates1[1] in val and not flag: # continue if it is a clear transgender item
                    continue
                if val.startswith('Not ') and len(val.split())==2:
                    values.append('Not '+w_cate1.replace('Not ','')+' '+val.replace('Not ',''))
                elif val.startswith('Not ')==False and len(val.split())==1:
                    values.append(w_cate1+' '+val)
                else:
                    values.append(val)
        if not found and w_cate1 == cates1[1]: # no specific gender found and not a biological gender, then add 'both'
            values.append(w_cate1 + ' Both')

        while valIndex < len(values):
            if cates1[0] in values[valIndex]:
                foundBio = True
            if cates1[1] in values[valIndex]:
                foundTran = True
            valIndex+=1
        if found and w_cate1 == cates1[1] and foundBio and not foundTran:
            values.append(w_cate1 + ' Both')

    found_Trans = False
    for val in values:
        if cates1[1] in val:
            found_Trans = True
            break
                    
    if not found_Trans and pre_label is not None and pre_label <> "": # use pre-defined labels or not as one item for decision making
        values.append(pre_label)
        
    gender = judge_gender(values)
    
#     return str(tags) + " | " + str(values) + " | " + str(gender)
    return gender

threshold = 1 # minimum number of difference
def judge_gender(values):
    if len(values) == 0:
        types = set(values)
#         types.add(cates1[0]+' '+cates2[0])
        types = list(types)
    else:
        # create category list 
        catelist = {}
        for i in xrange(0,len(cates1)):
            for j in xrange(1, len(cates2)): # without 'both'
                catelist[cates1[i]+' '+cates2[j]] = 0

        # get all values and normalized into catelist
        types = values
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
                if 'Not '+cate in rels1:
                    catelist[rels1['Not '+cate]] += 1

        # detect special gender (not bio); add effective genders into types
        types = set()
        sp_gender = False
        for cate, value in catelist.iteritems():
            if value > 0:
                types.add(cate)
                if not cate.startswith(cates1[0]):
                    sp_gender = True

        # value judge to get result by comparing with threshold
        if len(types) > 1:
            sort_cates = sorted([(value,key) for (key,value) in catelist.items()])
            if int(sort_cates[-1][0]) >= threshold*int(sort_cates[-2][0]):
                return [sort_cates[-1][1]]

        # if have special gender, then remove bio gender.
        types2 = list(types)
        for type in types2:
            if (type in rels2 and rels2[type] in types):
                types.remove(type) # merge if there is high coverage gender

        # combine genders 'bilogical male' +'biological female' = 'biological both'
        if (cates1[0]+' '+cates2[1] in types and cates1[0]+' '+cates2[2] in types):
            types.add(cates1[0]+' '+cates2[0])
            types.remove(cates1[0]+' '+cates2[1])
            types.remove(cates1[0]+' '+cates2[2])
        if (cates1[1]+' '+cates2[1] in types and cates1[1]+' '+cates2[2] in types):
            types.add(cates1[1]+' '+cates2[0])
            types.remove(cates1[1]+' '+cates2[1])
            types.remove(cates1[1]+' '+cates2[2])
            
    return list(types)


def judge_gender_NonTG(values):
    if len(values) == 0:
        types = set(values)
#         types.add(cates1[0]+' '+cates2[0])
        types = list(types)
    else:
        # create category list
        catelist = {}
        for i in xrange(0,len(cates1)):
            for j in xrange(1, len(cates2)): # without 'both'
                catelist[cates1[i]+' '+cates2[j]] = 0

        # get all values and normalized into catelist
        types = values
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
                if 'Not '+cate in rels1:
                    catelist[rels1['Not '+cate]] += 1

        # detect special gender (not bio); add effective genders into types
        types = set()
        sp_gender = False
        for cate, value in catelist.iteritems():
            if value > 0:
                types.add(cate)
                if not cate.startswith(cates1[0]):
                    sp_gender = True

        # value judge to get result by comparing with threshold


        # if have special gender, then remove bio gender.
        types2 = list(types)
        for type in types2:
            if (type in rels2 and rels2[type] in types):
                types.remove(type) # merge if there is high coverage gender

        # combine genders 'bilogical male' +'biological female' = 'biological both'
        if (cates1[0]+' '+cates2[1] in types and cates1[0]+' '+cates2[2] in types):
            types.add(cates1[0]+' '+cates2[0])
            types.remove(cates1[0]+' '+cates2[1])
            types.remove(cates1[0]+' '+cates2[2])
        if (cates1[1]+' '+cates2[1] in types and cates1[1]+' '+cates2[2] in types):
            types.add(cates1[1]+' '+cates2[0])
            types.remove(cates1[1]+' '+cates2[1])
            types.remove(cates1[1]+' '+cates2[2])

    return list(types)



# main function    

# processing the command line options
import argparse
def _process_args(fin,fout):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', default=fin, help='input training file')
#     parser.add_argument('-i', default="E:/programs/Gior_gender/data/alls.csv", help='input training file')
    parser.add_argument('-o', default=fout, help='output training file; None: get default output path')
    
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__' :
    print ''
    '''
#    fin = "F:/PythonProject/Gior_gender/data/before_article3/testing.csv"
    fin = "F:/PythonProject/Gior_gender/data/before_article4/alls_data2000.csv"
    for i in range(10):
        if (i+1)!=7:
            continue
#        fout = "F:/PythonProject/Gior_gender/data/before_article3/testing_"+str(i+1)+"_out.csv"
        fout = "F:/PythonProject/Gior_gender/data/before_article4/alls_data2000_out.csv"
        threshold=i+1
        args = _process_args(fin,fout)
        GAXer_wrapper (args.i, args.o)
    print ''

    '''
    #alls_data100_final
    fin = "F:/PythonProject/Gior_gender/data/before_article5/alls2.csv"
#    fin = "F:/PythonProject/Gior_gender/data/prere/alls_data1.csv"
    for i in range(10):
        if (i+1)!=7:
            continue
        fout = "F:/PythonProject/Gior_gender/data/prere/alltest_"+str(i+1)+"_out.csv"
#        fout = "F:/PythonProject/Gior_gender/data/prere/alls_data1_out.csv"
        threshold=i+1
        args = _process_args(fin,fout)
        args_ = _process_args("F:/PythonProject/Gior_gender/data/before_article5/list.csv","F:/PythonProject/Gior_gender/data/before_article5/alls_data5000.csv")
        Extract_nonGT(args.i, args.o,args_.i,args_.o,5000)

    print ''
