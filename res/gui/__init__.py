# ________________________________________________________
# Those lines are here due to the fact that i am unable to set Qt Designer correctly
# It adds import of resources without the relative path of project
# E.g. it should be from . import logo_rc
# But it is just a import logo_rc
# So i make resources globaly avaiable
# This should be fixed before some kind of main release
# import sys
# sys.path.append("C:\\VSCode\\PassWordManager\\res\\gui")
import sys
import os

# Assuming the current script is located in the passwordmanager directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# ________________________________________________________

from .gui import MainGuiHandler