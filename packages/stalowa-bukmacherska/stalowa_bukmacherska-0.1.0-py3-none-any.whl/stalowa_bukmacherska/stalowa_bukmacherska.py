import math
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from scipy.stats import pearsonr
from sklearn.svm import SVR

# Funkcja obliczania prawdopodobieństwa Poissona
def poisson_probability(k, lmbda):
    return (math.exp(-lmbda) * lmbda ** k) / math.factorial(k)

# Funkcja obliczania wyników drużyny 1
def oblicz_wynik_druzyny(gole_zdobyte, gole_stracone, bezposr_spotkania):
    srednia_zdobytych = gole_zdobyte / bezposr_spotkania
    srednia_straconych = gole_stracone / bezposr_spotkania
    return srednia_zdobytych, srednia_straconych

# Funkcja obliczania wyników drużyny 2
def oblicz_wynik_druzyny2(gole_zdobyte, gole_stracone, bezposr_spotkania):
    srednia_zdobytych = gole_zdobyte / bezposr_spotkania
    srednia_straconych = gole_stracone / bezposr_spotkania
    return srednia_zdobytych, srednia_straconych

# Modele Machine Learning
def train_models(X_train, y_train):
    models = {}

    # Model regresji logistycznej
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)
    models['log_reg'] = log_reg

    # Model gradientu boosting
    grad_boost = GradientBoostingClassifier()
    grad_boost.fit(X_train, y_train)
    models['grad_boost'] = grad_boost

    # Model lasu losowego
    rf_clf = RandomForestClassifier()
    rf_clf.fit(X_train, y_train)
    models['rf_clf'] = rf_clf

    # Model sieci neuronowych
    mlp_clf = MLPClassifier()
    mlp_clf.fit(X_train, y_train)
    models['mlp_clf'] = mlp_clf

    # Model klasteryzacji
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X_train)
    models['kmeans'] = kmeans

    # Model regresji liniowej
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    models['lin_reg'] = lin_reg

    # Model wspomagany przez maszynę (SVM)
    svm_clf = SVC()
    svm_clf.fit(X_train, y_train)
    models['svm_clf'] = svm_clf

    # Model regresji wspomagany przez maszynę (SVR)
    svr = SVR()
    svr.fit(X_train, y_train)
    models['svr'] = svr

    return models

def predict_with_models(models, X_test):
    predictions = {}

    predictions['log_reg'] = models['log_reg'].predict(X_test)
    predictions['grad_boost'] = models['grad_boost'].predict(X_test)
    predictions['rf_clf'] = models['rf_clf'].predict(X_test)
    predictions['mlp_clf'] = models['mlp_clf'].predict(X_test)
    predictions['kmeans'] = models['kmeans'].predict(X_test)
    predictions['lin_reg'] = models['lin_reg'].predict(X_test)
    predictions['svm_clf'] = models['svm_clf'].predict(X_test)
    predictions['svr'] = models['svr'].predict(X_test)

    return predictions

def rysuj_wykresy(srednia1_zdobytych, srednia1_straconych, srednia2_zdobytych, srednia2_straconych):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

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
