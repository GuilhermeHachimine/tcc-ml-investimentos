from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.utils.config import CONFIG


class ModelFactory:
    """
    Create supervised regression models used in the study.
    """

    @staticmethod
    def create_decision_tree() -> DecisionTreeRegressor:
        return DecisionTreeRegressor(
            max_depth=5,
            min_samples_leaf=20,
            random_state=CONFIG.random_state,
        )

    @staticmethod
    def create_random_forest() -> RandomForestRegressor:
        return RandomForestRegressor(
            n_estimators=200,
            max_depth=8,
            min_samples_leaf=20,
            random_state=CONFIG.random_state,
            n_jobs=-1,
        )

    @staticmethod
    def create_xgboost() -> XGBRegressor:
        return XGBRegressor(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            random_state=CONFIG.random_state,
            n_jobs=-1,
        )

    @classmethod
    def create_all_models(cls) -> dict[str, object]:
        return {
            "decision_tree": cls.create_decision_tree(),
            "random_forest": cls.create_random_forest(),
            "xgboost": cls.create_xgboost(),
        }
