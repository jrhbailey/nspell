#! /usr/bin/python
# make executable and run as ./nspell.py word1 word2

# From: http://norvig.com/spell-correct.html
import re
import collections as coll
import sys

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = coll.defaultdict(lambda:1)
    for f in features:
        model[f] += 1
    return model

g_nwords = None
def known(words):
    #print g_nwords
    return set(w for w in words if w in g_nwords)

# no param: use disk file
def setup_dict(text = None):
    global g_nwords
    if text == None:
        g_nwords = train(words(file("data/bigspell.txt").read()))
    else:
        g_nwords = train(words(text))

# allow garbage collection to unload
def unload_dict():
    global g_nwords
    g_nwords = None

g_alpha = "abcdefghijklmnopqrstuvwxyz"    
def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces   = [a + c + b[1:] for a,b in splits for c in g_alpha if b]
    inserts    = [a + c + b for a,b in splits for c in g_alpha]
    return set(deletes + transposes + replaces + inserts)
    #return set(deletes + transposes)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in g_nwords)

def correct(word):
    lword = word.lower()
    candidates = known([lword]) or known(edits1(lword)) or known_edits2(lword) or None

    if candidates == None:
        print "%s: - Unknown word" % (word)
        return
            
    if len(candidates) == 1:
        nwd = candidates.pop()
        if lword == nwd:
            print "%s: - Correct" % (word)
        else:
            print "%s: - Incorrect --> %s" % (word, nwd)
        return

    #print candidates
    print "%s: - Incorrect -" % (word)
    scandi = sorted(candidates, key=g_nwords.get, reverse=True)
    for scan in scandi:
        print "  :--> " + scan

def spell_check(wd_lst):
    print "\nChecking - " + str(wd_lst)
    setup_dict()
    for wd in wd_lst:
        correct(wd)
    unload_dict()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: spells.py word1 [word2...]"
        exit

    spell_check(sys.argv[1:])


# Test
# python spell2.py None kdiekkdjdddkd gaurd htis Canidates fuor
