txt = """Mis-spelled version
The brife timpeline of Natuural Langauge Processing (NLP)
The 1950s saww the birth of NLP, fuueled by intrest in machince translation and the developemnt of the Turing teest, a teest of a machince’s abiliity to exhibbit intelligent behaviour equivallent to, or indistinguishablle from, that of a human. In the feild of linguistics, Noam Chomsky's book "Syntactic Structures" proposed a theory of universaal grammar, laying the groundwoork for rul-based approachess to NLP.
The 1960s saw the developemnt of ELIZA, an early chatbot program that simulated conversasion with a psychotherapist. Also in the 1960s, the Automatic Languaghe Processing Advisory Committee (ALPAC) report recommeended a shifft in focus from rul-based to statiistical methods in NLP.
The 1970s saw researrch into case grammars, which analyzse the rolles of words in sentencēs, and semantic networks, which represent knowledgve as linked nodess. The 1970s also saw the developemnt of experrt systems, which use knowledgge basses to solve speficic problems. MYCIN, a medical diagnosis sysstem, is a famouss example of an experrt system.
The 1980s were an era of “AI Winter,” a periiod of declining funding and intrest in artificial intelligience researrch. Howeveer, NLP researrch continued, with a shifft towards statiistical methods. This era saw the developemnt of n-grams, which are sequencēs of words used to statiistically analize text.
The 1990s saw the rise of statiistical languaghe modeling, which usess statiistical methods to predictt the nexst word in a sequencē. This decaade also saw the developemnt of machince learning algorithms likke neural networks, which would become increasingly important in NLP in the yeerrs to come.
Since 2000, NLP has been transformd by the rise of machince learning and powerful computers. Statiistical methods likke n-grams and machince learning algorithms likke neural networks have become more sophisicated and more widely used. Notably, recurrent neural networks (RNNs) and Long Short-Term Memory (LSTM) networks have been particularly successful in NLP tasks becausse they can handlle sequenciall data like languaghe.
Also sincē 2000, there has been a rise in large languaghe models (LLMs), which are trained on massiive amounts of text data. LLMs are capabble of generating human-quality text, translating languaghes, writing different kinds of creativve content, and answering your quesstions in an informativve way."""



from termcolor import colored


import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



lines = txt.split('\n')


# รายการคำที่สร้างใหม่ โดยเช็กคำถูกผิดแล้ว
textList = []

# ข้อมูลใหม่สำหรับไฟล์
new_txt = []


numberOfIncorrect = 0; # จำนวนคำผิด
arrayToTable = []; # => เก็บข้อมูลเป็น subArray ที่ subArray จะสื่อถึงแต่ละบรรทัดของตาราง
wordSequence = 0; # นับไปทีละคำ เพื่อไว้ใช้ดูว่า คำผิดคือคำที่เท่าไหร่

number = 1
arrayToTable.append(["Number", "Sentence Number", "Position" , "Incorrect Word" , "Correct Word"])

for i in range(len(lines)):
# for line in lines:
    oneLine = lines[i].split(' ');
    # print(oneLine)
    for oneWord in oneLine:
        wordSequence += 1; # บวกไปทีละคำแบบ Bruth Force
        oneWord = oneWord.strip();
        # oneWord คือแยกเป็นคำแล้วใน 1 บรรทัด
        cleanWord = oneWord.replace('.', '');
        cleanWord = cleanWord.replace(',', '')
        cleanWord = cleanWord.replace('"', '')
        isCorrect = correction(cleanWord);
        if (cleanWord != isCorrect):
            numberOfIncorrect+=1;
            # print("คำคือ ", oneWord , "แก้เป็น : ", correction(oneWord) , '\n');
            # คำผิดก็ใส่
            textList.append(colored(isCorrect, 'red'))
            # ไฮไลท์คือคำที่โดนแก้
            arrayToTable.append([number ,i , wordSequence , cleanWord ,isCorrect]) # arrayToTable ก็จะมี oneWord คือคำที่โดนแก้
            number+=1;
        else:
            # กรณีคำถูกก็ใส่
            textList.append(oneWord)
    new_txt.append(textList)
    textList = []

endText = ""
for oneArray in new_txt:
    endText += " ".join(oneArray)
    endText += "\n";
# แสดงข้อความใหม่ที่ถูกแก้
print(endText)


print(len(arrayToTable))
for cat in arrayToTable:
    print(cat)




# กำหนดความกว้างของแต่ละคอลัมน์
col_widths = [max(len(str(item)) for item in col) for col in zip(*arrayToTable)]

for row in arrayToTable:
    print(" | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row)))


# pip install termcolor
