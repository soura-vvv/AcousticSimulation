import pyroomacoustics as pra
import numpy as np

# Parameters
sample_rate = 16000

# Room dimensions
room_dimensions = [5, 5, 5]

# Number of sources and microphone
num_sources = 5
num_microphone_positions_length = 10
num_microphone_positions_width=5

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
    print("Source Position : ",i)
    source_position=np.round(source_position,2)
    print(source_position)
    room.add_source(source_position)

# Initialize microphone at the extreme end
microphone_position = [room_dimensions[0], room_dimensions[1]/2, microphone_height]
microphone_position=np.round(microphone_position)
room.add_microphone(microphone_position)
print("Microphone Position 0:")
print(microphone_position)
# Compute RIR for the initial microphone position
#room.compute_rir()
print("Compute------------------------------------------")
print(len(microphone_position))
# Move the microphone gradually towards the center
room_width_temp=room_dimensions[1]
for i in range(1, num_microphone_positions_length + 1):
    # Move microphone position
    microphone_position[0] = room_dimensions[0] - i * (room_dimensions[0] / (2*(num_microphone_positions_length + 1)))
    #room.move_microphone(microphone_position)
    microphone_position=np.round(microphone_position,2)
    
    for j in range(1,num_microphone_positions_width+1):
        #print(i * (room_dimensions[1] / (num_microphone_positions_width + 1)))
        microphone_position[1]=room_dimensions[1] - j * (room_dimensions[1] / (num_microphone_positions_width + 1))
        microphone_position=np.round(microphone_position,2)
        print(microphone_position)
        print("Compute------------------------------------------")
    # Compute RIR for the new microphone position
    #room.compute_rir()
    #num_microphone_positions_width-=2
    #room_width_temp=room_width_temp - 1 * (room_dimensions[1] / (num_microphone_positions_width + 1))
    # Plot RIR (optional)
    # room.plot_rir()

    # Save RIR or further processing
    # Save or process room impulse response here