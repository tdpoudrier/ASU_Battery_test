import streamlit as st
import numpy as np
import time
import board
import adafruit_tsl2591
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize sensors
lux_sensor = adafruit_tsl2591.TSL2591(i2c)
adc = ADS.ADS1115(i2c)
data = np.array([])


#initialize clicked session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = not st.session_state.clicked

#Create UI elements
st.write("ASU Battery Test")
test_button_value = st.button("Toggle test", on_click=click_button)
chart = st.line_chart(data)
st.write("Lux sensor value " + str(lux_sensor.lux))

if st.session_state.clicked == True:
    st.write("Test Start Time: " + time.strftime("%Y-%m-%d %X"))

    while st.session_state.clicked == True:
        #Display start time below chart
        lux_value = lux_sensor.lux
        adc_value = AnalogIn(adc, ADS.P0)
        adc_voltage = float(adc_value.voltage)
        
        new_value = np.array([adc_voltage])
        data = np.append(data, adc_voltage)
        chart.add_rows(new_value)
        time.sleep(1)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
