import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split


DATASET_FILENAME = 'dataset.csv'
OUTPUT_XGBOOST_MODEL = 'model.xgb'
RANDOM_SEED = 42
TRAIN_SIZE = 0.75

NUM_OF_FEATURES = 42

def create_confusion_matrix(pred_labels, top_pred):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, classification_report

    labels = sorted(list(set(pred_labels)))
    cmx_data = confusion_matrix(pred_labels, top_pred, labels=labels)

    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(df_cmx, annot=True, fmt='g', square=False)
    ax.set_ylim(len(set(pred_labels)), 0)
    plt.show()


def run():
    data = np.loadtxt(DATASET_FILENAME, delimiter=',', dtype='float32', usecols=range(NUM_OF_FEATURES + 1))
    features = data[:, 1:]
    labels = data[:, 0].astype('int32')

    num_of_classes = len(set(labels))

    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, train_size=TRAIN_SIZE, random_state=RANDOM_SEED
    )

    # Convert labels to 0-based index for XGBoost compatibility
    labels_train -= labels_train.min()
    labels_test -= labels_test.min()

    # Define XGBoost DMatrix
    dtrain = xgb.DMatrix(features_train, label=labels_train)
    dtest = xgb.DMatrix(features_test, label=labels_test)

    # Model parameters
    params = {
        'objective': 'multi:softprob',
        'num_class': num_of_classes,
        'eval_metric': 'mlogloss',
        'seed': RANDOM_SEED,
        'max_depth': 6,
        'eta': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
    }

    # Train the model
    evals = [(dtrain, 'train'), (dtest, 'eval')]
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=500,
        evals=evals,
        early_stopping_rounds=20,
        verbose_eval=10
    )

    # Evaluate and display results
    predictions = model.predict(dtest)
    predicted_labels = np.argmax(predictions, axis=1)
    create_confusion_matrix(labels_test, predicted_labels)

    # Save the trained model
    model.save_model(OUTPUT_XGBOOST_MODEL)

run()
