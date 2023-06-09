# Calculates semantic similarity using Wordnet's Gene Ontology
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import re
import nltk
nltk.data.path.append('nltk_data')

def similarity(X, Y):
    S1 = re.split(r'[ ,.!;"()]', X)
    S2 = re.split(r'[ ,.!;"()]', Y)

    def penn_to_wn(tag):
        """Convert between a Penn Treebank tag to a simplified Wordnet tag"""
        if tag.startswith("N"):
            return "n"

        if tag.startswith("V"):
            return "v"

        if tag.startswith("J"):
            return "a"

        if tag.startswith("R"):
            return "r"

        return None

    def tagged_to_synset(word, tag):
        wn_tag = penn_to_wn(tag)
        if wn_tag is None:
            return None

        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    def sentence_similarity(sentence1, sentence2):
        """compute the sentence similarity using Wordnet"""
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))

        # Get the synsets for the tagged words
        synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
        synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]

        score, count = 0.0,0

        # For each word in the first sentence
        for synset in synsets1:
            # Get the similarity value of the most similar word in the other sentence
            best_score = max([synset.path_similarity(ss) for ss in synsets2])

            # Check that the similarity could have been computed
            if best_score is not None:
                score += best_score
                count += 1

        # Average the values
        print(score)
        print(count)
        score /= count
        return score

    sentences = [
        Y,
    ]

    focus_sentence = X

    for sentence in sentences:
        accu = sentence_similarity(focus_sentence, sentence)
        accu *= 100

    if (not ("not" in S1 and "not" in S2)) and ("not" in S1 or "not" in S2):
        accu = 100 - accu

    return accu


# X = "i am not batman" # fixed i.e teacher
# Y = "i am batman" #trascript

# print("similarity:", similarity(X, Y))
