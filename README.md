# slack-archiver

A simple python app that will automatically archive public channels if:
* the channel is empty.
* the channel has had no messages or joins for the last X days (i.e. ignoring leaves).

Also the channel must match the channel name regex pattern.

## Use

pip install slack-archiver

```
slack-archiver -h
```

## Configuration

This script uses [ConfigArgParse](https://pypi.python.org/pypi/ConfigArgParse) so
command line switches, config files, or environment variables can be used
