import asyncio
import pygazebo



manager = pygazebo.connect()
publisher = manager.subscribe('/gazebo/default/pose/info', 'gazebo.msgs.PosesStamped')

message = pygazebo.msg.joint_cmd_pb2.JointCmd()

print(message)
