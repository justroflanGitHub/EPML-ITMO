# Iris Dataset ML Experiments Summary Report

## Overview

- Total experiments: 18
- Successful experiments: 18
- Failed experiments: 0

## Model Performance Comparison

| Model | Accuracy | F1 Score | Precision | Recall |
|-------|----------|----------|-----------|--------|
| SVM_Linear | 1.0 | 1.0 | 1.0 | 1.0 |
| LogisticRegression_L2 | 1.0 | 1.0 | 1.0 | 1.0 |
| RandomForest_Minimal | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| SVM_RBF | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| DecisionTree_Tuned | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| GradientBoosting | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| NaiveBayes | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| MLPClassifier | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| GradientBoosting_Tuned | 0.9666666666666667 | 0.9665831244778613 | 0.9696969696969696 | 0.9666666666666667 |
| SVM_Poly | 0.9333333333333333 | 0.9326599326599326 | 0.9444444444444445 | 0.9333333333333333 |
| DecisionTree_Default | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 |
| LogisticRegression_Default | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 |
| LogisticRegression_L1 | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 |
| KNeighbors_Default | 0.9333333333333333 | 0.9326599326599326 | 0.9444444444444445 | 0.9333333333333333 |
| AdaBoost | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 | 0.9333333333333333 |
| RandomForest_Default | 0.9 | 0.8997493734335839 | 0.9023569023569024 | 0.9 |
| RandomForest_Tuned | 0.9 | 0.8997493734335839 | 0.9023569023569024 | 0.9 |
| RandomForest_ExtraTrees | 0.9 | 0.8997493734335839 | 0.9023569023569024 | 0.9 |

## Best Performing Model

**SVM_Linear** with accuracy: 1.0000


## MLflow Experiment Comparison

# MLflow Experiment Comparison Report

## Experiment: iris_ml_experiments

Total runs: 54

## Best Models by Type

| Model Type | Accuracy | F1 Score | Run ID |
|------------|----------|----------|--------|
| AdaBoostClassifier | 0.9333333333333333 | 0.9333333333333333 | e917daa2a8924737ab5b7ba9b04de706 |
| DecisionTreeClassifier | 0.9666666666666667 | 0.9665831244778613 | a09eb7c0c8fa4fdb9129f378cec0eb9c |
| GaussianNB | 0.9666666666666667 | 0.9665831244778613 | 1c8b7240a9fa4b339fab27dcdb135211 |
| GradientBoostingClassifier | 0.9666666666666667 | 0.9665831244778613 | 6123026e4582451f86f8a54f5cb85f66 |
| KNeighborsClassifier | 0.9333333333333333 | 0.9326599326599326 | 519f6b0e00644f69876eacb5fb54ba98 |
| LogisticRegression | 1.0 | 1.0 | 6f01a996d0554294b9aa15ddc30d73be |
| MLPClassifier | 0.9666666666666667 | 0.9665831244778613 | 987d25dbcea34c429c63df0e316e9265 |
| RandomForestClassifier | 0.9666666666666667 | 0.9665831244778613 | 8d3c1ea2aac04903a384462b782d9f9b |
| SVC | 1.0 | 1.0 | 3f1859c4eb604305a15cc74ed5787ccc |

## Detailed Run Information

### Run 6f01a996d0554294b9aa15ddc30d73be (LogisticRegression)
- Accuracy: 1.0
- Parameters: {}

### Run 3f1859c4eb604305a15cc74ed5787ccc (SVC)
- Accuracy: 1.0
- Parameters: {}

### Run 9b3092a5d9a847f18e3256387d6d724e (LogisticRegression)
- Accuracy: 1.0
- Parameters: {}

### Run 9f25374990a348378d7cadfc74724750 (SVC)
- Accuracy: 1.0
- Parameters: {}

### Run f0ad5b363c444332bc13e8515733030d (LogisticRegression)
- Accuracy: 1.0
- Parameters: {}

### Run d4bd3af6037448b591aa46d7fca0c85f (SVC)
- Accuracy: 1.0
- Parameters: {}

### Run 6123026e4582451f86f8a54f5cb85f66 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 987d25dbcea34c429c63df0e316e9265 (MLPClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 1c8b7240a9fa4b339fab27dcdb135211 (GaussianNB)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 3685b6f48b044911bdbd29e5b3f62f80 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run a09eb7c0c8fa4fdb9129f378cec0eb9c (DecisionTreeClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 5c916ee9b2b44aa381218171fe544131 (SVC)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 8d3c1ea2aac04903a384462b782d9f9b (RandomForestClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 29ff45db1031465a9e70ddd3f1d034f5 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run d24bff48eb244c27a7744a6ed3391c5b (MLPClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 7abfc756fecc41dcad82d8958d8cb78b (GaussianNB)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run e900f339a46d4efca60425cdce53f584 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 9532a3473e5547f5a73bbddcc3718cfe (DecisionTreeClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 9175c7412ac54748a10d06e04498cc34 (SVC)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run e0fcdccececf493fad456c81a0253c84 (RandomForestClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 7387939850fa4b728f06616937530e91 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 0fa56b8f444b4864953da81c2680e1bc (MLPClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run bcf67ef95ac443c0a63d9ba260a63ac8 (GaussianNB)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 0474dd37e49e4765a4482ecaf2a03321 (GradientBoostingClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 5a9881b00d744fd6a2393d2dd09af44d (DecisionTreeClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 6079bcc2b66e4b55af4ca1b6017f1fbc (SVC)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run 06b4032a8b3b4759bceb522333858c4c (RandomForestClassifier)
- Accuracy: 0.9666666666666667
- Parameters: {}

### Run e917daa2a8924737ab5b7ba9b04de706 (AdaBoostClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 519f6b0e00644f69876eacb5fb54ba98 (KNeighborsClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run f789e240dc424adf886066312483beb4 (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 905a4328883a460aa88d3815ade5776b (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run cc4ee8bb177b471d83f441a976bace6b (DecisionTreeClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 6da3ae40427a43f484133f3d001e50ba (SVC)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 20da18bd495a4c0dae5660f1f4631b81 (AdaBoostClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 992fd5a6daa44ec79bceea6c2983e37d (KNeighborsClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 141256d738bb4c708d3f125ceb6d52fc (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 157f1efe36e84f3da4a88f3d91d54824 (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 95977a63043043b8b36c9147d89abf8a (DecisionTreeClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run e011b9ed48924459ae7c333aee49e63b (SVC)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run cec6c6f900ef43c783c3a2da96512dc3 (AdaBoostClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 1cf6398586f1423a96d3813047f645bc (KNeighborsClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 83382525ca2541de813e6340731dfd69 (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 6c9f4fb363fd43c68ee9eafa36069261 (LogisticRegression)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run b609ebbf467e4291adf83d45f7653617 (DecisionTreeClassifier)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run dcfe41fe0cc2463f96fb197183e4da65 (SVC)
- Accuracy: 0.9333333333333333
- Parameters: {}

### Run 6491c608663a4936b67811ff29346150 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run c92684331034466982314ba312e214d4 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run 0eee23323077466bb9a775f73c350f53 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run ae79ad6aef8348bd8b020662c81220e3 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run 66ce9f055854454da4c0407a4b8377e2 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run e73cbfea178e42c6a5eabb9c23127d29 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run 5dc6864d8cf941a383e5a488672b5098 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run 4261f2635cd240bebf5356edff642d87 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}

### Run 6df664a577e64a66aa33ec7d3f9167f9 (RandomForestClassifier)
- Accuracy: 0.9
- Parameters: {}
