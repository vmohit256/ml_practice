// https://www.spoj.com/problems/CLOPPAIR/

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <limits>
#include <cstdlib>
#include <iomanip>
using namespace std;

double getDistance(pair<int, int> p1, pair<int, int> p2) {
    double x = (1.0 * p1.first) - p2.first;
    double y = (1.0 * p1.second) - p2.second;
    return sqrt(x * x + y * y);
}

// both endIdx and startIdx are included
pair<tuple<int, int, double>, vector<int>> findClosestPairOfPoints(const vector<pair<int, int>>& points, const vector<int>& idxSortedByX, int startIdx, int endIdx) {
    vector<int> idxSortedByY;
    int p1=-1, p2=-1;
    double minDistance = numeric_limits<double>::max();

    if((endIdx-startIdx+1) < 3) {
        for(int i=startIdx; i<=endIdx; i++) 
            idxSortedByY.push_back(idxSortedByX[i]);
        // base case. Compute things using brute force
        sort(idxSortedByY.begin(), idxSortedByY.end(), 
            [points](int i, int j) {
                if(points[i].second!=points[j].second)
                    return points[i].second <= points[j].second;
                return i <= j;
            }
        );

        for(int i=startIdx; i<=endIdx; i++)
            for(int j=i+1; j<=endIdx; j++) {
                double distance = getDistance(points[idxSortedByX[i]], points[idxSortedByX[j]]);
                if(distance < minDistance) 
                    p1 = idxSortedByX[i], p2 = idxSortedByX[j], minDistance = distance;
            }
        
        return make_pair(make_tuple(p1, p2, minDistance), idxSortedByY);
    }

    int midIdx = (startIdx + endIdx) / 2;
    auto leftSolution = findClosestPairOfPoints(points, idxSortedByX, startIdx, midIdx);
    auto rightSolution = findClosestPairOfPoints(points, idxSortedByX, midIdx+1, endIdx);

    // merge sort idxSortedByY
    int leftIdx=0, rightIdx=0;
    while ((leftIdx < leftSolution.second.size()) && (rightIdx < rightSolution.second.size())) {
        auto p1 = points[leftSolution.second[leftIdx]];
        auto p2 = points[rightSolution.second[rightIdx]];
        bool pickLeft = (((p1.second != p2.second) && (p1.second<p2.second)) 
            || ((p1.second == p2.second) && (leftSolution.second[leftIdx]<=rightSolution.second[rightIdx])));
        // cout << "d: " << leftSolution.second[leftIdx] << " " <<  rightSolution.second[rightIdx] << " " << pickLeft << endl;
        if(pickLeft)
            idxSortedByY.push_back(leftSolution.second[leftIdx++]);
        else
            idxSortedByY.push_back(rightSolution.second[rightIdx++]);
    }
    while (leftIdx < leftSolution.second.size())
        idxSortedByY.push_back(leftSolution.second[leftIdx++]);
    while (rightIdx < rightSolution.second.size())
        idxSortedByY.push_back(rightSolution.second[rightIdx++]);
    
    // filter candidates from idxSortedByY
    p1 = get<0>(leftSolution.first), p2 = get<1>(leftSolution.first), minDistance = get<2>(leftSolution.first);
    if (get<2>(rightSolution.first) < minDistance) 
        p1 = get<0>(rightSolution.first), p2 = get<1>(rightSolution.first), minDistance = get<2>(rightSolution.first);
    
    vector<int> candidates;
    for(int i=0; i<idxSortedByY.size(); i++) {
        if(abs(points[idxSortedByX[midIdx]].first-points[idxSortedByY[i]].first) < minDistance)
            candidates.push_back(idxSortedByY[i]);
    }

    // try to find a better minimum from candidates
    for(int currIdx=1; currIdx<candidates.size(); currIdx++) {
        int prevIdx = currIdx-1;
        while(prevIdx>=0) {
            if(abs(points[candidates[currIdx]].second - points[candidates[prevIdx]].second)>=minDistance)
                break;
            double distance = getDistance(points[candidates[currIdx]], points[candidates[prevIdx]]);
            if(distance < minDistance) 
                p1 = candidates[prevIdx], p2 = candidates[currIdx], minDistance = distance;
            prevIdx--;
        }
    }
    return make_pair(make_tuple(p1, p2, minDistance), idxSortedByY);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    vector<pair<int, int>> points(n);
    vector<int> idxSortedByX;
    for(int i=0; i<n; i++) {
        int x, y;
        cin >> x >> y;
        points[i].first = x;
        points[i].second = y;
        idxSortedByX.push_back(i);
    }
    
    sort(idxSortedByX.begin(), idxSortedByX.end(), 
        [points](int i, int j) {
            if(points[i].first!=points[j].first)
                return points[i].first <= points[j].first;
            return i <= j;
        }
    );
    
    auto solution = findClosestPairOfPoints(points, idxSortedByX, 0, idxSortedByX.size()-1);
    cout << min(get<0>(solution.first), get<1>(solution.first)) << " "
        << max(get<0>(solution.first), get<1>(solution.first)) << " "
        << fixed << setprecision(6) << get<2>(solution.first) << endl;

    // for(int i=0; i<solution.second.size(); i++) {
    //     cout << solution.second[i]<<endl;
    // }
}