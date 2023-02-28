import math

def set_pattern_strength(pattern, start_time, min_strength, max_strength):
    # Calculate the current time relative to the start time
    elapsed_time = time.monotonic() - start_time
    
    # Calculate the current strength based on the pattern name and the current time
    if pattern == 'sine':
        period = 10  # 10 seconds per cycle
        amplitude = (max_strength - min_strength) / 2
        offset = min_strength + amplitude
        current_strength = amplitude * math.sin(2 * math.pi * elapsed_time / period) + offset
    elif pattern == 'square':
        period = 10  # 10 seconds per cycle
        duty_cycle = 0.5  # 50% duty cycle
        if (elapsed_time % period) < (duty_cycle * period):
            current_strength = max_strength
        else:
            current_strength = min_strength
    elif pattern == 'triangle':
        period = 10  # 10 seconds per cycle
        amplitude = (max_strength - min_strength) / 2
        offset = min_strength + amplitude
        current_strength = (2 * amplitude / period) * abs((elapsed_time + period / 4) % period - period / 2) + offset
    else:
        # Unknown pattern name, default to maximum strength
        current_strength = max_strength
    
    # Set the current strength using the setStrength function
    setStrength(current_strength)
