import pyroomacoustics as pra
import numpy as np

# Parameters
sample_rate = 16000

# Define minimum and maximum values
min_room_volume = 25  # cubic meters
max_room_volume = 1000  # cubic meters
min_rt60 = 0.3  # seconds


max_rt60 = 12  # seconds
min_sources = 1
max_sources = 20
min_source_microphone_distance = 1  # meters
max_source_microphone_distance = 5  # meters

# Generate all possible combinations

room_volumes = np.arange(min_room_volume, max_room_volume + 1, 25)
rt60_values = np.linspace(min_rt60, max_rt60, num=10)
source_counts = np.arange(min_sources, max_sources + 1)
source_microphone_distances = np.linspace(min_source_microphone_distance, max_source_microphone_distance, num=5)
print("room_volumes:")
print(room_volumes)
print("rt_60valjues")
print(rt60_values)
print("source_counts")
print(source_counts)
print("source_microphone_distances")
print(source_microphone_distances)
'''
# Loop over all combinations
for room_volume in room_volumes:
    for rt60 in rt60_values:
        for num_sources in source_counts:
            for source_microphone_distance in source_microphone_distances:
                # Calculate room dimensions
                min_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
                max_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
                room_dimensions = [np.random.uniform(min_dimension, max_dimension),
                                   np.random.uniform(min_dimension, max_dimension),
                                   np.random.uniform(min_dimension, max_dimension)]

                # Calculate absorption
                e_absorption, max_order = pra.inverse_sabine(rt60, room_dimensions)

                # Create the room
                room = pra.ShoeBox(room_dimensions, fs=sample_rate, materials=pra.Material(e_absorption), max_order=max_order)

                # Add sources
                for _ in range(num_sources):
                    source_position = [np.random.uniform(0, room_dimensions[0] / 2),
                                       np.random.uniform(0, room_dimensions[1]),
                                       np.random.uniform(0, room_dimensions[2])]
                    room.add_source(source_position)

                # Add microphone
                microphone_position = [np.random.uniform(room_dimensions[0] / 2, room_dimensions[0]),
                                       np.random.uniform(0, room_dimensions[1]),
                                       np.random.uniform(0, room_dimensions[2])]
                room.add_microphone(microphone_position)

                # Compute RIR
                room.compute_rir()

                # Move microphone closer to the half line
                microphone_position[0] -= source_microphone_distance
                room.move_microphone(microphone_position)

                # Plot RIR (optional)
                # room.plot_rir()

                # Save RIR or further processing
                # Save or process room impulse response here
'''
