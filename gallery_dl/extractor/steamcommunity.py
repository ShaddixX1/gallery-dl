
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://steamcommunity.com"""

import datetime
from enum import Enum
from urllib.parse import urlparse

from .. import text
from ..extractor.common import Extractor, Message


class SteamItemType(Enum):
    SCREENSHOT = 'screenshot'
    ARTWORK = 'artwork'


class SteamCommunitySharedfileExtractor(Extractor):
    """Extractor for steamcommunity shared files"""
    category = "steamcommunity"

    directory_fmt = ("{category}", "{game}", "{content_type}")
    filename_fmt = "{filedetails_id}.{extension}"
    archive_fmt = "{category}_{game}_{filedetails_id}_{ugc_id}"

    pattern = r"(?:https?://)(?:www\.)?steamcommunity\.com/sharedfiles/filedetails/\?id=(\d+)$"
    example = "https://steamcommunity.com/sharedfiles/filedetails/?id=296316110"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.filedetails_id = match.group(1)

    @staticmethod
    def get_content_type(page_text) -> SteamItemType:

        tab = text.extr(
            page_text,
            'class="apphub_sectionTab active "><span>',
            '</span></a>'
        )

        if tab == 'Screenshots':
            return SteamItemType.SCREENSHOT
        if tab == 'Artwork':
            return SteamItemType.ARTWORK
        else:
            raise NotImplementedError("Could not parse content type", tab)

    def items(self): # type: ignore

        url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={self.filedetails_id}"

        page_text: str = self.request(url).text

        try:
            content_type = self.get_content_type(page_text)
        except ValueError as e:
            e2 = ValueError("Unknown content type for item", self.filedetails_id)
            raise e2 from e

        meta = {
            "content_type": content_type.value,
            "filedetails_id": self.filedetails_id,
            "url": url
        }

        if content_type in {SteamItemType.SCREENSHOT, SteamItemType.ARTWORK}:
            yield from self.basic_image_items(page_text, meta, content_type)
        else:
            raise NotImplementedError(content_type)

    def basic_image_items(self, page_text, meta: dict, content_type=None):

        game_div = text.extr(page_text, '<div class="screenshotAppName">', '</div>')
        meta['game'] = text.extr(game_div, '>', '<')
        meta['game_appid'] = text.extr(game_div, '/app/', '/')

        extr = text.extract_from(page_text)

        file_size = extr('<div class="detailsStatRight">', '</div>')
        meta["filesize"] = text.parse_bytes(file_size.replace(' ', '')[:-1])

        date_posted = extr('<div class="detailsStatRight">', '</div>')
        date = self.parse_datetime(date_posted, "%b %d, %Y @ %I:%M%p")
        if not date:
            date = self.parse_datetime(date_posted, "%b %d @ %I:%M%p")
            date =date.replace(year=datetime.datetime.now().year)
        meta["date"] = date

        meta["dimensions"] = extr('<div class="detailsStatRight">', '</div>')
        meta["creator"] = text.extr(
            page_text,
            '<div class="friendBlockContent">', '<br>'
        ).strip()

        meta["creator_id"] = (
            text.extr(
                page_text,
                '<a class="friendBlockLinkOverlay" href="https://steamcommunity.com/profiles/', '"></a>'
            )
            or
            text.extr(
                page_text,
                '<a class="friendBlockLinkOverlay" href="https://steamcommunity.com/id/', '"></a>'
            )
        ).strip()

        meta["title"] = text.extr(page_text, '<div class="workshopItemTitle">', '</div>')

        yield Message.Directory, '', meta

        actual_media = text.extr(page_text, '<img id="ActualMedia"', '>')
        img_src = text.extr(actual_media, 'src="', '"')

        url = urlparse(img_src)
        clean_url = url.scheme + '://' + url.netloc + url.path

        meta['ugc_id'] = url.path.replace('/ugc/', '')[:-1]
        meta['extension'] = ''  # Rely on extension fixing

        yield Message.Url, clean_url, meta
