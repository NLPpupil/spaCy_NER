'''
命令行输入文本文件，输出命名体识别结果。
load中的模型可以自己指定，只需将模型的路径填入。

例如：
python spacyner.py text.txt
'''

import sys 
import spacy 

nlp = spacy.load('en_core_web_lg')
filename = sys.argv[1]

with open(filename) as f:
    with open(filename+'.spacyners','w') as out:
	    for line in f:
	        doc = nlp(line.strip())
	        entities = [(ent.text,ent.label_) for ent in doc.ents]
	        out.write(str(entities)+'\n')
	        

