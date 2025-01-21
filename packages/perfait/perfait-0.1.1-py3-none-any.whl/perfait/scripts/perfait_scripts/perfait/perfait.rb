module Perfait
  class Stopwatch
    def self.get_time
      return Time.now().to_f
    end

    def initialize
      reset()
    end

    def reset
      @__StartTime = Stopwatch.get_time()
    end

    def elapsed_time
      Stopwatch.get_time() - @__StartTime
    end
  end
end
