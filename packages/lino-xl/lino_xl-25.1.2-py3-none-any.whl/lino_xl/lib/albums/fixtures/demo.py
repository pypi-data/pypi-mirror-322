# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None


def walk(p):
    # print("20230331", p)
    for c in sorted(p.iterdir()):
        if c.is_dir():
            for cc in walk(c):
                yield cc
        else:
            yield c


def objects():
    Album = rt.models.albums.Album
    Upload = rt.models.uploads.Upload

    demo_date = dd.demo_date()

    top = Album(**dd.str2kw("designation", _("All")))
    yield top
    yield Album(parent=top, **dd.str2kw("designation", _("Furniture")))
    yield Album(parent=top, **dd.str2kw("designation", _("Things")))
    yield Album(parent=top, **dd.str2kw("designation", _("Services")))

    books = Album(parent=top, **dd.str2kw("designation", _("Books")))
    yield books

    yield Album(parent=books, **dd.str2kw("designation", _("Biographies")))
    yield Album(parent=books, **dd.str2kw("designation", _("Business")))
    yield Album(parent=books, **dd.str2kw("designation", _("Culture")))
    yield Album(parent=books, **dd.str2kw("designation", _("Children")))
    yield Album(parent=books, **dd.str2kw("designation", _("Medicine")))

    thrill = Album(parent=books, **dd.str2kw("designation", _("Thriller")))
    yield thrill

    if DEMO_DATA is None:
        logger.warning("No DEMO_DATA found (is lino_book installed?)")
        return

    for cover in """\
MurderontheOrientExpress.jpg Murder_on_the_orient_express_cover
StormIsland.jpg Storm_island_cover
AndThenThereWereNone.jpg And_then_there_were_none
FirstThereWereTen.jpg First_there_were_ten
""".splitlines():
        name, description = cover.split()
        src = DEMO_DATA / "images" / name
        file = make_uploaded_file(name, src, demo_date)
        yield Upload(album=thrill,
                   file=file,
                   description=description.replace('_', ' '))

    # if dd.is_installed('products'):
    #     FILES = Cycler(Upload.objects.all())
    #     OWNERS = Cycler(rt.models.products.Product.objects.all())
    #     for i in range(10):
    #         yield Upload(file=FILES.pop(), owner=OWNERS.pop())

    Volume = rt.models.uploads.Volume
    root_dir = DEMO_DATA / 'photos'
    vol = Volume(ref="photos",
                 description="Photo album",
                 root_dir=root_dir)
    yield vol
    photos = Album(parent=top, **dd.str2kw("designation", _("Photos")))
    yield photos

    file_args = dict(album=photos,volume=vol)

    if dd.is_installed('sources'):
        yield (luc := rt.models.sources.Author(first_name="Luc", last_name="Saffre"))
        yield (source := rt.models.sources.Source(
            author=luc, year_published="2022", title="Private collection"))
        file_args.update(source=source)

    chop = len(str(root_dir)) + 1
    for fn in walk(root_dir):
        fns = str(fn)[chop:]
        # print("20230325 {}".format(fn))
        yield Upload(
            library_file=fns,
            description=fns.replace('_', ' ').replace('/', ' '),
            **file_args)
