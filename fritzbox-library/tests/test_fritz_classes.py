import unittest
from fritzbox_library.fritz_classes import Login_Error, Communication_Error, terminationmessage, trackingparameter, fritzdevice, fritzbox

class TestFritzClasses(unittest.TestCase):

    def test_login_error(self):
        error = Login_Error()
        self.assertIsNotNone(error.occurrence)

    def test_communication_error(self):
        error_message = "Test communication error"
        error_code = 404
        error = Communication_Error(error_message, error_code)
        self.assertEqual(error.message, error_message)
        self.assertEqual(error.error_code, error_code)
        self.assertIsNotNone(error.occurrence)

    def test_termination_message_warning(self):
        message = terminationmessage(0, "This is a warning")
        self.assertEqual(message.icon, 'warning')

    def test_termination_message_error(self):
        message = terminationmessage(1, "This is an error")
        self.assertEqual(message.icon, 'error')

    def test_tracking_parameter_initialization(self):
        params = ['param1', 'param2']
        devicename = "Device1"
        tracking = trackingparameter(params, devicename)
        self.assertEqual(tracking.list, sorted(params))

    def test_fritzdevice_initialization(self):
        ain = "123456789"
        devdetail = "<device><name>Test Device</name></device>"
        device = fritzdevice(ain, devdetail)
        self.assertEqual(device.ain, ain)
        self.assertIn('name', device.allparams)

    def test_fritzbox_initialization(self):
        # This test requires a valid Fritzbox setup to run properly
        # You may want to mock requests and responses for a real test
        pass

if __name__ == '__main__':
    unittest.main()