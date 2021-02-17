from hbo import HBO
from netflix import Netflix
from upload import Upload
import datetime as dt

print('hbo urls request started at: ', dt.datetime.now())

hbo = HBO()
hbo.make_url_list()
print('hbo url list produced at: ', dt.datetime.now())
# hbo.get_url_list()
# hbo.read_urls_from_json()
hbo.get_data()
print('hbo data ready at: ', dt.datetime.now())

upload = Upload()
upload.upload_file('hbo')

print('netflix urls request started at: ', dt.datetime.now())
netflix = Netflix()
netflix.make_urls()
print('netflix url list produced at: ', dt.datetime.now())
# netflix.read_urls_from_json()
netflix.get_data()
print('netflix data ready at: ', dt.datetime.now())

upload.upload_file('netflix')
