# combined_bukmacherska

combined_bukmacherska to biblioteka łącząca funkcjonalności bibliotek `bukmacherska` i `bukmacherska_crystal`. 

## Funkcje

- Funkcje gamma i beta
- Funkcje pomocnicze do obliczeń
- Modele maszynowego uczenia
- Funkcje rysujące wykresy

## Instalacja

Aby zainstalować bibliotekę, użyj poniższego polecenia:

```sh
pip install combined_bukmacherska


import combined_bukmacherska as cb

# Przykład użycia funkcji poisson_probability
beta = 2
alpha = 3
probability = cb.poisson_probability(beta, alpha)
print(f"Poisson Probability: {probability}")

# Trening modeli
X_train = ...
y_train = ...
models = cb.train_models(X_train, y_train)

# Predykcje
X_test = ...
predictions = cb.predict_with_models(models, X_test)

# Rysowanie wykresów
cb.plot_results(predictions, team1_lambda, team2_lambda, team1_avg_conceded, team2_avg_conceded)
