# SpectrogramDataset

- Converts audio folder to torch dataset (returns dict, requires further preprocessing) 
- Generates spectrograms for audio files, supports preloading them into memory for fast access. 
- Generates enumerated labels (classes) based on additional data provided in metadata.json file
- Generates masks (speech, gender, different noises etc), if intervals provided in metadata.json
- Supports multiple datasets via SpectrogramDatasetRouter class

## Usage:
```python
from spgdataset import SpectrogramDataset
```
```python
dst = SpectrogramDataset(
        audio_root: str,         
           # path to root audio folder
        spectrograms_root: str,  
           # path to folder to store generated spectrograms
        index_root: str,         
           # path to folder to store indexes
        metadata_json_path: str | None = None, 
           # path to metadata.json (see below for structure)
        sample_rate: int = 16000, 
           # sample rate (currently only 16kHz)
        window_size_sec: float = 1.92,  
           # sliding window size, in seconds
        window_offset_sec: float = 0.1, 
           # sliding window offset, in seconds
        window_content_ratio: float = 0.5, 
           # content to slice ratio, if intervals provided
        hop_length: int = 160,  
           # hop length to generate spectrograms
        n_mels: int = 80,       
           # number of mel filters (64 or 80)
        n_fft: int = 400,       
           # N_FFT
        normalize: bool = True, 
           # normalize spectrograms
        dtype: torch.dtype = torch.float32, 
           # torch.dtype to use for spectrograms
        split: tuple = (1,), 
           # divide samples into train, validate, test, etc sets via tuple
        output_configuration: dict | None =  
           # expected output configuration:
            {
                "audio": False,      
                    # bool, return audio
                "spectrogram": True, 
                    # bool, return spectrogram
                "masks": ["speech"], 
                    # list, names of masks to generate 
                    # based on provided intervals 
                    # in metadata.json
                "meta": [],          
                    # list, names of optional values 
                    # to return, based on provided
                    # values in 'metadata' dict
                    # in metadata.json
                "label": None,
                    # enumerate and return class labels
                    # based on metadata 
            },
        max_memory_cache: int = 0,  
           # max memory space to retain spectrograms
        num_workers: int = 0, 
           # number of dataset workers
        )
```
### metadata.json expected structure:
```
[
    path (str): {
            'length': int,
            'intervals': {
                    name (str): [[],...]
                },
            'metadata': {
                    key (str): value
                } 
        },
]


path:        file path (relative to audio root)
length:      audio file length in samples
intervals:   dict of various intervals {name: [[start,stop],...]}
metadata:    dict, optional data per file, like speaker name or gender, age etc, can be used as class labels
```

## SpectrogramDatasetRouter
Additional class to route multiple SpectrogramDatasets as a single dataset
```python
dstrt = SpectrogramDatasetRouter(
    datasets: list = []
        # list of datasets to route to
)
```