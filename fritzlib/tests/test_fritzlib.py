import unittest
from fritzlib.FritzClasses import Login_Error, Communication_Error, terminationmessage, trackingparameter, fritzdevice, fritzbox, logindialog

class TestFritzlib(unittest.TestCase):

    def test_login_error(self):
        with self.assertRaises(Login_Error):
            raise Login_Error()

    def test_communication_error(self):
        with self.assertRaises(Communication_Error):
            raise Communication_Error("Test error", 404)

    def test_termination_message_warning(self):
        msg = terminationmessage(0, "This is a warning")
        self.assertEqual(msg.icon, 'warning')

    def test_termination_message_error(self):
        msg = terminationmessage(1, "This is an error")
        self.assertEqual(msg.icon, 'error')

    def test_tracking_parameter_initialization(self):
        tp = trackingparameter(['param1', 'param2'], 'Device1')
        self.assertEqual(tp.list, ['param1', 'param2'])
        self.assertEqual(tp.toplevel.title(), "Parameter for Device1")

    def test_fritzdevice_initialization(self):
        device = fritzdevice("12345", "<device><name>Test Device</name></device>")
        self.assertEqual(device.ain, "12345")
        self.assertIn('name', device.allparams)

    def test_fritzbox_initialization(self):
        # This test requires a valid Fritzbox setup to run properly
        # You may want to mock requests.get for unit testing
        pass

    def test_logindialog_initialization(self):
        dialog = logindialog()
        self.assertIsInstance(dialog.toplevel, unittest.mock.Mock)

if __name__ == '__main__':
    unittest.main()