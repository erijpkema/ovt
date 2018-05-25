"""
"""
from flask import Flask
from gevent.pywsgi import WSGIServer
from urllib.request import urlopen
import xml.etree.ElementTree as ET

URL = 'https://rs.vpro.nl/v3/api/feeds/podcast/POMS_S_VPRO_788298?types=CLIP,SEGMENT'

app = Flask(__name__)


@app.route('/ovt')
def filter_ovt():
    """
    Parse the rss feed and edit out unwanted items in one pass.

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
    return ET.tostring(root, encoding='utf8', method='xml')


if __name__ == '__main__':
    http_server = WSGIServer(('', 4243), app)
    http_server.serve_forever()
    app.run(host='0.0.0.0', port=4243)
