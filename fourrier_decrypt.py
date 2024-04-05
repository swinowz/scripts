import numpy as np

data = np.fromfile("fftea", dtype=np.complex64)

decrypted_data = np.fft.fft(data, n=64)


flag = bytes(np.round(decrypted_data.real).astype(int))
flag_txt = flag[::4]

print(flag_txt)
