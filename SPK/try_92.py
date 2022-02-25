n = 1024

with open('de421.bsp', 'rb') as f:
    f.seek(0, 0)
    rec1 = f.read(n)


LOCIDW = rec1[:8]
ND = int.from_bytes(rec1[8:12], byteorder='big')
NI = int.from_bytes(rec1[12:16], byteorder='big')
LOCIFN = rec1[16:76]
FWARD = int.from_bytes(rec1[76:80], byteorder='big')
BWARD = int.from_bytes(rec1[80:84], byteorder='big')
FREE = int.from_bytes(rec1[84:88], byteorder='big')
LOCFMT = rec1[88:96]
PRENUL = rec1[96:699]
FTPSTR = rec1[699:727]
# FTPSTR = SPICELIB_ZZFTPSTR(FTPSTR)
PSTNUL = rec1[727:1024]

from struct import Struct

endian = {b'BIG-IEEE': '>', b'LTL-IEEE': '<'}.get(rec1[88:96])

fmt = endian + '8sII60sIII8s603s28s297s'

file_record_struct = Struct(fmt)

(locidw, nd, ni, locifn, fward, bward,
 free, locfmt, prenul, ftpstr, pstnul) = file_record_struct.unpack(rec1)


locifn_text = locifn.rstrip()
summary_format = 'd' * nd + 'i' * ni


summary_control_struct = Struct(endian + 'ddd')
summary_struct = struct = Struct(endian + summary_format)
summary_length = length = struct.size
summary_step = length + (-length % 8) # pad to 8 bytes
summaries_per_record = (1024 - 8 * 3) // summary_step
