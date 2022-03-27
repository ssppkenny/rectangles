import intervaltree
from intervaltree import interval
from enum import Enum
from collections import namedtuple, defaultdict
import networkx as nx
import matplotlib.pyplot as plt

Rect = namedtuple('Rect', "x y w h")
SweepEvent = namedtuple('SweepEvent', "x rect type")

class Solution:
   def solve(self, intervals):
      start, end = intervals.pop()
      while intervals:
         start_temp, end_temp = intervals.pop()
         start = max(start, start_temp)
         end = min(end, end_temp)
      return [start, end]


class SweepType(int, Enum):
    LEFT = 1
    RIGHT = 2


def all_pairs(s):
    lst = list(s)
    return [(a, b) for idx, a in enumerate(lst) for b in lst[idx + 1:]]


def join_rectangles(rects):
    sorted_rects = sorted(rects, key=lambda a: (a.x, a.y))
    numbered_rects = dict(((r, i) for (i, r) in enumerate(sorted_rects)))

    rects_dict = defaultdict(list)
    for r in rects:
        rects_dict[(r.y, r.y + r.h)].append(r)

    lefts = [SweepEvent(rect.x, rect, SweepType.LEFT) for rect in rects]
    rights = [SweepEvent(rect.x + rect.w, rect, SweepType.RIGHT) for rect in rects]
    events = lefts + rights
    sorted_events = sorted(events, key=lambda a: (a.x, a.type))
    g = nx.Graph()
    tree = intervaltree.IntervalTree()
    for event in sorted_events:
        rect = event.rect
        if event.type == SweepType.LEFT:
            if tree.overlaps(rect.y, rect.y + rect.h):
                overlapping_intervals = tree.overlap(rect.y, rect.y + rect.h)
                overlapping_intervals.add(interval.Interval(rect.y, rect.y + rect.h))
                pairs = all_pairs(overlapping_intervals)
                for p in pairs:
                    r1 = rects_dict[(p[0].begin, p[0].end)]
                    r1 = [r for r in r1 if event.x <= r.x + r.w and event.x >= r.x][0]
                    r2 = rects_dict[(p[1].begin, p[1].end)]
                    r2 = [r for r in r2 if event.x <= r.x + r.w and event.x >= r.x][0]

                    ind1 = numbered_rects[r1]
                    ind2 = numbered_rects[r2]
                    g.add_edge(ind1, ind2)
            tree.add(interval.Interval(rect.y, rect.y + rect.h))
        else:
            tree.discard(interval.Interval(rect.y, rect.y + rect.h))
    cc = nx.connected_components(g)
    joined_rects = []
    for c in cc:
        minx, miny = float('inf'), float('inf')
        maxx, maxy = 0, 0
        for i in c:
            r = sorted_rects[i]
            if r.x < minx:
                minx = r.x
            if r.x + r.w > maxx:
                maxx = r.x + r.w
            if r.y < miny:
                miny = r.y
            if r.y + r.h > maxy:
                maxy = r.y + r.h
        joined_rects.append(Rect(minx, miny, maxx - minx, maxy - miny))
    return g, joined_rects


def test():
    rects = [Rect(1, 1, 2, 3), Rect(2, 3, 4, 2), Rect(7, 4, 2, 3), Rect(8, 2, 2, 3), Rect(6, 6, 2, 2)]
    g, joined_rects = join_rectangles(rects)
    ##nx.draw_networkx(g)
    print(joined_rects)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
