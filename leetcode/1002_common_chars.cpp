/*
	Given a string array words, return an array of all characters that show up in all strings within the words (including duplicates). You may return the answer in any order.

	

	Example 1:

	Input: words = ["bella","label","roller"]
	Output: ["e","l","l"]
	Example 2:

	Input: words = ["cool","lock","cook"]
	Output: ["c","o"]
	

	Constraints:

	1 <= words.length <= 100
	1 <= words[i].length <= 100
	words[i] consists of lowercase English letters.
*/

#include <string>
#include <vector>
#include <map>

typedef std::string str_t;
typedef std::vector<str_t> vec_str_t;
typedef std::map<char, unsigned int> map_char_uint_t;

class Solution {
	public:
		vec_str_t commonChars(vec_str_t&);
};

vec_str_t
Solution::commonChars(vec_str_t& words) {
	map_char_uint_t comn;

	// Assigning common letter and count of appearance to the map like a, 3 / b, 2 / z, 5 from first word
	for (auto idx = 0; idx < words.front().length(); ++idx) {
		if (comn.find(words.front()[idx]) == comn.end())
			comn.insert(std::make_pair(words.front()[idx], 1));
		else
			++comn.at(words.front()[idx]);
	}

	// Seeing all words once, compare with the common letter map with current word and
	// so doing that decrease the common letter appearances. By decreasing count of elements for
	// criteria of common letter map, can obtain less comparing count
	for (auto it_words = words.begin(); it_words != words.end(); ++it_words) {
		auto it_comn = comn.begin();

		while (it_comn != comn.end()) {
			size_t appear = 0;

			for (auto idx = 0; (idx = it_words->find(it_comn->first, idx)) != str_t::npos; ++idx)
				++appear;
	
			if (appear) {
				if (appear < it_comn->second) it_comn->second = appear;
				++it_comn;
			}
			else it_comn = comn.erase(it_comn);
		}
	}

	// Assign string vector based from common letter map
	vec_str_t rst;
	for (auto it = comn.begin(); it != comn.end(); ++it) {
		for (auto cnt = it->second; cnt > 0; --cnt)
			rst.push_back(str_t(1, it->first));
	}

	return rst;
}

/* 1 */
// vec_str_t
// Solution::commonChars(vec_str_t& words) {
// 	vec_str_t rst;

// 	str_t crit = words.front();
// 	size_t cnt_words = words.size();
	
// 	while (crit.length()) {
// 		char letter = crit.front();
// 		size_t cnt_found = 0;

// 		for(vec_str_t::iterator iter = words.begin(); iter != words.end(); ++iter) {
// 			size_t idx = iter->find(letter);

// 			if ( idx != str_t::npos) {
// 				iter->replace(idx, 1, "");
// 				++cnt_found;
// 			}
// 		}

// 		if (cnt_found == cnt_words) rst.push_back(str_t(1, letter));
// 		crit.replace(0, 1, "");
// 	}
// 	return rst;
// }