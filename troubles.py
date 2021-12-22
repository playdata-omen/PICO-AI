#usr/bin/env python
import os
import tensorflow as tf

tensorflow_version = float(tf.__version__[0:3])

print(f"Your tensorflow version is : {tensorflow_version}\n")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# for 1.* versions
if (tensorflow_version < 2.0):
    tf_config=tf.compat.v1.ConfigProto()
    tf_config.gpu_options.allow_growth=True
    sess = tf.compat.v1.Session(config=tf_config)
# for 2.0 et 2.1 versions
elif (2.0 <= tensorflow_version <= 2.1):
    tf.config.gpu.set_per_process_memory_growth(True)
# for 2.2+ versions
else:
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(e)
