from collections import namedtuple
from math import sqrt
import random
import numpy
import urllib, cStringIO
try:
    import Image
except ImportError:
    from PIL import Image


HEX = '0123456789abcdef'
HEX2 = dict((a+b, HEX.index(a)*16 + HEX.index(b)) for a in HEX for b in HEX)


def rgb(triplet):
    triplet = triplet.lower()
    return (HEX2[triplet[0:2]], HEX2[triplet[2:4]], HEX2[triplet[4:6]])


def triplet(rgb):
    return format((rgb[0]<<16)|(rgb[1]<<8)|rgb[2], '06x')


def hsvToRGB(h, s, v):
    """Convert HSV color space to RGB color space
    
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  
    """
    import math
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    return {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
        5: (v, p, q),
    }[hi]


def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


def hsvbucket(h, s, v):
    h = (round(h / 10) * 10) % 360
    s = round(s * 10) / 10
    v = round(v * 10) / 10

    return h, s, v

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))


def get_colors_url(url, n=3):
    ff = cStringIO.StringIO(urllib.urlopen(url).read())
    img = Image.open(ff)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)


def get_colors(data, n=3):
    # data = unicode(data.strip(codecs.BOM_UTF8), 'utf-8')
    f = StringIO(data)
    img = Image.open(f)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)


def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)


def euclidean(p1, p2):
    a = numpy.array(p1[0])
    b = numpy.array(p2[0])
    # return numpy.linalg.norm(a-b)
    a = sqrt(sum((
        (p1.coords[i] - p2.coords[i]) ** 2 for i in xrange(p1.n)
    )))
    # print a
    return a


def calculate_center(points, n):
    vals = [0.0 for i in xrange(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in xrange(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in xrange(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in xrange(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in xrange(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters

if __name__ == '__main__':
    import sys
    print colorz(sys.argv[1])