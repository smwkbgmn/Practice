#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_SIZE 26

// graph theory

int is_solvable(int n, char** words)
{
	if (n < 2)
		return 0;

	int in_degree[ALPHABET_SIZE] = {0};
	int out_degree[ALPHABET_SIZE] = {0};
	int char_used[ALPHABET_SIZE] = {0};

	for (int i = 1; i < n; i++) {
		int first = words[i][0] - 'a';
		int last = words[i][strlen(words[i]) - 1] - 'a';
		out_degree[first]++;
		in_degree[last]++;
		char_used[first] = 1;
		char_used[last] = 1;
	}

	int start_count = 0;
	int end_count = 0;
	for (int i = 0; i < ALPHABET_SIZE; i++) {
		if (out_degree[i] - in_degree[i] == 1){//ある文字のoutがinよりも1つ多い=開始点
			start_count++;
		} else if (in_degree[i] - out_degree[i] == 1){
			end_count++;
		} else if (in_degree[i] != out_degree[i]) {
			return (0);
		}
	}

	//Eulerian Circuit or Eulerian Path
	if ((start_count == 0 && end_count == 0) || (start_count == 1 && end_count == 1)) {
		return (1);
	}

	return (0);
}

int main() {
	char *case1[] = {"dash", "hard"};
	printf("Output: %d\n", is_solvable(2, case1));
	char *case2[] = {"dash", "too", "hard"};
	printf("Output: %d\n", is_solvable(3, case2));
	return 0;
}