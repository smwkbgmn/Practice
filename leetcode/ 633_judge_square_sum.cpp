/*
	Given a non-negative integer c, decide whether there're two integers a and b such that a2 + b2 = c.

	

	Example 1:

	Input: c = 5
	Output: true
	Explanation: 1 * 1 + 2 * 2 = 5
	Example 2:

	Input: c = 3
	Output: false
	

	Constraints:

	0 <= c <= 231 - 1
*/

#include <cmath>

class Solution {
	public:
		bool judgeSquareSum(int);
};

bool Solution::judgeSquareSum(int c) {
	long long pow_a;
	for (long long a = 0; (pow_a = a * a) <= c; ++a) {
		double sqrt_rval = std::sqrt(c - pow_a);

		if (sqrt_rval == static_cast<int>(sqrt_rval)) return true;
	}
	return false;
}


/* 1 */
// bool Solution::judgeSquareSum(int c) {
// 	long long lval;
// 	for (int a = 0; (lval = a * a - c) <= 0; ++a) {
		
// 		long long rval;
// 		for (int b = a; (rval = -(b * b)) >= lval; ++b) {
// 			if (lval == rval) return true;
// 		}
// 	}
// 	return false;
// }