import numpy as np
from matplotlib import pyplot as plt

# def rt_plot(x1, x2):
#     global data1
#     data1 = np.append(data1, x1)


if __name__=='__main__':
    plt.axis([0,5.5,-1.25,1.25])
    plt.ion()
    plt.show()

    value = 0
    x_value = 0
    start = 1
    x = np.array([0])
    y = np.array([0])
    while True:   # plot x^1, x^2, ..., x^4
        x = np.append(x, x_value)
        y = np.append(y, np.sin(value))
        plt.plot(x, y, color='b')
        plt.draw()
        plt.pause(0.001)
        x_value += 0.05
        value += 0.05
        if len(x) > 100:
            plt.axis([x[start],x[start]+5,-1.25,1.25])
            start += 1