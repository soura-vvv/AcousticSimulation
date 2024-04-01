from email.mime import audio
from random import sample
import pyroomacoustics as pra
import numpy as np
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

room_dimensions=[100,100,100]
sample_rate=16000

room = pra.AnechoicRoom(fs=sample_rate)
room.add_source([10,10,10])
room.add_microphone([100,100,100])
room.compute_rir()
print(len(room.rir[0]))
write("exampleRIR.wav", sample_rate, room.rir[0][0].astype(np.int16))