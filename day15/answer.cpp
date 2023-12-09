// Fork of answer.py, but in c++
// To see if python is at fault
// I suspect python dicts are poorly optimized
#include <unordered_map>
#include <iostream>

int INPUT[] = {6, 19, 0, 5, 7, 13, 1}; // 1801753 expected
//int INPUT[] = {0, 3, 6}; // 175594 expected
int INPUT_SIZE = sizeof(INPUT)/sizeof(*INPUT);

class van_eck_generator {
    public:
        int next();
        van_eck_generator();
        int turn_offset;
    private:
        int turn;
        int last_value;
        std::unordered_map<int, int> seen;
};

van_eck_generator::van_eck_generator() {
    turn_offset = INPUT_SIZE + 1;
    int cur_value = 0;
    for (int i = 0; i < INPUT_SIZE; i++) {
        cur_value = INPUT[i];
        seen[cur_value] = i + 1;
    }
    turn = turn_offset;
    last_value = 0;
}

int van_eck_generator::next() {
    int result = last_value;
    auto contains = seen.contains(last_value);
    int next_value = contains ? turn - seen[last_value] : 0;
    seen[last_value] = turn;
    last_value = next_value;
    ++turn;
    return result;
}

int main() {
    van_eck_generator gen;
    int num_turns = 30000000 - gen.turn_offset + 1;
    //int num_turns = 2020 - gen.turn_offset + 1;
    int last_num = 0;
    for (int i = 0; i < num_turns; i++) {
        last_num = gen.next();
    }
    std::cout << "Part 2: " << last_num << std::endl;
    return 0;
}