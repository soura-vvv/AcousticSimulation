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

num_microphone_positions_length = 10
num_microphone_positions_width=5

source_height = 1.7  # meters
microphone_height = 1.7  # meters

sources=[]
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




# Loop over all combinations
for room_volume in room_volumes:
    for rt60 in rt60_values:
        for num_sources in source_counts:
            
            print("-----------------------------------------------------------------")
            # Calculate room dimensions
            min_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
            max_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
            room_dimensions = [np.random.uniform(min_dimension, max_dimension),
                                np.random.uniform(min_dimension, max_dimension),
                                np.random.uniform(min_dimension, max_dimension)]

            # Split the room into two halves
            half_length = room_dimensions[0] / 2
            # Calculate absorption
            e_absorption, max_order = pra.inverse_sabine(rt60, room_dimensions)

            print("Room Dimensions:")
            print(room_dimensions)
            print("rt60")
            print(rt60)
            # Create the room
            room = pra.ShoeBox(room_dimensions, fs=sample_rate, materials=pra.Material(e_absorption), max_order=max_order)
            sources=[]
            # Add sources
            for _ in range(num_sources):
                source_position = [np.random.uniform(0,half_length),
                                    np.random.uniform(0, room_dimensions[1]),
                                    source_height]
                sources.append(np.round(source_position,2))
                print("Source Position:")
                print(source_position)
                
            for source in (sources):
                room.add_source(source)

            # Add microphone
            microphone_position = [room_dimensions[0], room_dimensions[1]/2, microphone_height]
            room.add_microphone(microphone_position)
            print("Microphone Position")
            print(microphone_position)
            # Compute RIR
            print("Compute------------------------------------------")
            room.compute_rir()
                

            #Switch Microphone Positions (Moving it closer to the source graudually)
            for i in range(1, num_microphone_positions_length + 1):
                # Move microphone position
                microphone_position[0] = room_dimensions[0] - i * (room_dimensions[0] / (2*(num_microphone_positions_length + 1)))
                #room.move_microphone(microphone_position)
                microphone_position=np.round(microphone_position,2)
    
                for j in range(1,num_microphone_positions_width+1):
                #print(i * (room_dimensions[1] / (num_microphone_positions_width + 1)))
                    microphone_position[1]=room_dimensions[1] - j * (room_dimensions[1] / (num_microphone_positions_width + 1))
                    microphone_position=np.round(microphone_position,2)

                    # Create the room
                    room = pra.ShoeBox(room_dimensions, fs=sample_rate, materials=pra.Material(e_absorption), max_order=max_order)
                    #Add Sources
                    for source in (sources):
                        room.add_source(source)
                        print("Source Position:")
                        print(source_position)
                    
                    #Add Microphone
                    room.add_microphone(microphone_position)



                    print(microphone_position)
                    room.compute_rir()
                    print("Compute------------------------------------------")
                    # Compute RIR for the new microphone position
                    #room.compute_rir()
                    #num_microphone_positions_width-=2
                    #room_width_temp=room_width_temp - 1 * (room_dimensions[1] / (num_microphone_positions_width + 1))
                    # Plot RIR (optional)
                    # room.plot_rir()

                    # Save RIR or further processing
                    # Save or process room impulse response here

            # Move microphone closer to the half line
            #microphone_position[0] -= source_microphone_distance
            #room.move_microphone(microphone_position)
            print(len(room.rir[0]))
            # Plot RIR (optional)
            # room.plot_rir()
            
            # Save RIR or further processing
            # Save or process room impulse response here
        exit()

