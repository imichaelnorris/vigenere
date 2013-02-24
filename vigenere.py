import string
import rpy2
import rpy2.robjects as robjects
r = robjects.r
r.png('barplot-digram-21-d.png')
c = r.c
plot = r.plot
boxplot = r.boxplot
barplot = r.barplot
hist = r.hist
IntVector = robjects.IntVector

#simple form of polyalphabetic substitution

#note that there are some magic numbers in here, for instance my hardcoding 
#of the number of letters in the key

def kasiskiTest(frequent_trigrams, trigrams):
    testTrigram = trigrams[frequent_trigrams[0][1]] 
    return [testTrigram[i] - testTrigram[i-1] for i in range(1, len(testTrigram))]

def letterConvert(c):
    '''convert a letter to a number'''
    for i in range(0, 26):
        if c == string.ascii_uppercase[i]:
            return i

def numberConvert(i):
    return string.ascii_uppercase[i]

f = open('hw1-21-d.txt')
text = f.readline()
text = text[0:-1]
f.close()

frequency = {}
for i in text:
    try:
        frequency[i] += 1
    except:
        frequency[i] = 1

frequencyArr = []
#[frequency[j] for j in string.ascii_uppercase]
for i in string.ascii_uppercase:
    try:
        frequencyArr.append(frequency[i])
    except: #frequency for this letter not found
        frequencyArr.append(0)


#barplot(IntVector(frequencyArr), names=[i for i in string.ascii_uppercase])


digrams = {}
for i in range(0, len(text) - 1):
    try:
        digrams[text[i] + text[i+1]].append(i)
    except:
        digrams[text[i] + text[i+1]] = [i]

trigrams = {}
for i in range(0, len(text) - 2):
    try:
        trigrams[text[i] + text[i+1] + text[i+2]].append(i)
    except:
        trigrams[text[i] + text[i+1] + text[i+2]] = [i]

digram_list = [(len(digrams[i]), i) for i in digrams]
trigram_list = [(len(trigrams[i]), i)  for i in trigrams]
digram_list.sort()
trigram_list.sort()
digram_list.reverse()
trigram_list.reverse()

frequent_digrams = [i for i in digram_list if i[0] > 3]
frequent_trigrams = [i for i in trigram_list if i[0] > 1]

digram_vals = [i[0] for i in frequent_digrams]
digram_names = [i[1] for i in frequent_digrams]
trigram_vals = [i[0] for i in frequent_trigrams]
trigram_names = [i[1] for i in frequent_trigrams]


#print(frequent_digrams)
#print(frequent_trigrams)

#barplot(IntVector(digram_vals), names=digram_names)
#barplot(IntVector(trigram_vals), names=trigram_names)

#mappings = [('F', 'w'), ('C', 'e')]
#print(decode(text, mappings))

#krasiskiTest(frequent_trigrams, trigrams)

#def decrypt(textArr, a, b):
#    return "".join( [numberConvert((textArr[i] - b) * a % 26) for i in range(0, len(textArr))])

def decrypt(textArr, key):
    '''decrypt the text using a vigenere cipher decryption function. textArr should be an array of integers and key should be an array of integers.  It returns a string'''
    integers = [(textArr[i] - key[i % len(key)]) % 26 for i in range(0, len(textArr))]
    return "".join([numberConvert(i) for i in integers])


textArr = []
for i in text:
    textArr.append(letterConvert(i))

m = 6
#keyFrequency is how many times the number appears
keyFrequency = [{} for i in range(0, m)]
n = len(textArr)
#m = 7
nprime = float(n) // m

#probability of each letter
p = [.082, .015, .028, .043, .127, .022, .020, .061, .070, .002, .008, .040,
     .024, .067, .075, .019, .001, .060, .063, .091, .028, .010, .023, .001,
     .020, .001]

for i in range(0, len(textArr)):
    try:
        keyFrequency[i % m][textArr[i]] += 1
    except:
        keyFrequency[i % m][textArr[i]] = 1

letterFrequency = [[] for i in range(0, m)]

for i in range(0, m):
    for j in range(0, 26):
        try:
            letterFrequency[i].append(keyFrequency[i][j])
        except:
            letterFrequency[i].append(0)

#these are the probabilities of A-k0, B-k0, ...
letterProbabilities = [[letterFrequency[i][j] / nprime for j in range(0, 26)] for i in range(0, m)]

M = [[] for i in range(0, m)]


#computing dot product over measured probability and "english probability
# for each letter.  for each letter, we must shift the english probability by 
#the amount of shift corresponding to that letter, 0 for A, 1 for B, etc.
for i in range(0, m):
    for j in range(0, 26): #j is how much p is shifted by
        M[i].append((sum([letterProbabilities[i][k] * p[(k - j) % 26] for k in range(0, 26)]), numberConvert(j)))

for i in M:
    i.sort()
    i.reverse()

keyGuess = ""
for i in M:
    keyGuess += i[0][1]

print(keyGuess)
key = [letterConvert(i) for i in keyGuess]
print(decrypt(textArr, key))


#print(sum([letterProbabilities[0][i] * p[i - 2] for i in range(0, 26)]))


'''
M = [[] for i in range(0, m)]

for i in range(0, m):
    for j in range(0, 26):
        temp = 0
        for k in range(0, 26): #i in the equation 1.1 on page 35
            try:
                temp += p[k] * (keyFrequency[i][k] / nprime) + j
                temp /= nprime
            except:
                temp += float(j)
                temp /= nprime
        M[i].append(temp)



#key = ['C', 'R', 'Y', 'P', 'T', 'O']

#key = [letterConvert(i) for i in key]

'''
