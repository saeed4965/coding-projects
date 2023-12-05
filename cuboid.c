#include <stdio.h>
#include <stdbool.h>

long long int calculateLCM(long long int a, long long int b) {
    long long int max, min, lcm, i;

    max = (a > b) ? a : b;
    min = (a < b) ? a : b;

    for (i = 1; i <= max; i++) {
        lcm = max * i;
        if (lcm % min == 0) {
            return lcm;
        }
    }
    
    return max;
}

int main() {
    long long int lcmDenominator = 1;
    int numProducts = 0;

    printf("Product size:\n");

    while (1) {
        double length, width, height;
        int scanned = scanf("%lf %lf %lf", &length, &width, &height);

        if (scanned == EOF) {
            break;
        }

        if (scanned != 3) {
            printf("Invalid input. Three numbers were not entered for the product.\n");
            return 1;
        }

        if (length < 0.01 || width < 0.01 || height < 0.01 || length > 10000000.00 || width > 10000000.00 || height > 10000000.00) {
            printf("Invalid dimension entered for a product. Dimensions must be between 0.01 and 10000000.00.\n");
            return 1;
        }

        numProducts++;

        lcmDenominator = calculateLCM(lcmDenominator, (long long)(100 * length));
        lcmDenominator = calculateLCM(lcmDenominator, (long long)(100 * width));
        lcmDenominator = calculateLCM(lcmDenominator, (long long)(100 * height));
    }

    if (numProducts == 0) {
        printf("No products have been entered.\n");
        return 1;
    }
    double boxSize = (double)lcmDenominator / 100.0;
    printf("Product size:\n");
    if(boxSize > 10000000){
      printf("Box too Big");
    }
    else
    printf("Box size: %.2lf\n", boxSize);

    return 0;
}
