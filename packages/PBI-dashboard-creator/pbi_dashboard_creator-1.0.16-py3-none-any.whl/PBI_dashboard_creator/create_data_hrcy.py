# This is needed for creating data heirachy's for dates to make dates work correctly
import uuid, os

def create_date_hr(dataset_name, dashboard_path, report_name ):

	# create new file id
	FILE_ID = str(uuid.uuid4())

	# create new table id
	TABLE_ID = str(uuid.uuid4())

	date_template_path = os.path.join(dashboard_path, "python_resources/LocalDateTable_FILE_ID.tmdl" )
	date_heirarchy_path = os.path.join(dashboard_path, f"{report_name}.SemanticModel/definition/tables/LocalDateTable_{FILE_ID}.tmdl" )

	with open(date_heirarchy_path, "w") as date_hr:
		with open(date_template_path, "r") as date_template:
			# read line by line and replace
			for line in date_template:

				# loop through file and replace placeholders with values
				line = line.replace("FILE_ID", FILE_ID)
				line = line.replace("TABLE_ID", TABLE_ID)

				# create a random new UIID for each column
				line = line.replace("COL_ID", str(uuid.uuid4()))

				# replace data source
				line = line.replace("DATA_SOURCE", dataset_name )

				# write back to file
				date_hr.write(line)



create_date_hr(dataset_name = "colony", dashboard_path = "C:/Users/rps1303/PBI_projects/poop", report_name = "poop")
		








