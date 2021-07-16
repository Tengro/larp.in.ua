def split_string(text, chars_per_string):
    """
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.
    :param text: The text to split
    :param chars_per_string: The number of characters per line the text is split into.
    :return: The splitted text as a list of strings.
    """
    text = str(text)
    return [text[i:i + chars_per_string] for i in range(0, len(text), chars_per_string)]


def safe_message_send(bot, chat_id, text):
    splitted_text = split_string(text, 4080)
    for message in splitted_text:
        bot.sendMessage(chat_id, message)
