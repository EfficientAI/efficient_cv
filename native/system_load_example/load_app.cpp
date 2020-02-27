// Threading for creating synthetic system load.
#include <iostream> 
#include <thread> 
#include <vector>
#include <chrono>
#include <cstdlib>
#include <unistd.h>

typedef std::chrono::high_resolution_clock Clock;

using namespace std;

void workload(int compute_time, int sleep_time) { 
    // Based on the load, this function does proportinal useless computation
    // more load, more the computation and less the sleeping
    for(int i=0;i<10000;i++){
        float var = 2.0;
        auto t1 = Clock::now();
        auto wakeup = t1 + chrono::milliseconds(compute_time);
        while(Clock::now() < wakeup) {
            if(var > 1000000){
                var = 2.0;
            }
            var = var + 1.0;
            var = var*var;
        }
        this_thread::sleep_for(chrono::milliseconds(sleep_time));
    }
}

int main() 
{ 
    cout << "Threading example program" << endl; 
    thread thread1(workload, 100, 500);
    //thread thread2(workload, 100, 100);
    //thread thread3(workload, 100, 100);
    //thread thread4(workload, 100, 100);
    cout << "Launched threads, now waiting for it to complete" << endl;
    thread1.join();
    //thread2.join();
    //thread3.join();
    //thread4.join();
    cout << "All thread completed, now exiting" << endl;
    return 0; 
} 