# dataset_config_gen.py
This tool is meant to be used to assist in making the `dataset` part of a DiffSinger configuration. Currently, it only works for V2 type configs, but when V3 is out and documented, it will be updated.

## Usage
1. Set up dependencies. `pip install click tqdm`
2. Set up your DIFFSINGER-STYLE data folders to mirror the following structure (comments preceeded by a #):
```yaml
en # language code, can be any length. (for example, Cantonese is 'yue')
|  speaker1
|  |  wavs
|  |  |  blah_blah_seg000.wav
|  |  |  ...
|  |  transcriptions.csv
|  speaker2
ja
|  speaker1 # if speakers have the same name, they will be assigned the same spk_id
|  speaker2
yue
|  speaker4
...
```
3. Put your copy of the script in any folder, but the same folders as the 'en'/'ja'/etc folders works just fine.
4. Run the script like so: `python dataset_config_gen.py {PATH}` where {PATH} is the path to where your language code folders are. If you put the script in the same folder, you can enter "." (`python dataset_config_gen.py .`)
5. It will export a file called `dataset_cfg.yaml`, which you can copy and paste into your DiffSinger dataset.

By default, the amount of validation files will only be 1. If you want to do more, you can pass the following command:
`python dataset_config_gen.py {PATH} -v {VAL_NUM}` where VAL_NUM is the amount of validation files. PLEASE DO NOTE: Your VB must have at least that amount of segments + 1 otherwise the generator won't work. This is so unlikely that I'm not even coding a way to handle it in. Just use 1 validation file you don't need that many. This should work on any operating system thanks to pathlib.
