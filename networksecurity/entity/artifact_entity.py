from dataclasses import dataclass

@dataclass
class DataIngestionConfigArtifact:
    training_file_path: str
    testing_file_path: str