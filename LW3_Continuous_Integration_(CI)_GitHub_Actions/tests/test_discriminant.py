from src.discriminant import discriminant

# Положительные тесты (изменены: D=0 -> D=0, D=1 -> D=16)
def test_positive_discriminant():
    # Проверка D = 0: a=4, b=12, c=9. D = 144 - 4*4*9 = 0
    assert discriminant(4, 12, 9) == 0
    # Проверка D = 16: a=1, b=6, c=5. D = 36 - 4*1*5 = 16
    assert discriminant(1, 6, 5) == 16

# Негативные тесты (изменены: D=-4 -> D=-7)
def test_negative_discriminant():
    # Проверка D < 0: a=2, b=1, c=1. D = 1 - 4*2*1 = -7
    assert discriminant(2, 1, 1) < 0