## GenX
a Python tool to extract and structure transgender-related clinical trial eligibility criteria free text from ClinicalTrials.gov

**Objective:** To develop an automated approach to structuring transgender criteria text for enhancing transgender-related clinical trial recruitment.  
**Materials and Methods:** A gender criteria data model incorporating transgender populations is designed and an automated method called GenX is developed. GenX extracts and standardizes transgender specifications from clinical trial summaries using the proposed data model. GenX is compared to 42 machine learning methods on 105,078 clinical trials.  
**Results:** GenX achieves a macro-averaged precision of 0.82, a macro-averaged recall of 0.823 and a macro-averaged F1-measure of 0.821, outperforming all other 42 baseline methods.  
**Conclusion:** This study addresses the problems of gender information incompleteness and ambiguity, particularly for transgender populations. A new gender data model extending gender type coverage and an automated method GenX for transgender criteria extraction promise to enhance transgender-related clinical trial recruitment. The experiment results demonstrate the effectiveness of GenX in transgender criteria extraction.

## Usage

<code>
import GenX
</code>

### Clean text by preprocessing and split text into sentences

<code>
GenX.textPreProcessing(text)
</code>  

*text* is the original clinical research eligibility free text and this function will return a list of sentences split from that text  


### Load a set of rules that use to identify and annotate gender information
<code>
GenX.loadRule(ruleFile, genderDictionaryFile, catesFile)
</code>  

*ruleFile*, *genderDictionaryFile* and *catesFile* are corresponding to the files that contain the regular expression rules, gender feature dictionary and the gender categories. Those files are named 'rule.csv', 'genderDic.csv' and 'cates.csv' respectively and are saved in the file named 'rules'

### Extract and annotate the gender features in sentences
<code>
GenX.genderAnnotator(sentences, rules, pre_label=None)
</code>  

Using the *rules* from <code>GenX.loadRule(ruleFile, genderDictionaryFile, catesFile)</code> to process the *sentences* from <code>GenX.textPreProcessing(text)</code>. A set of candidate gender features will be returned. *pre_label* is the original gender type on ClinicalTrial.gov eligibility. This value can also not be input in this function.  

### Conclude the gender type

<code>
GenX.genderTypeConclusion(genderFeatureList, threshold)
</code>  

Using the set *threshold* to conclude the final gender type based on the gender features list from <code>GenX.genderAnnotator(sentences, rulePattern)</code>  

### Normalize the output gender type

<code>
GenX.genderOutputNormalization(gender)
</code>

### GenX method

<code>
GenX.GenX(text, threshold, pre_label=None)
</code>  

Using GenX method with pre-set *threshold* to identify the gender type from a clinical trial *text*, while *pre_label* is the original gender type on ClinicalTrial.gov eligibility. This value can also not be input in this function.  
e.g.,the *text* "*Biologically male, including male-to-female transgender women*" will be identified as ['Transgender Female', 'Biological Male'] with *threshold* 7.
### GenX method in clinical trials

Using GenX method with a *threshold* to process a list of clinical trials, while the input trial data saved in the file 'clinicaltrial' and output data in the same file.  
*fileIn* is the input csv file which contains a list of clinical trials with their clinical trial ID, original gender type in eligibility, study title, study description and eligibility criteria.  
*fileOut* is the output csv file which contains a list of clinical trials with their clinical trial ID and the gender type annotated by GenX

<code>
processByGenX(fileIn, fileOut, threshold)
</code>

## Citation
Hao T, Chen B, Qu Y. An Automated Method for Gender Information Identification from Clinical Trial Texts[C]// International Conference on Health Information Science. Springer International Publishing, 2016:109-118.

## Contributors
Tianyong Hao  
Boyu Chen