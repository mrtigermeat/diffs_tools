import csv
import random
import click
from glob import glob
from pathlib import Path as P
from tqdm import tqdm

def write_config(cfg, db_idx, val_num):
	with open('dataset_cfg.yaml', 'w', encoding='utf-8') as f:
		f.write("# generated with tigermeat\'s dataset config tool. :)\n")
		f.write(f"num_spk: {db_idx+1}\n\n")
		f.write(f"datasets:\n")
		for i, ds in enumerate(cfg):
			f.write(f"- language: {ds['language']}\n")
			f.write(f"  raw_data_dir: {ds['raw_data_dir']}\n")
			f.write(f"  speaker: {ds['speaker']}\n")
			f.write(f"  spk_id: {ds['spk_id']}\n")
			f.write(f"  test_prefixes: {str(ds['test_prefixes'][0])}\n")

def sort_val(trns_path: str, val_num: int):
	name_list = []
	val_list = []
	trns = []

	with open(trns_path, 'r', encoding='utf-8') as csv_file:
		trns_read = csv.DictReader(csv_file)

		for row in trns_read:
			trns = [row for row in trns_read]

	for i, line in enumerate(trns):
		name_list.append(trns[i]['name'])

	for i in range(val_num):
		random_prfx = random.choice(name_list)
		val_list.append(random_prfx)
		name_list.remove(random_prfx)

	return val_list

val_range = click.IntRange(min=0, max=10, clamp=True)
@click.command(help="Tool used to automate the creation of the dataset section of a DiffSinger configuration. For DSv2 Only!")
@click.argument('in_path', metavar='PATH')
@click.option('-v', '--val_num', type=val_range, required=False, default=1, help="Amount of validation files chosen per dataset.")
def build_db_config(in_path: str, val_num: int):
	datasets = []
	speakers = {}
	db_idx = 0

	for i, db in tqdm(enumerate(sorted(glob(f"{in_path}/**/transcriptions.csv", recursive=True)))):
		name_list = []
		temp_dict = {}
		db_path = P(db)
		language = str(db_path.parents[1])
		db_name = str(db_path.parents[0])[len(language)+1:]

		if db_name not in speakers.keys():
			speakers[db_name] = db_idx
			db_idx = db_idx + 1

		temp_dict['raw_data_dir'] = str(db_path.absolute().parents[0])
		temp_dict['speaker'] = db_name
		temp_dict['spk_id'] = speakers[db_name]
		temp_dict['language'] = language
		temp_dict['test_prefixes'] = []
		temp_dict['test_prefixes'].append(sort_val(db, val_num))
		datasets.append(temp_dict)

	try:
		write_config(datasets, db_idx, val_num)
		print('Successfully wrote config to \'dataset_cfg.yaml\'. You will need to manually add it to your DiffSinger configuration file.')
		return datasets
	except Exception as e:
		print('Unable to write config.')
		return None

if __name__ == "__main__":
	build_db_config()
