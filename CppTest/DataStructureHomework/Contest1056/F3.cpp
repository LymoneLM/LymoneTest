#include <iostream>
#include <stack>
#include <string>

using namespace std;

bool isMatchingPair(char opening, char closing) {
    if (opening == '(' && closing == ')')
        return true;
    if (opening == '[' && closing == ']')
        return true;
    if (opening == '{' && closing == '}')
        return true;
    return false;
}

string checkParentheses(const string& expression) {
    stack<char> s;

    for (char c : expression) {
        if (c == '(' || c == '[' || c == '{') {
            s.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (s.empty() || !isMatchingPair(s.top(), c)) {
                if (c == ')')
                    return "NO1";
                else if (c == ']')
                    return "NO2";
                else if (c == '}')
                    return "NO3";
            } else {
                s.pop();
            }
        }
    }

    return (s.empty()) ? "YES" : "NO3";
}

int main() {
    string expression;
    cin >> expression;

    cout << checkParentheses(expression) << endl;

    return 0;
}
