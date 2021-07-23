# Sherlock Connector

`pip install -e .`

Run `yarn fork` on sherlock-v1-periphery repo. Make sure the sherlock address printed at the end of the script matches the on in `config.py`

## TODO

## Implement single tx
Issue: Currently there is a transaction executed for every premium update, these updates can als be grouped in a single transaction

Possible solution:

Actions expose their data (by returning it, or making it available as object attributes), based on actions of all the configs in the `configs` directory. There will be a global config that can overwrite all actual actions (e.g. sending tx) but can read the needed data to send the tx, so action interface will be `prepare()` and `run()`, where `run()` is only called in case the action is not overwritten.

When overwriting all actions, the 'global' actions receives a reference to all prepared actions, which allows it to resolve the issue.