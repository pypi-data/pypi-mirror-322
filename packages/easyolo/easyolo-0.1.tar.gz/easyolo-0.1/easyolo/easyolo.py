import os
import torch
import cv2
import random
import shutil
import yaml
from pathlib import Path
from ultralytics import YOLO
import matplotlib.pyplot as plt

class EasyOLO:
    def __init__(self):
        self.data_yaml = None
        self.model = None

    def load_data(self, image_dir, annotation_dir, validation=False, val_image_dir=None, val_annotation_dir=None,
                  split=0.2, class_names=None):
        """
        Load and prepare dataset for training.

        Args:
            image_dir (str): Path to images directory.
            annotation_dir (str): Path to annotations directory.
            validation (bool): If True, use provided validation dataset.
            val_image_dir (str): Path to validation images directory (required if validation=True).
            val_annotation_dir (str): Path to validation annotations directory (required if validation=True).
            split (float): Proportion of validation data if splitting automatically.
            class_names (list): List of class names for the dataset.
        """
        train_image_dir = Path(image_dir) / 'train'
        val_image_dir = Path(image_dir) / 'val'
        train_annotation_dir = Path(annotation_dir) / 'train'
        val_annotation_dir = Path(annotation_dir) / 'val'

        if validation:
            if not (val_image_dir and val_annotation_dir):
                raise ValueError("Validation directories must be provided when validation=True.")
        else:
            self._split_data(image_dir, annotation_dir, split, train_image_dir, val_image_dir, train_annotation_dir,
                             val_annotation_dir)

        data = {
            'train': str(train_image_dir),
            'val': str(val_image_dir),
            'test': str(val_image_dir),  # Assuming no separate test set; using val set as test for now.
            'nc': len(class_names) if class_names else self._count_classes(annotation_dir),
            'names': class_names if class_names else self._get_class_names(annotation_dir),
        }

        self.data_yaml = '/content/data.yaml'
        with open(self.data_yaml, 'w') as file:
            yaml.dump(data, file)
        print(f"Data loaded and data.yaml created at {self.data_yaml}")

    def _split_data(self, image_dir, annotation_dir, split, train_image_dir, val_image_dir, train_annotation_dir,
                    val_annotation_dir):
        """Split dataset into training and validation sets."""
        train_image_dir.mkdir(parents=True, exist_ok=True)
        val_image_dir.mkdir(parents=True, exist_ok=True)
        train_annotation_dir.mkdir(parents=True, exist_ok=True)
        val_annotation_dir.mkdir(parents=True, exist_ok=True)

        images = list(Path(image_dir).glob('*.jpg')) + list(Path(image_dir).glob('*.png'))
        random.shuffle(images)
        split_idx = int(len(images) * (1 - split))

        for img in images[:split_idx]:
            shutil.copy(img, train_image_dir / img.name)
            annotation = Path(annotation_dir) / img.with_suffix('.txt').name
            shutil.copy(annotation, train_annotation_dir / annotation.name)

        for img in images[split_idx:]:
            shutil.copy(img, val_image_dir / img.name)
            annotation = Path(annotation_dir) / img.with_suffix('.txt').name
            shutil.copy(annotation, val_annotation_dir / annotation.name)

    def _count_classes(self, annotation_dir):
        """Count number of unique classes in annotation files."""
        class_ids = set()
        for file in Path(annotation_dir).glob('*.txt'):
            with file.open() as f:
                for line in f:
                    class_ids.add(line.split()[0])
        return len(class_ids)

    def _get_class_names(self, annotation_dir):
        """Get sorted class names from annotation files."""
        class_ids = set()
        for file in Path(annotation_dir).glob('*.txt'):
            with file.open() as f:
                for line in f:
                    class_ids.add(line.split()[0])
        return sorted(class_ids)

    def train(self, data_file, epochs=100, batch=16, img_size=640, lr=0.01, save_dir='output/training', weights='/content/yolov5su.pt'):
        if not data_file:
            raise ValueError("Data file must be specified for training.")
    
        if not Path(data_file).exists():
            raise FileNotFoundError(f"Data file {data_file} does not exist.")
    
        # Ensure the weights path exists
        if not Path(weights).exists():
            raise FileNotFoundError(f"Weight file {weights} does not exist.")
    
        # Load YOLO model
        self.model = YOLO(weights)
    
        # Train the model
        self.model.train(
            data=data_file,
            epochs=epochs,
            batch=batch,
            imgsz=img_size,
            lr0=lr,
            project=save_dir,
            name='yolo_finetuned',
            exist_ok=True
        )
        print(f"Training completed. Model saved at {save_dir}/yolo_finetuned")

    def predict(self, model_path, image_path=None, image_dir=None, webcam_index=None):
        """
        Predict using the YOLO model.

        Args:
            model_path (str): Path to the trained model.
            image_path (str): Path to an image for prediction.
            image_dir (str): Path to a directory of images for prediction.
            webcam_index (int): Index of the webcam for live prediction.
        """
        if not self.model:
            self.load_model(model_path)

        if image_path:
            self._predict_single_image(image_path)
        elif image_dir:
            self._predict_multiple_images(image_dir)
        elif webcam_index is not None:
            self._predict_webcam(webcam_index)
        else:
            print("Provide an image path, directory, or webcam index for prediction.")

    def load_model(self, model_path):
        """Load a trained YOLO model."""
        if Path(model_path).exists():
            self.model = YOLO(model_path)
            print(f"Model loaded from {model_path}")
        else:
            raise FileNotFoundError(f"Model path {model_path} does not exist.")

    def _predict_single_image(self, image_path):
        """Predict on a single image."""
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image {image_path} does not exist.")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Error reading image {image_path}.")
        results = self.model(image)
        
        # Plot the result using matplotlib for environments like Google Colab
        plt.imshow(results[0].plot())
        plt.axis('off')  # Hide axes
        plt.show()

    def _predict_multiple_images(self, image_dir):
        """Predict on multiple images in a directory."""
        for image_path in Path(image_dir).glob('*.[jp][pn]g'):
            self._predict_single_image(str(image_path))

    def _predict_webcam(self, webcam_index):
        """Predict using a webcam feed."""
        cap = cv2.VideoCapture(webcam_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open webcam at index {webcam_index}.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model(frame)
            
            # Plot the result using matplotlib for webcam feed
            plt.imshow(results[0].plot())
            plt.axis('off')  # Hide axes
            plt.draw()
            plt.pause(0.001)  # Brief pause to update the plot

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def track_objects(self, source, conf=0.3, iou=0.5, show=True):
        """
        Track objects in a video or webcam feed using the YOLO model.

        Args:
            source (str): Path to the video file, YouTube URL, or 'webcam' for live tracking.
            conf (float): Confidence threshold for tracking.
            iou (float): Intersection over union threshold for tracking.
            show (bool): If True, display the tracking results in a window.
        """
        if not self.model:
            raise ValueError("Model is not loaded. Please load a model first.")

        # Perform object tracking
        results = self.model.track(source=source, conf=conf, iou=iou, show=show)
        
        if show:
            plt.imshow(results[0].plot())  # Display the tracked results using matplotlib for environments like Google Colab
            plt.axis('off')
            plt.show()
        else:
            print("Tracking completed.")
