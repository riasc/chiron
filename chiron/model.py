from xgboost import XGBClassifier
#import xgboost as xgb
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
from skopt import BayesSearchCV
from skopt.space import Real, Integer
#import optuna
import shap
import matplotlib.pyplot as plt

# classes
import helper

class Model:
    def __init__(self, df, options):
        # convert target to numeric (forcing errors to NaN)
        df["he_b008_high_cholesterol"] = pd.to_numeric(df["he_b008_high_cholesterol"], errors='coerce')
        # drop rows were target is NaN
        df = df.dropna(subset=["he_b008_high_cholesterol"])

        # separate features and target
        self.X = df.drop("he_b008_high_cholesterol", axis=1)
        self.Y = df["he_b008_high_cholesterol"]

        if options.challenge:
            # if part of challenge, use all data for training
            self.X_train = self.X
            self.Y_train = self.Y
        else:
            # split the data (into training/testing) - 80/20
            self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X,
                                                                                    self.Y,
                                                                                    test_size=0.2,
                                                                                    random_state=42)

        self.best_model = None

    def train(self):
        search_space = {
            "learning_rate": Real(0.01, 0.5, prior="log-uniform"),
            "max_depth": Integer(1,10),
            "n_estimators": Integer(100, 500),
            "subsample": Real(0.6, 1.0),
            "colsample_bytree": Real(0.6, 1.0),
            "gamma": Real(0, 0.5),
            "min_child_weight": Integer(1, 10),
            "reg_alpha": Real(0, 1),
            "reg_lambda": Real(1, 3)
        }

        # Bayesian Optimization
        bayes_search = BayesSearchCV(
            estimator=XGBClassifier(),
            search_spaces=search_space,
            n_iter=150,
            cv=5,
            scoring="roc_auc",
            random_state=42
        )

        bayes_search.fit(self.X_train, self.Y_train)

        # best parameters and score
        self.best_params = bayes_search.best_params_
        self.best_score = bayes_search.best_score_
        self.best_model = bayes_search.best_estimator_

        print(f"{helper.get_current_time()}parameters: {self.best_params}")
        print(f"{helper.get_current_time()}score: {self.best_score:.4f}")

    def predict(self, features):
        if self.best_model:
#            dtest = xgb.DMatrix(features, enable_categorical=True)
            return self.best_model.predict_proba(features)[:,1]
        else:
            raise Exception("Model not trained yet")

    def explain(self):
        if self.best_model:
            explainer = shap.Explainer(self.best_model, self.X_train)
            shap_values = explainer(self.X_test)

            # Create and save summary plot
            plt.figure(figsize=(12, 8))
            shap.summary_plot(shap_values, self.X_test, max_display=20, show=False)
            plt.tight_layout()
            plt.savefig('shap_summary_plot.svg', format="svg", dpi=300, bbox_inches='tight')
            plt.close()

            # Create and save waterfall plot
            plt.figure(figsize=(12, 8))
            shap.plots.waterfall(shap_values[0], show=False)
            plt.tight_layout()
            plt.savefig('shap_waterfall_plot.png', dpi=300, bbox_inches='tight')
            plt.close()

            # Aggregate SHAP values to get feature importance
            shap_values_mean = np.abs(shap_values.values).mean(axis=0)
            feature_importance = pd.DataFrame({
                'Feature': self.X_train.columns,
                'SHAP_mean_abs': shap_values_mean
            })

            # Sort by most affected features
            affected = feature_importance.sort_values(by='SHAP_mean_abs', ascending=False)
            affected.to_csv('affected_features.csv', index=False)
