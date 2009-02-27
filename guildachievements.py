# inspired by http://www.petersblog.org/node/1408
# Originally by Tom Insam <tom@jerakeen.org>
# Some utf8 fixes and other improvements by Martin Glaude

import md5
from datetime import datetime, timedelta
import urllib, urllib2
import xmltramp
import socket
import sys
from time import gmtime, strftime

#####################################

realm = 'Nordrassil'
guild = "unassigned variable"
wowserver = "eu.wowarmory.com" # or 'www.' for US
# these two are ugly, but it should be abstracted, and I have legacy data to worry about here
feed_id = "http://jerakeen.org/achievmentsfor%s"%( urllib.quote(guild,'') )
entry_id_root = "http://jerakeen.org/achievement"

#realm = 'Kirin Tor'
#guild = "The Twilight Phoenix"
#wowserver = "www.wowarmory.com" # or 'eu.' for EU
#feed_id = "http://www.twilightphoenix.com/atom_feed/ttp-achievements.atom"
#entry_id_root = "http://www.twilightphoenix.com/atom_feed/achievement"

#####################################

url = "http://%s/guild-info.xml?r=%s&n=%s&p=1"%( wowserver, urllib.quote(realm,''), urllib.quote(guild,'') )

# Need to specify firefox as user agent as this makes the server return an XML file.
opener = urllib2.build_opener()
opener.addheaders = [ ('user-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4') ]

# timeout in seconds - the armoury falls over a lot
socket.setdefaulttimeout(10)
req = urllib2.Request( url)
try:
    data = opener.open(req)
except urllib2.HTTPError:
    sys.exit(1)
except urllib2.URLError:
    sys.exit(1)
    
xml = xmltramp.seed( data )

achievements = []

for character in xml['guildInfo']['guild']['members']['character':]:
    char_url = "http://%s/character-achievements.xml?r=%s&n=%s"%( wowserver, urllib.quote(realm,''), urllib.quote(character('name').encode('utf-8'),'') )
    

    char_req = urllib2.Request(char_url)
    try:
        char_data = opener.open(char_req)
    except urllib2.HTTPError:
        sys.exit(1)
    except urllib2.URLError:
        sys.exit(1)
    char_xml = xmltramp.seed( char_data )
    
    for ach in char_xml['achievements']['summary']['achievement':]:
        achievements.append( {
            'ach_root':entry_id_root,
            'name':character('name'),
            'achievement_id':ach('id'),
            'date':ach('dateCompleted')[0:10],
            'title':ach("title").replace("&", "&amp;"),
            'desc':ach('desc').replace("&", "&amp;"),
            'image_tag':"""<img src="http://%s/wow-icons/_images/51x51/%s.jpg" style="float: left" width="51" height="51" />"""%( wowserver, ach('icon') ),
        } )

achievements.sort(lambda a,b: cmp(b['date'], a['date']))

output = ""

output += """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>%s Achievements</title>
  <id>%s</id>
  <updated>%s</updated>
  <link href="http://%s/guild-info.xml?r=%s&amp;n=%s&amp;p=1" rel="alternate"></link>
"""%( guild, feed_id, strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()), wowserver, urllib.quote(realm,''), urllib.quote(guild,'') )

for ach in achievements[:50]:
    # TODO - More XML escaping. We already do title above, but that's a little crude.
    output += """
        <entry>
            <title>%(name)s gained the achievement %(title)s</title>
            <link href="http://www.wowhead.com/?achievement=%(achievement_id)s" rel="alternate"></link>
            <updated>%(date)sT00:00:00Z</updated>
            <id>%(ach_root)s-%(date)s-%(achievement_id)s-%(name)s</id>
            <summary>%(desc)s</summary>
            <content type="xhtml">
                <div xmlns="http://www.w3.org/1999/xhtml">
                    %(image_tag)s %(desc)s
                    <div style='break: both;'></div>
                </div>
            </content>  
            <author><name>%(name)s</name></author>
        </entry>
    """%ach

output += "</feed>"

print output.encode("utf-8")

