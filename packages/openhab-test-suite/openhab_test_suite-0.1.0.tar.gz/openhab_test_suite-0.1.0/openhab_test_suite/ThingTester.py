from .OpenHABConnector import OpenHABConnector

class ThingTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the ThingTester with the given OpenHAB connector.

        Parameters:
            connector (OpenHABConnector): The OpenHAB connector used to interact with the OpenHAB server.
        """
        self.connector = connector

    def _getThingStatus(self, thingUid: str) -> str:
        """
        Retrieves the status of a Thing based on its UID.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            str: The status of the Thing (e.g., "ONLINE", "OFFLINE", etc.). Returns "UNKNOWN" if status cannot be determined.
        """
        endpoint = f"/rest/things/{thingUid}"
        response = self.connector.get(endpoint)

        if response:
            statusInfo = response.get("statusInfo", {})
            return statusInfo.get("status", "UNKNOWN")
        return "UNKNOWN"

    def isThingStatus(self, thingUid: str, statusToCheck: str) -> bool:
        """
        Checks whether a Thing has the specified status.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.
            statusToCheck (str): The status to check against (e.g., "ONLINE", "OFFLINE").

        Returns:
            bool: True if the Thing has the specified status, False otherwise.
        """
        return self._getThingStatus(thingUid) == statusToCheck

    def isThingOnline(self, thingUid: str) -> bool:
        """
        Checks if a Thing is ONLINE.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is ONLINE, False otherwise.
        """
        return self.isThingStatus(thingUid, "ONLINE")

    def isThingOffline(self, thingUid: str) -> bool:
        """
        Checks if a Thing is OFFLINE.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is OFFLINE, False otherwise.
        """
        return self.isThingStatus(thingUid, "OFFLINE")

    def isThingPending(self, thingUid: str) -> bool:
        """
        Checks if a Thing is in PENDING status.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in PENDING status, False otherwise.
        """
        return self.isThingStatus(thingUid, "PENDING")

    def isThingUnknown(self, thingUid: str) -> bool:
        """
        Checks if a Thing is in UNKNOWN status.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNKNOWN status, False otherwise.
        """
        return self.isThingStatus(thingUid, "UNKNOWN")

    def isThingUninitialized(self, thingUid: str) -> bool:
        """
        Checks if a Thing is in UNINITIALIZED status.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in UNINITIALIZED status, False otherwise.
        """
        return self.isThingStatus(thingUid, "UNINITIALIZED")

    def isThingError(self, thingUid: str) -> bool:
        """
        Checks if a Thing is in ERROR state.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing.

        Returns:
            bool: True if the Thing is in ERROR state, False otherwise.
        """
        return self.isThingStatus(thingUid, "ERROR")

    def enableThing(self, thingUid: str) -> bool:
        """
        Enables a Thing by sending a PUT request to activate it.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing to be enabled.

        Returns:
            bool: True if the Thing was successfully enabled, False otherwise.
        """
        endpoint = f"/rest/things/{thingUid}/enable"
        data = "true"  # Enables the Thing (plain text "true")
        header = {"Content-Type": "text/plain"}
        
        # Execute PUT request
        response = self.connector.put(endpoint, header=header, data=data)
        
        if response and response.status_code == 200:
            print(f"Thing {thingUid} was successfully enabled.")
            return True
        print(f"Error enabling Thing {thingUid}. Response: {response}")
        return False

    def disableThing(self, thingUid: str) -> bool:
        """
        Disables a Thing by sending a PUT request to deactivate it.

        Parameters:
            thingUid (str): The unique identifier (UID) of the Thing to be disabled.

        Returns:
            bool: True if the Thing was successfully disabled, False otherwise.
        """
        endpoint = f"/rest/things/{thingUid}/enable"
        data = "false"  # Disables the Thing (plain text "false")
        header = {"Content-Type": "text/plain"}

        # Execute PUT request
        response = self.connector.put(endpoint, header=header, data=data)

        if response and response.status_code == 200:
            print(f"Thing {thingUid} was successfully disabled.")
            return True
        print(f"Error disabling Thing {thingUid}. Response: {response}")
        return False
