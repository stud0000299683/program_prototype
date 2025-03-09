# Вероятности событий
p_experienced = 0.9  # Вероятность выбора опытного сотрудника
p_inexperienced = 0.1  # Вероятность выбора неопытного сотрудника

# Условные вероятности ошибки
p_error_given_experienced = 0.01
p_error_given_inexperienced = 0.2

# Формула полной вероятности
p_error = p_error_given_experienced * p_experienced + p_error_given_inexperienced * p_inexperienced

print("Вероятность совершения ошибки:", p_error)
