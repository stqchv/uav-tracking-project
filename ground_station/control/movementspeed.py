import time

class ErrorToMovement:
    def __init__(self, kp, ki, kd, max_output=0.4):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_output

        self.prev_error = 0.0
        self.integral = 0.0
        self.last_time = time.time()

    def update(self, error):
        current_time = time.time()
        dt = current_time - self.last_time
        
        # Zabezpieczenie przed dzieleniem przez zero przy zbyt szybkich pętlach
        if dt <= 0.001:
            return 0.0
        
        # 1. Człon proporcjonalny (P)
        p_term = self.kp * error

        # 2. Człon całkujący (I)
        self.integral += error * dt
        i_term = self.ki * self.integral

        # 3. Człon różniczkujący (D)
        derivative = (error - self.prev_error) / dt
        d_term = self.kd * derivative

        # Sumowanie
        output = p_term + i_term + d_term

        # Aktualizacja zmiennych stanu dla następnej iteracji!
        self.prev_error = error
        self.last_time = current_time

        # Nasycenie wyjścia (Clamp)
        if output > self.max_output:
            return self.max_output
        elif output < -self.max_output:
            return -self.max_output
        else:
            return output

    def reset(self):
        """Wywołaj tę funkcję, gdy dron zgubi cel z kadru!"""
        self.integral = 0.0
        self.prev_error = 0.0
        self.last_time = time.time()