#!/usr/bin/env python3
"""
MLflow Integration Example with Open WebUI
This script demonstrates how to track AI experiments and model performance
"""
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import os
import json
from datetime import datetime
import openai
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenWebUIMLflowTracker:
    """MLflow integration for Open WebUI experiments"""
    
    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        """Initialize MLflow tracking"""
        mlflow.set_tracking_uri(tracking_uri)
        self.client = mlflow.tracking.MlflowClient()
        
    def start_experiment(self, experiment_name: str = "openwebui_chat"):
        """Start or get existing experiment"""
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = mlflow.create_experiment(experiment_name)
            else:
                experiment_id = experiment.experiment_id
            
            mlflow.set_experiment(experiment_name)
            return experiment_id
        except Exception as e:
            logger.error(f"Error setting up experiment: {e}")
            return None
    
    def track_chat_session(self, 
                          messages: List[Dict[str, str]], 
                          model: str,
                          response: str,
                          metrics: Dict[str, float],
                          tags: Dict[str, str] = None):
        """Track a chat session with MLflow"""
        
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("model", model)
            mlflow.log_param("num_messages", len(messages))
            mlflow.log_param("session_id", datetime.now().isoformat())
            
            # Log metrics
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
            
            # Log tags
            if tags:
                for key, value in tags.items():
                    mlflow.set_tag(key, value)
            
            # Log the conversation as artifact
            conversation_data = {
                "messages": messages,
                "response": response,
                "model": model,
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics
            }
            
            with open("conversation.json", "w") as f:
                json.dump(conversation_data, f, indent=2)
            
            mlflow.log_artifact("conversation.json")
            
            # Clean up
            os.remove("conversation.json")
            
            logger.info(f"Tracked chat session with run_id: {mlflow.active_run().info.run_id}")
    
    def track_model_performance(self, 
                               model_name: str,
                               performance_metrics: Dict[str, float],
                               hyperparameters: Dict[str, Any] = None):
        """Track model performance metrics"""
        
        with mlflow.start_run():
            # Log model name
            mlflow.log_param("model_name", model_name)
            
            # Log hyperparameters
            if hyperparameters:
                for key, value in hyperparameters.items():
                    mlflow.log_param(key, value)
            
            # Log performance metrics
            for key, value in performance_metrics.items():
                mlflow.log_metric(key, value)
            
            # Log model as artifact
            mlflow.log_artifact(f"models/{model_name}")
            
            logger.info(f"Tracked model performance with run_id: {mlflow.active_run().info.run_id}")
    
    def track_api_usage(self, 
                        api_calls: int,
                        total_tokens: int,
                        cost: float,
                        response_times: List[float]):
        """Track API usage and costs"""
        
        with mlflow.start_run():
            # Log API usage parameters
            mlflow.log_param("api_calls", api_calls)
            mlflow.log_param("total_tokens", total_tokens)
            
            # Log metrics
            mlflow.log_metric("total_cost", cost)
            mlflow.log_metric("avg_response_time", sum(response_times) / len(response_times))
            mlflow.log_metric("max_response_time", max(response_times))
            mlflow.log_metric("min_response_time", min(response_times))
            
            # Log cost per token
            if total_tokens > 0:
                mlflow.log_metric("cost_per_token", cost / total_tokens)
            
            logger.info(f"Tracked API usage with run_id: {mlflow.active_run().info.run_id}")
    
    def get_experiment_history(self, experiment_name: str = "openwebui_chat"):
        """Get experiment history"""
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment:
                runs = mlflow.search_runs(experiment.experiment_id)
                return runs
            return None
        except Exception as e:
            logger.error(f"Error getting experiment history: {e}")
            return None
    
    def compare_models(self, experiment_name: str = "openwebui_chat"):
        """Compare different models performance"""
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment:
                runs = mlflow.search_runs(
                    experiment.experiment_id,
                    filter_string="metrics.response_time < 5.0"  # Example filter
                )
                
                # Group by model and calculate averages
                model_performance = {}
                for _, run in runs.iterrows():
                    model = run.params.get("model", "unknown")
                    if model not in model_performance:
                        model_performance[model] = {
                            "response_times": [],
                            "costs": [],
                            "run_count": 0
                        }
                    
                    if "response_time" in run.metrics:
                        model_performance[model]["response_times"].append(run.metrics["response_time"])
                    if "cost" in run.metrics:
                        model_performance[model]["costs"].append(run.metrics["cost"])
                    
                    model_performance[model]["run_count"] += 1
                
                return model_performance
            return None
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return None

def example_usage():
    """Example of how to use the MLflow tracker"""
    
    # Initialize tracker
    tracker = OpenWebUIMLflowTracker()
    
    # Start experiment
    experiment_id = tracker.start_experiment("openwebui_demo")
    
    if experiment_id:
        # Example: Track a chat session
        messages = [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
        ]
        
        metrics = {
            "response_time": 1.2,
            "tokens_used": 15,
            "cost": 0.0003,
            "user_satisfaction": 0.9
        }
        
        tags = {
            "session_type": "greeting",
            "user_id": "user123",
            "platform": "openwebui"
        }
        
        tracker.track_chat_session(
            messages=messages,
            model="gpt-4o-mini",
            response="I'm doing well, thank you for asking!",
            metrics=metrics,
            tags=tags
        )
        
        # Example: Track API usage
        tracker.track_api_usage(
            api_calls=1,
            total_tokens=15,
            cost=0.0003,
            response_times=[1.2]
        )
        
        # Get experiment history
        history = tracker.get_experiment_history()
        print(f"Experiment history: {len(history)} runs")
        
        # Compare models
        comparison = tracker.compare_models()
        print(f"Model comparison: {comparison}")

if __name__ == "__main__":
    example_usage()
