# To read https://github.com/ci-group/pygazebo/blob/py2to3/test_pygazebo_msgs.py

import asyncio

import pygazebo
from msg.v11 import world_stats_pb2
#import pygazebo.msg.joint_cmd_pb2


async def subscriber_loop():
    print('hello1')
    manager = await pygazebo.connect()
    print(manager)
    

    async def callback2(data):
        print(data)
        message = world_stats_pb2.WorldStatistics.ParseFromString(data)
        print(message)

    subscriber = manager.subscribe('/gazebo/world/world_stats', 'gazebo.msgs.WorldStatistics',callback2)
    print(dir(subscriber),'\n')

    print(subscriber.__dict__)

'''
    while True:
        await subscriber.wait_for_connection()
        print('hello2')
        await asyncio.sleep(1)
        print(subscriber)
'''

loop = asyncio.get_event_loop()
loop.run_until_complete(subscriber_loop())
