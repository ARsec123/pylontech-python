#!/usr/bin/env python

import main
import rospy
from sensor_msgs.msg import BatteryState


def battery_publisher():

    rospy.init_node("battery_publisher", anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz
    battery_state_pub = rospy.Publisher("battery_state", BatteryState, queue_size=10)

    while not rospy.is_shutdown():

        # Read battery state data from main.py file
        battery_state = get_battery_state()

        # Create BatteryState message
        battery_msg = BatteryState()
        battery_msg.header.stamp = rospy.Time.now()
        battery_msg.voltage = battery_state["voltage"]
        battery_msg.cell_voltage = battery_state["cell_Voltages"]
        battery_msg.temperature = battery_state["temperature"]
        # battery_msg.cell_temperature = battery_state[""]
        battery_msg.current = battery_state["current"]
        battery_msg.charge = battery_state["charge"]
        battery_msg.capacity = battery_state["capacity"]
        battery_msg.design_capacity = battery_state["design_capacity"]
        battery_msg.percentage = battery_state["percentage"]
        battery_msg.serial_number = battery_state["serial_number"]
        battery_msg.power_supply_status = battery_state["power_supply_status"]
        battery_msg.power_supply_health = battery_state["power_supply_health"]
        battery_msg.power_supply_technology = battery_state["power_supply_technology"]

        # Publish BatteryState message
        battery_state_pub.publish(battery_msg)

        rate.sleep()


def get_battery_state():
    # Call the get_battery_state() function in main.py to retrieve the battery state data
    battery_state_data = main.battery_state()
    print(battery_state_data)

    # Create a dictionary to store the BatteryState message fields
    battery_state = {}

    # correspond the data from the battery with those of ros sensor_msgs/BatteryState
    battery_state["voltage"] = battery_state_data["Voltage"]
    battery_state["cell_voltage"] = battery_state_data["CellVoltages"]
    battery_state["temperature"] = battery_state_data["Temperatures"]
    battery_state["current"] = battery_state_data["Current"]
    battery_state["charge"] = battery_state_data["ChargeCurrent"]
    battery_state["capacity"] = battery_state_data["RemainCapacity"]
    battery_state["design_capacity"] = battery_state_data["ModuleTotalCapacity"]
    battery_state["percentage"] = battery_state_data["RemainCapacity"] / battery_state_data["ModuleTotalCapacity"]
    battery_state["serial_number"] = battery_state_data["ModuleSerialNumber"]
    battery_state["power_supply_status"] = BatteryState.POWER_SUPPLY_STATUS_DISCHARGING
    battery_state["power_supply_health"] = BatteryState.POWER_SUPPLY_HEALTH_GOOD
    battery_state["power_supply_technology"] = BatteryState.POWER_SUPPLY_TECHNOLOGY_LIPO

    return battery_state


if __name__ == "__main__":
    try:
        battery_publisher()
    except rospy.ROSInterruptException:
        pass
