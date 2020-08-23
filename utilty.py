import datetime
import re

from discord.ext.commands import BadArgument

from Exceptions import InvalidResponseException


async def id_to_uuid(userid: int):
    # 自分のAPIをどうぞ。
    raise InvalidResponseException()


async def uuid_to_mcid(uuid: str):
    # 自分のAPIをどうぞ。
    raise InvalidResponseException()


async def getservername(player: str):
    # 自分のAPIをどうぞ。
    raise InvalidResponseException()


def user_friendly_time(arg):
    if re.fullmatch("([0-9]+[smhdwy])+", arg) is None:
        raise BadArgument
    result = datetime.datetime.utcnow() - datetime.datetime.utcnow()
    print(result)
    matches = re.findall("[0-9]+[smhdwy]", arg)
    for match in matches:
        value = match.rstrip("smhdwy")
        if match.endswith("s"):
            result = result + datetime.timedelta(seconds=int(value))
        elif match.endswith("m"):
            result = result + datetime.timedelta(minutes=int(value))
        elif match.endswith("h"):
            result = result + datetime.timedelta(hours=int(value))
        elif match.endswith("d"):
            result = result + datetime.timedelta(days=int(value))
        elif match.endswith("w"):
            result = result + datetime.timedelta(weeks=int(value))
        elif match.endswith("y"):
            result = result + datetime.timedelta(days=int(value) * 365)
    return result
