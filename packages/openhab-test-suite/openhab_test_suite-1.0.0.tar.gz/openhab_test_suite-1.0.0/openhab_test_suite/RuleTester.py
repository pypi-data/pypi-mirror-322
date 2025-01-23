import time
from .OpenHABConnector import OpenHABConnector
import json
from openhab import CRUD

class RuleTester:
    def __init__(self, connector: OpenHABConnector):
        """
        Initializes the RuleTester with an OpenHAB connector.

        :param connector: The OpenHABConnector instance used to communicate with the OpenHAB system.
        """
        self.connector = connector

    def runRule(self, ruleUid: str) -> bool:
        """
        Executes a rule immediately.

        :param ruleUid: The UID of the rule to be executed.
        :return: True if the rule was executed successfully, False otherwise.
        """
        if self.isRuleDisabled(ruleUid):
            print(f"Error: Rule {ruleUid} could not be executed because it is disabled.")
            return False

        endpoint = f"/rules/{ruleUid}/runnow"
        # Sending JSON data
        data = {}  # Add necessary data here if required
        response = self.connector.post(endpoint, header={"Content-type": "application/json", "Accept": "application/json"}, data=json.dumps(data))

        print(response.text)

        if response and response.status_code == 200:
            print(f"Rule {ruleUid} executed successfully.")
            return True
        print(f"Error executing rule {ruleUid}. Response: {response}")
        return False

    def enableRule(self, ruleUid: str) -> bool:
        """
        Enables a rule.

        :param ruleUid: The UID of the rule to be enabled.
        :return: True if the rule was successfully enabled, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}/enable"
        data = "true"
        header = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}

        # Performing the POST request
        response = self.connector.post(endpoint, header=header, data=data)

        if response and response.status_code == 200:
            print(f"Rule {ruleUid} enabled successfully.")
            return True
        print(f"Error enabling rule {ruleUid}. Response: {response}")
        return False

    def disableRule(self, ruleUid: str) -> bool:
        """
        Disables a rule.

        :param ruleUid: The UID of the rule to be disabled.
        :return: True if the rule was successfully disabled, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}/enable"
        data = "false"
        header = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}

        # Performing the POST request
        response = self.connector.post(endpoint, header=header, data=data)

        if response and response.status_code == 200:
            print(f"Rule {ruleUid} disabled successfully.")
            return True
        print(f"Error disabling rule {ruleUid}. Response: {response}")
        return False

    def testRuleExecution(self, ruleUid: str, expectedItem: str, expectedValue: str) -> bool:
        """
        Tests the execution of a rule and verifies the expected outcome.

        :param ruleUid: The UID of the rule to be tested.
        :param expectedItem: The item to check after rule execution.
        :param expectedValue: The expected value of the item.
        :return: True if the test was successful, otherwise False.
        """
        try:
            # Run the rule
            if not self.runRule(ruleUid):
                print(f"Error: Rule {ruleUid} could not be executed.")
                return False

            # Short pause for rule execution
            time.sleep(2)

            # Retrieve the state of the item
            crud = CRUD(self.connector.url, self.connector.username, self.connector.password)
            testItem = crud.read(expectedItem)
            state = testItem.get("state")
            
            if state is None or state != expectedValue:
                print(f"Error: State of item {expectedItem} after rule execution does not match. Expected: {expectedValue}, Found: {state}")
                return False

            print(f"{expectedItem} state after rule execution: {state}")
            return state == expectedValue
        except Exception as e:
            print(f"Error during rule test execution: {e}")
            return False

    def isRuleActive(self, ruleUid: str) -> bool:
        """
        Checks if the rule is active.

        :param ruleUid: The UID of the rule to check.
        :return: True if the rule is active, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}"
        response = self.connector.get(endpoint, header={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNINITIALIZED")
            print(f"Rule status: {status}")
            return status != "UNINITIALIZED"

        # Error case
        print(f"Error retrieving the status of rule {ruleUid}. Response: {response}")
        return False

    def isRuleDisabled(self, ruleUid: str) -> bool:
        """
        Checks if the rule is disabled.

        :param ruleUid: The UID of the rule to check.
        :return: True if the rule is disabled, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}"
        response = self.connector.get(endpoint, header={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status and statusDetail
            status = response.get("status", {}).get("status", "IDLE")
            statusDetail = response.get("status", {}).get("statusDetail", "NONE")
            print(f"Rule status: {status}, Detail: {statusDetail}")

            # Rule is disabled if status is "UNINITIALIZED" and statusDetail is "DISABLED"
            return status == "UNINITIALIZED" and statusDetail == "DISABLED"

        # Error case
        print(f"Error retrieving the status of rule {ruleUid}. Response: {response}")
        return False

    def isRuleRunning(self, ruleUid: str) -> bool:
        """
        Checks if the rule is currently running.

        :param ruleUid: The UID of the rule to check.
        :return: True if the rule is running, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}"
        response = self.connector.get(endpoint, header={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is running if the status is "RUNNING"
            return status == "RUNNING"

        # Error case
        print(f"Error retrieving the status of rule {ruleUid}. Response: {response}")
        return False

    def isRuleIdle(self, ruleUid: str) -> bool:
        """
        Checks if the rule is in the IDLE state.

        :param ruleUid: The UID of the rule to check.
        :return: True if the rule is in the IDLE state, False otherwise.
        """
        endpoint = f"/rules/{ruleUid}"
        response = self.connector.get(endpoint, header={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract the status
            status = response.get("status", {}).get("status", "UNKNOWN")
            print(f"Rule status: {status}")

            # Rule is in the IDLE state if the status is "IDLE"
            return status == "IDLE"

        # Error case
        print(f"Error retrieving the status of rule {ruleUid}. Response: {response}")
        return False

    def getRuleStatus(self, ruleUid: str) -> dict:
        """
        Retrieves the full status of a rule.

        :param ruleUid: The UID of the rule whose status is to be retrieved.
        :return: A dictionary containing status information or an empty dictionary in case of an error.
        """
        endpoint = f"/rules/{ruleUid}"
        response = self.connector.get(endpoint, header={"Accept": "application/json"})

        # Check if the response is a valid dictionary
        if isinstance(response, dict) and "status" in response:
            # Extract status information
            statusInfo = {
                "status": response.get("status", {}).get("status", "UNKNOWN"),
                "statusDetail": response.get("status", {}).get("statusDetail", "UNKNOWN"),
                "editable": response.get("editable", False),
                "name": response.get("name", ""),
                "uid": response.get("uid", ""),
            }
            print(f"Rule status details: {statusInfo}")
            return statusInfo

        # Error case
        print(f"Error retrieving the status of rule {ruleUid}. Response: {response}")
        return {}
