import numpy as np
import cv2 as cv

flann_params= dict(algorithm = 6,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2


def init_feature():
    """initialize feature detector and matcher algorithm
    """
    detector = cv.ORB_create(3000)
    norm = cv.NORM_HAMMING
    #matcher = cv.BFMatcher(norm)
    matcher = cv.FlannBasedMatcher(flann_params, {})
    return detector, matcher


def filter_matches(kp1, kp2, matches, ratio = 0.8):
    """filter matches to keep strong matches only
    """
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, list(kp_pairs)


c = []
def explore_match(win, img1, img2, kp_pairs, status = None, H = None):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2, 3), np.uint8)
    vis[:h1, :w1, :3] = img1
    vis[:h2, w1:w1+w2, :3] = img2
    img3 = vis
    h3, w3 = img3.shape[:2]

    if H is not None:
        corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
        corners1 = np.float32( cv.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
        corners = np.int32( cv.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
        c = corners
        cv.polylines(vis, [corners], True, (0, 0, 255))

    if status is None:
        status = np.ones(len(kp_pairs), np.bool_)
    
    p1, p2 = [], [] 
    for kpp in kp_pairs:
        p1.append(np.int32(kpp[0].pt))
        p2.append(np.int32(np.array(kpp[1].pt) + [w1, 0]))

    green = (0, 255, 0)
    red = (0, 0, 255)

    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            col = green
            cv.circle(vis, (x1, y1), 2, col, -1)
            cv.circle(vis, (x2, y2), 2, col, -1)
        else:
            col = red
            r = 2
            thickness = 3
            cv.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
            cv.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
            cv.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
            cv.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)

    for (x1, y1), (x2, y2), inlier in zip(p1, p2, status):
        if inlier:
            cv.line(vis, (x1, y1), (x2, y2), green)

    cv.imshow(win, vis)
    return corners1


scale_percent =25
img1 = cv.imread(cv.samples.findFile('table.jpg'))
width = int(img1.shape[1] * scale_percent / 100)
height = int(img1.shape[0] * scale_percent / 100)
img1 = cv.resize(img1, (width,height))


detector, matcher = init_feature()

# apply orb on table image
kp1, desc1 = detector.detectAndCompute(img1, None)

def getCorners(frame):
    
    # apply orb on frame
    kp2, desc2 = detector.detectAndCompute(frame, None)

    print('matching...')
    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) 
    #filter matches and keep strong matches
    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches)
    if len(p1) >= 4:
        # H: transformation matrix
        H, status = cv.findHomography(p1, p2, cv.RANSAC, 5.0)
        print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
    else:
        H, status = None, None
        print('%d matches found, not enough for homography estimation' % len(p1))

    corners = explore_match('find_table', img1, frame, kp_pairs, status, H)
    return corners

def getTableFromFrame (corners, frame):
    h1, w1 = img1.shape[:2]
    h2, w2 = frame.shape[:2]
    vis = np.zeros((max(h1, h2), w1+w2, 3), np.uint8)
    vis[:h1, :w1, :3] = img1
    vis[:h2, w1:w1+w2, :3] = frame
    pts1 = corners
    pts2 = np.float32([[0,0],[w1,0],[w1,h1], [0,h1]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    # print((w1, h1))
    dst = cv.warpPerspective(vis, M,(w1,h1))
    return dst
