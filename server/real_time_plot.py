import numpy as np
from matplotlib import pyplot as plt

def main():
    plt.axis([0,5.5,-1.25,1.25])
    plt.ion()
    plt.show()

    value = 0
    x_value = 0
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
            x = x[1:]
            y = y[1:]
            x = x - 0.05
            x_value  = x[-1] + 0.05
            plt.clf()
            plt.axis([0,5.5,-1.25,1.25])

            
    

if __name__ == '__main__':
    main()