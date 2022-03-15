# PR (Pull Request) data and analysis of benchmarking bots

## Project layout

### data
This directory contains all the data and analyses for each of the mined projects.

- **projects**: In this folder you can find each of the mined projects with their corresponding data.
  - **_project name_**: This folder contains all the images created by the analyses as well as the PR data for the project. All the results flow from 2 .json files:
    - **botPRData.json**: This file contains all the PR's the project's benchmarking bot contributed to.
    - **nonBotPRs.json**: This file contains all the PR's the project's benchmarking bot **did not** contribute to.
- **summary**: This directory contains a summary created for each of the projects, _not used in the article_.

### settings
This directory contains all the settings that can be changed during mining/analysis. Currently, the only change that can be made is to specify which project(s) you want to mine/analyze. This can be done in the _projects.json_ file.

### src
This is the folder where the mining/analysis is performed. The top-level Python files perform the following action
- **analyzer.py**: Performs the analysis according to the settings.
- **get-pip.py**: File to get Pip, a Python module manager.
- **miner.py**: Performs the mining according to the settings.
- **summarizer.py**: Creates the summary data, again this is _not used in the article_.

The other Python scripts are utilities used for various purposed in the project. Feel free to have a look.

## Running the project

First off, all the analysis data can be found in the data directory without running either the analysis or mining script.

If you want to run the project do the following:

1. Navigate to the root directory of this project (..\\..\\IEE2021BenchmarkingBot)
2. If you do not have Pip installed: `python -m src.get-pip`
3. Then install the required modules: `pip install -r requirements.txt`

Now you have the required modules installed to perform either mining or analysis:

To **mine**: `python -m src.miner`. Note that you will mine more recent data as well which is not included in the collected data that was used to perform the analysis. Furthermore, you need to create a file named "token.txt" to the root of this directory, i.e. (IEEE2021\\token.txt), that contains your GitHub API token.

To **analyse**: `python -m src.analyzer`


