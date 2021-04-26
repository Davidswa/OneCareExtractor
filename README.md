# OneCareExtractor
Restores data from Microsoft OneCare Backup file

## Installation

Download and run locally... more instructions coming later

## Usage

Unzip all folders to a source folder. Then use CLI to set the source and destination folders.

`python File_Aggregator C:\User\[your name]\Source_Folder C:\User\[your name]\Destination_Folder`

Note the conda environment is saved in the `environment.yml` file. To create this environment on your system, run 
the following command:

`conda env create -f environment.yml`

## TODO
1) ~~Make command line interface~~
2) ~~Let user select destination folder for reconstructed dir~~
3) ~~Automatically unzip folders for user~~
4) Various path name checks to make sure only the zip files are handeled
5) Reconstruct split files and change their file names as needed

## Contributing
TBD... 

## License
TBD...