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

#include <iostream>

/* 3 */
int Solution::subarraysDivByK(std::vector<int>& nums, int k) {
	if (nums.size() == 1) {
		if (nums.front() % k == 0) return 1;
		else return 0;
	}

	int rst = 0;

	int chain = 0;
	for (auto it = nums.begin(); it != nums.end(); ) {
		std::cout << "it pointing element " << *it << "\n";
		if (*it % k == 0) {
			++chain;
			++it;
		}
		else {
			int sub = 0;
			int submod = 0;
			
			auto it_sub = it + 1;
			for (; it_sub != nums.end(); ++it_sub) {
				*it = (*it + *it_sub) % k;

				if (*it == 0) {
					++chain;
					break;
				}
				else if (*it_sub % k == 0) ++sub;
				else {
					submod = (submod + *it_sub) % k;
					if (submod == 0) ++sub;
				}
			}
			
			if (sub) {
				int facto = sub--;
				while (sub) facto *= sub--;
				rst += facto;
			}

			it = it_sub;
		}
	}

	if (chain) {
		int facto = chain--;
		while (chain) facto *= chain--;
		rst += facto;
	}

	return rst;
}

/* 2 */
// int Solution::subarraysDivByK(std::vector<int>& nums, int k) {
// 	int rst = 0;

// 	int chain = 0;
// 	for (auto it = nums.begin(); it != nums.end();) {
// 		if (*it % k == 0) {
// 			++chain;
// 			++it;
// 		}

// 		else {
// 			int crit = *it % k;
// 			int sub = 0;

// 			auto it_sub = it + 1;
// 			for (; it_sub != nums.end(); ++it_sub) {
// 				*it = (*it + *it_sub) % k;
// 				// std::cout << "now *it: " << *it << "\n";

// 				if (*it % k == 0) break;
// 				else if (*it_sub % k == 0 || *it == crit || *it == crit + (k * (crit < 0? 1 : -1))) {
// 					// std::cout << "subary added " << *it << ", " << crit << "\n";
// 					++sub;
// 				}
// 			}
			
// 			// std::cout << "subary done with " << sub << "\n";

// 			int fact = 0;

// 			if (sub) {
// 				fact = sub--;
// 				while (sub) fact *= sub--;
// 			}

// 			rst += fact;

// 			if (*it % k != 0) {
// 				int fact = 0;

// 				if (chain) {
// 					fact = chain--;
// 					while (chain) fact *= chain--;
// 				}

// 				rst += fact;
// 			}
// 			else ++chain;

// 			it = it_sub;
// 		}
// 	} 

// 	if (chain) {
// 		int fact = chain--;
// 		while (chain) fact *= chain--;
// 		rst += fact;
// 	}

// 	return rst;
// }

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

int main(void) {
	Solution test;
	std::vector<int> vec;

	vec.push_back(7);
	vec.push_back(-5);
	vec.push_back(5);
	vec.push_back(-8);
	vec.push_back(-6);
	vec.push_back(6);
	vec.push_back(-4);
	vec.push_back(7);
	vec.push_back(-8);
	vec.push_back(-7);

	std::cout << test.subarraysDivByK(vec, 7) << std::endl;
	
	return 0;
}