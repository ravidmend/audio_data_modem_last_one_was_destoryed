import numpy as np
import matplotlib.pyplot as plt

# loaded_vector = np.load('../../withpreamble.npy')
# plt.figure()
# plt.plot(loaded_vector)
# plt.title("with preamble")
# plt.show()

# loaded_vector = np.load('../../withoutpreamble.npy')
# plt.figure()
# plt.plot(loaded_vector)
# plt.title("without preamble")
# plt.show()

loaded_vector = np.load('../../data.npy')
plt.figure()
plt.plot(loaded_vector)
plt.show()


