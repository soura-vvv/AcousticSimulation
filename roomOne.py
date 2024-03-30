import pyroomacoustics as pra
import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt

#Initialize Parameters
sampleRate=16000



#Room Dimensions

# The desired reverberation time and dimensions of the room
rt60 = 0.5  # seconds
room_dim = [9, 7.5, 3.5]  # meters

# We invert Sabine's formula to obtain the parameters for the ISM simulator
e_absorption, max_order = pra.inverse_sabine(rt60, room_dim)

# Create the room
room = pra.ShoeBox(
    room_dim, fs=sampleRate, materials=pra.Material(e_absorption), max_order=max_order
)

#room=pra.ShoeBox(room_dim,fs=sampleRate,max_order=10)

room.plot();

room.add_source([2,5,5]);

room.add_microphone([8,5,5]);

#fig, ax = room.plot(mic_marker_size=30)
#ax.set_xlim([0,11])
#ax.set_ylim([0,11])
#ax.set_zlim([0,11]);

room.compute_rir()

#plt.figure()
#room.plot_rir()
#plt.grid()
#print(len(room.rir[0][2]))
#t60 = pra.experimental.measure_rt60(room.rir[0][0], fs=room.fs, plot=True)
#print(f"The RT60 is {t60 * 1000:.0f} ms")
