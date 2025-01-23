import itertools
import random
from math import factorial


class ShapleyValueCalculator:
    def __init__(self, model, data, target, num_samples=100000):
        self.model = model
        self.data = data
        self.target = target
        self.num_samples = num_samples
        self.n_features = len(data[0])

    def predict(self, X):
        return [self.model(x) for x in X]

    def _calculate_weight(self, coalition_size):
        """Вычисляет вес для коалиции заданного размера"""
        n = self.n_features
        if coalition_size == 0 or coalition_size == n:
            return 0
        return factorial(coalition_size - 1) * factorial(n - coalition_size) / factorial(n)

    def get_shapley_values(self):
        shapley_values = [0] * self.n_features
        n_samples_per_size = self.num_samples // (self.n_features - 1)
        
        # Для каждого признака
        for i in range(self.n_features):
            # Для каждого возможного размера коалиции
            for size in range(1, self.n_features):
                weight = self._calculate_weight(size)
                
                # Берем несколько случайных выборок для каждого размера коалиции
                for _ in range(n_samples_per_size):
                    # Выбираем случайную коалицию заданного размера, не включающую текущий признак
                    available_features = list(set(range(self.n_features)) - {i})
                    coalition = random.sample(available_features, size - 1)
                    
                    # Создаем маски для коалиций с и без текущего признака
                    mask_with_i = [j in coalition or j == i for j in range(self.n_features)]
                    mask_without_i = [j in coalition for j in range(self.n_features)]
                    
                    # Подготавливаем данные для обеих коалиций
                    X_with_i = [[x[j] if include else 0 for j, include in enumerate(mask_with_i)] 
                               for x in self.data]
                    X_without_i = [[x[j] if include else 0 for j, include in enumerate(mask_without_i)]
                                 for x in self.data]
                    
                    # Вычисляем предсказания
                    pred_with_i = sum(self.predict(X_with_i))
                    pred_without_i = sum(self.predict(X_without_i))
                    
                    # Обновляем значение Шепли с учетом веса
                    marginal_contribution = (pred_with_i - pred_without_i) / len(self.data)
                    shapley_values[i] += weight * marginal_contribution / n_samples_per_size

        # Нормализуем значения
        total = sum(shapley_values)
        if total != 0:
            shapley_values = [v / total for v in shapley_values]
            
        return shapley_values