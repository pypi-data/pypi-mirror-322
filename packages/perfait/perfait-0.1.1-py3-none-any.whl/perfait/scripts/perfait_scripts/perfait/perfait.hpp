#ifndef __PERFAIT_H__
#define __PERFAIT_H__
#include <cstdlib>
#include <stdio.h>
#include <time.h>

namespace Perfait {
  class Stopwatch {
    public:
      static double GetTime(){
        struct timespec ts;
        clock_gettime(CLOCK_REALTIME, &ts);
        return (double)ts.tv_sec + ((double)ts.tv_nsec / 1000000000);
      }

    private:
      double __StartTime;

    public:
      Stopwatch(){
        Reset();
      }

      void Reset(){
        __StartTime = GetTime();
      }

      double ElapsedTime(){
        return GetTime() - __StartTime;
      }
  };
}
#endif
