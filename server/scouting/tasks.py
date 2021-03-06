import json

import server.config as s_config
import server.model.connection

engine = server.model.connection.engine
conn = engine.connect()


class Task(object):
    def __init__(self, line):
        value = line.split(',')
        self.actor = value[0]
        self.task = value[1]
        self.claim = value[2]
        self.auto = value[3]
        self.teleop = value[4]
        self.finish = value[5]
        self.success = value[6]
        self.miss = value[7]
        self.enums = value[8]


class TaskDal(object):
    @staticmethod
    def sqltasks():
        results = conn.execute("SELECT * FROM games")

        out = ''
        for line in results:
            task = Task(line)
            data = json.dumps(task, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)
            out += data + '\n'
        return out

    #todo(Stacy) Update code to use get_season function
    @staticmethod
    def csvtasks():
        with open(s_config.season(s_config.current_season, "gametasks.csv"), "r") as text:
            out = ''
            for line in text:
                if 'actor,task' not in line:
                    task = Task(line)
                    data = json.dumps(task, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)
                    out += data + '\n'
            return out
