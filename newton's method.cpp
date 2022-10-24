/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
#include <math.h>

using namespace std;

double x1 = 1;
double xn1,xn,numerator,denominator;

int main()
{

    do{
        numerator = pow(x1,2)-3*sin(x1);
        denominator = 2*x1-3*cos(x1);
        xn = x1-numerator/denominator;
        xn1 = x1;
        x1 = xn;
    }
    while(xn1 != xn);
    
    printf("The answer is %f\n",xn1);

    return 0;
}
