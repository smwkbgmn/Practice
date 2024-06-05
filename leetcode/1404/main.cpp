#include <iostream>
#include <string>
#include <bitset>

class Solution {
	public:
		static int numSteps( std::string );
};

int Solution::numSteps( std::string s ) {
	int rst = 0;
	bool up = false;
	std::string::reverse_iterator iter = s.rbegin();

	while(iter != s.rend()) {
		if (*iter == '1') {
			*iter = '0';
			up = true;
			++rst;
		}
		else {
			
		}
	}

	return rst;
}

int main( void ) {
	
	
	return 0;
}
