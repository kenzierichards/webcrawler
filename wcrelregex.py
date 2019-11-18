#Kenzie Richards
#Web Crawler

#urllib2 used for requesting pages, re for regex, ssl for HTTP errors
#deque used for queue
import urllib2, re, ssl
from collections import deque
ssl.match_hostname = lambda cert, hostname: True

#keep track of pages and links for output at end
totalPagesRetrieved = 0
relative = 0
absolute = 0

queue = deque(["http://www.muhlenberg.edu/"])

#holds links for file writing
stack = []
relLinks = []
absLinks = []


#-------------robots.txt-------------
robots = "http://www.muhlenberg.edu/robots.txt"
req = urllib2.Request(robots)

#accounts for HTTP errors
try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()

#reuse regex for relative links to keep track of which pages cannot be indexed
disallowedLinks = re.findall(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*', str(content))

print("Crawling started")

#-------------main web crawler-------------
while len(queue) > 0 and len(queue) <= 500:
    req = urllib2.Request(queue.popleft())

    #opens page if it's not in disallowed links
    if req not in disallowedLinks:
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()

    content = page.read()

    #list of all links on the page
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"',str(content))

    #regex for each type of link
    relRegEx = re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*')
    absRegEx = re.compile(r'(http://|/)[^ :]+')

    #traverses list of links
    #if it matches regex, adds to queue to be traversed
    #adds to stack that holds the # of relative/abs links for each link
    for eachLink in links:
        if re.match(relRegEx, eachLink):
            relative = relative + 1
            queue.append("http://www.muhlenberg.edu" + eachLink)
            stack.append("http://www.muhlenberg.edu" + eachLink)
            totalPagesRetrieved = totalPagesRetrieved + 1
        else:
            absolute = absolute + 1
            queue.append(eachLink)
            stack.append(eachLink)
            totalPagesRetrieved = totalPagesRetrieved + 1

    #adds each relative link to list for file writing
    relLinks.append(relative)
    absLinks.append(absolute)

#-------------file writing and user output-------------
#I used range(0, 3) specifically for this project - 3 files

fileList = []
for x in range(0,3):
    f = open("site" + str(x) + ".txt","w+")
    fileList.append("site" + str(x) + ".txt")
    f.write(stack.pop() + "\n")
    f.write("Number of relative links: " + str(relLinks[x]) + "\n")
    f.write("Number of absolute links: " + str(absLinks[x]) + "\n")
    f.write("\n")
    f.write(content)


print("Crawling finished!")
print("Total pages retrieved: " + str(totalPagesRetrieved))
print("Absolute links: " + str(absolute))
print("Relative links: " + str(relative))
print("Files made: " + str(fileList))
