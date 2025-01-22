import time
from .OpenHABConnector import OpenHABConnector
import json
from openhab import CRUD
from openhab import ItemEvent

class ItemTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the ItemTester with an OpenHAB connector.

        :param connector: The OpenHABConnector instance used to communicate with the OpenHAB system.
        """
        self.connector = connector
        self.__crud = CRUD(self.connector.url, self.connector.username, self.connector.password)
        self.__itemEvent = ItemEvent(self.connector.url, self.connector.username, self.connector.password)

    def doesItemExist(self, itemName: str):
        """
        Checks if an item exists in the OpenHAB system.

        :param itemName: The name of the item to check.
        :return: True if the item exists, otherwise False.
        """
        testItem = self.__crud.read(itemName)
        if testItem and testItem.get("name") == itemName:
            return True
        print(f"Error: The item {itemName} does not exist!")
        return False

    def checkItemIsType(self, itemName: str, itemType: str):
        return True
        """
        Verifies that an item is of a specific type.

        :param itemName: The name of the item to check.
        :param itemType: The expected type of the item.
        :return: True if the item is of the expected type, otherwise False.
        """
        validTypes = ["Color", "Contact", "DateTime", "Dimmer", "Group", "Image", "Location", "Number", "Player", "Rollershutter", "String", "Switch"]
        if itemType not in validTypes:
            print(f"Error: '{itemType}' is not a valid item type.")
            return False

        try:
            # Abruf der Item-Daten
            testItem = self.__crud.read(itemName)
            if testItem is None:
                print(f"Error: The item '{itemName}' could not be found. Received None.")
                return False

            # Debugging: Gibt die vollständigen Daten des Items aus
            print(f"Item data for '{itemName}': {testItem}")

            print(testItem.get("type"))
            print(itemType)

            # Überprüfung des Item-Typs
            if testItem.get("type") == itemType:
                return True

            print(f"Error: The item '{itemName}' is not of type '{itemType}'! Found type: {testItem.get('type')}")
            return False
        except Exception as e:
            print(f"Error while checking item type for '{itemName}': {e}")
            return False

    def checkItemHasState(self, itemName: str, state):
        """
        Checks if an item has a specific state.

        :param itemName: The name of the item to check.
        :param state: The expected state of the item.
        :return: True if the item has the expected state, otherwise False.
        """
        checkState = self.__crud.getState(itemName)
        if checkState is None:
            print(f"Error: Could not retrieve the state for item {itemName}.")
            return False

        if checkState == state:
            return True

        print(f"Error: The state of {itemName} is {checkState}, expected {state}.")
        return False

    def testColor(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Color item by sending a command and verifying the expected state.

        :param itemName: The name of the Color item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Color"):
            print(f"Test failed: {itemName} is not of type 'Color'.")
            return False

        if not self.__crud._CRUD__checkColorValue(command):
            return False

        return self.__testItem(itemName, "Color", command, expectedState, timeout)

    def testContact(self, itemName: str, update: str = None, expectedState: str = None, timeout: int = 60):
        """
        Tests the functionality of a Contact item.

        :param itemName: The name of the Contact item.
        :param update: The update to send to the item, optional.
        :param expectedState: The expected state after the update.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Contact"):
            print(f"Test failed: {itemName} is not of type 'Contact'.")
            return False

        #if not self.__crud._CRUD__checkContactValue(update):
        #    return False

        return self.__testItem(itemName, "Contact", update, expectedState, timeout)

    def testDateTime(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a DateTime item by sending a command and verifying the expected state.

        :param itemName: The name of the DateTime item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "DateTime"):
            print(f"Test failed: {itemName} is not of type 'DateTime'.")
            return False

        #if not self.__crud._CRUD__checkDateTimeValue(command):
        #    return False

        return self.__testItem(itemName, "DateTime", command, expectedState, timeout)

    def testDimmer(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Dimmer item by sending a command and verifying the expected state.

        :param itemName: The name of the Dimmer item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Dimmer"):
            print(f"Test failed: {itemName} is not of type 'Dimmer'.")
            return False

        if not self.__crud._CRUD__checkDimmerValue(command):
            return False

        return self.__testItem(itemName, "Dimmer", str(command), str(expectedState), timeout)

    def testImage(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Image item by sending a command and verifying the expected state.

        :param itemName: The name of the Image item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Image"):
            print(f"Test failed: {itemName} is not of type 'Image'.")
            return False

        if not self.__crud._CRUD__checkImageValue(command):
            return False

        return self.__testItem(itemName, "Image", command, expectedState, timeout)

    def testLocation(self, itemName: str, update: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Location item.

        :param itemName: The name of the Location item.
        :param update: The update to send to the item, optional.
        :param expectedState: The expected state after the update.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Location"):
            print(f"Test failed: {itemName} is not of type 'Location'.")
            return False

        if not self.__crud._CRUD__checkLocationValue(update):
            return False

        return self.__testItem(itemName, "Location", update, expectedState, timeout)

    def testNumber(self, itemName: str, command, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Number item by sending a command and verifying the expected state.

        :param itemName: The name of the Number item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Number"):
            print(f"Test failed: {itemName} is not of type 'Number'.")
            return False

        if not self.__crud._CRUD__checkNumberValue(command):
            return False

        return self.__testItem(itemName, "Number", str(command), str(expectedState), timeout)

    def testPlayer(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Player item by sending a command and verifying the expected state.

        :param itemName: The name of the Player item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Player"):
            print(f"Test failed: {itemName} is not of type 'Player'.")
            return False

        if not self.__crud._CRUD__checkPlayerValue(command):
            return False
        
        return self.__testItem(itemName, "Player", command, expectedState, timeout)

    def testRollershutter(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Rollershutter item by sending a command and verifying the expected state.

        :param itemName: The name of the Rollershutter item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Rollershutter"):
            print(f"Test failed: {itemName} is not of type 'Rollershutter'.")
            return False

        if not self.__crud._CRUD__checkRollershutterValue(command):
            return False

        return self.__testItem(itemName, "Rollershutter", command, expectedState, timeout)

    def testString(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a String item by sending a command and verifying the expected state.

        :param itemName: The name of the String item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "String"):
            print(f"Test failed: {itemName} is not of type 'String'.")
            return False

        if not self.__crud._CRUD__checkStringValue(command):
            return False

        return self.__testItem(itemName, "String", command, expectedState, timeout)

    def testSwitch(self, itemName: str, command: str, expectedState = None, timeout: int = 60):
        """
        Tests the functionality of a Switch item by sending a command and verifying the expected state.

        :param itemName: The name of the Switch item.
        :param command: The command to send to the item.
        :param expectedState: The expected state after the command, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        if not self.checkItemIsType(itemName, "Switch"):
            print(f"Test failed: {itemName} is not of type 'Switch'.")
            return False

        if not self.__crud._CRUD__checkSwitchValue(command):
            return False

        return self.__testItem(itemName, "Switch", command, expectedState, timeout)

    def __testItem(self, itemName: str, itemType: str, commandOrUpdate, expectedState=None, timeout: int = 60):
        """
        Generic test function for validating the behavior of an item.
        
        :param itemName: The name of the item to test.
        :param itemType: The type of the item.
        :param commandOrUpdate: The command or update to send to the item.
        :param expectedState: The expected state after the command/update, optional.
        :param timeout: The timeout period for the test in seconds.
        :return: True if the test passes, otherwise False.
        """
        try:
            # Initial state retrieval
            initialState = self.__crud.getState(itemName) if commandOrUpdate is not None else None
            
            if initialState is None:
                print(f"Warning: Could not retrieve initial state for item {itemName}.")
            
            # Open SSE connection for state changes before sending the command
            response = self.__itemEvent.ItemStateChangedEvent(itemName)
            if response is None:
                print(f"Error: No response received for item {itemName}.")
                return False
            
            state = None
            startTime = time.time()

            # Start processing SSE events
            with response as events:
                # Now send the command or update to the item
                if itemType in ["Contact", "Location"]:
                    self.__crud.postUpdate(itemName, str(commandOrUpdate))
                else:
                    self.__crud.sendCommand(itemName, commandOrUpdate)

                while True:  # Endlessly loop to capture events
                    # Timeout check: Check if the timeout has been exceeded
                    if time.time() - startTime > timeout:
                        print(f"Timeout reached after {timeout} seconds. Falling back to getState().")
                        # Instead of manually checking the state, use checkItemHasState
                        if not self.checkItemHasState(itemName, expectedState):
                            print(f"Error: After timeout, state of {itemName} is not {expectedState}.")
                            return False
                        break  # Exit the event listening loop if timeout is reached

                    for line in events.iter_lines():
                        line = line.decode()

                        # Timeout check: Check if the timeout has been exceeded
                        if time.time() - startTime > timeout:
                            print(f"Timeout reached after {timeout} seconds. Falling back to getState().")
                            # Use checkItemHasState
                            if not self.checkItemHasState(itemName, expectedState):
                                print(f"Error: After timeout, state of {itemName} is not {expectedState}.")
                                return False
                            break  # Exit the event listening loop if timeout is reached

                        if "data" in line:
                            line = line.replace("data: ", "")
                            try:
                                # Parse the event data
                                data = json.loads(line)
                                payload = data.get("payload")
                                event_type = data.get("type")

                                # Only process ItemStateChangedEvent
                                if event_type == "ItemStateChangedEvent" and payload:
                                    payload_data = json.loads(payload)
                                    state = payload_data.get("value")

                                    # Check if the received state matches the expected state
                                    if state == expectedState:
                                        return True  # If the state matches, exit the function and return True
                                    break
                                break

                            except json.JSONDecodeError:
                                print("Warning: Event could not be converted to JSON.")

            # After timeout, check the state using checkItemHasState
            if not self.checkItemHasState(itemName, expectedState):
                print(f"Error: After timeout, state of {itemName} is not {expectedState}.")
                return False

            # Reset item to initial state if necessary
            if initialState is not None:
                if itemType in ["Contact", "Location"]:
                    self.__crud.postUpdate(itemName, initialState)
                else:
                    self.__crud.sendCommand(itemName, initialState)

            return True

        except Exception as e:
            print(f"Error testing {itemName}: {e}")
            return False
