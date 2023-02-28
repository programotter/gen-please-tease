import time
import random

from patterns import *

def setStrength(value):
    # Code to send Bluetooth signal to vibrator with desired strength
    print(f"Setting vibrator strength to {value}")
    
def generate_random_phases(total_duration, min_tease_duration, max_tease_duration,
                           min_buildup_duration, max_buildup_duration, 
                           tease_min_strength, tease_max_strength, 
                           buildup_min_strength, buildup_max_strength, 
                           final_min_strength, final_max_strength,
                           patterns):
    phase_start_time = 0
    remaining_time = total_duration

    phases = []
    while remaining_time > 0:
        is_tease = remaining_time >= max_buildup_duration or \
                   (remaining_time >= min_tease_duration and random.random() < 0.5)

        if is_tease:
            duration = random.uniform(min_tease_duration, min(max_tease_duration, remaining_time))
            pattern = random.choice(patterns)
            strength_range = (tease_min_strength, tease_max_strength)
        else:
            duration = random.uniform(min_buildup_duration, min(max_buildup_duration, remaining_time))
            pattern = random.choice(patterns)
            strength_range = (buildup_min_strength, buildup_max_strength)

        phases.append(('tease' if is_tease else 'buildup', phase_start_time, 
                       duration, strength_range, pattern))
        phase_start_time += duration
        remaining_time -= duration

    # Add a final phase with a random duration and strength range
    pattern = random.choice(patterns)
    strength_range = (final_min_strength, final_max_strength)
    phases.append(('final', phase_start_time, None, strength_range, pattern))

    return phases

def run_phase(phase_name, start_value, end_value, duration, pattern_name, min_strength, max_strength):
    # Get the start time
    start_time = time.monotonic()

    # Loop until the duration has elapsed
    while duration > 0:
        # Calculate the current strength based on the pattern
        set_pattern_strength(pattern_name, start_time, min_strength, max_strength)
        
        # Update the duration and strength for the next iteration
        duration -= 0.1
        current_value = start_value + (end_value - start_value) * (1 - duration / phase_duration)
        
        # Wait for 0.1 seconds
        time.sleep(0.1)

    # Set the final strength for the phase
    setStrength(end_value)


# Define the sequence of phases
phases = generate_random_phases(720, 10, 120, 0.1, 0.3, 0.3, 0.6, 0.8, 1.0, ["sine", "square", "triangle", None])

# Run through the phases
for phase in phases:
    phase_name, start_value, end_value, duration = phase
    if duration is None:
        print(f"Starting {phase_name} phase")
        setStrength(end_value)
        break
    while duration > 0:
        run_phase(phase_name, start_value, end_value, duration)
        duration -= 1
    time.sleep(random.randint(60, 120))

 
