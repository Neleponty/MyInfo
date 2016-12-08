def forEachNgramm(ngramm):
    words = ngramm[0][1]
    self = ngramm[1]
    for word in words:
        alreadyExistWord = self.parsed_words.get(word)
        if alreadyExistWord is None:
            self.parsed_words.update([(word, self.analyzer.parse(word)[0].tag,)])
