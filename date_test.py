import arrow as ar

gametime =  ar.get('2022-09-03T19:30:00.000Z', 'YYYY-MM-DDTHH:mm:ss.000Z').to('local').format()
print(gametime[:10])
#print(gametime)
