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
    def __init__(self, df):
        # convert target to numeric (forcing errors to NaN)
        df["he_b008_high_cholesterol"] = pd.to_numeric(df["he_b008_high_cholesterol"], errors='coerce')
        # drop rows were target is NaN
        df = df.dropna(subset=["he_b008_high_cholesterol"])

        # separate features and target
        self.X = df.drop("he_b008_high_cholesterol", axis=1)
        self.Y = df["he_b008_high_cholesterol"]

        # split the data (into training/testing) - 80/20
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X,
                                                                                self.Y,
                                                                                test_size=0.2,
                                                                                random_state=42)

        # self.X_train = xgb.DMatrix(self.X_train, label=self.Y_train, enable_categorical=True)
        # self.X_test = xgb.DMatrix(self.X_test, label=self.Y_test, enable_categorical=True)

        self.best_model = None

    # def objective(self, trial):
    #     params = {
    #         "objective": "binary:logistic",
    #         "eval_metric": "auc",
    #         "booster": "gbtree",
    #         "lambda": trial.suggest_float("lambda", 1e-3, 1.0, log=True), "alpha": trial.suggest_float("alpha", 1e-3, 1.0, log=True), "subsample": trial.suggest_float("subsample", 0.4, 1.0), "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
    #         "max_depth": trial.suggest_int("max_depth", 3, 15),
    #         "eta": trial.suggest_float("eta", 1e-3, 1.0, log=True),
    #         "gamma": trial.suggest_float("gamma", 1e-3, 5, log=True),
    #         "min_child_weight": trial.suggest_int("min_child_weight", 1, 20),
    #         "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1, 20),
    #         "max_bin": trial.suggest_int("max_bin", 10, 500),
    #         "grow_policy": trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"]),
    #     }

    #     model = XGBClassifier(**params, use_label_encoder=False)
    #     model.fit(self.X_train, self.Y_train)
    #     preds = model.predict(self.X_test)

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

        print(f"{helper.get_current_time()} parameters: {self.best_params}")
        print(f"{helper.get_current_time()} score: {self.best_score:.4f}")

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

            # shap.summary_plot(shap_values, self.X_test, max_display=50)
            # shap.plots.waterfall(shap_values[0])

             # Create and save summary plot
            plt.figure(figsize=(12, 8))
            shap.summary_plot(shap_values, self.X_test, max_display=100, show=False)
            plt.tight_layout()
            plt.savefig('shap_summary_plot.png', dpi=300, bbox_inches='tight')
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
            most_affected = feature_importance.sort_values(by='SHAP_mean_abs', ascending=False)
            least_affected = feature_importance.sort_values(by='SHAP_mean_abs', ascending=True)

            # Save most affected features to file
            most_affected.to_csv('most_affected_features.csv', index=False)

            # Save least affected features to file
            least_affected.to_csv('least_affected_features.csv', index=False)





#     def objective(self, trial):
#         params = {
#             "objective": "binary:logistic",
#             "eval_metric": "auc",
#             "booster": "gbtree",
#             "lambda": trial.suggest_float("lambda", 1e-3, 1.0),
#             "alpha": trial.suggest_float("alpha", 1e-3, 1.0),
#             "subsample": trial.suggest_float("subsample", 0.4, 1.0),
#             "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
#             "max_depth": trial.suggest_int("max_depth", 3, 15),
#             "eta": trial.suggest_float("eta", 1e-3, 1.0),
# #            "n_estimators": trial.suggest_int("n_estimators", 100, 2000),
#             "gamma": trial.suggest_float("gamma", 1e-3, 5),
#             "min_child_weight": trial.suggest_int("min_child_weight", 1, 20),
#             "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1, 20),
#             "max_bin": trial.suggest_int("max_bin", 10, 500),
#             "grow_policy": trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"]),
#         }

#         # Convert to DMatrix with enable_categorical
#         # dtrain = xgb.DMatrix(self.X_train, label=self.Y_train, enable_categorical=True)
#         # dtest = xgb.DMatrix(self.X_test, label=self.Y_test, enable_categorical=True)

#         # model = xgb.train(params, dtrain, num_boost_round=100)
#         # preds_proba = model.predict(dtest)
#         model = XGBClassifier(**params)
#         model.fit(self.X_train, self.Y_train)
#         preds = model.predict(self.X_test)
#         auc = roc_auc_score(self.Y_test, preds)
#         return auc


        # model = XGBClassifier(**params)
        # model.fit(self.X_train, self.Y_train)
        # preds = model.predict(self.X_test)
        # # accuracy = accuracy_score(self.Y_test, preds)
        # # return accuracy
        # auc = roc_auc_score(self.Y_test, preds)
        # return auc


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



        # study = optuna.create_study(direction="maximize")
        # study.optimize(self.objective, n_trials=1000)

        # self.best_params = study.best_params
        # self.best_score = study.best_value

        # # xgb.config_context(verbosity=0)

        # # Train the final model with the best parameters
        # # dtrain = xgb.DMatrix(self.X_train, label=self.Y_train, enable_categorical=True)
        # # self.best_model = xgb.train(self.best_params, dtrain, num_boost_round=100)


        # self.best_model = XGBClassifier(**self.best_params)
        # self.best_model.fit(self.X_train, self.Y_train)

        # print(f"Best parameters: {self.best_params}")
        # print(f"Best score: {self.best_score:.2f}")
