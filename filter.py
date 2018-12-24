from urllib.request import urlopen
import datetime
import sys
import xml.etree.ElementTree as ET

URL = 'https://rs.vpro.nl/v3/api/feeds/podcast/POMS_S_VPRO_788298?types=CLIP,SEGMENT'


def filter_ovt(outfile):
    """
    Parse the rss feed and edit out unwanted items in one pass.
    Args:
      outfile (str): file to write the filtered xml to
    Returns: (str) the updated rss feed.
    """
    tree = ET.parse(urlopen(URL))
    root = tree.getroot()
    channel = root.find("channel")
    new_items = []
    for item in channel.findall("item"):
        for subitem in item.getiterator():
            if subitem.tag == 'title':
                if 'e uur' in subitem.text:
                    date_list = item.find('pubDate').text.split()
                    date = datetime.datetime.strptime(
                        '{} {} {}'.format(date_list[1], date_list[2],
                                          date_list[3]), '%d %b %Y')
                    if '1e uur' in subitem.text:
                        new_items.append((date, 1, item))
                    elif '2e uur' in subitem.text:
                        new_items.append((date, 2, item))
        channel.remove(item)

    # Sort by reverse date and item # positive
    new_items.sort(key=lambda e: (e[0], -e[1]), reverse=True)

    for new_item in new_items:
        print(new_item)
        channel.append(new_item[2])
    # We want the '2e uur' to appear below the '1e uur'

    tree.write(outfile)


if __name__ == "__main__":
    filter_ovt(sys.argv[1])
