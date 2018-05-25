import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen

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
    for item in channel.findall("item"):
        for subitem in item.getiterator():
            if subitem.tag == 'title':
                if 'e uur' not in subitem.text:
                    channel.remove(item)
    tree.write(outfile)


if __name__ == "__main__":
    filter_ovt(sys.argv[1])
