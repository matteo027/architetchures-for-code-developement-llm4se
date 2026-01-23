class TestTask17:
  """Test Suite for CodeNet/p03671 - minimum_two_bells_price"""

  def __init__(self, min_two_bells):
    self.fun = min_two_bells

  def get_benchmark_input(self):
    return ([700, 600, 780],)

  def execute_tests(self):
    tests_passed = 0
    test_methods = [method for method in dir(self) if method.startswith('test_')]
    total_tests = len(test_methods)
    
    for method_name in test_methods:
      method = getattr(self, method_name)
      try:
        method()
        tests_passed += 1
      except Exception as e:
        print(f"[DEBUG]: Task 17 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_case(self):
    assert self.fun([700, 600, 780]) == 1300

  def test_02_first_two_cheapest(self):
    assert self.fun([100, 200, 500]) == 300

  def test_03_last_two_cheapest(self):
    assert self.fun([1000, 100, 200]) == 300

  def test_04_first_and_last_cheapest(self):
    assert self.fun([100, 500, 200]) == 300

  def test_05_all_same_price(self):
    assert self.fun([100, 100, 100]) == 200

  def test_06_two_same_prices(self):
    assert self.fun([100, 100, 200]) == 200
    assert self.fun([200, 100, 100]) == 200

  def test_07_large_values(self):
    assert self.fun([10000, 20000, 30000]) == 30000

  def test_08_minimum_values(self):
    assert self.fun([1, 1, 1]) == 2
