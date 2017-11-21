import matplotlib.pyplot as plt
import numpy as np
plt.style.use("ggplot")

def play():
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x))
    ax.plot(x, np.cos(x))

    return fig
