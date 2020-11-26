#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # set default setting path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    # execute command
    execute_from_command_line(sys.argv)
