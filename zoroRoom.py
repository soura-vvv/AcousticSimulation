from email.mime import audio
import pyroomacoustics as pra
import numpy as np
from scipy.io.wavfile import write
import os
import subprocess
#import soundfile as sf
#import pyflac
import json
import matplotlib.pyplot as plt

import itertools
#dir_obj = CardioidFamily(
#    orientation=DirectionVector(azimuth=90, colatitude=15, degrees=True),
#    pattern_enum=DirectivityPattern.CARDIOID,
#)



# Define a set of typical room sizes
typical_lengths = [5, 7, 9, 11, 13, 15]  # meters
typical_widths = [5, 7, 9, 11, 13, 15]    # meters
typical_heights = [2.5, 3, 3.5, 4, 4.5, 5] # meters

# Generate combinations of room dimensions
room_dimensions_list = list(itertools.product(typical_lengths, typical_widths, typical_heights))

#for dims in room_dimensions_list:
    #print("Room Dimensions:", dims)
# Parameters
sample_rate = 16000
file_count=0
min_sources = 1
max_sources = 10

num_microphone_positions_length = 10
num_microphone_positions_width=5

source_height = 1.7  # meters
microphone_height = 1.7  # meters

sources=[]
# Generate all possible combinations

source_counts = np.arange(min_sources, max_sources + 1)

corpus = pra.datasets.CMUArcticCorpus(download=False)
# http://www.festvox.org/cmu_arctic/

dataset_num_samples=len(corpus)
#playsound(corpus[0])

json_file="zoro.json"
# Loop over all combinations
for room_dimensions in room_dimensions_list:
    print("-----------------------------------------------------------------")
    print("Room Dimensions: ")
    print(room_dimensions)
    for num_sources in source_counts:
        print("Number Of Sources:")
        print(num_sources)
        
        # Calculate room dimensions
        #min_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
        #max_dimension = max(2.5, (room_volume / 2.5) ** (1 / 3))
        #room_dimensions = [np.random.uniform(min_dimension, max_dimension),
        #                    np.random.uniform(min_dimension, max_dimension),
        #                    np.random.uniform(min_dimension, max_dimension)]
        #room_dimensions=[18,18,18]
        # Split the room into two halves
        #room_dimensions=[15,15,5]
        directoryUnzoomed = os.path.join("Dataset", f"{room_dimensions[0]}_{room_dimensions[1]}_{room_dimensions[2]}_{num_sources}","Unzoomed")
        os.makedirs(directoryUnzoomed,exist_ok=True)
        half_length = room_dimensions[0] / 2
        
        # Calculate absorption
        #e_absorption, max_order = pra.inverse_sabine(rt60, room_dimensions)

        #print("Room Dimensions:")
        #print(room_dimensions)

        room = pra.ShoeBox(room_dimensions, fs=sample_rate)#, materials=pra.Material(e_absorption), max_order=max_order)
        sources=[]
        signals=[]
        # Add sources
        for _ in range(num_sources):
            source_position = [np.random.uniform(0,half_length),
                                np.random.uniform(0, room_dimensions[1]),
                                source_height]
            sources.append(np.round(source_position,2))
            #print("Source Position:")
            #print(np.round(source_position,2))
            
        for source in (sources):
            sig=corpus[np.random.randint(0,dataset_num_samples)].data.astype(float)
            room.add_source(source,signal=sig)
            signals.append(sig)
            #room.sources[]

        # Add microphone
        microphone_position = [room_dimensions[0], room_dimensions[1]/2, microphone_height]
        #microphone_position = [1.5,1.5,1.7]
        room.add_microphone(microphone_position)#,directivity=dir_obj)
        #print("Microphone Position")
        #print(microphone_position)
        # Compute RIR
        #print("Compute UNZOOMED AUDIO-------------------SIMULATE")
        room.simulate()#reference_mic=0,snr=-10)
        #print(len(room.mic_array.signals[0]))
        write(f"{directoryUnzoomed}/{microphone_position[0]}_{microphone_position[1]}_{microphone_position[2]}.wav", sample_rate, room.mic_array.signals[0].astype(np.int16))
        file_count+=1
        
        
        
        #plt.title("Signal Wave...")
        #plt.plot(room.mic_array.signals[0])
        #plt.show()
        
        directoryZoomed = os.path.join("Dataset", f"{room_dimensions[0]}_{room_dimensions[1]}_{room_dimensions[2]}_{num_sources}","Zoomed")
        os.makedirs(directoryZoomed,exist_ok=True)
        
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
                room = pra.ShoeBox(room_dimensions, fs=sample_rate)
                #Add Sources
                idx=0
                for source in (sources):
                    room.add_source(source,signal=signals[idx])
                    #print("Source Position:")
                    #print(source)
                    idx+=1
                
                #Add Microphone
                room.add_microphone(microphone_position)



                #print(microphone_position)
                room.simulate()
                #print("Compute------------------------------------------")
                
                write(f"{directoryZoomed}/{microphone_position[0]}_{microphone_position[1]}_{microphone_position[2]}.wav", sample_rate, room.mic_array.signals[0].astype(np.int16))
                file_count+=1
                
                coordinatex=(microphone_position[0]-(room_dimensions[0]/2))/(room_dimensions[0]/2)
                coordinatex=np.round(1-coordinatex,2)
                coordinatey=np.round(microphone_position[1]/room_dimensions[1],2)
                length=np.round(len(room.mic_array.signals[0])/sample_rate,2)
                jsonData={f"{room_dimensions[0]}_{room_dimensions[1]}_{room_dimensions[2]}_{num_sources}/{microphone_position[0]}_{microphone_position[1]}_{microphone_position[2]}":{
                        "wav":f"{directoryZoomed}/{microphone_position[0]}_{microphone_position[1]}_{microphone_position[2]}.wav",
                        "length":length,
                        "coordinates":[coordinatex,coordinatey],
                        "noisy_wav":f"{directoryUnzoomed}/{microphone_position[0]}_{microphone_position[1]}_{microphone_position[2]}.wav"
                }}
                
                with open(json_file, 'r') as f:
                    existing_data = json.load(f)

                # Update existing data with new data
                existing_data.update(jsonData)

                # Write updated data back to JSON file
                with open(json_file, 'w') as f:
                    json.dump(existing_data, f, indent=4)
                    
                
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
            # Plot RIR (optional)
            # room.plot_rir()
            
            # Save RIR or further processing
            # Save or process room impulse response here
    exit()

print("Total Number of files: ")
print(file_count)
