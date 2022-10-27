from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import BaseObject, Campaign
from eaw2web.text import Encyclopedia, from_csv_line, preserve_newlines, strip_entries
from eaw2web.xml.base import parse_base_object
from eaw2web.xml.text import text_entry_from_tag, text_or_empty


def parse_campaign(child: Element, encyclopedia: Encyclopedia) -> BaseObject:
    return Campaign(
        **parse_base_object(child).dict(),
        conquest_set=text_or_empty(child.find("Campaign_Set")),
        active_player=text_or_empty(child.find("Starting_Active_Player")),
        text=text_entry_from_tag(child.find("Text_ID"), encyclopedia),
        description=preserve_newlines(
            text_entry_from_tag(child.find("Description_Text"), encyclopedia)
        ),
        planets=strip_entries(from_csv_line(text_or_empty(child.find("Locations")))),
        traderoutes=strip_entries(
            from_csv_line(text_or_empty(child.find("Trade_Routes")))
        )

    )
