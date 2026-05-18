# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import datetime

from gallery_dl.extractor import steamcommunity

__tests__ = (
{
    "#url"     : "https://steamcommunity.com/sharedfiles/filedetails/?id=296316110",
    "#class"   : steamcommunity.SteamCommunitySharedfileExtractor,
    "#count"   : 1,

    'content_type': 'screenshot',
    'filedetails_id': '296316110',
    'url': 'https://steamcommunity.com/sharedfiles/filedetails/?id=296316110',
    'game': 'The Stanley Parable',
    'game_appid': '221910',
    'filesize': 177209,
    'date': datetime.datetime(2014, 8, 5, 9, 29),
    'dimensions': '1366 x 768',
    'creator': 'GiovanH',
    'creator_id': 'giovanh',
    'title': '',
    'category': 'steamcommunity',
    'ugc_id': '567770337564660542/8552FC9551546163E36D29B0512097A7084C8B1B',
    '_url': 'https://images.steamusercontent.com/ugc/567770337564660542/8552FC9551546163E36D29B0512097A7084C8B1B/'
},
{
    "#url": "https://steamcommunity.com/sharedfiles/filedetails/?id=2667137268",
    "#class"   : steamcommunity.SteamCommunitySharedfileExtractor,
    "#count"   : 1,

    "content_type": "artwork",
    "url": "https://steamcommunity.com/sharedfiles/filedetails/?id=2667137268",
    "game": "The Beginner's Guide",
    "game_appid": "303210",
    "filesize": 1080033,
    "date": datetime.datetime(2021, 11, 28, 7, 6),
    "dimensions": "1472 x 1667",
    "creator": "SomewhatTolerable",
    "creator_id": "76561199186562768",
    "title": "Escape",
    "category": "steamcommunity",
    '_url': "https://images.steamusercontent.com/ugc/1839154007536501034/6478074127CCBB03226274B8035FD607B9DA0673/"
}
)