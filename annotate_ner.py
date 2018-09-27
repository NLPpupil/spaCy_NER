'''
用于为训练spacy命名体识别模型标记数据。输入分词后的文本文件，输入标记spacy所需格式的标记数据。

用法：
python annotate.py text.txt.tok
命令行会打印形如：

第1句: 
美国 0
癌症 1
治疗 2
公司 3
RiMO 4
的 5
新型 6
“ 7
放疗 8
放射 9
动态 10
治疗 11
” 12
( 13
RTRDT 14
) 15
技术 16
是 17
全球 18
首创 19
的 20
高效 21
、 22
低毒 23
的 24
具有 25
革命性 26
的 27
癌症 28
治疗 29
技术 30
。 31

对某个实体，在命令行输入起始坐标和类别，以空格分隔，cate_map指定了实体类别和标记时用的简称，每标记一个实体按下回车，例如：

4 o
8 11 t
14 t
28 z

此句标记完成后，在命令行输入f进入下一句。如果想要撤回某个词的标记，输入r。

标记若干句后，ctrl+c终止程序。会产生一个text.txt.tok.annotation文件，将这个文件改名后放入某个文件夹备份。
'''
import sys 

filename = sys.argv[1]

cate_map = {'p':'PERSON',\
            'o':'ORG',\
            'l':'DOMAIN',\
            'z':'SYMPTOM',\
            'y':'DRUG',\
            'e':'EQUIP',\
            't':'TECH',\
            'c':'PRODUCT',\
            }

def char_range(tokens,ids):
    start = ids[0]
    end = ids[-1]
    previous_toknes = tokens[:start]
    range_start = len(' '.join(previous_toknes)) + 1
    range_end = range_start + len(' '.join(tokens[start:end+1])) 

    return range_start,range_end


def valid_inputs(inputs,sent_length):
    try:
        if not inputs:
            print ('Empty Inputs,Try Again')
            return False
        for i in inputs[:-1]:
            if not type(eval(i))==int:
                print ('Leading Inputs Must be Integers,Try Again')
                return False
            elif int(i) >= sent_length:
                print ('Token Index Out of Sentence Length,Try Again')
                return False

        if inputs[-1] in cate_map.keys():
            return True
        else:
            print (str(cate_map)+', Try Again')
            return False
    except NameError:
        print ('Invalid Inputs,Try Again')
        return False




with open(filename) as f,open(filename + '.annotation','w') as out:
    anntation_num = 0
    drop_num = 0
    try :
        for i,line in enumerate(f):
            tokens = line.split()
            tokens_with_ids = list(zip(tokens,range(len(tokens))))
            tokens_with_ids = [t[0]+' '+str(t[1]) for t in tokens_with_ids]
            finish = False
            print ('第{0}句: '.format(i+1))
            for t in tokens_with_ids:
                print (t)
            entities = []
            while not finish:
                inputs = input()
                if inputs == 'f':
                    if entities:
                        print ('标记第{0}句'.format(i+1))
                        print ('#'*100+'\n\n')
                        anntation_num += 1
                        out.write(str((line.strip(),{'entities':entities}))+'\n')
                    else:
                        print ('丢弃第{0}句'.format(i+1))
                        print ('#'*100+'\n\n')
                        drop_num += 1
                    finish = True
                elif inputs == 'r':
                    if entities:
                        print ('撤回，删除上一个标记。')
                        entities.pop()
                    else:
                        print ('标记序列为空，无法继续撤回。')
                elif not valid_inputs(inputs.split(),len(tokens)):
                    pass
                else:
                    inputs = inputs.split()
                    ids = [int(i) for i in inputs[:-1]]
                    category = inputs[-1]
                    start,end = char_range(tokens,ids)
                    entities.append((start,end,cate_map[category]))
    except KeyboardInterrupt:
        print ('标记结束。共标记{0}句，丢弃{1}句。'.format(anntation_num,drop_num))

