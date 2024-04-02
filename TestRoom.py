from email.mime import audio
from random import sample
import pyroomacoustics as pra
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from pyroomacoustics.directivities import (
    DirectivityPattern,
    DirectionVector,
    CardioidFamily,
)
dir_obj = CardioidFamily(
    orientation=DirectionVector(azimuth=90, colatitude=15, degrees=True),
    pattern_enum=DirectivityPattern.CARDIOID,
)

room_dimensions=[10,10,10]
sample_rate=16000

room = pra.ShoeBox(room_dimensions, fs=sample_rate,max_order=10)
room.add_source([1,1,5])
room.add_microphone([9,9,5])
room.image_source_model()

room.compute_rir()
print(room.rir[0][0])
plt.figure(1)
plt.title("Signal Wave...")
plt.plot(room.rir[0][0])
plt.show()
write("exampleRIR.wav", sample_rate, room.rir[0][0].astype(np.int16))
