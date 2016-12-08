import math
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import numpy



# расстояние левенштейна - > the same as normal_form
# def levenstainDistance(self,term,term2):
# если {W} - попарно независимы,то p(w|wi) = p(w)*p(wi)
# если {W} - совместно независимы,то p(w|W) = p(w1)*p(w2)....p(wn)
def twogrammAnalys(ngramm_counter, documents):
    counted = CountVectorizer()
    garbage = counted.fit_transform(documents)
    diction = ngramm_counter.vocabulary_
    words_twoplix = diction.keys()
    probability = {}
    d = sum(diction.values())
    c = (numpy.sum(garbage))

    # Частотный метод
    for wordset in words_twoplix:
        count_of_set = diction[wordset]
        words_prob = []
        posterior_distrib = count_of_set / d

        # p(w)
        for word in wordset.split():
            # Есть совпадение
            word_count = counted.vocabulary_.get(word)
            word_probability = word_count / c
            words_prob.append(word_probability)
        apriorDistrib = 0

        for item in words_prob:
            apriorDistrib *= item
            #
            # Student's t-statistic
            #    t_stat_dividor = math.sqrt(1/len(words_twoplix))
        t_stat = math.log2(apriorDistrib / posterior_distrib)
        probability.update([(wordset, t_stat), ])

    # Word_probability
    return probability
