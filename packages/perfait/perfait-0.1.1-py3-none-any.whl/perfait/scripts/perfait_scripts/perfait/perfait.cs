using System;

namespace Perfait {
  public class Stopwatch {
    static public double GetTime(){
      DateTime nowTime = DateTime.UtcNow;
      return new DateTimeOffset(nowTime).ToUnixTimeSeconds() + (double)nowTime.Millisecond / 1000;
    }

    private double m_StartTime;

    public Stopwatch(){
      Reset();
    }

    public void Reset(){
      m_StartTime = GetTime();
    }

    public double ElapsedTime(){
      return GetTime() - m_StartTime;
    }
  }
}
