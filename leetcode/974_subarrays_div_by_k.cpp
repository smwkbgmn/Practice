/*
	Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.

	A subarray is a contiguous part of an array.

	

	Example 1:

	Input: nums = [4,5,0,-2,-3,1], k = 5
	Output: 7
	Explanation: There are 7 subarrays with a sum divisible by k = 5:
	[4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
	Example 2:

	Input: nums = [5], k = 9
	Output: 0
	

	Constraints:

	1 <= nums.length <= 3 * 104
	-104 <= nums[i] <= 104
	2 <= k <= 104
*/

#include <vector>

class Solution {
	public:
		int subarraysDivByK(std::vector<int>&, int);
};

/* 2 */
int Solution::subarraysDivByK(std::vector<int>& nums, int k) {
	int rst = 0;

	auto it = nums.begin();

	int crit = *it % k;
	if (crit == 0) ++rst;

	int subchain = 0;
	for (auto it_next = it + 1; it_next != nums.end(); ++it_next) {
		*it += *it_next;

		int mod = *it % k;
		if (mod == 0) {
			int fact = subchain--;
			while (subchain > 0) fact *= subchain--;
			rst += fact + 1;
			crit = 0;
		}
		else if (mod == crit || mod == crit - k) {
			*it = crit;
			++subchain;
		}
	}
	return rst;
}

/* 1 */
// int Solution::subarraysDivByK(std::vector<int>& nums, int k) {
// 	int rst = 0;

// 	for (auto it = nums.begin(); it != nums.end(); ++it) {
// 		if (*it % k == 0) ++rst;
// 		for (auto it_sub = it + 1; it_sub != nums.end(); ++it_sub) {
// 			*it += *it_sub;
// 			if (*it % k == 0) {
// 				*it = 0;
// 				++rst;
// 			}
// 		}
// 	}
	
// 	return rst;
// }