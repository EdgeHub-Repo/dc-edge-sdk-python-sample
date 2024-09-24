from datetime import datetime
from edgesync360edgehubedgesdk.EdgeAgent import EdgeAgent
from edgesync360edgehubedgesdk.Model.Edge import (
    AzureIotHubOptions,
    BlockConfig,
    EdgeAgentOptions,
    EdgeData,
    EdgeTag,
)
from edgesync360edgehubedgesdk.Model.Edge import (
    EdgeAgentOptions,
    EdgeConfig,
    NodeConfig,
    DeviceConfig,
    AnalogTagConfig,
    DiscreteTagConfig,
    TextTagConfig,
)
import edgesync360edgehubedgesdk.Common.Constants as constant
import time
import random

from edgesync360edgehubedgesdk.Model.Event import MessageReceivedEventArgs


def on_connected(isConnected: bool):
    if isConnected:
        print("connect success")


def on_disconnected(isDisconnected: bool):
    if isDisconnected:
        print("disconnected")


def on_message(messageReceivedEventArgs: MessageReceivedEventArgs):
    # messageReceivedEventArgs format: Model.Event.MessageReceivedEventArgs
    type = messageReceivedEventArgs.type
    message = messageReceivedEventArgs.message
    if type == constant.MessageType["WriteValue"]:
        # message format: Model.Edge.WriteValueCommand
        for device in message.deviceList:
            print("deviceId: {0}".format(device.Id))
            for tag in device.tagList:
                print("tagName: {0}, Value: {1}".format(tag.name, str(tag.value)))
    elif type == constant.MessageType["WriteConfig"]:
        print("WriteConfig")
    elif type == constant.MessageType["TimeSync"]:
        # message format: Model.Edge.TimeSyncCommand
        print(str(message.UTCTime))
    elif type == constant.MessageType["ConfigAck"]:
        # message format: Model.Edge.ConfigAck
        print(f"Upload Config Result: {str(message.result)}")


def main():
    options = EdgeAgentOptions(
        reconnectInterval=1,  # MQTT reconnect interval in seconds.
        nodeId="01f3d322-ef6d-4d6b-ab09-9fb53535b0fc",  # Get from portal
        deviceId="Device1",  # If the type is Device, deviceId must be input.
        type=constant.EdgeType[
            "Gateway"
        ],  # Configure the edge as a Gateway or Device. The default setting is Gateway.
        heartbeat=60,  # The default is 60 seconds.
        dataRecover=True,  # Whether to recover data when disconnected
        connectType=constant.ConnectType[
            "AzureIotHub"
        ],  # Connection type (DCCS, MQTT). The default setting is DCCS.
        AzureIotHub=AzureIotHubOptions(
            connectionString="HostName=edge365-dev.azure-devices.net;DeviceId=01f3d322-ef6d-4d6b-ab09-9fb53535b0fc;SharedAccessKey=DEpzt+DVdH5kAF0KFtw9/16AlNk/oTyPHnJhE5jnuQA=",
        ),
    )

    agent = EdgeAgent(options)
    agent.on_connected = on_connected
    agent.on_disconnected = on_disconnected
    agent.on_message = on_message
    agent.connect()

    config = EdgeConfig()
    # set node config
    nodeConfig = NodeConfig(nodeType=constant.EdgeType["Device"])
    config.node = nodeConfig

    # set device config
    deviceConfig = DeviceConfig(
        id="Device1",
        name="Device 1",
        deviceType="Device Type",
        description="Description",
    )

    # set block config
    blockConfig = BlockConfig(
        blockType="Pump",
        analogTagList=[
            AnalogTagConfig(
                name="ATag",
                description="AnalogTag",
                readOnly=True,
                arraySize=0,
                spanHigh=10,
                spanLow=0,
                engineerUnit="cm",
                integerDisplayFormat=2,
                fractionDisplayFormat=4,
            )
        ],
        discreteTagList=[
            DiscreteTagConfig(
                name="DTag",
                description="DiscreteTag",
                readOnly=False,
                arraySize=0,
                state0="1",
                state1="0",
                state2=None,
                state3=None,
                state4=None,
                state5=None,
                state6=None,
                state7=None,
            )
        ],
        textTagList=[
            TextTagConfig(
                name="TTag", description="TextTag", readOnly=True, arraySize=0
            )
        ],
    )

    # add block
    deviceConfig.addBlock("Pump01", blockConfig)
    deviceConfig.addBlock("Pump02", blockConfig)

    nodeConfig.deviceList.append(deviceConfig)
    config.node = nodeConfig

    # upload config
    result = agent.uploadConfig(constant.ActionType["Delsert"], edgeConfig=config)
    print(result)

    for i in range(0, 10):
        edgeData = EdgeData()
        for tag in deviceConfig.analogTagList:
            deviceId = options.deviceId
            tagName = tag.name
            value = random.uniform(0, 100)
            tag = EdgeTag(deviceId, tagName, value)
            edgeData.tagList.append(tag)
        for tag in deviceConfig.discreteTagList:
            deviceId = options.deviceId
            tagName = tag.name
            value = random.randint(0, 99) % 2
            tag = EdgeTag(deviceId, tagName, value)
            edgeData.tagList.append(tag)
        for tag in deviceConfig.textTagList:
            deviceId = options.deviceId
            tagName = tag.name
            value = "TEST " + str(random.randint(0, 100))
            tag = EdgeTag(deviceId, tagName, value)
            edgeData.tagList.append(tag)

        edgeData.timestamp = datetime.now()
        success = agent.sendData(data=edgeData)
        if success:
            print(f"send data {i+1} success")
        else:
            print(f"send data {i+1} failed")

        time.sleep(1)

    agent.disconnect()


if __name__ == "__main__":
    main()
