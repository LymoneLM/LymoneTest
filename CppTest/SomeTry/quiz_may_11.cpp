
// Your name :
// Quiz May 11

/*
An object of class Box can be printed as rectangle shape formed by characters. By  default the shape is hollow, and the character  '.' are printed at the border.
if x is an object of Bar, then
-   +x creates a new object, which is the same as x but when it is printed, a solid rectangle is shown.
-   x*n creates a new object, (for some positive integer n) whose height and width are n times with x
-   (bonus)   x.contain("text") will put the text inside a box, in away that and when part of the text fill the space of a row within the box, then the remaining text it will go to the next line. only the content of the text that the box can hold will appear (and remembered) in the box. You can decide other behavior of the Box.
*/

/* provide missing code, which may include  the following:
 - declaration of the class Box
 - some constructors of Box
 - destructor of Bar if needed (if it has storage on the heap)
 - overloaded operator of postive +
 - overloaded operator of *
 - overloaded operator of <<
 - overloaded operator of =  (if it is needed)
 - the member function contain().
*/

#include <bits/stdc++.h>
#include "box.hpp"
using namespace std;
int main(void) {

    Box x(3, 3), y(3, 5, '*');
    Box z = y;
    cout << "x is :  \n"
         << x << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    cout << "y is :  \n"
         << y << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    cout << "z is :  \n"
         << z << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    cout << "+x is :  \n"
         << +x << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    cout << "x*3 is :  \n"
         << x * 3 << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    z = (+y) * 2; // z has 10 +
    cout << "after z = (+y)*2, z is :  \n"
         << z << endl;
    cout << "~~~~~~~~~~~~~~~~~~~~~~~\n";
    // Bonus part, do it if you have time:
    Box book(6, 10, '+');
    book.contain("long long time ago, in a galaxy far far away. ");
    cout << "book is \n";
    cout << book << endl;
    return 0;
}

/* Results shown on screen

x is :
. . .
.   .
. . .
~~~~~~~~~~~~~~~~~~~~~~~
y is :
* * * * *
*       *
* * * * *
~~~~~~~~~~~~~~~~~~~~~~~
z is:
* * * * *
*       *
* * * * *
~~~~~~~~~~~~~~~~~~~~~~~
+x is :
. . .
. . .
. . .
~~~~~~~~~~~~~~~~~~~~~~~
x*3 is :
. . . . . . . . .
.               .
.               .
.               .
.               .
.               .
.               .
.               .
. . . . . . . . .
~~~~~~~~~~~~~~~~~~~~~~~
after z = (+y)*2, z is :
* * * * * * * * * *
* * * * * * * * * *
* * * * * * * * * *
* * * * * * * * * *
* * * * * * * * * *
* * * * * * * * * *
~~~~~~~~~~~~~~~~~~~~~~~
book is :
+ + + + + + + + + +
+long long time ag+
+o, in a galaxy fa+
+r far away.      +
+                 +
+ + + + + + + + + +


*/