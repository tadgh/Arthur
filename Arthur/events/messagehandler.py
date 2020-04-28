import logging

from nltk import ngrams
from nltk.tokenize import word_tokenize
from rest_framework import status
from rest_framework.response import Response
from slack import WebClient

from Arthur import settings
from events.models import HotWord, SlackMessage, Utterance
from events.slackhelper import is_bot_message, is_in_thread, is_edit_message, respond_with_acronym_information, \
    fetch_most_recent_message_from_channel, respond_with_no_hot_words_found, respond_with_no_valid_messages

SLACK_SIGNING_SECRET = getattr(settings, 'SLACK_SIGNING_SECRET', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)

logger = logging.getLogger(__name__)
bot_client = WebClient(SLACK_BOT_USER_TOKEN)

def parse_define_command(payload):
    text = payload.get('text')
    parts = text.split(":")
    if len(parts) != 2:
        logger.info(f"Failed to define a keyword, wrong format: {text}")
        return None, None
    else:
        return parts

def extract_hot_words_from_message(text):
    unigrams = list(word_tokenize(text))
    bigrams = list(ngrams(unigrams, 2))
    joined_bigrams = [" ".join(bigram) for bigram in bigrams]

    grams_to_check = unigrams + joined_bigrams

    return HotWord.objects.filter(text__in=grams_to_check)

def handle_explain(slash_payload):
    message = slash_payload.get("text")
    channel_id = slash_payload.get("channel_id")
    caller = slash_payload.get("user_id")
    logger.debug(slash_payload)
    if len(message) == 0:
        logger.info("No message passed to /explain command, fetching most recent message.")

        message = fetch_most_recent_message_from_channel(caller, bot_client, channel_id)
    if not message:
        return Response(respond_with_no_valid_messages(), status=status.HTTP_200_OK)

    logger.info(f"pulling hotwords from [{message}]")
    hot_words = extract_hot_words_from_message(message)
    if hot_words.count() > 0:
        return Response(respond_with_acronym_information(hot_words), status=status.HTTP_200_OK)
    else:
        return Response(respond_with_no_hot_words_found(), status=status.HTTP_200_OK)

def _respond_with_help():
    return f"Sorry, I didn't understand that. Try a message like this: `/define TGIF : Thank god it's friday!`. The messages must follow the format of `/define <word> : <definition>` with a colon separating them."

def _respond_already_exists(hotword):
    return f"Sorry, looks like that word has already been defined as: *{hotword.meaning}*"

def classify_hotword(hotword):
    if hotword.isupper():
        return HotWord.ACRONYM
    else:
        return HotWord.BUZZWORD

def _respond_successfully_saved_response(hotword):
    return f"Successfully defined *{hotword.text}* as *{hotword.meaning}*"

def handle_define(slash_payload):
    text, definition = parse_define_command(slash_payload)
    if text is None or definition is None:
        outcome_response = _respond_with_help()
    else:
        try:
            text = text.strip()
            found = HotWord.objects.get(text=text)
            outcome_response = _respond_already_exists(found)
        except HotWord.DoesNotExist:
            hotword = HotWord.objects.create(
                text=text,
                meaning=definition,
                type=HotWord.classify(text)
            )
            outcome_response = _respond_successfully_saved_response(hotword)
    return Response(data={"response_type": "ephemeral", "text": outcome_response}, status=status.HTTP_200_OK)


def handle_event(event_message):
    if  is_bot_message(event_message) or is_in_thread(event_message) or is_edit_message(event_message):
        return Response(status=status.HTTP_200_OK)

    user = event_message.get("user")
    text = event_message.get("text")
    channel = event_message.get("channel")
    hot_words = extract_hot_words_from_message(text)

    if hot_words.count() > 0:
        record_hot_word_usage(channel, text, hot_words, user)

    return Response(status=status.HTTP_200_OK)


def record_hot_word_usage(channel, message, hot_words, utterer):
    # Create a SlackMessage
    slack_message = SlackMessage.objects.create(
        utterer=utterer,
        message=message,
        channel=channel
    )
    logger.info(f"Found a valid SlackMessage that contained [{len(hot_words)}] hotwords: {slack_message}")

    # For every hot word found, create an utterance.
    for hot_word in hot_words:
        utterance = Utterance.objects.create(
            original_context=slack_message,
            utterer=utterer,
            hot_word=hot_word
        )
        logger.info(f"Created Utterance: {utterance}")
