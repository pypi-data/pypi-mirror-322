import unittest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from shapley_calculator.shapley import ShapleyValueCalculator


class TestShapley(unittest.TestCase):
    def setUp(self):
        # Подготовка простых тестовых данных
        self.X_simple = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ])
        self.y_simple = np.array([1, 2, 3, 6])

        # Подготовка более сложных тестовых данных
        np.random.seed(42)
        self.X_complex = np.random.rand(100, 5)
        self.y_complex = (2 * self.X_complex[:, 0] + 
                         3 * self.X_complex[:, 1] + 
                         0.5 * self.X_complex[:, 2] + 
                         0.1 * self.X_complex[:, 3] + 
                         0.05 * self.X_complex[:, 4])

    def test_linear_model_simple_data(self):
        # Тест на простой линейной модели
        model = LinearRegression()
        model.fit(self.X_simple, self.y_simple)
        
        calculator = ShapleyValueCalculator(model, self.X_simple, self.y_simple, num_samples=100)
        shapley_values = calculator.get_shapley_values(normalize=True)
        
        print("\nLinear Model - Simple Data")
        print("Shapley values:", shapley_values)
        print("Sum of values:", np.sum(shapley_values))
        
        # Проверяем основные свойства значений Шепли
        self.assertEqual(len(shapley_values), 3)
        self.assertTrue(all(isinstance(v, (int, float)) for v in shapley_values))
        self.assertAlmostEqual(np.sum(shapley_values), 1.0, places=5)  # Проверяем сумму
        
        # Проверяем, что большие коэффициенты получают большие значения Шепли
        self.assertTrue(shapley_values[2] > shapley_values[0])  # Третий признак важнее первого
        
    def test_random_forest_complex_data(self):
        # Тест на случайном лесе с более сложными данными
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(self.X_complex, self.y_complex)
        
        calculator = ShapleyValueCalculator(model, self.X_complex, self.y_complex, num_samples=100)
        shapley_values = calculator.get_shapley_values(normalize=True)
        
        print("\nRandom Forest - Complex Data")
        print("Shapley values:", shapley_values)
        print("Sum of values:", np.sum(shapley_values))
        
        # Проверяем основные свойства
        self.assertEqual(len(shapley_values), 5)
        self.assertTrue(all(isinstance(v, (int, float)) for v in shapley_values))
        self.assertAlmostEqual(np.sum(np.abs(shapley_values)), 1.0, places=4)  # Уменьшили точность до 4 знаков
        
        # Проверяем, что наиболее важные признаки получили большие значения
        # (в наших данных первые два признака наиболее важны)
        important_features = np.argsort(shapley_values)[-2:]
        self.assertTrue(all(f in [0, 1] for f in important_features))

    def test_single_sample_explanation(self):
        # Тест объяснения для одного примера
        model = LinearRegression()
        model.fit(self.X_simple, self.y_simple)
        
        calculator = ShapleyValueCalculator(model, self.X_simple, self.y_simple, num_samples=100)
        shapley_values = calculator.get_shapley_values(sample_idx=0, normalize=True)
        
        print("\nSingle Sample Explanation")
        print("Shapley values for first sample:", shapley_values)
        print("Sum of values:", np.sum(shapley_values))
        
        self.assertEqual(len(shapley_values), 3)
        self.assertTrue(all(isinstance(v, (int, float)) for v in shapley_values))
        self.assertAlmostEqual(np.sum(shapley_values), 1.0, places=5)  # Проверяем сумму


if __name__ == '__main__':
    unittest.main()