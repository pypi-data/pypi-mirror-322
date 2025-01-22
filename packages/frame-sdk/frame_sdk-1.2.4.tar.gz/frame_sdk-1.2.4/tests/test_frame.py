import unittest
import asyncio
import time

from frame_sdk import Frame
from frame_sdk.camera import Quality

class TestFrame(unittest.IsolatedAsyncioTestCase):
    async def test_send_lua(self):
        async with Frame() as f:

            self.assertEqual(await f.run_lua("print('hi')", await_print=True), "hi")

            self.assertIsNone(await f.run_lua("print('hi')"))
            await asyncio.sleep(0.1)

            with self.assertRaises(Exception):
                await f.run_lua("a = 1", await_print=True, timeout=1)


    async def test_send_data(self):
        async with Frame() as f:
            await f.run_lua(
                "frame.bluetooth.receive_callback((function(d)frame.bluetooth.send(d)end))"
            )

            self.assertEqual(await f.bluetooth.send_data(b"test", await_data=True), b"test")

            self.assertIsNone(await f.bluetooth.send_data(b"test"))
            await asyncio.sleep(0.1)

            await f.run_lua("frame.bluetooth.receive_callback(nil)")

            with self.assertRaises(Exception):
                await f.bluetooth.send_data(b"test", await_data=True)

    async def test_long_send(self):
        """
        Test sending lua over the MTU limit to the device and ensure it still works.
        """
        async with Frame() as f:
            a_count = 32
            script = "a = 0;" + " ".join(f"a = a + 1;" for _ in range(a_count)) + "print(a)"
            response = await f.send_long_lua(script, await_print=True)
            self.assertEqual(str(a_count), response)
            
            a_count = 250
            script = "a = 0;" + " ".join(f"a = a + 1;" for _ in range(a_count)) + "print(a)"
            response = await f.send_long_lua(script, await_print=True)
            self.assertEqual(str(a_count), response)
        
    async def test_long_receive(self):
        """
        Test receiving lua over the MTU limit from the device and ensure it still works.
        """
        async with Frame() as f:
            self.assertEqual(await f.run_lua("prntLng('hi')", await_print=True), "hi")
            msg = "hello world! "
            msg = msg + msg
            msg = msg + msg
            msg = msg + msg
            msg = msg + msg
            msg = msg + msg
            await f.run_lua("msg = \"hello world! \";msg = msg .. msg;msg = msg .. msg;msg = msg .. msg;msg = msg .. msg;msg = msg .. msg", await_print=False)
            self.assertEqual("about to send 416 characters.",(await f.run_lua("print('about to send '..tostring(string.len(msg))..' characters.')", await_print=True)))
            self.assertEqual(msg, await f.evaluate("msg"))

    async def test_long_send_and_receive(self):
        """
        Test sending and receiving lua over the MTU limit to the device and ensure it still works.
        """
        async with Frame() as f:
            a_count = 2
            message = "".join(f"and #{i}, " for i in range(a_count))
            script = "message = \"\";" + "".join(f"message = message .. \"and #{i}, \"; " for i in range(a_count)) + "print(message)"
            response = await f.run_lua(script, await_print=True)
            self.assertEqual(message, response)
            
            a_count = 50
            message = "".join(f"and #{i}, " for i in range(a_count))
            script = "message = \"\";" + "".join(f"message = message .. \"and #{i}, \"; " for i in range(a_count)) + "print(message)"
            response = await f.run_lua(script, await_print=True)
            self.assertEqual(message, response)
        
    async def test_battery(self):
        async with Frame() as f:
            self.assertGreater(await f.get_battery_level(), 0)
            self.assertLessEqual(await f.get_battery_level(), 100)
            self.assertAlmostEqual(await f.get_battery_level(), int(float(await f.evaluate("frame.battery_level()"))), delta=15)
            
    async def test_sleep(self):
        async with Frame() as f:
            await f.run_lua("test_var = 1")
            self.assertAlmostEqual(int(float(await f.evaluate("frame.time.utc()"))), int(time.time()), delta=5)
            await f.sleep()
            self.assertEqual(await f.evaluate("test_var"), '1')
            self.assertFalse(f.camera.is_awake)

if __name__ == "__main__":
    unittest.main()