from tensorflow.keras.applications import ResNet50V2, DenseNet169
from tensorflow.keras.layers import Input, Concatenate, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from .layers import DeepSeekBlock

def build_model(input_shape=(224, 224, 3), num_classes=10, initial_lr=1e-4):
    inputs = Input(shape=input_shape, name="main_input")

    # Feature extractors
    resnet_base = ResNet50V2(weights='imagenet', include_top=False, pooling='avg', name='resnet_base')
    densenet_base = DenseNet169(weights='imagenet', include_top=False, pooling='avg', name='densenet_base')

    # Extract features and combine
    resnet_out = resnet_base(inputs)
    densenet_out = densenet_base(inputs)
    combined = Concatenate(name='concatenate')([resnet_out, densenet_out])

    # Pass through DeepSeekBlock
    deepseek = DeepSeekBlock(num_experts=4, top_k=2, expert_units=128, d_model=128, num_heads=4)
    deepseek_out = deepseek(combined)

    # Classification head
    x = Dense(256, activation='relu', kernel_regularizer=l2(0.01), name='fc1')(deepseek_out)
    x = Dropout(0.5, name='dropout1')(x)
    x = Dense(128, activation='relu', kernel_regularizer=l2(0.01), name='fc2')(x)
    x = Dropout(0.5, name='dropout2')(x)
    output = Dense(num_classes, activation='softmax', name='output')(x)

    model = Model(inputs=inputs, outputs=output, name="AlphaNetworks")
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=initial_lr),
                  loss="categorical_crossentropy", metrics=["accuracy"])
    return model
