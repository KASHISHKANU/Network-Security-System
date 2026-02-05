import os 
import sys

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationConfigArtifact, ModelTrainerConfigArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utlis import load_object, save_object
from networksecurity.utils.main_utils.utlis import load_numpy_array_data, evaluate_models 
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
import mlflow


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_config_artifact: DataTransformationConfigArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_config_artifact = data_transformation_config_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def track_mlflow(self, best_model, classificationmetric):
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model, "model")


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
                'criterion': ['gini', 'entropy', 'log_loss'],
                'max_features': ['sqrt', 'log2', None],
                'n_estimators': [8,16,32,64,128,256]
            },

            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'splitter': ['best', 'random'],
                'max_features': ['sqrt', 'log2']
            },

            "Gradient Boosting": {
                'learning_rate': [0.1,0.01,0.05],
                'subsample': [0.7,0.8,0.9],
                'loss': ['log_loss'],
                'max_features': ['sqrt','log2'],
                'n_estimators': [50,100,200]
            },

            "Logistic Regression": {
                'penalty': ['l2'],
                'C': [0.1,1,10],
                'solver': ['liblinear']
            },

            "AdaBoost": {
                'n_estimators': [50,100,200],
                'learning_rate': [0.01,0.05,0.1],
                'algorithm': ['SAMME','SAMME.R']
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
            key=lambda model_name: model_report[model_name]["test_score"]
        )

        best_model_score = model_report[best_model_name]["test_score"]

        best_model = models[best_model_name]

        logging.info(f"Best found model is {best_model_name} with score {best_model_score}")

        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        # TRACK EXPERIMENTS WITH THE MLFLOW
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)


        logging.info(f"Train Metric: {classification_train_metric}")
        logging.info(f"Test Metric: {classification_test_metric}")

        preprocessor = load_object(
            file_path=self.data_transformation_config_artifact.transformed_object_file_path
        )

        model_dir = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir, exist_ok=True)

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=best_model
        )

        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=network_model
        )

        model_trainer_artifact = ModelTrainerConfigArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )

        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerConfigArtifact:
        logging.info("Entered initiate_model_trainer")

        try:
            train_arr = load_numpy_array_data(
                file_path=self.data_transformation_config_artifact.transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                file_path=self.data_transformation_config_artifact.transformed_test_file_path
            )

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
