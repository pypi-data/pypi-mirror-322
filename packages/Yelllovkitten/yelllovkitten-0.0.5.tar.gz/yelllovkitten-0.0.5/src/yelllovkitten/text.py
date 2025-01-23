from datetime import datetime, timezone
import warnings
import yelllovkitten

def color(text: str,color: str=None,color_light: bool=True):
    if not color_light:
        if color == 'red':
            command = '31m'
        elif color == 'green':
            command = '32m'
        elif color == 'yellow' or color == 'yelllov':
            command = '33m'
        elif color == 'blue':
            command = '34m'
        elif color == 'magenta':
            command = '35m'
        elif color == 'cyan':
            command = '36m'
        elif color == 'white':
            command = '37m'
        elif color == 'black':
            command = '30m'
        else:
            return text
    else:
        if color == 'red':
            command = '91m'
        elif color == 'green':
            command = '92m'
        elif color == 'yellow' or color == 'yelllov':
            command = '93m'
        elif color == 'blue':
            command = '94m'
        elif color == 'magenta':
            command = '95m'
        elif color == 'cyan':
            command = '96m'
        elif color == 'white':
            command = '97m'
        elif color == 'black':
            command = '90m'
        else:
            return text
    return f'\033[{command}{text}\033[m'

def font(text: str,font: str=None):
    if font == None:
        return text
    elif font == 'bold':
        command = '1m'
    elif font == 'italic':
        command = '3m'
    elif font == 'underline':
        command = '4m'
    elif font == 'reverse':
        command = '7m'
    else:
        return text

    return f'\033[{command}{text}\033[m'

def background(text: str,color: str=None,color_light: bool=True):
    if not color_light:
        if color == 'red':
            command = '41m'
        elif color == 'green':
            command = '42m'
        elif color == 'yellow' or color == 'yelllov':
            command = '43m'
        elif color == 'blue':
            command = '44m'
        elif color == 'magenta':
            command = '45m'
        elif color == 'cyan':
            command = '46m'
        elif color == 'white':
            command = '47m'
        elif color == 'black':
            command = '40m'
        else:
            return text
    else:
        if color == 'red':
            command = '101m'
        elif color == 'green':
            command = '102m'
        elif color == 'yellow' or color == 'yelllov':
            command = '103m'
        elif color == 'blue':
            command = '104m'
        elif color == 'magenta':
            command = '105m'
        elif color == 'cyan':
            command = '106m'
        elif color == 'white':
            command = '107m'
        elif color == 'black':
            command = '90m'
        else:
            return text
    return f'\033[{command}{text}\033[m'

#def default(text: str):

def info(text, utc: bool=True):
    return out(color(str(text),'green'),info=False,utc=utc)
def warn(text, utc: bool=True):
    return out(color(str(text),'yellow'),info=False,utc=utc)
def error(text, utc: bool=True):
    return out(color(str(text),'red'),info=False,utc=utc)


def out(text, utc: bool=True, info: bool=True, only_info: bool=False):
    if utc: time_now = str(datetime.now(timezone.utc))[:19]
    else: time_now = str(datetime.now())[:19]
    textout = '\n' + time_now + ' | ' + str(text)
    if not only_info:
        print(textout,end='')
    if info:
        return textout
    else:
        return text