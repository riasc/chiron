from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd


class Model:
    def __init__(self, df):
        # convert target to numeric (forcing errors to NaN)
        df[df.columns[-1]] = pd.to_numeric(df[df.columns[-1]], errors='coerce')
        # drop rows were target is NaN
        df = df.dropna(subset=[df.columns[-1]])

        # separate features and target
        self.X = df.drop(df.columns[-1], axis=1)
        self.Y = df[df.columns[-1]]

        # split the data (into training/testing) - 80/20
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X,
                                                                                self.Y,
                                                                                test_size=0.2,
                                                                                random_state=42)

        self.best_model = None


    def train(self):
        # tune hyperparameters
        param_grid = {
            'learning_rate': [0.1, 0.2, 0.3],
            'max_depth': [3, 4, 5],
            'n_estimators': [100, 200, 300]
        }

        # grid search
        grid_search = GridSearchCV(estimator=XGBClassifier(),
            param_grid=param_grid,
            cv=5,
            scoring='accuracy')

        # fit the grid search
        grid_search.fit(self.X_train, self.Y_train)

        # best parameters
        self.best_params = grid_search.best_params_
        self.best_score = grid_search.best_score_
        self.best_model = grid_search.best_estimator_

        print(f"Best parameters: {self.best_params}")
        print(f"Best score: {self.best_score:.2f}")

    def predict(self, features):
        if self.best_model:
            return self.best_model.predict_proba(features)
        else:
            raise Exception("Model not trained yet")
