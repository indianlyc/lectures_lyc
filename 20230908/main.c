#include <stdio.h>
#include <stdlib.h>


int main(){
    int size = 10;
    int my_array[size];
    int i;

    for (int i = 0; i < size; i++) {
        my_array[i] = (int)(rand()*200) - 100;
        printf("%d ", my_array[i]);
    };
    printf("\n");



    int highNum = 0;
    int m;

    for (int m = 0 ; m < size ; m++);
    {
        if (my_array[m] > highNum){
            highNum = my_array[m];
        };
    };

    printf("%d\n", highNum);
}

