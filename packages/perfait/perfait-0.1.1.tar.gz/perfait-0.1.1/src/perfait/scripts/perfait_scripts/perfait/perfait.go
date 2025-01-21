package perfait

import (
  "time"
)

func GetTime()(float64){
  nowTime := time.Now()
  return float64(nowTime.Unix()) + (float64(nowTime.UnixNano()) / 1000000000)
}

type Stopwatch struct {
  __StartTime float64
}

func StopwatchNew()(*Stopwatch){
  stopwatch := &Stopwatch{}
  stopwatch.Reset()
  return stopwatch
}

func (stopwatch *Stopwatch)Reset(){
  stopwatch.__StartTime = GetTime()
}

func (stopwatch *Stopwatch)ElapsedTime()(float64){
  return GetTime() - stopwatch.__StartTime
}
