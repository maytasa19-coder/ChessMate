#!/usr/bin/env python3
import time
import rospy
from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from armpi_pro import bus_servo_control

rospy.init_node('arm_quick_test', anonymous=True)
joints_pub = rospy.Publisher('/servo_controllers/port_id_1/multi_id_pos_dur', MultiRawIdPosDur, queue_size=1)
time.sleep(0.5)  # המתנה קצרה לחיבור ה-Publisher

# הזזת מנוע הבסיס (ID 6) הצידה למשך 1.5 שניות
bus_servo_control.set_servos(joints_pub, 1.5, ((6, 350),))
time.sleep(2.0)

# החזרת מנוע הבסיס למרכז (500)
bus_servo_control.set_servos(joints_pub, 1.5, ((6, 500),))
time.sleep(2.0)
print("Done!")