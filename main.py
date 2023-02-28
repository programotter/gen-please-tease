import time
import random

def setStrength(value):
    # Code to send Bluetooth signal to vibrator with desired strength
    print(f"Setting vibrator strength to {value}")
    
def generate_random_phases(total_duration, min_duration, max_duration, tease_min_strength, tease_max_strength, buildup_min_strength, buildup_max_strength, final_min_strength, final_max_strength):
    phases = []
    total = 0
    has_tease = False
    has_buildup = False
    while total < total_duration:
        if not has_tease or (has_tease and has_buildup and random.random() < 0.5):
            phase_duration = random.uniform(min_duration, max_duration)
            strength = random.uniform(tease_min_strength, tease_max_strength)
            phases.append(('tease', strength, strength, phase_duration))
            total += phase_duration
            has_tease = True
        else:
            phase_duration = random.uniform(min_duration, max_duration)
            start_strength = random.uniform(buildup_min_strength, buildup_max_strength)
            end_strength = random.uniform(start_strength, 1.0)
            phases.append(('buildup', start_strength, end_strength, phase_duration))
            total += phase_duration
            has_buildup = True
    final_duration = random.uniform(min_duration, max_duration)
    final_strength = random.uniform(final_min_strength, final_max_strength)
    phases.append(('final', final_strength, final_strength, final_duration))
    return phases

def run_phase(phase_name, start_value, end_value, duration):
    print(f"Starting {phase_name} phase")
    value = start_value
    value_delta = (end_value - start_value) / duration
    phase_start_time = time.monotonic()
    while duration > 0:
        setStrength(value)
        duration -= 1
        value += value_delta
        time.sleep(1/10)
    setStrength(end_value)
    print(f"Ending {phase_name} phase")

# Define the sequence of phases
phases = generate_random_phases(720, 10, 120, 0.1, 0.3, 0.3, 0.6, 0.8, 1.0)

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
