/*
	Given a string s which consists of lowercase or uppercase letters, return the length of the longest 
	palindrome
	that can be built with those letters.

	Letters are case sensitive, for example, "Aa" is not considered a palindrome.

	

	Example 1:

	Input: s = "abccccdd"
	Output: 7
	Explanation: One longest palindrome that can be built is "dccaccd", whose length is 7.
	Example 2:

	Input: s = "a"
	Output: 1
	Explanation: The longest palindrome that can be built is "a", whose length is 1.
	

	Constraints:

	1 <= s.length <= 2000
	s consists of lowercase and/or uppercase English letters only.
*/

#include <string>
#include <map>

typedef std::map<char, unsigned int> map_char_uint_t;

class Solution {
	public:
		int longestPalindrome(std::string);
};

int
Solution::longestPalindrome(std::string str) {
	map_char_uint_t table;

	// Assigning the table for map representing the count of appearances of each letter
	// with case sensitive
	for (auto idx = 0; idx < str.length(); ++idx) {
		if (table.find(str[idx]) != table.end()) ++table.at(str[idx]);
		else table.insert(std::make_pair(str[idx], 1));
	}

	// Counting all letter apperances and only one odd apperance can be added to this result
	int rst = 0;
	bool odd = false;
	for (auto it = table.begin(); it != table.end(); ++it) {
		if (it->second & 0b1) {
			rst += (it->second - 1);
			odd = true;
		}
		else rst += it->second;
	}

	return rst + odd;
}
