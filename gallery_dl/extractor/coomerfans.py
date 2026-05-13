# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://coomerfans.com/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?coomerfans\.com"


class CoomerfansExtractor(Extractor):
    """Base class for coomerfans extractors"""

    category = "coomerfans"
    root = "https://coomerfans.com"
    directory_fmt = ("{category}", "{platform}", "{username}")
    filename_fmt = "{post_id}_{num}.{extension}"
    archive_fmt = "{post_id}_{num}"


class CoomerfansPostExtractor(CoomerfansExtractor):
    """Extractor for individual posts on coomerfans.com"""

    subcategory = "post"
    pattern = BASE_PATTERN + r"/p/(\d+)/(\d+)/(\w+)"
    example = "https://coomerfans.com/p/12345/67890/onlyfans"

    def items(self):
        post_id, creator_id, platform = self.groups
        url = f"{self.root}/p/{post_id}/{creator_id}/{platform}"
        page = self.request(url).text

        data = {
            "post_id": text.parse_int(post_id),
            "creator_id": text.parse_int(creator_id),
            "platform": platform,
            "username": text.extr(page, f"/u/{platform}/{creator_id}/", '"') or "",
            "description": text.unescape(
                text.extr(page, '<meta name="description" content="', '"') or ""
            ),
        }

        date_str = text.extr(page, '<time datetime="', '"')
        if date_str:
            data["date"] = self.parse_datetime_iso(date_str)

        yield Message.Directory, "", data

        num = 0
        seen = set()

        for img_url in text.extract_iter(page, 'src="https://img', '"'):
            full_url = "https://img" + img_url
            if "/storage/" not in full_url or full_url in seen:
                continue
            seen.add(full_url)
            num += 1
            data["num"] = num
            yield Message.Url, full_url, text.nameext_from_url(full_url, dict(data))

        for vid_url in text.extract_iter(page, '<source src="', '"'):
            if vid_url in seen:
                continue
            seen.add(vid_url)
            num += 1
            data["num"] = num
            yield Message.Url, vid_url, text.nameext_from_url(vid_url, dict(data))


class CoomerfansCreatorExtractor(CoomerfansExtractor):
    """Extractor for all posts from a coomerfans creator"""

    subcategory = "creator"
    pattern = BASE_PATTERN + r"/u/(\w+)/(\d+)/([^/?#]+)"
    example = "https://coomerfans.com/u/onlyfans/12345/USERNAME"

    def items(self):
        platform, creator_id, username = self.groups
        url = f"{self.root}/u/{platform}/{creator_id}/{username}"
        data = {"_extractor": CoomerfansPostExtractor}

        page_num = 1
        while True:
            params = {"page": page_num} if page_num > 1 else {}
            page = self.request(url, params=params).text

            seen = set()
            found = False
            for post_path in text.extract_iter(page, 'href="/p/', '"'):
                post_url = f"{self.root}/p/{post_path}"
                if post_url in seen:
                    continue
                seen.add(post_url)
                found = True
                yield Message.Queue, post_url, data

            if not found or f"?page={page_num + 1}" not in page:
                return
            page_num += 1
