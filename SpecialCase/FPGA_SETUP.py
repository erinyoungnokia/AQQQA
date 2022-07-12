import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions
import matplotlib.pyplot as plt

SETUP_FPGA = True
FPGA_Wait = 660

Set = Set_Up.Set_Up()
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)