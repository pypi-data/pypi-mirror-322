import math
import numpy as np
from sklearn.linear_model import LogisticRegression, PoissonRegressor
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Funkcja obliczania prawdopodobieństwa Poissona
def poisson_probability(k, lmbda):
    return (math.exp(-lmbda) * lmbda ** k) / math.factorial(k)

# Funkcja obliczania wyników drużyny
def oblicz_wynik_druzyny(gole_zdobyte, gole_stracone, bezposr_spotkania):
    srednia_zdobytych = gole_zdobyte / bezposr_spotkania
    srednia_straconych = gole_stracone / bezposr_spotkania
    return srednia_zdobytych, srednia_straconych

# Modele Machine Learning
def train_models(X_train, y_train):
    models = {}

    # Model regresji logistycznej
    models['log_reg'] = LogisticRegression().fit(X_train, y_train)

    # Model gradientu boosting
    models['grad_boost'] = GradientBoostingClassifier().fit(X_train, y_train)

    # Model lasu losowego
    models['rf_clf'] = RandomForestClassifier().fit(X_train, y_train)

    # Model sieci neuronowych
    models['mlp_clf'] = MLPClassifier().fit(X_train, y_train)

    # Model klasteryzacji
    models['kmeans'] = KMeans(n_clusters=2).fit(X_train)

    # Model regresji Poissona
    models['poisson_reg'] = PoissonRegressor().fit(X_train, y_train)

    # Model wspomagany przez maszynę (SVM)
    models['svm_clf'] = SVC().fit(X_train, y_train)

    # Model Naive Bayes
    models['naive_bayes'] = GaussianNB().fit(X_train, y_train)

    # Model drzew decyzyjnych
    models['decision_tree'] = DecisionTreeClassifier().fit(X_train, y_train)

    # Model AdaBoost
    models['adaboost'] = AdaBoostClassifier().fit(X_train, y_train)

    # Model Extra Trees
    models['extra_trees'] = ExtraTreesClassifier().fit(X_train, y_train)

    # Model LightGBM
    models['lightgbm'] = LGBMClassifier().fit(X_train, y_train)

    return models

def predict_with_models(models, X_test):
    predictions = {}

    for model_name, model in models.items():
        predictions[model_name] = model.predict(X_test)

    return predictions

def rysuj_wykresy(srednia1_zdobytych, srednia1_straconych, srednia2_zdobytych, srednia2_straconych):
    plt.figure(figsize=(15, 5))

    # Wykres średnich zdobytych goli - słupkowy
    plt.subplot(1, 3, 1)
    plt.bar(['Drużyna 1', 'Drużyna 2'], [srednia1_zdobytych, srednia2_zdobytych], color=['blue', 'red'])
    plt.title('Średnie zdobyte gole')
    plt.xlabel('Drużyna')
    plt.ylabel('Średnia goli')

    # Wykres średnich zdobytych goli - liniowy
    plt.subplot(1, 3, 2)
    plt.plot(['Drużyna 1', 'Drużyna 2'], [srednia1_zdobytych, srednia2_zdobytych], marker='o', color='blue', label='Zdobyte')
    plt.plot(['Drużyna 1', 'Drużyna 2'], [srednia1_straconych, srednia2_straconych], marker='o', color='red', label='Stracone')
    plt.title('Średnie gole')
    plt.xlabel('Drużyna')
    plt.ylabel('Średnia goli')
    plt.legend()

    # Wykres średnich goli - obszarowy 3D
    ax = plt.subplot(1, 3, 3, projection='3d')
    x = [0, 1]
    y = [srednia1_zdobytych, srednia2_zdobytych]
    z = [srednia1_straconych, srednia2_straconych]
    ax.bar3d(x, [0]*len(x), [0]*len(x), [0.5]*len(x), y, z, color=['blue', 'red'])
    ax.set_title('Średnie gole 3D')
    ax.set_xticks(x)
    ax.set_xticklabels(['Drużyna 1', 'Drużyna 2'])
    ax.set_xlabel('Drużyna')
    ax.set_ylabel('Zdobyte')
    ax.set_zlabel('Stracone')

    plt.tight_layout()
    plt.show()
