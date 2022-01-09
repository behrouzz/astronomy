import numpy as np
from jplephem.spk import SPK
from jplephem.excerpter import write_excerpt

kernel = SPK.open('../bsp_files/de421.bsp')

sm = kernel.daf.summaries()
"""
write_excerpt(input_spk='../bsp_files/de421.bsp',
              output_file='test_de421.bsp',
              start_jd=2450000.50,
              end_jd=2460000.50),
              #summaries=sm)
"""

#python -m jplephem excerpt 2018/1/1 2018/4/1 https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/jup310.bsp excerpt.bsp
