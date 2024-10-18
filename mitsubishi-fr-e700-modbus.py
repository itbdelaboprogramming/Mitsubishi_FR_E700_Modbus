#!/usr/bin/env python
#title           :mitsubishi-fr-e700-modbus.py
#description     :Reads data from FR-E700 Mitsubishi via Modbus RTU.
#author          :Fajar Muhammad Noor Rozaqi (adapted)
#version         :0.2
#usage           :Frequency, Voltage, Current Monitoring System
#python_version  :3.8

import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import datetime

# Setup Modbus RTU connection to FR-E700 Mitsubishi
client = ModbusClient(
    method='rtu',
    port='/dev/ttyUSB1',  # Adjust to your serial port
    baudrate=9600,
    timeout=2,
    stopbits=1,
    bytesize=8,
    parity='E'  # Even parity
)

# Connect to the client
if client.connect():
    print("Connected to FR-E700 Mitsubishi")

    try:
        while True:
            # Get current time
            timer = datetime.datetime.now()

            # Read Modbus registers for frequency, current, and voltage using hexadecimal addresses
            frequency = client.read_holding_registers(0x0200, count=2, unit=1)  # Output frequency
            current = client.read_holding_registers(0x0201, count=2, unit=1)    # Output current
            voltage = client.read_holding_registers(0x0202, count=2, unit=1)    # Output voltage

            # Extract the register values
            if frequency.isError() or current.isError() or voltage.isError():
                print("Error reading registers")
                continue  # Skip this loop iteration if there's an error

            output_frequency = (frequency.registers[0] << 16 | frequency.registers[1]) / 100.0  # Assuming scale of 100
            output_current = (current.registers[0] << 16 | current.registers[1]) / 100.0        # Assuming scale of 100
            output_voltage = (voltage.registers[0] << 16 | voltage.registers[1]) / 10.0         # Assuming scale of 10

            # Print the values
            print(f"Time: {timer.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Output Frequency: {output_frequency} Hz")
            print(f"Output Current: {output_current} A")
            print(f"Output Voltage: {output_voltage} V")
            print("")

            # Sleep for 5 seconds before the next read
            time.sleep(5)

    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()
        print("Connection closed.")
else:
    print("Failed to connect to FR-E700 Mitsubishi")
