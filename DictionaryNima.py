input_count = int(input())
NimasDictionary = {}
for i in range(input_count):
    Word = input()
    WordList = Word.split()
    for j in range(len(WordList)):
        if j != 0:
            NimasDictionary[WordList[j]] = WordList[0]
Sentence = input()
TranslatedSentence = []
SentenceList = Sentence.split()

for words in SentenceList:
    if words in NimasDictionary:
        TranslatedSentence.append(NimasDictionary[words] + " ")
    else:
        TranslatedSentence.append(words + " ")
print("".join(TranslatedSentence))