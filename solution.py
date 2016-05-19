from collections import Counter
import gzip
import math
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
import matplotlib; matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

PREPOSITIONS = ['about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'as', 'at', 'atop',
                'before', 'behind', 'below', 'beneath', 'between', 'beyond', 'by', 'down', 'during', 'for', 'from',
                'in', 'inside', 'into', 'like', 'of', 'off', 'on', 'onto', 'out', 'outside', 'over', 'since', 'through',
                'till', 'to', 'toward', 'under', 'until', 'up', 'upon', 'with', 'within']
MAX_NGRAM_RANK = 5


def solution():
    print '...reading data...'
    with gzip.open('sentences.txt.gz') as fin:
        sentences = [l.rstrip('\r\n').split(' ') for l in fin]
    print 'sentences:'
    print '\n'.join(' '.join(s) for s in sentences[0:3])
    print

    ngrams = {}
    with gzip.open('ngrams.txt.gz') as fin:
        for l in fin:
            fields = l.split('\t')
            ngrams[fields[0]] = int(fields[1])
    print 'ngrams:'
    print '\n'.join(k + '\t' + str(v) for k, v in ngrams.items()[0:3])
    print

    print '...generating features...'
    x = []
    y = []
    for sentence in sentences:
        for j in xrange(len(sentence)):
            if sentence[j] in PREPOSITIONS:
                # features for j-th word that is a preposition
                x_row = []
                for prep in PREPOSITIONS:
                    for rank in xrange(2, MAX_NGRAM_RANK + 1):
                        for k in xrange(rank):
                            # k-th n-gram of chosen rank containing j-th word
                            end = j + 1 + k
                            start = end - rank
                            if 0 <= start and end <= len(sentence):
                                ngram = ' '.join(sentence[start:j] + [prep] + sentence[j + 1:end])
                                # add one smoothing to avoid infinity
                                x_row.append(math.log(ngrams.get(ngram, 0) + 1))
                            else:
                                # n-gram spans out of the sentence
                                x_row.append(0)
                x.append(x_row)
                y.append(sentence[j])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)
    print 'train data:'
    print '\n'.join(y + '\t' + ' '.join(str(x1) for x1 in x) for x, y in zip(x_train, y_train)[0:3])
    print

    print '...training...'
    # creating linear SVM classifier model
    model = LinearSVC(random_state=1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    print 'accuracy = %.1f%%' % (accuracy_score(y_test, y_pred) * 100)
    print 'most common preposition = %.1f%%' % (Counter(y_test).most_common(1)[0][1] * 100. / len(y_test))


if __name__ == '__main__':
    solution()
