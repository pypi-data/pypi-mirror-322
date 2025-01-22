import numpy as np
from sklearn.linear_model import (LogisticRegression, LinearRegression, PoissonRegressor,
                                  Ridge, Lasso, ElasticNet, BayesianRidge,
                                  SGDRegressor, PassiveAggressiveRegressor, HuberRegressor,
                                  RANSACRegressor, TheilSenRegressor, OrthogonalMatchingPursuit)
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import bukmacherska as bk
import matplotlib.pyplot as plt

# Funkcja trenowania modeli
def train_models(X_train, y_train):
    models = {}

    # Modele regresji
    models['log_reg'] = LogisticRegression().fit(X_train, y_train)
    models['lin_reg'] = LinearRegression().fit(X_train, y_train)
    models['poisson_reg'] = PoissonRegressor().fit(X_train, y_train)
    models['ridge'] = Ridge().fit(X_train, y_train)
    models['lasso'] = Lasso().fit(X_train, y_train)
    models['elastic_net'] = ElasticNet().fit(X_train, y_train)
    models['bayesian_ridge'] = BayesianRidge().fit(X_train, y_train)
    models['sgd'] = SGDRegressor().fit(X_train, y_train)
    models['passive_aggressive'] = PassiveAggressiveRegressor().fit(X_train, y_train)
    models['huber'] = HuberRegressor().fit(X_train, y_train)
    models['ransac'] = RANSACRegressor().fit(X_train, y_train)
    models['theil_sen'] = TheilSenRegressor().fit(X_train, y_train)
    models['omp'] = OrthogonalMatchingPursuit().fit(X_train, y_train)
    models['quantile'] = make_pipeline(PolynomialFeatures(degree=2), LinearRegression()).fit(X_train, y_train)
    
    # Modele klasyfikacji
    models['rf_clf'] = RandomForestClassifier().fit(X_train, y_train)
    models['grad_boost'] = GradientBoostingClassifier().fit(X_train, y_train)
    models['adaboost'] = AdaBoostClassifier().fit(X_train, y_train)
    models['extra_trees'] = ExtraTreesClassifier().fit(X_train, y_train)
    models['svm_clf'] = SVC().fit(X_train, y_train)
    models['knn'] = KNeighborsClassifier().fit(X_train, y_train)
    models['naive_bayes'] = GaussianNB().fit(X_train, y_train)
    models['decision_tree'] = DecisionTreeClassifier().fit(X_train, y_train)
    models['mlp_clf'] = MLPClassifier().fit(X_train, y_train)
    
    return models

# Funkcja przewidywania z użyciem modeli
def predict_with_models(models, X_test):
    predictions = {}

    for model_name, model in models.items():
        predictions[model_name] = model.predict(X_test)

    return predictions

# Funkcja rysowania wyników
def plot_results(predictions):
    plt.figure(figsize=(10, 5))

    for model_name, prediction in predictions.items():
        plt.plot(prediction, label=model_name)

    plt.title("Porównanie przewidywań modeli")
    plt.xlabel("Próby")
    plt.ylabel("Wynik")
    plt.legend()
    plt.show()

# Funkcja obliczania correct score z użyciem biblioteki bukmacherska
def calculate_correct_score(team1_avg_scored, team1_avg_conceded, team2_avg_scored, team2_avg_conceded):
    team1_lambda = team1_avg_scored * team2_avg_conceded
    team2_lambda = team2_avg_scored * team1_avg_conceded
    best_score, win_ratio, stake = bk.calculate_correct_score(team1_lambda, team2_lambda)
    return best_score, win_ratio, stake, team1_lambda, team2_lambda

# Dodanie funkcji z biblioteki bukmacherska
def oblicz_prawdopodobienstwo(gole_druzyna1, gole_druzyna2, wspolczynnik):
    prawd = bk.oblicz_prawdopodobienstwo(gole_druzyna1, gole_druzyna2, wspolczynnik)
    return prawd

def analiza_wynikow(dane):
    analiza = bk.analiza_wynikow(dane)
    return analiza
