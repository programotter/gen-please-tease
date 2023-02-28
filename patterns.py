import math
import time
import random

def set_pattern_strength(pattern_name, current_time, time_since_start, min_strength, max_strength, pattern_duration=None):
    if pattern_name == 'sine':
        return sine_pattern(current_time, min_strength, max_strength)
    elif pattern_name == 'square':
        return square_pattern(current_time, min_strength, max_strength)
    elif pattern_name == 'triangle':
        return triangle_pattern(current_time, min_strength, max_strength)
    elif pattern_name == 'escalation':
        return escalation_pattern(current_time, time_since_start, min_strength, max_strength, pattern_duration)
    elif pattern_name == 'morse':
        return morse_code_pattern(current_time, time_since_start, min_strength, max_strength)
    elif pattern_name == 'echo':
        return echo_pattern(current_time, time_since_start, pattern_duration, min_strength, max_strength)
    else:
        raise ValueError("Invalid pattern name")

    
def morse_code_pattern(current_time, time_since_start, min_strength, max_strength):
    dot_duration = 0.2
    dash_duration = dot_duration * 3
    symbol_duration = dot_duration
    silence_duration = dot_duration
    dot_strength = (min_strength + max_strength) / 2
    dash_strength = max_strength

    if time_since_start < symbol_duration:
        return dot_strength
    else:
        num_symbols = random.randint(1, 5)
        symbols = []
        for i in range(num_symbols):
            symbol = random.choice(['dot', 'dash'])
            symbols.append(symbol)

        symbol_index = int((time_since_start - symbol_duration) // (symbol_duration + silence_duration))
        if symbol_index < len(symbols):
            symbol = symbols[symbol_index]
            if symbol == 'dot':
                return dot_strength
            elif symbol == 'dash':
                return dash_strength
        else:
            return 0

def sine_pattern(time_since_start, pattern_duration, min_strength, max_strength):
    period = 2 * math.pi
    time_scaled = time_since_start / pattern_duration
    value = (math.sin(period * time_scaled) + 1) / 2
    return (value * (max_strength - min_strength)) + min_strength

def square_pattern(time_since_start, pattern_duration, min_strength, max_strength):
    duty_cycle = 0.5
    time_scaled = time_since_start / pattern_duration
    value = 1 if (time_scaled % 1) < duty_cycle else 0
    return (value * (max_strength - min_strength)) + min_strength

def triangle_pattern(time_since_start, pattern_duration, min_strength, max_strength):
    slope = (max_strength - min_strength) / (pattern_duration / 2)
    time_scaled = time_since_start % pattern_duration
    value = slope * (time_scaled - pattern_duration / 4)
    value = max(min(value, max_strength), min_strength)
    return value
        
def escalation_pattern(time_since_start, pattern_duration, min_strength, max_strength):
    slope = (max_strength - min_strength) / pattern_duration
    value = slope * time_since_start
    value = max(min(value, max_strength), min_strength)
    return value

def echo_pattern(current_time, time_since_start, pattern_duration, min_strength, max_strength):
    period = 10  # The period of the echo pattern (in seconds)
    start_time = current_time - time_since_start
    phase_time = current_time - start_time
    phase_time_in_period = phase_time % period
    phase_strength = min_strength + ((max_strength - min_strength) / 2) * math.sin((2 * math.pi / period) * phase_time_in_period)

    # Compute strength for the echo pattern
    echo_strength = min_strength + (max_strength - min_strength) * (pattern_duration - phase_time) / pattern_duration

    # Set the vibration strength for the current phase
    if phase_strength > echo_strength:
        return phase_strength
    else:
        return echo_strength
