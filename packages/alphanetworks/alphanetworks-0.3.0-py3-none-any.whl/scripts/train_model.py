import os
import argparse
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from alphanetworks.models import build_model

def train_model(train_dir, val_dir, output_dir, input_shape=(224, 224, 3),
                num_classes=10, batch_size=8, epochs=50, initial_lr=1e-4):
    os.makedirs(output_dir, exist_ok=True)

    # Data generators
    datagen_train = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )
    datagen_val = ImageDataGenerator(rescale=1./255)

    train_gen = datagen_train.flow_from_directory(train_dir, target_size=input_shape[:2],
                                                  batch_size=batch_size, class_mode="categorical")
    val_gen = datagen_val.flow_from_directory(val_dir, target_size=input_shape[:2],
                                              batch_size=batch_size, class_mode="categorical")

    # Build and compile model
    model = build_model(input_shape=input_shape, num_classes=num_classes, initial_lr=initial_lr)
    model.summary()

    # Callbacks
    early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    lr_reduction = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, min_lr=1e-6)

    # Train
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs,
                        callbacks=[early_stopping, lr_reduction])

    # Save final model
    model.save(os.path.join(output_dir, "final_model.keras"))
    return history

if __name__ == "__main__":
    # Define CLI arguments
    parser = argparse.ArgumentParser(description="Train a hybrid deep learning model with AlphaNetworks. Proposed by ihtesham jahangir and Alpha team.")
    parser.add_argument("--train_dir", "-t", required=True, type=str,
                        help="Path to the training dataset directory.")
    parser.add_argument("--val_dir", "-v", required=True, type=str,
                        help="Path to the validation dataset directory.")
    parser.add_argument("--output_dir", "-o", default="./output", type=str,
                        help="Directory to save the trained model and logs (default: './output').")
    parser.add_argument("--num_classes", "-nc", default=10, type=int,
                        help="Number of classes in the dataset (default: 10).")
    parser.add_argument("--input_shape", "-is", default=(224, 224, 3), type=tuple,
                        help="Input shape of the images (default: (224, 224, 3)).")
    parser.add_argument("--batch_size", "-b", default=8, type=int,
                        help="Batch size for training and validation (default: 8).")
    parser.add_argument("--epochs", "-e", default=50, type=int,
                        help="Number of epochs for training (default: 50).")
    parser.add_argument("--learning_rate", "-lr", default=1e-4, type=float,
                        help="Initial learning rate for the optimizer (default: 0.0001).")

    # Parse arguments
    args = parser.parse_args()

    # Call the training function with parsed arguments
    train_model(train_dir=args.train_dir, val_dir=args.val_dir, output_dir=args.output_dir,
                input_shape=args.input_shape, num_classes=args.num_classes,
                batch_size=args.batch_size, epochs=args.epochs, initial_lr=args.learning_rate)
