# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import coomerfans

__tests__ = (
    {
        "#url": "https://coomerfans.com/p/84930879/350442/onlyfans",
        "#category": ("", "coomerfans", "post"),
        "#class": coomerfans.CoomerfansPostExtractor,
        "#results": (
            "https://img1.coomerfans.com/storage/1/vd/gr/2892ac-0197737a-f8a5-72ed-a961-bbd8891479b7.jpg",
        ),
        "post_id": 84930879,
        "creator_id": 350442,
        "platform": "onlyfans",
        "username": "evekozi",
        "extension": "jpg",
    },
    {
        "#url": "https://coomerfans.com/p/84930883/350442/onlyfans",
        "#category": ("", "coomerfans", "post"),
        "#class": coomerfans.CoomerfansPostExtractor,
        "#count": 3,
    },
    {
        "#url": "https://coomerfans.com/u/onlyfans/226845/lenaslittlesecret",
        "#category": ("", "coomerfans", "creator"),
        "#class": coomerfans.CoomerfansCreatorExtractor,
        "#pattern": coomerfans.CoomerfansPostExtractor.pattern,
        "#range": "1-30",
        "#count": 30,
    },
    {
        "#url": "https://coomerfans.com/u/onlyfans/226845/lenaslittlesecret",
        "#category": ("", "coomerfans", "creator"),
        "#class": coomerfans.CoomerfansCreatorExtractor,
        "#count": "> 30",
    },
    {
        "#url": "https://coomerfans.com/u/fansly/346390/Blue_Rose8900",
        "#category": ("", "coomerfans", "creator"),
        "#class": coomerfans.CoomerfansCreatorExtractor,
        "#pattern": coomerfans.CoomerfansPostExtractor.pattern,
        "#range": "1-30",
        "#count": 30,
    },
    {
        "#url": "https://coomerfans.com/u/fansly/346390/Blue_Rose8900",
        "#category": ("", "coomerfans", "creator"),
        "#class": coomerfans.CoomerfansCreatorExtractor,
        "#count": "> 30",
    },
)
