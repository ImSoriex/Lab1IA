import random

N = 8  # Definimos el tamaño del problema, en este caso 8 reinas

# Generar un tablero aleatorio
def random_board():
    # Se crea una lista de longitud N
    # Cada índice representa una columna y el valor es la fila donde está la reina
    return [random.randint(0, N-1) for _ in range(N)]

# Calcular el número de conflictos
def conflicts(board):
    attacks = 0  # Inicializamos el contador de conflictos en 0
    # Recorremos todas las reinas
    for i in range(N):
        for j in range(i+1, N):
            # Dos reinas se atacan si están en la misma fila
            if board[i] == board[j]:
                attacks += 1
            # O si están en la misma diagonal (diferencia de filas = diferencia de columnas)
            elif abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return attacks  # Retornamos el número total de ataques

# Buscar el mejor vecino de un tablero
def best_neighbor(board):
    current_conf = conflicts(board)  # Calculamos conflictos del estado actual
    neighbors = []  # Lista para guardar vecinos candidatos
    # Recorremos cada columna para intentar mover la reina
    for col in range(N):
        for row in range(N):
            if board[col] != row:  # Si la reina ya está en esa fila, no lo consideramos
                new_board = board.copy()  # Hacemos una copia del tablero
                new_board[col] = row  # Movemos la reina a la nueva fila
                c = conflicts(new_board)  # Calculamos conflictos del nuevo tablero
                # Si mejora (menos conflictos), reemplazamos la lista de vecinos
                if c < current_conf:
                    neighbors = [(new_board, c)]
                    current_conf = c
                # Si es igual de bueno que el mejor hasta ahora, lo agregamos como opción
                elif c == current_conf:
                    neighbors.append((new_board, c))
    # Si encontramos al menos un vecino válido, escogemos uno al azar
    if neighbors:
        return random.choice(neighbors)
    # Si no hay vecinos mejores, regresamos el mismo tablero
    return board, current_conf

# Algoritmo de ascenso de colinas (hill climbing)
def hill_climbing(no_sideways=False, sideways_limit=100, restarts=False, max_restarts=1000):
    steps = 0  # Contador de pasos realizados
    sideways_moves = 0  # Contador de movimientos laterales
    attempts = 0  # Contador de intentos (para reinicios aleatorios)

    # Si usamos reinicios, intentamos hasta max_restarts veces
    while attempts < (max_restarts if restarts else 1):
        board = random_board()  # Generamos un tablero inicial aleatorio
        current_conf = conflicts(board)  # Calculamos los conflictos iniciales
        sideways_moves = 0  # Reiniciamos el contador de movimientos laterales

        # Empezamos la búsqueda local desde este tablero
        while True:
            steps += 1  # Cada iteración cuenta como un paso
            next_board, next_conf = best_neighbor(board)  # Buscamos el mejor vecino

            # Caso éxito: si ya no hay conflictos, encontramos solución
            if next_conf == 0:
                return True, steps

            # Caso mejora: si el vecino es mejor, lo tomamos
            if next_conf < current_conf:
                board, current_conf = next_board, next_conf
                sideways_moves = 0  # Reiniciamos movimientos laterales

            # Caso empate: mismo costo que el actual
            elif next_conf == current_conf and not no_sideways:
                if sideways_moves < sideways_limit:  # Aceptamos hasta sideways_limit
                    board, current_conf = next_board, next_conf
                    sideways_moves += 1
                else:  # Si ya nos pasamos del límite, nos estancamos
                    break
            else:
                # Si no hay mejora ni empate permitido → estancamiento
                break

        # Si no hay reinicios, regresamos fracaso
        if not restarts:
            return False, steps

        # Si hay reinicios, incrementamos intento y probamos de nuevo
        attempts += 1

    # Si terminamos todos los reinicios sin solución, devolvemos fracaso
    return False, steps

# Función para correr experimentos masivos
def experiment(algorithm, trials=3000):
    success = 0  # Contador de experimentos exitosos
    success_steps = []  # Pasos cuando sí hubo éxito
    fail_steps = []  # Pasos cuando no hubo éxito

    # Repetimos el experimento la cantidad de veces indicada
    for _ in range(trials):
        ok, steps = algorithm()  # Ejecutamos el algoritmo
        if ok:  # Si tuvo éxito
            success += 1
            success_steps.append(steps)
        else:  # Si falló
            fail_steps.append(steps)

    # Calculamos métricas pedidas
    prob_success = success / trials
    avg_success = sum(success_steps)/len(success_steps) if success_steps else 0
    avg_fail = sum(fail_steps)/len(fail_steps) if fail_steps else 0

    return prob_success, avg_success, avg_fail



# 1. Ascenso de colinas sin movimientos laterales
print("Sin laterales:", experiment(lambda: hill_climbing(no_sideways=True)))

# 2. Ascenso de colinas con laterales (100 movimientos permitidos)
print("Con laterales:", experiment(lambda: hill_climbing(no_sideways=False, sideways_limit=100)))

# 3. Ascenso de colinas con laterales + reinicios
print("Con laterales + reinicios:", experiment(lambda: hill_climbing(no_sideways=False, sideways_limit=100, restarts=True)))

# Crear README con los miembros del grupo
with open("readme.txt", "w", encoding="utf-8") as f:
    f.write("Laboratorio 1\n")
    f.write("===========================================================\n\n")
    f.write("Miembros del grupo:\n")
    f.write(" - Juan Jose Torres\n")
    f.write(" - Jorge Almeida\n")
    f.write(" - Emilio Soria\n")
