"""
Helper functions only
"""

def formate_output(output):
    """
    strips the last line not ending with a terminator.
    """

    sentences = output.strip().split(". ")

    if sentences[-1][-1] != ".":
        sentences.pop()
        output = ". ".join(sentences)

    return output


def count_words(string):
    """
    words counter in a string
    """

    words = string.split(' ')
    return len(words)
