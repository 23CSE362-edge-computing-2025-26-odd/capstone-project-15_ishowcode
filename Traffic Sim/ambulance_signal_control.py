import traci
import sumolib
import time

# Configuration
SUMO_BINARY = "sumo-gui"  # or "sumo" for CLI
CONFIG_FILE = "map.sumocfg"
AMBULANCE_ID = "ambulance_1"
JUNCTIONS = ["J1", "J2", "J3", "J4", "J5", "J6"]

# Map ambulance route to junctions it will cross
AMBULANCE_ROUTE_JUNCTIONS = ["J1", "J2", "J3"]

# Helper: set all signals to red except one
def set_signals_for_ambulance(green_junction):
    for junction in JUNCTIONS:
        if junction == green_junction:
            # Set all links to green
            logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(junction)[0]
            green_state = "G" * len(logic.getPhases()[0].state)
            traci.trafficlight.setRedYellowGreenState(junction, green_state)
        else:
            logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(junction)[0]
            red_state = "r" * len(logic.getPhases()[0].state)
            traci.trafficlight.setRedYellowGreenState(junction, red_state)

# Main simulation loop
if __name__ == "__main__":
    import subprocess
    import os
    sumo_cmd = [SUMO_BINARY, "-c", CONFIG_FILE]  # Removed --start to wait for user
    traci.start(sumo_cmd)
    ambulance_active = False
    last_junction = None
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if AMBULANCE_ID in traci.vehicle.getIDList():
            ambulance_active = True
            # Use getNextTLS to find the next traffic light the ambulance will encounter
            tls_list = traci.vehicle.getNextTLS(AMBULANCE_ID)
            if tls_list:
                junction = tls_list[0][0]  # traffic light id
                if junction != last_junction:
                    set_signals_for_ambulance(junction)
                    last_junction = junction
        elif ambulance_active:
            # Reset signals to normal after ambulance passes
            for junction in JUNCTIONS:
                traci.trafficlight.setProgram(junction, "0")
            ambulance_active = False
            last_junction = None
    traci.close()
    print("Simulation finished.")
