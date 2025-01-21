class Stopwatch {
  static get_time(){
    var nowTime = (new Date()).getTime();
    return nowTime / 1000 + ((nowTime % 1000) / 1000);
  }

  #__StartTime;

  constructor(){
    this.reset();
  }

  reset(){
    this.#__StartTime = Stopwatch.get_time();
  }

  elapsed_time(){
    return Stopwatch.get_time() - this.#__StartTime;
  }
}

module.exports = {
  Stopwatch: Stopwatch,
}
