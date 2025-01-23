# Stalowa Bukmacherka

**Stalowa Bukmacherka** to biblioteka do przewidywania wyników różnych zdarzeń w meczach piłkarskich, używająca różnych modeli regresji i klasyfikacji.

## Instalacja

Aby zainstalować bibliotekę, użyj:

```sh
pip install stalowa_bukmacherka


import stalowa_bukmacherka as sb

# Przygotowanie danych treningowych
X_train = ...
y_train = ...

# Trening modeli
models = sb.train_models(X_train, y_train)

# Przewidywanie wyników
X_test = ...
predictions = sb.predict_with_models(models, X_test)

# Wyświetlanie wyników
sb.plot_results(predictions, team1_lambda, team2_lambda, team1_avg_conceded, team2_avg_conceded)
