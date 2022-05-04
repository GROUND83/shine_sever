#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sonoff


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # s = sonoff.Sonoff("wonchang.k@gmail.com", "Flslwl1212", "as")
    # devices = s.get_devices()
    # print(devices)
    # if devices:
    #     # We found a device, lets turn something on
    #     device_id = devices[0]["deviceid"]
    #     for device in devices:
    #         print(device)
    #     # s.switch('on', device_id, None)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":

    main()
