# Simulator
The Simulator is a comprehensive simulation platform for activity recognition and behavioral modeling within smart home environments.
It reproduces user interactions with domestic objects and environmental sensors, enabling a context-aware understanding of daily activities and the generation of alternative behavioral scenarios.

The simulated activities exhibit realistic temporal and contextual patterns, closely reflecting real-world behaviors and providing a reliable basis for training and testing classification algorithms for human activity recognition and behavior analysis.


## Requirements
- Python **3.12+**
- Python packages:
  - `pandas`
  - `matplotlib`
  - `pillow`  (PIL)

## Project Structure
- **activity.py**: defines the logic for activity recognition.  
- **automatic.py**: enables the automatic simulation mode, divided into two variants: *folder mode* and *user path mode*.  
- **common.py**: contains functions and variables used throughout the simulation and helps prevent cyclic imports between files.  
- **consumption_profiles.py**: defines a consumption profile for each device that can be created, as well as functions to calculate energy consumption during the simulation.  
- **device.py**, **door.py**, **wall.py**, **read.py**, **point.py**, and **sensor.py**: used to build the simulation scenario.  
- **graph.py** and **log.py**: generate graphs and logs of sensor behavior at the end of both manual and automatic simulations.  
- **timer.py**: creates and manages the simulation timer.  
- **sim.py**: contains all the methods and functions that allow the user to interact with the scenario during manual simulation.  
- **utils.py**: provides utility functions used in multiple parts of the project.  
- **main.py**: serves as the main entry point that connects all the other modules. To use the simulator, simply run this file.  
- **read_scenario.txt** and **saved.txt**: the first file stores the configuration of a scenario that can be loaded before the simulation; the second file saves the configuration created by the user.  
- **images/** folder: contains three images — one for the avatar (*omino.png*) and two for the canvas grid.

## Installation
1. Download or clone this repository.
2. Open the folder in your IDE (e.g., VS Code, PyCharm).
3. Use Python **3.12** or later.
4. Run `main.py`.

> The project only imports the libraries it uses.  
> If your environment is missing any of them, install them with:
> `pip install <library-name>`

## License
boh

## Author
