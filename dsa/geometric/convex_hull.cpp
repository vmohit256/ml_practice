// https://leetcode.com/problems/erect-the-fence/

class Solution {
public:
    long getDistanceSquare(pair<int, int> x0, pair<int, int> x1) {
        long x = static_cast<long>(x0.first) - x1.first;
        long y = static_cast<long>(x0.second) - x1.second;
        return x * x + y * y;
    }

    // returns coefficient of z-coordinate of (x0->x1) x (x1->x2)
    long getCrossProductZCoordinateCoeff(pair<int, int> x0, pair<int, int> x1, pair<int, int> x2) {
        // v1 is vector from x0 to x1
        pair<int, int> v1 = {x1.first-x0.first, x1.second-x0.second};
        // v2 is a vector from x1 to x2
        pair<int, int> v2 = {x2.first-x1.first, x2.second-x1.second};
        // return the z-coordinate of (v1, 0) x (v2, x)
        return static_cast<long>(v1.first) * v2.second - static_cast<long>(v2.first) * v1.second;
    }

    // returns the index of convex hull points in clockwise order starting 
    // from the point with lowest (y, x) sorted key
    // collinear points that lie on the convex hull are also included in the result
    // implements graham's scan as described here: https://cp-algorithms.com/geometry/convex-hull.html 
    vector<int> computeConvexHull(const vector<pair<int, int>>& points) {
        // get index of point with minimum (y, x)
        int p0Idx = 0;
        for(int i=1; i<points.size(); i++) {
            if(
                (points[i].second < points[p0Idx].second) ||
                ((points[i].second == points[p0Idx].second) && (points[i].first < points[p0Idx].first)) ||
                ((points[i] == points[p0Idx]) && (i<p0Idx))
            )
                p0Idx = i;
        }
        // printf("%d: (%d, %d)\n", p0Idx, points[p0Idx].first, points[p0Idx].second);

        // sort rest of the points using the grahm scan logic
        vector<int> remPoints;
        for(int i=0; i<points.size(); i++)
            if(i!=p0Idx) remPoints.push_back(i);

        sort(remPoints.begin(), remPoints.end(),
            [this, points, p0Idx](int p1, int p2) {
                // first get z-axis coeff of (p1->p0) x (p0->p2)
                // return True if +ve and False if negative
                long zCoordinateCoeff = getCrossProductZCoordinateCoeff(points[p1], points[p0Idx], points[p2]);
                if (zCoordinateCoeff!=0) return zCoordinateCoeff > 0;
                // if its zero, calculate distance squared and return smaller one
                long distanceSq1 = getDistanceSquare(points[p1], points[p0Idx]);
                long distanceSq2 = getDistanceSquare(points[p2], points[p0Idx]);
                if (distanceSq1 != distanceSq2) return distanceSq1 < distanceSq2;
                return p1 < p2;
            }
        );

        // reverse the end segment of the array that is collinear
        // identify the segment
        int endIdx = remPoints.size()-1;
        int startIdx = endIdx;
        while(startIdx > 0) {
            if(getCrossProductZCoordinateCoeff(points[remPoints[endIdx]], points[p0Idx], points[remPoints[startIdx-1]])==0)
                startIdx --;
            else
                break;
        }

        // reverse it
        vector<int> stack;
        for(int i=startIdx; i<=endIdx; i++) {
            stack.push_back(remPoints[i]);
        }
        for(int i=startIdx; i<=endIdx; i++) 
            remPoints.pop_back();
        while(stack.size()>0) {
            remPoints.push_back(stack[stack.size()-1]);
            stack.pop_back();
        }

        // run graham scan
        vector<int> pointsOnConvexHull = {p0Idx};
        for(int i=0; i<remPoints.size(); i++) {
            while (pointsOnConvexHull.size()>=2) {
                auto x0 = points[pointsOnConvexHull[pointsOnConvexHull.size()-2]];
                auto x1 = points[pointsOnConvexHull[pointsOnConvexHull.size()-1]];
                auto x2 = points[remPoints[i]];
                if (getCrossProductZCoordinateCoeff(x0, x1, x2) <= 0)
                    break;
                else 
                    pointsOnConvexHull.pop_back();
            }
            pointsOnConvexHull.push_back(remPoints[i]);
        }
        return pointsOnConvexHull;
    }

    vector<vector<int>> outerTrees(vector<vector<int>>& trees) {
        if(trees.size()<2)
            return trees;
        vector<pair<int, int>> points;
        for(int i=0; i<trees.size(); i++)
            points.emplace_back(trees[i][0], trees[i][1]);

        vector<int> pointsOnConvexHull = computeConvexHull(points);
        vector<vector<int>> treesOnConvexHull;
        for(int i=0; i<pointsOnConvexHull.size(); i++) {
            treesOnConvexHull.push_back(trees[pointsOnConvexHull[i]]);
        }
        return treesOnConvexHull;
    }
};