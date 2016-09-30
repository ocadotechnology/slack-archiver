import logging
import slacker
import time

LOGGER = logging.getLogger(__name__)


def run(api_token, inactivity_days, valid_channel_regex, check_interval):
    slack = slacker.Slacker(api_token)

    try:
        slack.api.test()
    except slacker.Error as err:
        LOGGER.error("Test API call failed: %s", err)
        raise SystemExit(1)

    while True:
        channels = list(find_channels(slack, inactivity_days, valid_channel_regex))
        LOGGER.debug("Found %d channels for archiving", len(channels))

        for channel, reason in channels:
            LOGGER.info("Archiving channel %s: %s", channel['name'], reason)
            slack.channels.archive(channel['id'])

        time.sleep(check_interval)


def find_channels(client, inactivity_days, matcher):
    channels = client.channels.list(exclude_archived=True)
    for channel in channels.body['channels']:
        # Check for the regex
        if not matcher.match(channel['name']):
            continue

        if channel['num_members'] == 0:
            # Channel is empty, archive it
            yield channel, 'empty'
            continue

        latest_message = get_latest_real_channel_message(client, channel)
        print 'M', latest_message['ts'], time.time() - inactivity_days * 60*60*24
        if float(latest_message['ts']) < time.time() - inactivity_days * 60*60*24:
            # Last message is older than inactivity timeout, archive it
            yield channel, 'inactive'
            continue


def get_latest_real_channel_message(client, channel):
    for message in get_channel_messages(client, channel['id']):
        if message['subtype'] != 'channel_leave':
            return message


def get_channel_messages(client, channel_id):
    has_more = True
    latest = None
    while has_more:
        response = client.channels.history(channel_id)
        has_more = response.body['has_more']
        for message in response.body['messages']:
            latest = message['ts']
            yield message
