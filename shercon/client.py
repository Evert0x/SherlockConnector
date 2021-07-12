import os
import yaml

import shercon.sources
import shercon.triggers
import shercon.actions

def parse_file(f):
    sources = ""
    with open(f, 'r') as i:
        i.readline()
        for line in i:
            if '"""' in line:
                break
            sources += line
    return yaml.safe_load(sources)

class DataValidator:
    def __init__(self, data):
        self.data = data

    def __validate_config_fields(self):
        assert type(self.data.get("interval")) == int, "Invalid interval"
        assert type(self.data.get("max-age")) == int, "Invalid max-age"
        assert type(self.data.get("trigger")) == str, "Invalid trigger"
        assert type(self.data.get("args")) == dict, "Invalid args"
        assert type(self.data.get("actions")) == dict, "Invalid actions"

        for k, v in self.data["actions"].items():
            assert type(v) == dict, "Invalid action value"
            assert type(v.get("max-age")) == int, "Invalid max-age in action %s" % k
            assert type(v.get("args")) == dict, "Invalid args in action %s" % k

    def __validate_sources(self, sources):
        assert type(sources) == list, "Invalid sources"
        for source in sources:
            assert type(source.get("module")) == str, "Source: invalid module"

            source_object = shercon.sources.plugins.get(source["module"])
            assert source_object != None, "Source: not a source"

            assert type(source.get("args")) == list, "Source: invalid args"

    def __validate_trigger(self):
        trigger = shercon.triggers.plugins.get(self.data["trigger"])
        assert trigger != None, "Trigger %s not found" % self.data["trigger"]
        assert os.path.isfile(self.data["trigger_file"]), "invalid file"

        self.__validate_sources(parse_file(self.data["trigger_file"]))

    def __validate_actions(self):
        actions = self.data.get("actions")
        assert type(actions) == dict, "Invalid action"

        for k, v in actions.items():
            action_object = shercon.actions.plugins.get(k)
            assert action_object != None, "Source: not a source"
            assert os.path.isfile(v["file"]), "invalid file"

            self.__validate_sources(parse_file(v["file"]))

    def validate(self):
        self.__validate_config_fields()
        self.__validate_trigger()
        self.__validate_actions()

class Client:
    def __init__(self, configs=[]):
        self.configs = configs
        self.tasks = []

    def __enrich_data(self, data):
        data["trigger_file"] = os.path.join(
            "shercon", "triggers", "%s.py" % data["trigger"].lower()
        )
        for action, value in data["actions"].items():
            data["actions"][action]["file"] = os.path.join(
                "shercon", "actions", "%s.py" % action.lower()
            )

        return data

    def __load_file(self, config):
        with open(config, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError("YAML error in %s: %s" % (config, exc))

    def __parse(self):
        for config in self.configs:
            data = self.__load_file(config)
            data = self.__enrich_data(data)
            self.tasks.append(data)

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
        sources = parse_file(options["file"])
        data = self.__execute_sources(sources)
        # TODO verify max age
        shercon.actions.plugins.get(action).run(*data, config=options["args"])

    def __run_task(self, task):
        sources = parse_file(task["trigger_file"])
        data = self.__execute_sources(sources)

        trigger = shercon.triggers.plugins[task["trigger"]]
        if trigger.run(*data, config=task["args"]):
            for action, options in task["actions"].items():
                self.__run_action(action, options)

    def verify(self):
        self.__parse()
        for task in self.tasks:
            DataValidator(task).validate()

    def single(self):
        self.__parse()
        for task in self.tasks:
            self.__run_task(task)

    def loop(self):
        self.__parse()
        # TODO, schedule tasks based on interval