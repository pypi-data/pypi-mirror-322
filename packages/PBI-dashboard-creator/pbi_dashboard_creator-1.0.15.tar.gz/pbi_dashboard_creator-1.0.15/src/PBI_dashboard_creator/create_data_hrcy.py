# This is needed for creating data heirachy's for dates to make dates work correctly
import uuid

function(DATA_SOURCE = dataset_name, )

# create new file id
# create new table id


FILE_ID = str(uuid.uuid4())
TABLE_ID = str(uuid.uuid4())

with open("python_resources/LocalDateTable_FILE_ID.tmdl") as date_hr:
	# read line by line and replace
	# write back to file


