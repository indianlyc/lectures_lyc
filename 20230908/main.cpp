#include <iostream>
#include <algorithm>

using namespace std;

int get_max()


int main()
{
    int array[11];
    int n = 10;
    for (int i = 0; i < n; i++) {
       array[i] = i;
    }
    array[5] = 5000;
    max(array , array + n);
    for (int i = 0; i < n; i++)
        cout << array[i] << " ";
    return 0;
}