from dataclasses import dataclass

@dataclass
class DataIngestionConfigArtifact:
    training_file_path: str
    testing_file_path: str

@dataclass
class DataValidationConfigArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationConfigArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str