/*
	Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size groupSize, and consists of groupSize consecutive cards.

	Given an integer array hand where hand[i] is the value written on the ith card and an integer groupSize, return true if she can rearrange the cards, or false otherwise.

	

	Example 1:

	Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
	Output: true
	Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]
	Example 2:

	Input: hand = [1,2,3,4,5], groupSize = 4
	Output: false
	Explanation: Alice's hand can not be rearranged into groups of 4.

	

	Constraints:

	1 <= hand.length <= 104
	0 <= hand[i] <= 109
	1 <= groupSize <= hand.length
	

	Note: This question is the same as 1296: https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/
*/

#include <iostream>

#include <vector>
#include <algorithm>

#define ABS(n) ((n) < 0? -(n) : (n))

typedef std::vector<int> vec_int_t;

class Solution {
	public:
		bool isNStraightHand(vec_int_t&, int);
};

/* 3 */
bool Solution::isNStraightHand(vec_int_t& hand, int group_size) {
	if (hand.size() % static_cast<size_t>(group_size) != 0) return false;

	std::sort(hand.begin(), hand.end());

	while (hand.size()) {
		int min = hand.front();
		hand.erase(hand.begin());

		for (int cnt = 1; cnt < group_size; ++cnt) {
			vec_int_t::iterator next = std::upper_bound(hand.begin(), hand.end(), min);
			
			if (next == hand.end() || min + 1 != *next) return false;

			min = *next;
			hand.erase(next);
		}
	}
	return true;
}

/* 2 */
// bool Solution::isNStraightHand(vec_int_t& hand, int group_size) {
// 	if (hand.size() % static_cast<size_t>(group_size) != 0) return false;

// 	std::sort(hand.begin(), hand.end());

// 	while (hand.size()) {
// 		int min = hand.front();
// 		hand.erase(hand.begin());

// 		for (int cnt = 1; cnt < group_size; ++cnt) {
// 			vec_int_t::iterator next = std::upper_bound(hand.begin(), hand.end(), min);
			
// 			if (next == hand.end() || min + 1 != *next) return false;

// 			min = *next;
// 			hand.erase(next);
// 		}
// 	}
// 	return true;
// }

/* 1 */
// bool Solution::isNStraightHand(vec_int_t& hand, int group_size) {
// 	if (hand.size() % static_cast<size_t>(group_size) != 0) return false;

// 	while (hand.size()) {
// 		vec_int_t::iterator min = std::min_element(hand.begin(), hand.end());
// 		int crit = *min;
// 		hand.erase(min);
		
// 		for (auto cnt = 1; cnt < group_size; ++cnt) {
// 			vec_int_t::iterator next = std::find(hand.begin(), hand.end(), crit + cnt);

// 			if (next == hand.end()) return false;
// 			else hand.erase(next);
// 		}
// 	}
// 	return hand.size() == 0;
// }

int main(void) {
	Solution test;
	
	vec_int_t tmp;
	tmp.push_back(2);
	tmp.push_back(1);
	test.isNStraightHand(tmp, 2);
	
	return 0;
}