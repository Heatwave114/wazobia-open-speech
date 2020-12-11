#! /bin/bash


# path to this script
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


# into ./ directories
TRAINING_CSVS_DIR="$SCRIPTPATH/DeepSpeech9/training_csvs"


# into deepspeech directories
DS_OUTPUT_MODELS_DIR="$SCRIPTPATH/DeepSpeech9/output_models"
DS_FINE_TUNING_CHECKPOINTS_DIR="$SCRIPTPATH/DeepSpeech9/fine_tuning_checkpoints"
DS_TRAINING_CSVS_DIR="$SCRIPTPATH/DeepSpeech9/training_csvs"


# make into deepspeech directories if they don't exist
if [ ! -d "$DS_OUTPUT_MODELS_DIR" ]
then
  echo "making output_models directory"
  mkdir "$DS_OUTPUT_MODELS_DIR"
fi

if [ ! -d "$DS_FINE_TUNING_CHECKPOINTS_DIR" ]
then
  echo "making fine_tuning_checkpoints directory"
  mkdir "$DS_FINE_TUNING_CHECKPOINTS_DIR"
fi

if [ ! -d "$DS_TRAINING_CSVS_DIR" ]
then
  echo "making training_csvs directory"
  mkdir "$DS_TRAINING_CSVS_DIR"
fi


# prepare and install requirements for util
pip install pipreqs
pipreqs --force "$SCRIPTPATH/util/"
pip install -r "$SCRIPTPATH/util/requirements.txt"


# prepare training data
echo "preparing csvs..."
python "$SCRIPTPATH/util/prepare_tokens.py"
echo "splitting csvs..."
python "$SCRIPTPATH/util/build_dataset.py"

# # # # # # # # # # # # # #
# if [ $(ls -A "$TRAINING_CSVS_DIR") ]
# then
#   echo "Training files already exsit in ./"
# else
#   echo "preparing csvs..."
#   python "$SCRIPTPATH/util/prepare_tokens.py"
#   echo "splitting csvs..."
#   python "$SCRIPTPATH/util/build_dataset.py"
# fi
# # # # # # # # # # # # # #


# copy csvs into deepspeech
echo "moving prepared csvs into deepspeech..."
cp -a "$SCRIPTPATH/training_csvs/." "$SCRIPTPATH/DeepSpeech9/training_csvs/"

# # # # # # # # # # # # # #
# if [ $(ls -A "$DS_TRAINING_CSVS_DIR") ]
# then
#   echo "Training files already exsit in deepspeech"
# else
#   echo "moving prepared csvs into deepspeech..."
#   cp -a "$SCRIPTPATH/training_csvs/." "$SCRIPTPATH/DeepSpeech9/training_csvs/"
# fi
# # # # # # # # # # # # # #


#install all runtime dependencies
sudo apt install sox -y
sudo apt install git -y
sudo apt install git-lfs -y
git lfs install -y
sudo apt-get install python-dev -y
sudo apt-get install build-essential -y


#install all deepspeech dependencies
cd "$SCRIPTPATH/DeepSpeech9"
pip install --upgrade pip==20.2.2 wheel==0.34.2 setuptools==49.6.0
pip install --upgrade -e .
make Dockerfile.train


# check if there is a GPU
python "$SCRIPTPATH/util/check_gpu.py"

echo -e "\e[32mAll done!"
