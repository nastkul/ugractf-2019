#include <ctime>
#include <cstdio>

const int MAX_SIZE = 100000;

const int EXIT_OK = 0, EXIT_WA = 1;

int main(int argc, char* argv[]) { 
    struct {
        FILE *rnfd, *infd, *oufd;
        int random, n, k, i, sum, tokens;
        int numbers[MAX_SIZE];
        int read;
        int verdict;
    } v;

    v.rnfd = fopen("/dev/urandom", "r");
    
    fread((void*)&v.random, 1, 4, v.rnfd);
    fclose(v.rnfd);
    
    if (v.random < 0) {
        v.random = ~v.random;
    }
    
    v.infd = fopen(argv[1], "r");
    v.oufd = fopen(argv[2], "r");
    
    v.verdict = EXIT_WA;
    
    fscanf(v.infd, "%d", &v.n);
    v.random %= v.n;
    
    fscanf(v.oufd, "%d", &v.k);
    
    v.sum = 0;
    v.read = 0;
    
    for (v.i = 0; v.i < v.k; v.i++) {
        v.tokens = fscanf(v.oufd, "%d", &v.numbers[v.i]);
        v.sum += v.numbers[v.i];
        
        if (v.numbers[v.i] > v.n) {
            fprintf(stderr, "participant number %d is greater than n = %d\n", v.numbers[v.i], v.n);
            return EXIT_WA;
        }
        
        v.read += v.tokens;
        v.sum %= v.n;
    }
    
    if (v.read < v.k) {
        fprintf(stderr, "can't read input %d\n", v.read);
        return EXIT_WA;
    }
    
    if (v.k <= v.n && v.sum == v.random) {
        v.verdict = EXIT_OK;
    }
    
    fprintf(stderr, "magic number was %d, participant has %d\n", v.random, v.sum);
    
    fclose(v.infd);
    fclose(v.oufd);
    
    return v.verdict;
}
