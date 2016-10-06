# -*- coding: utf-8 -*-
# xajkep@20161006
import sys, requests, re, base64, math, time

URL = "http://ph.dog"
URL_POST = "http://ph.dog/wp-content/plugins/pretty-link/pro/prlipro-create-public-link.php"
UPLOAD_SIZE = 2**12

print """
  _____  _    _ _____   ____   _____ _    _
 |  __ \| |  | |  __ \ / __ \ / ____| |  | |
 | |__) | |  | | |  | | |  | | (___ | |__| |
 |  _  /| |  | | |  | | |  | |\___ \|  __  |
 | | \ \| |__| | |__| | |__| |____) | |  | |
 |_|  \_\\_____/|_____/ \____/|_____/|_|  |_|
                                      v. 0.1
"""

def reach(url, limit=-1, display=True):
    counter = limit
    while counter != 0:
        try:
            if display:
                print "[+] Reach %s" % url
            r = requests.get(url, allow_redirects=False)
            url = r.headers["location"]
            return url
        except KeyError as e:
            if display:
                print "[+] Final destination: %s" % r.url
            return ""
            break
        except Exception as e:
            print "[-] Error"
            print e
            exit()
        counter -= 1

def init():
    r = requests.get("http://ph.dog")

    nonce = re.findall("name=\"_wpnonce\" value=\"[a-f0-9]{10}", r.text)[0][-10:]
    return (nonce, r.cookies)


def short(destination):
    r = requests.get(URL)
    nonce, COOKIES = init()
    DATA = {
    "referral-url": "/",
    "redirect_type": -1,
    "track": -1,
    "group": -1,
    "_wpnonce": nonce,
    "_wp_http_referer": URL,
    "url": destination,
    "Submit": "Shrink"
    }

    r = requests.post(URL_POST, data=DATA, cookies = COOKIES)
    return r.url.replace("?slug=", "")

def uploadFile(filename):
    data = open(filename, "r").read()
    print "[+] File size: %i bytes" % len(data)
    b64 = base64.b64encode(data)
    print "[+] B64 encoded size: %i bytes" % len(b64)
    url = URL
    limit = int(math.ceil(len(b64) / float(UPLOAD_SIZE)))
    start = time.time()
    for i in range(limit):
        if i == limit -1:
            print "[*] Uploading %i bytes" % (len(b64) % UPLOAD_SIZE)
        else:
            print "[*] Uploading %i bytes" % UPLOAD_SIZE
        url = short(url+"#"+b64[UPLOAD_SIZE*i:UPLOAD_SIZE*(i+1)])
    print ""
    print "[+] %i bytes uploaded in %i seconds (%i b/s)" % (len(b64), time.time() - start, len(b64)/(time.time() - start))
    print "[+] File uploaded: %s" % url

def downloadFile(url, filename):
    b64_data = ""
    start = time.time()
    while 1:
        url = reach(url, display=False)
        pos = url.find("#")

        if pos == -1:
            break

        pos += 1

        print "[+] %i bytes recovered" % len(url[pos:])
        b64_data = url[pos:] + b64_data
    print "[+] %i bytes downloaded in %i seconds (%i b/s)" % (len(b64_data), time.time() - start, len(b64_data)/(time.time() - start))
    data = base64.b64decode(b64_data)
    open(filename, "w").write(data)
    print "[+] %i bytes written to %s" % (len(data), filename)



if len(sys.argv) == 3 and sys.argv[1] == "-r":
    url = sys.argv[2]
    while url != "":
        url = reach(url)
elif len(sys.argv) == 3 and sys.argv[1] == "-u":
    uploadFile(sys.argv[2])
elif len(sys.argv) == 4 and sys.argv[1] == "-d":
    downloadFile(sys.argv[2], sys.argv[3])
else:
    print "Usage: python rudosh.py -r <url>"
    print "       python rudosh.py -u <file>"
    print "       python rudosh.py -d <url> <output>"
    exit()
