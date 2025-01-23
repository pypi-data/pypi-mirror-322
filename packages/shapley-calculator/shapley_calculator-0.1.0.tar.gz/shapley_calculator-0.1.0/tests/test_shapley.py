import unittest
from shapley_calculator.shapley import ShapleyValueCalculator


def simple_model(X):
    # Простая модель, суммирующая признаки
    return sum(X)


data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
target = [6, 15, 24]


class TestShapley(unittest.TestCase):
    def test_shapley_values(self):
        calculator = ShapleyValueCalculator(simple_model, data, target, num_samples=100000)
        shapley_values = calculator.get_shapley_values()
        
        print("Computed Shapley values:", shapley_values)
        
        # Проверяем размерность и тип
        self.assertEqual(len(shapley_values), 3)
        self.assertTrue(all(isinstance(value, float) for value in shapley_values))
        
        # Проверяем, что сумма равна 1
        self.assertAlmostEqual(sum(shapley_values), 1, places=5)
        print(f"Sum of Shapley values: {sum(shapley_values)}")
        
        # Проверяем, что значения примерно равны с большим допуском
        expected_value = 1 / len(shapley_values)
        for value in shapley_values:
            self.assertTrue(abs(value - expected_value) < 0.1,
                          f"Value {value} differs from expected {expected_value} by more than 0.1")
            print(f"Expected value: {expected_value}, Computed value: {value}")


if __name__ == '__main__':
    unittest.main()