import time

class ErrorToMovement:
    def __init__(self, kp, ki, kd, max_output=.4):
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
        if dt <= 0.0:
            dt = 1e-4
        
        p_term = self.kp * error

        self.integral += error * dt
        i_term = self.ki * self.integral

        derivative = (error - self.prev_error) / dt
        # d_term 

        output = p_term + i_term #+ d_term


        return output

    def reset(self):
        pass