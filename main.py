import random
import time

from simulationWindow import SimulationWindow

if __name__ == '__main__':
    random.seed(2020)

    simulation_window = SimulationWindow()
    simulation_window.start()

    try:
        while simulation_window.is_alive():
            time.sleep(1)
    except:
        simulation_window.stop()

    simulation_window.join()
