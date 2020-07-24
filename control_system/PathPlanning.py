from queue import PriorityQueue
from copy import deepcopy
from table import Table
from data.cellDatabase import *
import cv2 as cv

def dijPath (n, m, start, goal):
    inf = 1e8
    dis = [[inf for i in range(m)] for j in range(n)]
    vis = [[0 for i in range(m)] for j in range(n)]
    parents = [[[-1, -1] for i in range(m)] for j in range(n)]
    delta = [[0,-2], [-1, -1],[-1, 1],[0,2],[1,1],[1,-1]]
    [x, y] = start
    dis[x][y] = 0
    q = PriorityQueue()
    q.put((0, x, y))
    while(not q.empty()):
        d, x1, y1 = q.get()
        if (vis[x1][y1]):
            continue
        vis[x1][y1] = 1
        for i in range(len(delta)):
            [dx, dy] = delta[i]
            x2 = dx + x1
            y2 = dy + y1
            if x2 < 0 or x2 >= n or y2 < 0 or y2 >= m:
                continue
            if x2 == 0 or x2 == n-1 or y2<=1 or y2 >= m-2:
                w = 2
            else:
                w = 1
            if dis[x1][y1] + w < dis[x2][y2]:
                dis[x2][y2] = dis[x1][y1]+ w
                q.put((w, x2, y2))
                parents[x2][y2] = [x1, y1]

    path = []
    def generatePath(x,y):
        if parents[x][y] ==[-1, -1]:
            path.append(start)
            path.reverse()
            return
        path.append([x, y])
        [xp, yp] = parents[x][y]
        generatePath(xp, yp)

    generatePath(goal[0], goal[1])
    return path


def pathCoordinates(path, table):
    new_path = [table.getCellByLocation(path[i]).coordinates for i in range(len(path))]
    return new_path


def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):
    newpath = deepcopy(path)
    change = tolerance
    while change >= tolerance:
        change = 0.0
        for i in range (1,len(path)-1):
            for j in range(2):
                r = newpath[i][j]
                newpath[i][j] += weight_data *(path[i][j]- newpath[i][j]) + \
                    weight_smooth * (newpath[i-1][j] + newpath[i+1][j] - 2.0 * newpath[i][j])
                change += abs(r - newpath[i][j])
                
    return newpath

def mmToPixel(location,w1,h1):
    (x,y)= location
    xp = int(x * w1/1150)
    yp =  int(y * h1/800)
    # print(w1, h1)
    return (xp, yp)

mytable = Table(cellDatabase)

path = dijPath(4, 10, [2,6], [2,0])
path1 = pathCoordinates(path, mytable)
new_path = smooth(path1)
print (path)
print (new_path)

# scale_percent =30
# img1 = cv.imread(cv.samples.findFile('table.jpg'))
# width = int(img1.shape[1] * scale_percent / 100)
# height = int(img1.shape[0] * scale_percent / 100)
# img1 = cv.resize(img1, (width,height))
# h1, w1 = img1.shape[:2]
# for i in range(len(new_path)): 

#     px = mmToPixel(new_path[i], w1, h1)
#     px1 = mmToPixel(path[i], w1, h1)
#     cv.circle(img1, px1, 5, (255,0,0), -1)
#     cv.circle(img1, px, 5, (0,255,0), -1)
    
# cv.imshow('img', img1)
# k = cv.waitKey(0)  
  
# #closing all open windows  
# cv.destroyAllWindows()  