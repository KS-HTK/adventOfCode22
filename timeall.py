from time import perf_counter

times = {}
for i in range(20):
  name = f'day{i+1:02d}.day{i+1:02d}'
  day = __import__(name, fromlist=[''])

  t = perf_counter()
  day.solve()
  times[perf_counter()-t] = name

max_time = max(times.keys())
print(times[max_time], f'{max_time:,.4f}', 'sec')
