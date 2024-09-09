from edgesync360edgehubedgesdk.EdgeAgent import EdgeAgent
from edgesync360edgehubedgesdk.Model.Edge import BlockConfig, EdgeAgentOptions
from edgesync360edgehubedgesdk.Model.Edge import (
  EdgeAgentOptions,
  DCCSOptions,
  EdgeConfig,
  NodeConfig,
  DeviceConfig,
  AnalogTagConfig,
  DiscreteTagConfig,
  TextTagConfig
)
import edgesync360edgehubedgesdk.Common.Constants as constant
import time

def on_connected(agent: EdgeAgent, isConnected: bool):
  if isConnected:
    print('connect success')

def on_disconnected(agent: EdgeAgent, isDisconnected: bool):
  if isDisconnected:
    print('disconnected')

def main():
  options = EdgeAgentOptions(
    reconnectInterval = 1,                                # MQTT reconnect interval in seconds.
    nodeId = 'e58192e0-6420-11ef-a616-6fad91acf168',      # Get from portal
    deviceId = 'device1',                                 # If the type is Device, deviceId must be input. 
    type = constant.EdgeType['Gateway'],                  # Configure the edge as a Gateway or Device. The default setting is Gateway.
    heartbeat = 60,                                       # The default is 60 seconds.
    dataRecover = True,                                   # Whether to recover data when disconnected
    connectType = constant.ConnectType['DCCS'],           # Connection type (DCCS, MQTT). The default setting is DCCS.
    DCCS = DCCSOptions(
      apiUrl = 'http://api-dccs-ensaas.isghpc.wise-paas.com/',         # DCCS API URL
      credentialKey = '132431dfe90de02abefc01806a46f68s'  # Credential key
    )
  )

  agent = EdgeAgent(options)
  agent.on_connected = on_connected
  agent.on_disconnected = on_disconnected
  agent.connect()

  while agent.isConnected() == False:
    print('check connecting ...')
    time.sleep(1)

  print('connected!')
  config = EdgeConfig()

  # set node config
  nodeConfig = NodeConfig(nodeType = constant.EdgeType["Device"])
  config.node = nodeConfig

  # set device config
  deviceConfig = DeviceConfig(
    id = 'Device1',
    name = 'Device 1',
    deviceType = 'Device Type',
    description = 'Description'
  )

  # set block config
  blockConfig = BlockConfig(
    blockType = 'Pump',
    analogTagList = [
      AnalogTagConfig(
        name = 'ATag',
        description = 'AnalogTag',
        readOnly = True,
        arraySize = 0,
        spanHigh = 10,
        spanLow = 0,
        engineerUnit = 'cm',
        integerDisplayFormat = 2,
        fractionDisplayFormat = 4
      )
    ],
    discreteTagList = [
      DiscreteTagConfig(
        name = 'DTag',
        description = 'DiscreteTag',
        readOnly = False,
        arraySize = 0,
        state0 = '1',
        state1 = '0',
        state2 = None,
        state3 = None,
        state4 = None,
        state5 = None,
        state6 = None,
        state7 = None
      )
    ],
    textTagList = [
      TextTagConfig(
        name = 'TTag',
        description = 'TextTag',
        readOnly = True,
        arraySize = 0
      )
    ]
  )

  # add block
  deviceConfig.addBlock('Pump01',blockConfig)
  deviceConfig.addBlock('Pump02',blockConfig)

  # add not block tag
  # notBlockTag = AnalogTagConfig(
  #   name = 'not block tag',
  #   description = 'AnalogTag',
  #   readOnly = True,
  #   arraySize = 0,
  #   spanHigh = 10,
  #   spanLow = 0,
  #   engineerUnit = 'cm',
  #   integerDisplayFormat = 2,
  #   fractionDisplayFormat = 4
  # )
  # deviceConfig.analogTagList.append(notBlockTag)

  nodeConfig.deviceList.append(deviceConfig)
  config.node = nodeConfig

  # upload config
  result = agent.uploadConfig(constant.ActionType['Delsert'], edgeConfig = config)
  print(result)

  while True:
    print('waiting')
    time.sleep(1)


if __name__ == "__main__":
  main()
