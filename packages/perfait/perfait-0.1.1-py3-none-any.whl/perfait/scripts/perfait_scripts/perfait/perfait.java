package perfait;

class Stopwatch {
  static public double get_time(){
    var nanoTime = (double)System.nanoTime();
    return nanoTime / 1000000000 + ((nanoTime % 1000000000) / 1000000000);
  }

  private double __StartTime;

  public Stopwatch(){
    this.reset();
  }

  public void reset(){
    this.__StartTime = Stopwatch.get_time();
  }

  public double elapsed_time(){
    return Stopwatch.get_time() - this.__StartTime;
  }
}
