#!/bin/bash
#### BEGIN INIT INFO
# Provides:          aws.musk
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: wsocket service
# Description:       wsocket service daemon
### END INIT INFO
cd /home/ubuntu/videoTool
/usr/bin/python3.5 /home/ubuntu/videoTool/videoClicksTool.py
