import pyroomacoustics as pra
import numpy as np

# Parameters
sample_rate = 16000

# Room dimensions
room_dimensions = [10, 10, 10]

# Number of sources and microphone
num_sources = 5
num_microphone_positions = 10

# Heights of sources and microphones
source_height = 1  # meters
microphone_height = 1  # meters

# Split the room into two halves
half_length = room_dimensions[0] / 2
source_half_length = half_length / 2  # Sources will be placed in the first half

# Initialize room
room = pra.ShoeBox(room_dimensions, fs=sample_rate)

# Add sources to the first half of the room
for i in range(num_sources):
    source_position = [np.random.uniform(0, half_length),
                       np.random.uniform(0, room_dimensions[1]),
                       source_height]
    print("Source Position : ", i)
    print(source_position)
    room.add_source(source_position)

# Initialize microphone at the extreme end
microphone_position = [room_dimensions[0], room_dimensions[1] / 2, microphone_height]
room.add_microphone(microphone_position)
print("Microphone Position 0:")
print(microphone_position)
# Compute RIR for the initial microphone position
# room.compute_rir()
print("Compute------------------------------------------")

# Move the microphone gradually towards the center
for i in range(1, num_microphone_positions + 1):
    # Move microphone position
    print("Microphone position ", i)
    if i <= num_microphone_positions / 2:
        microphone_position[0] = room_dimensions[0] - i * (room_dimensions[0] / (num_microphone_positions / 2 + 1))
        microphone_position[1] = i * (room_dimensions[1] / (num_microphone_positions / 2 + 1))
    else:
        microphone_position[0] = i * (room_dimensions[0] / (num_microphone_positions / 2 + 1))
        microphone_position[1] = (num_microphone_positions - i) * (room_dimensions[1] / (num_microphone_positions / 2 + 1))
    # room.move_microphone(microphone_position)
    print(microphone_position)
    # Compute RIR for the new microphone position
    # room.compute_rir()
    print("Compute------------------------------------------")
    # Plot RIR (optional)
    # room.plot_rir()

    # Save RIR or further processing
    # Save or process room impulse response here