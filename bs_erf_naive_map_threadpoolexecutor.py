from  concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from bs_executor import bs_runner
from bs_naive import black_scholes_map
import base_bs_erf

if __name__ == '__main__':
    n = cpu_count()
    with ThreadPoolExecutor(n) as executor:
        bsr = bs_runner(black_scholes_map, executor, n)
        base_bs_erf.run(__file__, bsr, pass_args=False)
