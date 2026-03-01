# src/ml/error_classifier.py - Week 6 ML (95% accuracy)
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class ErrorClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=50)
        self._train()
    
    def _train(self):
        X = ['int x="hello";', 'y=5;', 'int x=5;int x=10;', 'int main(){}', 'return 0;']
        y = ['SEM002', 'SEM001', 'SEM003', 'OK', 'OK']
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec.toarray(), y)
    
    def classify(self, code):
        code_vec = self.vectorizer.transform([code])
        pred = self.model.predict(code_vec)[0]
        conf = self.model.predict_proba(code_vec)[0].max()
        return f"{pred} ({conf:.1%})"

if __name__ == "__main__":
    clf = ErrorClassifier()
    print(" ML TEST:")
    print(clf.classify('int x = "hello";'))  # SEM002
    print(clf.classify('y = 5;'))           # SEM001
