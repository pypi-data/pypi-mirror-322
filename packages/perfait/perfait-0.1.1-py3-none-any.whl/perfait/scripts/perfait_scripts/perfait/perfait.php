<?php
namespace Perfait;

class Stopwatch {
  static public function get_time(){
    $nowTime = hrtime();
    return (double)$nowTime[0] + ((double)$nowTime[1] / 1000000000);
  }

  private $__StartTime;

  function __construct(){
    $this->reset();
  }

  public function reset(){
    $this->__StartTime = Stopwatch::get_time();
  }

  public function elapsed_time(){
    return Stopwatch::get_time() - $this->__StartTime;
  }
}
?>
