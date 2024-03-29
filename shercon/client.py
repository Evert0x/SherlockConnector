import os
import yaml
import datetime
import time

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
        self.waiters = {}
        self.timers = {}

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
            data["id"] = config
            self.tasks.append(data)

    def __execute_source(self, source, args, config):
        if args:
            return shercon.sources.plugins.get(source).run(*args, config=config)
        return shercon.sources.plugins.get(source).run(config=config)

    def __execute_sources(self, sources, config):
        if not sources:
            return []

        data = []
        for source in sources:
            data.append(
                self.__execute_source(
                    source["module"],
                    source.get("args"),
                    config
                )
            )

        return data

    def __run_action(self, action, options, config):
        sources = parse_file(options["file"])
        data = self.__execute_sources(sources, config)
        # TODO verify max age
        return shercon.actions.plugins.get(action).run(
            *data, starg=options["args"], config=config
        )

    def __run_task(self, task):
        sources = parse_file(task["trigger_file"])
        data = self.__execute_sources(sources, task["config"])

        trigger = shercon.triggers.plugins[task["trigger"]]
        if trigger.run(*data, starg=task["args"], config=task["config"]):
            for action, options in task["actions"].items():
                self.waiters[task["id"]] = self.__run_action(
                    action, options, task["config"]
                )

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

        while True:
            start = datetime.datetime.now()

            for task in self.tasks:
                last = self.timers.get(task["id"], datetime.datetime.min)
                now = datetime.datetime.now()

                if (now-last).seconds < task["interval"]:
                    continue

                waiter = self.waiters.get(task["id"])
                if waiter:
                    if not waiter.verify_done():
                        continue
                    del self.waiters[task["id"]]

                error = (now-last).seconds - task["interval"]
                if last != datetime.datetime.min and error > 5:
                    print("Execution error of %s seconds for %s" % (
                        error, task["id"]
                    ))

                self.__run_task(task)
                # Can also be `datetime.datetime.now()`, but like this
                # It will execute on interval defined in config
                self.timers[task["id"]] = now

            # Dont do too many loopy loopy
            if (datetime.datetime.now() - start).seconds < 3:
                time.sleep(1)