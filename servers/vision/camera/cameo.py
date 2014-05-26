import cv2
from .managers import WindowManager, CaptureManager
from .depth import DepthTracker
from .object_tracker import ObjectTrackerManager


class Cameo(object):

    def __init__(self, left_channel=0, right_channel=1):

        self.window_manager = WindowManager('Debug Window', self.onKeypress)

        # Capture Video Streams for the left and right cameras
        self._leftCaptureManager = CaptureManager(
            cv2.VideoCapture(left_channel), True, channel=0)

        self._rightCaptureManager = CaptureManager(
            cv2.VideoCapture(right_channel), True, channel=1)

        self._objectTrackerManager = ObjectTrackerManager(
            self._leftCaptureManager)

    def start(self, device):
        """ Run `start` from Tango """
        self.device = device

        # Start Video Stream Loop
        self.run()

    def run(self):
        """Run the main loop."""
        self.window_manager.createWindow()
        while self.window_manager.isWindowCreated:

            self._leftCaptureManager.enterFrame()
            left_frame = self._leftCaptureManager.frame

            self._rightCaptureManager.enterFrame()
            right_frame = self._rightCaptureManager.frame

            # Compute disparity
            disparity_frame=DepthTracker.computeDisparity(left_frame,right_frame, ndisparities=16, SADWindowSize=25);

            # Display disparity map
            self.window_manager.show(disparity_frame)

            self._leftCaptureManager.exitFrame()
            self._rightCaptureManager.exitFrame()
            self.window_manager.processEvents()

    def onKeypress(self, keycode):
        """Handle a keypress.

        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.

        """

        if keycode == 32:  # space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9:  # tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
                    'screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:  # escape
            self.window_manager.destroyWindow()
