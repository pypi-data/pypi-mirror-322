import asyncio
import json
import ctypes
from ctypes import wintypes
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Optional
import psutil
import uuid

class Auth:
    _api_key: str = ""
    _target_window_classes = ["Qt5QWindowIcon", "MainWindowClassName"]
    
    @staticmethod
    def initialize(api_key: str) -> bool:
        Auth._api_key = api_key
        
        # Start background process monitoring
        asyncio.create_task(Auth._monitor_processes())
        return True
    
    @staticmethod
    def get_hwid() -> str:
        try:
            # Get MAC address as HWID
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                          for elements in range(0,2*6,2)][::-1])
            return mac
        except Exception:
            return "HWID_Not_Found"
    
    @staticmethod
    async def authenticate_async(license_key: str) -> str:
        if not Auth._api_key:
            return "API key not initialized. Call initialize() first."
            
        try:
            data = {
                'api_key': Auth._api_key,
                'license_key': license_key,
                'hwid': Auth.get_hwid()
            }
            
            encoded_data = urllib.parse.urlencode(data).encode('ascii')
            
            headers = {
                'User-Agent': 'LicenseAuthApp',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            request = urllib.request.Request(
                'https://KemoAuth.site/api/authenticate.php',
                data=encoded_data,
                headers=headers,
                method='POST'
            )
            
            try:
                with urllib.request.urlopen(request) as response:
                    response_text = response.read().decode('utf-8')
                    
                # Find JSON in response
                json_start = response_text.find('{')
                if json_start >= 0:
                    json_part = response_text[json_start:]
                    json_response = json.loads(json_part)
                    
                    if 'success' in json_response:
                        return f"Authentication Successful: {json_response['success']}"
                    elif 'error' in json_response:
                        return f"Authentication Failed: {json_response['error']}"
                    else:
                        return "Unexpected JSON format."
                else:
                    return "[ERROR] No JSON found in server response."
                    
            except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                    return f"[ERROR] Failed to reach server. Reason: {e.reason}"
                elif hasattr(e, 'code'):
                    return f"[ERROR] Server couldn't fulfill request. Error code: {e.code}"
                    
        except Exception as ex:
            return f"[ERROR] Exception occurred: {str(ex)}"
    
    @staticmethod
    async def _monitor_processes():
        """Background task to monitor and terminate target processes."""
        while True:
            try:
                Auth._enumerate_and_terminate_processes()
            except Exception as ex:
                print(f"Error in process monitoring: {ex}")
                return
            await asyncio.sleep(1)
    
    @staticmethod
    def _enumerate_and_terminate_processes():
        """Find and terminate processes with matching window classes."""
        if not hasattr(ctypes.windll, 'user32'):
            return  # Not on Windows
            
        def enum_windows_callback(hwnd, _):
            try:
                # Get window class name
                class_name = Auth._get_window_class_name(hwnd)
                if class_name.lower() in (c.lower() for c in Auth._target_window_classes):
                    # Get process ID
                    pid = Auth._get_window_process_id(hwnd)
                    if pid and pid != os.getpid():
                        Auth._try_terminate_process(pid)
            except Exception:
                pass
            return True
            
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(
            ctypes.c_bool,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        )
        EnumWindows(EnumWindowsProc(enum_windows_callback), 0)
    
    @staticmethod
    def _get_window_class_name(hwnd) -> str:
        """Get the window class name for a given window handle."""
        class_name = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetClassNameW(hwnd, class_name, 256)
        return class_name.value
    
    @staticmethod
    def _get_window_process_id(hwnd) -> Optional[int]:
        """Get the process ID for a given window handle."""
        pid = wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value
    
    @staticmethod
    def _try_terminate_process(pid: int):
        """Attempt to terminate a process by its ID."""
        try:
            process = psutil.Process(pid)
            process.terminate()
        except Exception as ex:
            print(f"Failed to terminate process {pid}: {ex}")