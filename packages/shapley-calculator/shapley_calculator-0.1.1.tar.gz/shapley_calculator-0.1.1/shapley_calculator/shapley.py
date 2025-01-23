import numpy as np
from math import factorial
import random
from tqdm import tqdm


class ShapleyValueCalculator:
    def __init__(self, model, X, y, num_samples=1000):
        """
        Инициализация калькулятора значений Шепли
        
        Args:
            model: Обученная модель с методом predict
            X: numpy array или list - входные данные shape (n_samples, n_features)
            y: numpy array или list - целевые значения
            num_samples: int - количество сэмплов для оценки значений Шепли
        """
        self.model = model
        self.X = np.array(X)
        self.y = np.array(y)
        self.num_samples = num_samples
        self.n_features = self.X.shape[1]
        self.baseline = self._get_baseline_prediction()

    def _get_baseline_prediction(self):
        """Получение базового предсказания на нулевых признаках"""
        X_baseline = np.zeros((1, self.n_features))
        return self.model.predict(X_baseline)[0]

    def _calculate_weights(self):
        """Предварительный расчет весов для всех размеров коалиций"""
        n = self.n_features
        weights = np.zeros(n + 1)
        for size in range(1, n):
            weights[size] = factorial(size - 1) * factorial(n - size) / factorial(n)
        return weights

    def _get_predictions_batch(self, x, coalitions):
        """Получает предсказания модели для батча коалиций"""
        X_modified = np.zeros((len(coalitions), self.n_features))
        for i, coalition in enumerate(coalitions):
            X_modified[i, coalition] = x[coalition]
        return self.model.predict(X_modified)

    def get_shapley_values(self, sample_idx=None, normalize=False):
        """
        Вычисляет значения Шепли для заданного примера или усредненные по всем примерам
        
        Args:
            sample_idx: индекс примера для расчета или None для усреднения по всем примерам
            normalize: bool, нормализовать ли значения Шепли, чтобы их сумма была равна 1
        """
        if sample_idx is not None:
            values = self._compute_shapley_for_sample(self.X[sample_idx])
        else:
            print("Computing Shapley values for all samples...")
            values = np.mean([self._compute_shapley_for_sample(x) for x in tqdm(self.X)], axis=0)
        
        if normalize:
            # Обрабатываем случай, когда есть отрицательные значения
            abs_values = np.abs(values)
            total = np.sum(abs_values)
            if total != 0:
                # Нормализуем, сохраняя знаки и обеспечивая точную сумму 1
                signs = np.sign(values)
                normalized = abs_values / total
                values = signs * normalized
                
                # Корректируем, чтобы сумма была точно 1
                values = values / np.sum(np.abs(values))
                
        return values

    def _compute_shapley_for_sample(self, x):
        """Вычисляет значения Шепли для одного примера"""
        shapley_values = np.zeros(self.n_features)
        weights = self._calculate_weights()
        batch_size = 32  # Размер батча для предсказаний
        
        # Генерируем все коалиции заранее
        for i in range(self.n_features):
            coalitions_with_i = []
            coalitions_without_i = []
            n_samples_per_size = max(1, self.num_samples // (self.n_features - 1))
            
            for size in range(1, self.n_features):
                for _ in range(n_samples_per_size):
                    available_features = list(set(range(self.n_features)) - {i})
                    coalition = random.sample(available_features, size - 1)
                    coalitions_without_i.append(coalition)
                    coalitions_with_i.append(coalition + [i])
            
            # Батчевая обработка
            for j in range(0, len(coalitions_with_i), batch_size):
                batch_with = coalitions_with_i[j:j + batch_size]
                batch_without = coalitions_without_i[j:j + batch_size]
                
                pred_with_i = self._get_predictions_batch(x, batch_with)
                pred_without_i = self._get_predictions_batch(x, batch_without)
                
                # Вычисляем маргинальные вклады для батча
                marginal_contributions = pred_with_i - pred_without_i
                
                # Обновляем значения Шепли с учетом весов
                for k, (size, margin) in enumerate(zip([len(c) for c in batch_with], marginal_contributions)):
                    shapley_values[i] += weights[size] * margin / n_samples_per_size
        
        return shapley_values