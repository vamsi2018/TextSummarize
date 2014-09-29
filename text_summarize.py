import sys
import re
class TextSummarize:

    def getStopWords(self):
        f=open(self.stopwordsFile, 'r')
        self.stopWordList=[line.rstrip() for line in f]
        #print self.stopWordList
        f.close()
        
    def __init__(self):
        param = sys.argv
        self.stopwordsFile='stopwords.txt'
        self.getStopWords()
        self.inputFile = param[1]
        #self.inputFile = 'hello.txt'
        #Damping factor
        self.dampingFactor = 0.85
        return
    

    def removeStopwords(self,wordList):
        #print "in removeStopWords"
        #print wordList
        tempWordList = list(wordList)
        for word in tempWordList:
            #print word
            if word in self.stopWordList:
                #print "STOPWORD:"
                #print word
                wordList.remove(word)
        #print wordList
        return wordList

    def stemWordList(self,wordList):
        
        return wordList
    
    def extractSentenceList(self):
        f = open(self.inputFile,'r')
        text = ''
        sentenceList = []
        for line in f:
            #print line
            text = text+line.lower()
        text = text.replace('\n',' ')
        sentenceList = re.split("\.\s",text)
##        for sentence in text.split('.'):
##            sentence = sentence.strip()
##            sentence.replace('\n','')
##            #print line
##            if len(sentence) != 0:
##                sentenceList.append(sentence)
        return sentenceList
    
    def processSentences(self):
        self.sentenceList = self.extractSentenceList()
        wordList = []
        self.list_sentenceSet=[]
        for line in self.sentenceList:
            wordList = line.split()
            wordList = self.removeStopwords(wordList)
            wordList = self.stemWordList(wordList)
            self.list_sentenceSet.append(set(wordList))
        #print self.list_sentenceSet
        setLength = len(self.list_sentenceSet)
        #for i in range(setLength):
            #print len(self.list_sentenceSet[i])
            #print self.list_sentenceSet[i]
        self.similarityMatrix = [[0 for j in range(setLength)] for i in range(setLength)]
        for i in range(setLength):
            for j in range(setLength):
                try:
                    self.similarityMatrix[i][j] = float(len(self.list_sentenceSet[i]&self.list_sentenceSet[j]))/(len(self.list_sentenceSet[i])+len(self.list_sentenceSet[j]))
                except:
                    self.similarityMatrix[i][j] = 0.0
        #self.similarityMatrix = [[float(len(self.list_sentenceSet[i]&self.list_sentenceSet[j]))/(len(self.list_sentenceSet[i])+len(self.list_sentenceSet[j])) for j in range(setLength)] for i in range(setLength)]
##        print self.similarityMatrix
        
    def calculateScore(self,nodeIndex):
        sum = 0.0
        setLength = len(self.list_sentenceSet)
        for i in range(setLength):
            if ((self.similarityMatrix[i][nodeIndex] > 0)&(i != nodeIndex)):
                denom = 0.0
                for out in range(setLength):
                    denom += self.similarityMatrix[i][out]
                if denom != 0:
                    sum += self.similarityMatrix[i][nodeIndex]*self.score[i]/denom
                
        self.score[nodeIndex] = (1-self.dampingFactor) + self.dampingFactor*sum
        
    def initializeScore(self):
        setLength = len(self.list_sentenceSet)
        self.score = [1 for i in range(setLength)]
        #for i in range(setLength):
        #    self.score.append()
    def printSummary(self):
        self.sortedsentenceDict = dict(zip(range(len(self.score)),self.score))
        sortedKeys = sorted(self.sortedsentenceDict.keys(),key = self.sortKeyFun,reverse=True)
        for i in sortedKeys:
            print self.sortedsentenceDict[i]
            print self.sentenceList[i]
        return
    def sortKeyFun(self,index):
        return self.sortedsentenceDict[index]
    def main(self):
        self.processSentences()
        self.initializeScore()
        setLength = len(self.list_sentenceSet)
        for j in range(30):
            for i in range(setLength):
                self.calculateScore(i)
            #print self.score
        self.printSummary()

if __name__ == '__main__':
    obj = TextSummarize()
    obj.main()

