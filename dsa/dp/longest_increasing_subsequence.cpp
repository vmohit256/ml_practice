// https://leetcode.com/problems/longest-increasing-subsequence/

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        // smallestEndpointsOfLIS[l-1] = index of smallest endpoint of any l sized LIS
        vector<int> smallestEndpointsOfLIS = {0};

        for(int i=1; i<nums.size(); i++) {
            if (nums[i] > nums[smallestEndpointsOfLIS[smallestEndpointsOfLIS.size()-1]])
                smallestEndpointsOfLIS.push_back(i);
            else {
                if (nums[i] <= nums[smallestEndpointsOfLIS[0]]) {
                    smallestEndpointsOfLIS[0] = i;
                }
                else {
                    int lo = 0, hi=smallestEndpointsOfLIS.size()-1;
                    // at this point
                    // nums[i] <= nums[smallestEndpointsOfLIS[hi]]
                    // nums[i] > nums[smallestEndpointsOfLIS[lo]]
                    // goal: find smallest index j such that nums[i] <= nums[smallestEndpointsOfLIS[j]]
                    while((hi-lo)!=1) {
                        int mid = (hi+lo)/2;
                        if (nums[i] <= nums[smallestEndpointsOfLIS[mid]]) 
                            hi = mid;
                        else
                            lo = mid;
                    }
                    smallestEndpointsOfLIS[hi] = i;
                }
            }
        }
        return smallestEndpointsOfLIS.size();
    }
};