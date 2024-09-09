# EdgeSync360 EdgeHub Python SDK Example

This project provides a graphical user interface (GUI) for testing the Edge SDK using Python. The application uses `tkinter` to interact with the SDK, which supports both MQTT and DCCS connection types.

## Features

- **Connect and Disconnect** : Connect to and disconnect from the edge using MQTT or DCCS protocols.

- **Send Data** : Send simulated data to the edge.

- **Update Device Status** : Send device status updates.

- **Upload, Update, and Delete Configurations** : Manage edge configurations.

- **View Real-time Data** : Display and manage real-time data from the edge.

## Requirements

- Python 3.x

- `tkinter`

- `edgesync360edgehubedgesdk` package

## Installation

1. Clone the repository:

```複製程式碼
git clone <repository-url>
```

2. Install dependencies:

```複製程式碼
pip install -r requirements.txt
```

Ensure `edgesync360edgehubedgesdk` is available. You might need to install it from a private repository or other source.

## Usage

### Running the GUI Application

Run the `main.py` script to start the GUI application:

```複製程式碼
python main.py
```

### GUI Components

- **Tabs** : The application contains two tabs:

  - **DCCS** : Configure settings for DCCS.
  - **MQTT** : Configure settings for MQTT.

- **Input Fields** :

  - **NodeId** : Required for connection.
  - **Device Count** , **Analog Tag Count** , **Discrete Tag Count** , **Text Tag Count** : Used to simulate data.
  - **Data Frequency** : Set how frequently data is sent.

- **Buttons** :

  - **Connect** : Establish a connection with the edge.
  - **Disconnect** : Disconnect from the edge.
  - **Update Device Status** : Update the device status.
  - **Send Data** : Send simulated data.
  - **Upload Config** : Upload a new configuration.
  - **Update Config** : Update the existing configuration.
  - **Delete All Config** : Delete all configurations.
  - **Delete Devices** : Delete devices.
  - **Delete Tag** : Delete tags.

### Console Script

The `console.py` script provides a command-line interface (CLI) for interacting with the SDK. It demonstrates how to connect to the edge and configure it programmatically.Run the `console.py` script:

```複製程式碼
python console.py
```

### Configuration

Update the following parameters in `main.py` and `console.py` as needed:

- **DCCS API URL** : The API endpoint for DCCS.

- **Credential Key** : The key used for authentication with DCCS.

- **MQTT HostName and Port** : The address and port for MQTT.

- **Username and Password** : The credentials for MQTT.

## Code Overview

- **`main.py`** : Provides a GUI for interacting with the Edge SDK, including configuration and data handling.

- **`console.py`** : Demonstrates how to use the SDK via a command-line interface.
