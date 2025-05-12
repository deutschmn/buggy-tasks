#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Priority Calculation Module

This module uses machine learning to predict the priority of tasks based on their tags.
It uses a Support Vector Classifier with TF-IDF feature extraction.
"""

# Standard library imports
import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Union

# Third-party imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline, make_pipeline
import joblib
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

# Constants and configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / "data"

# File paths
REFERENCE_DATA_PATH = DATA_DIR / "train-data.json"
MODEL_PATH = BASE_DIR / "priority_model.pkl"


def train_priority_model(train_data_path: str = REFERENCE_DATA_PATH) -> None:
    """
    Train and save a machine learning model to predict task priority.

    This function loads reference data containing tags and priorities,
    trains a machine learning model (TF-IDF + SVC), and saves it to disk.
    """
    logger.info("Starting model training process...")

    try:
        # Load the reference training data
        logger.info(f"Loading reference data from {train_data_path}")
        with open(train_data_path, 'r') as file_handle:
            training_data = json.load(file_handle)

        logger.info(f"Loaded {len(training_data)} training examples")

        # Prepare features (tags) and target (priority)
        feature_texts = [" ".join(item['tags']) for item in training_data]
        target_priorities = [item['priority'] for item in training_data]

        logger.debug(f"Feature sample: {feature_texts[:3]}")
        logger.debug(f"Target sample: {target_priorities[:3]}")

        # Create a machine learning pipeline
        # First, convert text to numerical features using TF-IDF
        # Then, use a Support Vector Classifier to predict priorities
        ml_pipeline = make_pipeline(
            TfidfVectorizer(min_df=2, max_df=0.95),
            SVC(kernel='linear', probability=True)
        )

        # Train the model on our data
        logger.info("Training model...")
        ml_pipeline.fit(feature_texts, target_priorities)

        # Save the trained model to disk for later use
        logger.info(f"Saving trained model to {MODEL_PATH}")
        joblib.dump(ml_pipeline, MODEL_PATH)
        logger.info("Model training completed successfully")

    except Exception as e:
        logger.error(f"Error training priority model: {e}")
        raise


def compute_priority(tags: List[str]) -> int:
    """
    Predict the priority of a task based on its tags.

    Args:
        tags: A list of tags associated with the task

    Returns:
        Integer priority score (higher means more important)

    Raises:
        FileNotFoundError: If the trained model file doesn't exist
    """
    # Verify the model file exists
    if not MODEL_PATH.exists():
        error_msg = f"Priority model not found at {MODEL_PATH}. Run train_priority_model() first."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        # Load the trained machine learning model
        logger.debug(f"Loading model from {MODEL_PATH}")
        priority_model = joblib.load(MODEL_PATH)

        # Convert tags list to the format expected by the model
        tags_feature = " ".join(tags)
        logger.debug(f"Computing priority for tags: {tags_feature}")

        # Make prediction using the model
        predicted_priority = priority_model.predict([tags_feature])[0]

        # Convert to Python int if needed (from numpy type)
        if isinstance(predicted_priority, np.integer):
            predicted_priority = int(predicted_priority)

        logger.info(f"Computed priority {predicted_priority} for tags: {tags}")
        return predicted_priority

    except Exception as e:
        logger.error(f"Error computing priority: {e}")
        # Return a default priority in case of error
        return 2
