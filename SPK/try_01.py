from jplephem.spk import SPK

k = SPK.open('de421.bsp')
d = k.daf

print([i for i in dir(d) if i[0]!='_'])

# reserved records
#print(d.comments())

# summary records
sum_rec = [*d.summary_records()][0] #binary

rec1 = d.read_record(1)

com = d.comments()

k.close()
