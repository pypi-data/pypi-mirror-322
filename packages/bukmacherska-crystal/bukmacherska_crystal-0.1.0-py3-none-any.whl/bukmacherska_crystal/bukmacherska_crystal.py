import numpy as np
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import bukmacherska as bk
import matplotlib.pyplot as plt

def train_models(X_train, y_train):
    models = {}

    # Modele regresji i nieliniowe
    models['bayesian_ridge'] = BayesianRidge().fit(X_train, y_train)
    
    # Modele klasyfikacji
    models['rf_clf'] = RandomForestClassifier().fit(X_train, y_train)
    models['grad_boost'] = GradientBoostingClassifier().fit(X_train, y_train)
    models['knn'] = KNeighborsClassifier().fit(X_train, y_train)
    models['svm_clf'] = SVC().fit(X_train, y_train)
    models['naive_bayes'] = GaussianNB().fit(X_train, y_train)
    models['decision_tree'] = DecisionTreeClassifier().fit(X_train, y_train)
    models['mlp_clf'] = MLPClassifier().fit(X_train, y_train)
    
    return models

def predict_with_models(models, X_test):
    predictions = {}

    for model_name, model in models.items():
        predictions[model_name] = model.predict(X_test)

    return predictions

def plot_results(predictions, team1_lambda, team2_lambda, team1_avg_conceded, team2_avg_conceded):
    fig, axs = plt.subplots(15, 3, figsize=(15, 45))

    events = ['Liczba goli', 'Rzuty rożne', 'Spalone', 'Kartki', 'Kontuzje', 'Faule', 'Rzuty karne', 
              'Posiadanie piłki', 'Strzały na bramkę', 'Skuteczność strzałów', 'Podania', 'Przejęcia piłki', 
              'Interwencje bramkarzy', 'Ofiary fauli', 'Celne podania']
    
    for i, event in enumerate(events):
        # Wykres Liniowy
        axs[i*3].plot([1, 2], [team1_lambda, team2_lambda], marker='o')
        axs[i*3].set_title(f"{event} - Liniowy")

        # Wykres Słupkowy
        axs[i*3 + 1].bar(['Drużyna 1', 'Drużyna 2'], [team1_lambda, team2_lambda], color=['blue', 'red'])
        axs[i*3 + 1].set_title(f"{event} - Słupkowy")

        # Wykres 3D
        ax1 = fig.add_subplot(15, 3, i*3 + 2, projection='3d')
        x1 = [0, 1]
        y1 = [team1_lambda, team2_lambda]
        z1 = [team1_avg_conceded, team2_avg_conceded]
        ax1.bar3d(x1, [0]*len(x1), [0]*len(x1), [0.5]*len(x1), y1, z1, color=['blue', 'red'])
        ax1.set_title(f"{event} - 3D")
        ax1.set_xticks(x1)
        ax1.set_xticklabels(['Drużyna 1', 'Drużyna 2'])
        ax1.set_xlabel('Drużyna')
        ax1.set_ylabel('Zdobyte')
        ax1.set_zlabel('Stracone')

    plt.tight_layout()
    plt.show()
