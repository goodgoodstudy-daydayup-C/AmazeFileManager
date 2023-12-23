import sys
import time

import uiautomator2 as u2

def custom_wait(seconds=2):
    for i in range(seconds):
        print("等待 1 秒...")
        time.sleep(1)

def connect_to_avd(avd_serial):
    return u2.connect(avd_serial)

def launch_amaze_file_manager(device):
    device.app_start("com.amaze.filemanager.debug")
    custom_wait()

def wait_for_app_start(device, package_name):
    while True:
        current_app = device.app_current()
        if current_app['package'] == package_name:
            break
        time.sleep(2)

def click_element(device, element_class, element_description=None):
    if element_description:
        out = device(className=element_class, description=element_description).click()
    else:
        out = device(className=element_class).click()

    if not out:
        print(f"成功：点击 {element_description}" if element_description else f"成功：点击 {element_class}")
    custom_wait()

def stop_uiautomator_service(device):
    while True:
        device.service("uiautomator").stop()
        time.sleep(2)
        if not device.service("uiautomator").running():
            print("断开连接 UIAutomator2 成功")
            break
        time.sleep(2)

if __name__ == '__main__':
    avd_serial = sys.argv[1]
    d = connect_to_avd(avd_serial)
    launch_amaze_file_manager(d)
    wait_for_app_start(d, "com.amaze.filemanager.debug")

    click_element(d, "android.widget.ImageButton", "map_cache.db")
    click_element(d, "android.widget.TextView", "Open with")
    click_element(d, "android.widget.CheckedTextView", "database")

    stop_uiautomator_service(d)
