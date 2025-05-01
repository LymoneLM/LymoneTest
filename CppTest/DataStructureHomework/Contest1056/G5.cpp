#include <iostream>
#include <stack>
#include <string>

bool isOperator(char c) {
    return (c == '+' || c == '-' || c == '*' || c == '/');
}

int getPrecedence(char c) {
    if (c == '+' || c == '-') {
        return 1;
    } else if (c == '*' || c == '/') {
        return 2;
    }
    return 0;
}

std::string infixToPostfix(const std::string& infix) {
    std::string postfix;
    std::stack<char> operators;

    for (size_t i = 0; i < infix.length(); ++i) {
        char c = infix[i];

        if (std::isdigit(c)) {
            std::string number;
            while (i < infix.length() && std::isdigit(infix[i])) {
                number += infix[i];
                ++i;
            }
            --i;
            postfix += number;
            postfix += ' ';
        } else if (isOperator(c)) {
            while (!operators.empty() && operators.top() != '(' && getPrecedence(operators.top()) >= getPrecedence(c)) {
                postfix += operators.top();
                postfix += ' ';
                operators.pop();
            }
            operators.push(c);
        } else if (c == '(') {
            operators.push(c);
        } else if (c == ')') {
            while (!operators.empty() && operators.top() != '(') {
                postfix += operators.top();
                postfix += ' ';
                operators.pop();
            }
            if (!operators.empty() && operators.top() == '(') {
                operators.pop();
            }
        }
    }

    while (!operators.empty()) {
        postfix += operators.top();
        postfix += ' ';
        operators.pop();
    }

    return postfix;
}

int main() {
    std::string infix;
    std::getline(std::cin, infix);

    std::string postfix = infixToPostfix(infix);
    std::cout << postfix << std::endl;

    return 0;
}
