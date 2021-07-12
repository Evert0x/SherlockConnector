import os
import click

from shercon import Client

@click.group()
def cli():
    pass

if __name__ == "__main__":
    cli()

def get_configs(config):
    configs = []

    if os.path.isfile(config):
        configs = [config]
    elif os.path.isdir(config):
        for filename in os.listdir(config):
            configs.append(os.path.join(config, filename))
        raise ValueError("Directories not supported yet")
    else:
        raise ValueError("Supply file or directory")

    return configs

@cli.command("verify")
@click.argument("config")
def verify(config):
    """
    Based on configs, check if all mentioned source,actions,triggers are valid
    """
    configs = get_configs(config)

    c = Client(configs)
    c.verify()

@cli.command("single")
@click.argument("config")
@click.option('-v', '--verify', is_flag=True)
def watch(config, verify):
    """
    Run all actions defined in the config a single time, ignoring interval.
    """
    configs = get_configs(config)
    if verify:
        c.verify()

    c = Client(configs)
    c.single()