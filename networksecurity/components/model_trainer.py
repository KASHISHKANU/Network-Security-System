import os
import sys

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import (
    DataTransformationConfigArtifact,
    ModelTrainerConfigArtifact
)
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utlis import (
    load_object,
    save_object,
    load_numpy_array_data,
    evaluate_models
)
from networksecurity.utils.ml_utils.metric.classification_metric import (
    get_classification_score
)

import mlflow


if os.getenv("ENV") != "production":
    try:
        import dagshub
        dagshub.init(
            repo_owner="KASHISHKANU",
            repo_name="Network-Security-System",
            mlflow=True
        )
        logging.info("DAGSHUB initialized (local environment)")
    except Exception as e:
        logging.warning(f"DAGSHUB init skipped: {e}")


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_config_artifact: DataTransformationConfigArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_config_artifact = (
                data_transformation_config_artifact
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def track_mlflow(self, model, classification_metric):
        """
        Track metrics and model in MLflow (local only)
        """
        if os.getenv("ENV") == "production":
            return  

        with mlflow.start_run():
            mlflow.log_metric("f1_score", classification_metric.f1_score)
            mlflow.log_metric("precision_score", classification_metric.precision_score)
            mlflow.log_metric("recall_score", classification_metric.recall_score)

            mlflow.sklearn.log_model(model, "model")


    def train_model(self, x_train, y_train, x_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
            "Logistic Regression": LogisticRegression(verbose=1),
            "Decision Tree": DecisionTreeClassifier()
        }

        params = {
            "Random Forest": {
                "criterion": ["gini", "entropy", "log_loss"],
                "max_features": ["sqrt", "log2", None],
                "n_estimators": [8, 16, 32, 64, 128]
            },

            "Decision Tree": {
                "criterion": ["gini", "entropy", "log_loss"],
                "splitter": ["best", "random"],
                "max_features": ["sqrt", "log2"]
            },

            "Gradient Boosting": {
                "learning_rate": [0.1, 0.01, 0.05],
                "subsample": [0.7, 0.8, 0.9],
                "loss": ["log_loss"],
                "max_features": ["sqrt", "log2"],
                "n_estimators": [50, 100]
            },

            "Logistic Regression": {
                "penalty": ["l2"],
                "C": [0.1, 1, 10],
                "solver": ["liblinear"]
            },

            "AdaBoost": {
                "n_estimators": [50, 100],
                "learning_rate": [0.01, 0.05, 0.1],
                "algorithm": ["SAMME", "SAMME.R"]
            }
        }

        model_report = evaluate_models(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            models=models,
            params=params
        )

        best_model_name = max(
            model_report,
            key=lambda name: model_report[name]["test_score"]
        )

        best_model = models[best_model_name]
        best_score = model_report[best_model_name]["test_score"]

        logging.info(
            f"Best model: {best_model_name} | Test Score: {best_score}"
        )

        y_train_pred = best_model.predict(x_train)
        train_metric = get_classification_score(
            y_true=y_train,
            y_pred=y_train_pred
        )
        self.track_mlflow(best_model, train_metric)

        y_test_pred = best_model.predict(x_test)
        test_metric = get_classification_score(
            y_true=y_test,
            y_pred=y_test_pred
        )
        self.track_mlflow(best_model, test_metric)

        logging.info(f"Train Metric: {train_metric}")
        logging.info(f"Test Metric: {test_metric}")

        preprocessor = load_object(
            self.data_transformation_config_artifact
            .transformed_object_file_path
        )

        os.makedirs(
            os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            ),
            exist_ok=True
        )

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model
        )

        save_object(
            self.model_trainer_config.trained_model_file_path,
            network_model
        )

        save_object("final_models/model.pkl", best_model)

        return ModelTrainerConfigArtifact(
            trained_model_file_path=(
                self.model_trainer_config.trained_model_file_path
            ),
            train_metric_artifact=train_metric,
            test_metric_artifact=test_metric
        )


    def initiate_model_trainer(self) -> ModelTrainerConfigArtifact:
        logging.info("Starting model training")

        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_config_artifact
                .transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                self.data_transformation_config_artifact
                .transformed_test_file_path
            )

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(
                x_train, y_train, x_test, y_test
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
