import pandas as pd
import os, uuid, json


def add_csv(dashboard_path, data_path):

  # generate a random id for the data set
	dataset_id = str(uuid.uuid4())


	# extract bits of names for later
	path_end = os.path.basename(data_path)
	split_end = os.path.splitext(path_end)

	dataset_name = split_end[0]
	dataset_extension =split_end[1]


	report_name = os.path.basename(dashboard_path)

  # Reverse slash directions bc windows is stooooooopid
	data_path_reversed = data_path.replace('/', '\\')
	


	# file paths
	semantic_model_folder = os.path.join(dashboard_path, f'{report_name}.SemanticModel' )
	model_path = os.path.join(semantic_model_folder, 'definition/model.tmdl')
	diagram_layout_path = os.path.join(semantic_model_folder, 'diagramLayout.json')

	tables_folder = os.path.join(semantic_model_folder, 'definition/tables')
	dataset_file_path = os.path.join(tables_folder, f'{dataset_name}.tmdl')

	# create a tables folder if it doesn't already exist
	if not os.path.exists(tables_folder):
		os.makedirs(tables_folder)

    
    # sink inital header stuff about dataset
	with open(dataset_file_path, 'w') as file:
		file.write(f'table {dataset_name}\n\tlineageTag: {dataset_id}\n\n')

    # read in the dataset
    # compare how pandas manages to do this in a single line 
    # and Power BI requires 40 lines of code and modifying multiple files to do the same thing
    # in case you needed evidence of how dummmmmmmbbb Power BI, Power querry and M are.....

    # load dataset using pandas
	dataset = pd.read_csv(data_path)


	col_names = []
	col_deets = []


    # loop through columns and write specs out to model file
	for col in dataset:

		# add the column's name to a set for later
		col_names.append(col)

		# record more details in a different set

		col_id = str(uuid.uuid4())

		if dataset[col].dtype == "int64" or dataset[col].dtype == "float64":

			# record more details in a different set
			col_deets.append(f'{{"{col}", Int64.Type}}')


			with open(dataset_file_path, 'a') as file:
				file.write(f'\tcolumn {col}\n')
				file.write('\t\tdataType: int64\n')
				file.write('\t\tformatString: 0\n')
				file.write(f'\t\tlineageTag: {col_id}\n')
				file.write('\t\tsummarizeBy: sum\n')
				file.write(f'\t\tsourceColumn: {col}\n\n')
				file.write('\t\tannotation SummarizationSetBy = Automatic\n\n')

		if dataset[col].dtype == "object":

			# record more details in a different set
			col_deets.append(f'{{"{col}", type text}}')

			with open(dataset_file_path, 'a') as file:
				file.write(f'\tcolumn {col}\n')
				file.write('\t\tdataType: string\n')
				file.write(f'\t\tlineageTag: {col_id}\n')
				file.write('\t\tsummarizeBy: sum\n')
				file.write(f'\t\tsourceColumn: {col}\n\n')
				file.write('\t\tannotation SummarizationSetBy = Automatic\n\n')



	# write out M code 
	# bc we're stilllllllll not done.....
	with open(dataset_file_path, 'a') as file:
		file.write(f'\tpartition {dataset_name} = m\n')
		file.write('\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n')
		file.write(f'\t\t\t\t\tSource = Csv.Document(File.Contents("{data_path_reversed}"),[Delimiter=",", Columns=10, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n')
		file.write('\t\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n')
		file.write(f'\t\t\t\t\t#"Replaced Value" = Table.ReplaceValue(#"Promoted Headers","NA",null,Replacer.ReplaceValue,{{\"{'", "'.join(col_names)}\"}}),\n')
		file.write(f'\t\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Replaced Value",{{{', '.join(map(str, col_deets))}}})\n')
		file.write('\t\t\t\tin\n\t\t\t\t\t#"Changed Type"\n\n')
		file.write('\tannotation PBI_ResultType = Table\n\n\tannotation PBI_NavigationStepName = Navigation\n\n')




	# add dataset to diagramLayout file ---------------------------------------------------------------------
	with open(diagram_layout_path,'r') as file:
		diagram_layout = json.load(file)


	# add all this junk to describe the table's "nodes"
	diagram_layout["diagrams"][0]["nodes"] =  [
        {
          "location": {
            "x": 0,
            "y": 0
          },
          "nodeIndex": "colony",
          "nodeLineageTag": dataset_id,
          "size": {
            "height": 300,
            "width": 234
          },
          "zIndex": 0
        }
      ]

   
	# write to file
	with open(diagram_layout_path,'w') as file:
		json.dump(diagram_layout, file, indent = 2)





	# modify model.tdml file -------------------------------------------------------------------------------------
	with open(model_path, 'a') as file:
		file.write(f'annotation PBI_QueryOrder = [{dataset_name}]\n\nref table {dataset_name}')












