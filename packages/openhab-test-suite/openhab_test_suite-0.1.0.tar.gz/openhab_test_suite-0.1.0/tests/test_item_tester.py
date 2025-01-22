from openhab_test_suite import OpenHABConnector, ItemTester

# Establishing connection to the OpenHAB API
connector = OpenHABConnector("http://127.0.0.1:8080", "openhab", "habopen")

# Instantiating the ItemTester
tester = ItemTester(connector)

# Test for doesItemExist
print(f"doesItemExists: ", tester.doesItemExist(itemName="testColor"))

# Test for checkItemIsType
print(f"checkItemIsType: ", tester.checkItemIsType(itemName="testColor", itemType="Color"))

# Test for checkItemHasState
print(f"checkItemHasState: ", tester.checkItemHasState(itemName="testColor", state="ON"))

# Test for testColor
print(f"testColor: ", tester.testColor(itemName="testColor", command="255,0,0", expectedState="255,0,0"))

# Test for testContact
print(f"testContact: ", tester.testContact(itemName="testContact", update="CLOSED", expectedState="CLOSED"))

# Test for testDateTime
print(f"testDateTime: ", tester.testDateTime(itemName="testDateTime", command="2025-01-20T06:38:12.813337920-0800", expectedState="2025-01-20T06:38:12.813337920-0800"))

# Test for testDimmer
print(f"testDimmer: ", tester.testDimmer(itemName="testDimmer", command=50, expectedState=50))

# Test for testImage
#print(f"testImage: ", tester.testImage(itemName="testImage", command="", expectedState=""))

# Test for testLocation
print(f"testLocation: ", tester.testLocation(itemName="testLocation", update="48.054398,8.205645,0.1", expectedState="48.054398,8.205645,0.1"))

# Test for testNumber
print(f"testNumber: ", tester.testNumber(itemName="testNumber", command=42, expectedState=42))

# Test for testPlayer
print(f"testPlayer: ", tester.testPlayer(itemName="testPlayer", command="PLAY", expectedState="PLAY"))

# Test for testRollershutter
print(f"testRollershutter: ", tester.testRollershutter(itemName="testRollershutter", command="DOWN", expectedState="100"))

# Test for testString
print(f"testString: ", tester.testString(itemName="testString", command="Hello", expectedState="Hello"))

# Test for testSwitch
print(f"testSwitch: ", tester.testSwitch(itemName="testSwitch", command="ON", expectedState="ON"))
