from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
# from skopt import BayesSearchCV
# from skopt.space import Real, Integer
import optuna



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

    def objective(self, trial):
        params = {
            "objective": "binary:logistic",
            "eval_metric": "auc",
            "booster": "gbtree",
            "lambda": trial.suggest_float("lambda", 1e-3, 1.0),
            "alpha": trial.suggest_float("alpha", 1e-3, 1.0),
            "subsample": trial.suggest_float("subsample", 0.4, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
            "max_depth": trial.suggest_int("max_depth", 3, 15),
            "eta": trial.suggest_float("eta", 1e-3, 1.0),
            "n_estimators": trial.suggest_int("n_estimators", 100, 2000),
            "gamma": trial.suggest_float("gamma", 1e-3, 5),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 20),
            "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1, 20),
            "max_bin": trial.suggest_int("max_bin", 10, 500),
            "grow_policy": trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])
        }

        model = XGBClassifier(**params)
        model.fit(self.X_train, self.Y_train)
        preds = model.predict(self.X_test)
        # accuracy = accuracy_score(self.Y_test, preds)
        # return accuracy
        auc = roc_auc_score(self.Y_test, preds)
        return auc


    def train(self):
        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=1000)

        self.best_params = study.best_params
        self.best_score = study.best_value
        self.best_model = XGBClassifier(**self.best_params)
        self.best_model.fit(self.X_train, self.Y_train)

        print(f"Best parameters: {self.best_params}")
        print(f"Best score: {self.best_score:.2f}")

        # search_space = {
        #     "learning_rate": Real(0.01, 0.5, prior="log-uniform"),
        #     "max_depth": Integer(1,10),
        #     "n_estimators": Integer(100, 500)
        # }

        # # Bayesian Optimization
        # bayes_search = BayesSearchCV(
        #     estimator=XGBClassifier(),
        #     search_spaces=search_space,
        #     n_iter=50,
        #     cv=5,
        #     scoring='accuracy',
        #     random_state=42
        # )



        # bayes_search.fit(self.X_train, self.Y_train)

        # # best parameters and score
        # self.best_params = bayes_search.best_params_
        # self.best_score = bayes_search.best_score_
        # self.best_model = bayes_search.best_estimator_

        # print(f"Best parameters: {self.best_params}")
        # print(f"Best score: {self.best_score:.2f}")

        # # tune hyperparameters
        # param_grid = {
        #     'learning_rate': [0.1, 0.2, 0.3],
        #     'max_depth': [3, 4, 5],
        #     'n_estimators': [100, 200, 300]
        # }

        # # grid search
        # grid_search = GridSearchCV(estimator=XGBClassifier(),
        #     param_grid=param_grid,
        #     cv=5,
        #     scoring='accuracy')

        # # fit the grid search
        # grid_search.fit(self.X_train, self.Y_train)

        # # best parameters
        # self.best_params = grid_search.best_params_
        # self.best_score = grid_search.best_score_
        # self.best_model = grid_search.best_estimator_


    def predict(self, features):
        if self.best_model:
            return self.best_model.predict_proba(features)
        else:
            raise Exception("Model not trained yet")
