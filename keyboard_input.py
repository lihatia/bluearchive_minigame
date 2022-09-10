from pykeyboard import PyKeyboard
import re
import win32gui
left='a'
right='d'
left_slide_key= "q"
right_slide_key= "e"
start="w"
def left_tap(keyboard):
    keyboard.tap_key(left)

def right_tap(keyboard):
    keyboard.tap_key(right)

def left_slide(keyboard):
    keyboard.tap_key(left_slide_key)

def right_slide(keyboard):
    keyboard.tap_key(right_slide_key)

def left_hold(keyboard):
    keyboard.press_key(left)

def left_endhold(keyboard):
    keyboard.release_key(left)

def right_hold(keyboard):
    keyboard.press_key(right)

def right_endhold(keyboard):
    keyboard.release_key(right)

def both_tap(keyboard):
    keyboard.tap_key(left)
    keyboard.tap_key(right)

def both_hold(keyboard):
    keyboard.press_key(left)
    keyboard.press_key(right)

def both_endhold(keyboard):
    keyboard.release_key(left)
    keyboard.release_key(right)

def retry_button(keyboard):
    keyboard.tap_key(start)

# find the emulator
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def set_handle(self,hwnd):
        self._handle=hwnd
    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

# import time
# keyboard = PyKeyboard()
# w=WindowMgr()
# w.find_window_wildcard("夜神")
# w.set_foreground()
#
# left_tap(keyboard)
# time.sleep(0.5)
# right_tap(keyboard)
# time.sleep(0.5)
# left_slide(keyboard)
# time.sleep(0.5)
# right_slide(keyboard)
