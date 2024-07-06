// https://leetcode.com/problems/k-closest-points-to-origin/

class Solution {
public:
    double getDistance(const vector<int>& point) {
        return sqrt(static_cast<double>(point[0]) * point[0] + static_cast<double>(point[1]) * point[1]);
    }

    void minHeapSiftDown(int i, vector<int>& points_heap, const vector<vector<int>>& points) {
        if (i>=points_heap.size())
            return;
        // index of the child that is: (i) minimum of the at max 2 children, 
        // and (ii) is closer than the parent we're sifting down
        int min_smaller_child_idx = -1;
        double distanceForParent = getDistance(points[points_heap[i]]);
        double distanceForChild1 = numeric_limits<double>::max();
        double distanceForChild2 = numeric_limits<double>::max();
        if ((2*i+1) < points_heap.size()) {
            distanceForChild1 = getDistance(points[points_heap[2*i+1]]);
            if (distanceForChild1 < distanceForParent) 
                min_smaller_child_idx = 2*i+1;
        }
        if ((2*i+2) < points_heap.size()) {
            distanceForChild2 = getDistance(points[points_heap[2*i+2]]);
            if ((distanceForChild2 < distanceForParent) && (distanceForChild2 < distanceForChild1))
                min_smaller_child_idx = 2*i+2;
        }
        if (min_smaller_child_idx!=-1) {
            int buffer = points_heap[i];
            points_heap[i] = points_heap[min_smaller_child_idx];
            points_heap[min_smaller_child_idx] = buffer;
            minHeapSiftDown(min_smaller_child_idx, points_heap, points);
        }
    }

    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        // Approach:
        // 1. Build a min heap -> O(n)
        // 2. Call extract min k times -> O(klogn)
        int n = points.size(); // 3

        // children of 0 are 2*0+1 and 2*0+2
        // children of i are 2*i+1, 2*i+2
        // parent of 1 and 2 are floor((1-1)/2), floor((2-1)/2) = 0
        // parent of j is floor((j-1)/2)
        vector<int> points_heap;
        for (int i=0; i<n; i++)
            points_heap.push_back(i);
        
        // heapify
        // biggest index with children is ci
        // 2*ci+1 <= n-1 
        // -> ci <= (n-2)/2
        // -> ci = floor((n-2)/2) // = (3-2)/2= 0
        for (int ci=(n-2)/2; ci>=0; ci--) {
            // call sift down
            minHeapSiftDown(ci, points_heap, points);
        }

        // call extract min k times
        vector<vector<int>> result;
        for (int i=0; i<k; i++) {
            vector<int> closest_point = {points[points_heap[0]][0], points[points_heap[0]][1]};
            result.push_back(closest_point);

            // delete closest point from the heap and call siftDown again
            points_heap[0] = points_heap[points_heap.size()-1];
            points_heap.pop_back();
            minHeapSiftDown(0, points_heap, points);
        }
        return result;
    }
};