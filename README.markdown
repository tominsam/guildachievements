Cribbed from [my blog entry](http://jerakeen.org/notes/2009/02/warcraft-guild-achievements-as-rss/) asn an initial cut as a readme file. Needs work.

I play World of Warcraft. Oh, the shame. But I play it because I'm in a [fun guild][1] - we do [science!][2]. Well, actually *they* do science. I'm still at the 'cleaning the glassware afterwards' stage, but a tauren can dream..

Anyway, I code. It's what I do. So once WoLK came out and half the guild went completely insane and started chasing the really silly achievements, it was clear we were going to need an RSS feed of the things. So I built one. It's based on the [Armory][3], like most WoW tools, and is a complete kludge, like most of my tools. But here are my notes anyway.

The trick to scraping the Armoury is pretending to be Firefox. If you visit as a normal web browser, they serve you a traditional HTML page with some Ajax, and it's all quite normal and boring. If you visit the armoury in firefox they return an XML document with an XSL stylesheet referenced in the header that transforms the XML into a web page. Why are they doing this? It must be a _huge_ amount of work compared to just serving HTML, I don't get it. Let's ignore that. Fake a firefox user agent, and you can fetch lovely XML documents that describe things!

There's no 'guild achievement' page, alas, so we start by fetching the page that lists the people in the guild. The rendered web page has pagination, but the underlying XML seems to have all characters in a single document, so no messing around fetching multiple pages here. (I've tried this on a guild of 350ish people. Maybe it paginates beyond that. Don't use this script on a guild that big, it won't make you happy.)

Alas, the next thing we have to do is loop over every character and fetch their achievements page (that's _why_ you shouldn't run this script over a large guild). This is extremely unpleasant and slow.

My biggest annoyance here is that there's no timestamp on these things better than 'day', so you don't get very good ordering when you combine them later. I could solve this by storing some state myself, remembering the first time I see each new entry, etc, etc, but I'm trying to avoid keeping any state here, so I don't do that. The XML also lists only 5 achievements per character, and getting more involves fetching a lot more pages, so the final feed includes only the 5 most recent achievements per character. Again, something I could solve with local storage.

Anyway, now I have a list of everyone in the guild, and their last 5 achievements. It's pretty trivial building a list of these and outputting Atom or something. I do it using 'print' statements, myself, because I'm inherently evil. You can't deep-link to the achievement itself on the Armoury, so I link to the [wowhead page][7] for individual achievements.

Because the Armoury is unreliable, and my script is slow, I don't use this thing to generate the feed on demand. I have a crontab call the script once an hour, and if it doesn't explode, it copies the result into a directory served by my web browser. If it _does_ explode, then meh, I'll try again in an hour. The feed isn't exactly timely, but we're not controlling nuclear power stations here, we're tracking a computer game. It'll do.

[1]: http://www.unassignedvariable.org/
[2]: http://www.spaaace.com/cope/?p=108
[3]: http://eu.wowarmory.com/guild-info.xml?r=Nordrassil&n=unassigned+variable&p=1
[4]: http://www.aaronsw.com/2002/xmltramp/
[7]: http://www.wowhead.com/?achievement=1559