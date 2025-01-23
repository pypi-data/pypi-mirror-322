
import logging
from typing import Optional
from simpleCan.util import xldriver
from simpleCan.util.task  import SendMessageTask, RecvMessageTask
from simpleCan.util.messageList import MessageList

__all__ = ['SimpleCan']

class SimpleCan:

    def __init__(self):
        # create a list to store all messages sending to DDU
        self.tasklist = []
        self.messageList = MessageList()
        xldriver.setup()

    def env_setup(self,duration = 360):
        self.messageList.clearMessageList()
        self.messageList.load_default_messageList()
        messageList = self.messageList.get_messageList()
        self.clearTaskList()
        for i in range(len(messageList)):
            self.tasklist.append(SendMessageTask(message_id=messageList[i].id,
                                                 data=messageList[i].data,
                                                 period=messageList[i].period,
                                                 duration=duration))
    def env_run(self):
        for task in self.tasklist:
            task.task_run()
    def sendMessage(self, message_id, data, period, duration = 30):
        task = SendMessageTask(message_id=message_id,
                               data = data,
                               period = period,
                               duration = duration)
        self.tasklist.append(task)
        task.task_run()

    def recvMessage(self, duration:Optional[int]):
        task = RecvMessageTask(duration)
        task.task_run()

    def modifyMessage(self, message_id, data):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    logging.critical(task.get_messageID())
                    task.task_modifyData(newData = data)

        except Exception as e:
            logging.error(e)
    def stopMessage(self, message_id):
        try:
            for task in self.tasklist:
                if task.get_messageID() == message_id:
                    task.task_stop()
        except Exception as e:
            logging.error(e)
    def clearTaskList(self):
        self.tasklist = []
    def endAllTasks(self):
        for task in self.tasklist:
            task.task_stop()

    def __del__(self):
        self.endAllTasks()