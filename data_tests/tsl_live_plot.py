import time
import board
import adafruit_tsl2591
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []
count = 0

def animate(count):
    lux = sensor.lux
    ys.append(lux)
    xs.append(count)
    count += 1
    ax1.clear()
    ax1.plot(xs,ys)
    
ani = animation.FuncAnimation(fig, animate(count), interval=1000)
plt.show()