import os
import yaml

import shercon.sources
import shercon.triggers
import shercon.actions

class Client:
    def __init__(self, configs=[]):
        self.configs = configs
        self.tasks = []

    def __validate_data(self, data):
        # TODO, validate all fields
        # TODO, validate if trigger: file exists
        # TODO, validate if actions exists and have right arguments
        data["trigger_file"] = os.path.join(
            "shercon", "triggers", "%s.py" % data["trigger"].lower()
        )
        for action, value in data["actions"].items():
            data["actions"][action]["file"] = os.path.join(
                "shercon", "actions", "%s.py" % action.lower()
            )

        return data

    def __validate_file(self, config):
        with open(config, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError("YAML error in %s: %s" % (config, exc))

    def __parse(self):
        for config in self.configs:
            data = self.__validate_file(config)
            data = self.__validate_data(data)

            self.tasks.append(data)

    def verify(self):
        self.__parse()

    def __parse_file(self, f):
        sources = ""
        with open(f, 'r') as input:
            input.readline()
            for line in input:
                if '"""' in line:
                    break
                sources += line
        return yaml.safe_load(sources)

    def __execute_source(self, source, args):
        if args:
            return shercon.sources.plugins.get(source).run(*args)
        return shercon.sources.plugins.get(source).run()

    def __execute_sources(self, sources):
        if not sources:
            return []

        data = []
        for source in sources:
            data.append(
                self.__execute_source(source["module"], source.get("args"))
            )

        return data

    def __run_action(self, action, options):
        sources = self.__parse_file(options["file"])
        data = self.__execute_sources(sources)
        # TODO verify max age
        shercon.actions.plugins.get(action).run(*data, config=options["args"])

    def __run_task(self, task):
        # TODO
        # parse trigger
        # parse action
        sources = self.__parse_file(task["trigger_file"])
        data = self.__execute_sources(sources)

        trigger = shercon.triggers.plugins.get(task["trigger"])
        if trigger.run(*data, config=task["args"]):
            for action, options in task["actions"].items():
                self.__run_action(action, options)

    def single(self):
        self.__parse()
        for task in self.tasks:
            self.__run_task(task)

    def loop(self):
        self.__parse()
        # TODO, schedule tasks based on interval