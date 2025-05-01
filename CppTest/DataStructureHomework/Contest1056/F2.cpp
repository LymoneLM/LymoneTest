#include <iostream>
#include <stack>
#include <string>

bool checkBrackets(const std::string& expression) {
    std::stack<char> stack;
    std::string openingBrackets = "([{";
    std::string closingBrackets = ")]}";

    for (char c : expression) {
        if (openingBrackets.find(c) != std::string::npos) {
            stack.push(c);
        } else if (closingBrackets.find(c) != std::string::npos) {
            if (stack.empty() || openingBrackets.find(stack.top()) != closingBrackets.find(c)) {
                return false;
            }
            stack.pop();
        }
    }

    return stack.empty();
}

int main() {
    std::string expression;
    std::getline(std::cin, expression);

    bool bracketsMatch = checkBrackets(expression);

    if (bracketsMatch) {
        std::cout << "YES" << std::endl;
    } else {
        std::cout << "NO";

        char lastBracket = expression.back();
        if (lastBracket == ')') {
            std::cout << "1";
        } else if (lastBracket == ']') {
            std::cout << "2";
        } else if (lastBracket == '}') {
            std::cout << "3";
        }

        std::cout << std::endl;
    }

    return 0;
}
