# [![wazobia logo][]][play link]

wazobia-open-speech is an automatic speech recognition system that can understand english accents spoken by native Africans. Wazobia open speech is built on top of Mozilla's [DeepSpeech engine][deepspeech link].

## Steps to train
Download [training audio files][wazobia folder link]. Use download as zip option.

Move unzipped wazobia directory to ./util

Change directory to root of repo

Install all python and runtime dependencies
```bash
$ sudo bash prepare.sh
```
Change directory to deepspeech
```bash
$ cd DeepSpeech9
```
Train
```bash
$ python DeepSpeech.py --n_hidden 2048 --checkpoint_dir fine_tuning_checkpoints/ --epochs 100 --train_files training_csvs/train.csv --dev_files training_csvs/dev.csv --test_files training_csvs/test.csv --learning_rate 0.0001 --export_dir output_models/ --use_allow_growth true --train_cudnn true
```

## Tips before training
- Wazobia open speech wiil only run on a linux based system. It has been tested on Ubuntu 18.04.
- Using a GPU is 20x faster, to opt-out of using a GPU set the --train_cudnn flag to false
- We recommend using google colab especially if you don't have a GPU, see [./wzb_colab_example.ipynb](wzb_colab_example.ipynb)

## Benchmark
We provide a [model][benchmark model link] as benchmark trained with the following flags:
- **n_hidden** (number of hidden layers): &nbsp; **2048**
- **epochs**: &nbsp; **100**
- **learning_rate**: &nbsp; **0.0001**

### Result in benchmark
WER = Word Error Rate  
CER = Character Error Rate

| WER | CER |
| ------ | ------ |
| 0.992230 | 0.581740 |

## Data collection
Speech data is collected by means of a mobile application ([wazobia open speech mobile][play link]) written with [flutter](https://flutter.dev). The app is currently only available for download in Nigeria although a website will be available in the near future for data collection. The source codes for the mobile and web applications will also be availed to the public.

## Collecting your own data
Wazobia open speech mobile and web can be modified to collect your own data.


[wazobia logo]: <https://user-images.githubusercontent.com/47289054/101842706-ef18dc00-3b48-11eb-98f7-c717d0cdc193.png>
[play link]: <https://play.google.com/store/apps/details?id=com.fgml5g.wazobia>
[deepspeech link]: <https://deepspeech.readthedocs.io/en/latest/TRAINING.html>
[benchmark model link]: <https://mega.nz/file/YQB2RbQD#TnbUPbO35oIY7NIQ2uinrJ2qgmKewt-cYQyEf-hhRmQ>
[wazobia folder link]: <https://mega.nz/folder/NN4k2STb#WjOoK2i2iw8aUbzKTsX-Vw>
