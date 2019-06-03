import logging

logger = logging.getLogger(__name__)

def is_bot_message(slack_event):
    return slack_event.get("subtype") =="bot_message"

def is_in_thread(slack_event):
    return slack_event.get("thread_ts") is not None

def is_edit_message(slack_event):
    return slack_event.get("subtype") =="message_changed"

def format_response_for_hot_words(hot_words):
    retval = "\n".join([hot_word.explain() for hot_word in hot_words])
    return retval

def respond_with_no_hot_words_found():
    return {
        "text": "Sorry, but we couldn't find any explainable words in that message.",
        "response_type": "ephemeral"
    }

def respond_with_acronym_information(hot_words):
    return {
        "text": format_response_for_hot_words(hot_words),
        "response_type": "ephemeral"
    }

def fetch_most_recent_message_from_channel(client, channel):
    response = client.api_call("channels.history", channel=channel, count=1)
    if response['ok']:
        try:
            return response['messages'][0]['text']
        except (IndexError, AttributeError) as e:
            logger.warning(f"Unable to pull from channel with id {channel}. No messages in it?")
            return None
    else:
        logger.error(f"Client was unable to read channel history: {response['error']}")
        return None