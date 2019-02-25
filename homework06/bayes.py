from collections import Counter
import math


class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.model = {
            'number_watch_of_label': {},
            'likelihood_of_label': {},
            'words_likelihood': {},
        }

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        lst = []
        for sentence, labels in zip(X, y):
            for word in sentence.split():
                lst.append((word, labels))
        self.words_labels = Counter(lst)
        self.possible_labels = dict(Counter(y))
        words = [word for sentence in X for word in sentence.split()]
        self.possible_words = dict(Counter(words))
        for label in self.possible_labels:
            count = 0
            for word, label_item in self.words_labels:
                if label == label_item:
                    count += self.words_labels[(word, label)]
            self.model['number_watch_of_label'][label] = count
            self.model['likelihood_of_label'][label] = self.possible_labels[label] / len(y)
        for word in self.possible_words:
            word_likelihood = {}
            for label in self.possible_labels:
                word_likelihood[label] = self.smoothing_likelihood(word, label)
            self.model['words_likelihood'][word] = word_likelihood

    def smoothing_likelihood(self, word, label):
        """ Returns the smoothed likelihood with the given word and label in loop. """
        nc = self.model['number_watch_of_label'][label]
        nic = self.words_labels.get((word, label), 0)
        alpha = self.alpha
        d = len(self.possible_words)
        return (nic + alpha) / (nc + alpha * d)

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        results = []
        for sentence in x:
            labels_likelihood = []
            words = sentence.split()
            for label in self.possible_labels:
                sum = math.log(self.model['likelihood_of_label'][label], math.e)
                for word in words:
                    word_likeliholds = self.model['words_likelihood'].get(word, None)
                    if word_likeliholds is not None:
                       word_likelihold = word_likeliholds[label]
                       sum += math.log(word_likelihold, math.e)
                labels_likelihood.append((sum, label))
            _, result = max(labels_likelihood)
            results.append(result)
        return results

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        correct_predict = 0
        predicts = len(y_test)
        for item, result in enumerate(self.predict(X_test)):
            if result == y_test[item]:
                correct_predict += 1
        return correct_predict/predicts
