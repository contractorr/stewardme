# AI/ML Glossary: Key Terms Quick Reference

## Overview

This glossary provides concise definitions of essential AI and machine learning terms. Terms are organized alphabetically within thematic categories for easy reference while studying or working with AI systems.

---

## Core AI Concepts

**Artificial Intelligence (AI)**
Machines exhibiting intelligent behavior such as learning, reasoning, problem-solving, perception, and language understanding.

**Artificial General Intelligence (AGI)**
Hypothetical AI with human-level intelligence across all cognitive domains, capable of learning any intellectual task a human can.

**Artificial Superintelligence (ASI)**
Theoretical AI surpassing human intelligence in all domains—scientific creativity, general wisdom, and social skills.

**Narrow AI**
AI specialized for specific tasks (current state of technology). Examples: chess engines, image classifiers, voice assistants.

**Machine Learning (ML)**
Subset of AI where systems learn from data without explicit programming, improving performance through experience.

**Deep Learning**
Machine learning using neural networks with multiple layers (typically 10+) to learn hierarchical representations.

**Turing Test**
Test of machine intelligence: if a human evaluator cannot distinguish machine from human in conversation, the machine passes.

---

## Machine Learning Paradigms

**Supervised Learning**
Learning from labeled data where each input has corresponding correct output. Used for classification and regression.

**Unsupervised Learning**
Learning patterns from unlabeled data. Includes clustering, dimensionality reduction, and anomaly detection.

**Reinforcement Learning (RL)**
Learning through trial-and-error interaction with environment, receiving rewards or penalties for actions.

**Semi-Supervised Learning**
Combining small labeled dataset with large unlabeled dataset to improve learning.

**Self-Supervised Learning**
Creating training signals from data structure itself (e.g., predicting masked words, image rotations).

**Transfer Learning**
Using knowledge learned on one task to improve performance on related task.

**Few-Shot Learning**
Learning from very few examples (1-10) per class.

**Zero-Shot Learning**
Performing task without any training examples, using only task description.

---

## Neural Networks

**Neural Network**
Computing system inspired by biological neural networks, consisting of interconnected artificial neurons organized in layers.

**Perceptron**
Simplest neural network with single layer, capable of learning linearly separable patterns.

**Multi-Layer Perceptron (MLP)**
Neural network with multiple layers enabling learning of non-linear patterns.

**Neuron (Node/Unit)**
Basic computational unit that receives inputs, applies weights and bias, and outputs result through activation function.

**Weight**
Parameter representing connection strength between neurons, adjusted during training.

**Bias**
Parameter added to weighted sum, allowing shifting of activation function.

**Activation Function**
Non-linear function applied to neuron output, enabling networks to learn complex patterns.

**Feedforward Network**
Neural network where information flows in one direction: input → hidden layers → output.

**Hidden Layer**
Intermediate layer between input and output, extracting features and transforming data.

**Backpropagation**
Algorithm for training neural networks by computing gradients using chain rule, propagating error backward through layers.

**Epoch**
One complete pass through entire training dataset.

**Batch**
Subset of training data processed together before updating weights.

---

## Activation Functions

**ReLU (Rectified Linear Unit)**
Activation function: f(x) = max(0, x). Most common choice for hidden layers.

**Sigmoid**
Activation function: σ(x) = 1/(1+e⁻ˣ), outputs values between 0 and 1. Used for binary classification output.

**Tanh (Hyperbolic Tangent)**
Activation function outputting values between -1 and 1. Zero-centered alternative to sigmoid.

**Softmax**
Activation function converting logits to probability distribution summing to 1. Used for multi-class classification output.

**Leaky ReLU**
ReLU variant allowing small negative values: f(x) = max(0.01x, x). Addresses dying ReLU problem.

---

## Deep Learning Architectures

**Convolutional Neural Network (CNN)**
Neural network specialized for grid-structured data (images), using convolutional and pooling layers.

**Convolutional Layer**
Layer applying filters to input, detecting local patterns through sliding window operation.

**Pooling Layer**
Downsampling layer reducing spatial dimensions, creating translation invariance. Common types: max pooling, average pooling.

**Recurrent Neural Network (RNN)**
Neural network with feedback connections for processing sequential data, maintaining hidden state as memory.

**Long Short-Term Memory (LSTM)**
RNN variant with gating mechanisms enabling learning of long-term dependencies.

**Gated Recurrent Unit (GRU)**
Simplified LSTM variant with fewer parameters, similar performance.

**Transformer**
Architecture based on attention mechanisms without recurrence, enabling parallel processing of sequences.

**Attention Mechanism**
Method for dynamically focusing on relevant parts of input by computing weighted combinations.

**Self-Attention**
Attention where each element in sequence attends to all elements in same sequence.

**Multi-Head Attention**
Running multiple attention mechanisms in parallel, each learning different relationships.

**Encoder**
Component that processes input into intermediate representation. In transformers, uses bidirectional attention.

**Decoder**
Component that generates output from intermediate representation. In transformers, uses causal (left-to-right) attention.

**ResNet (Residual Network)**
CNN architecture using skip connections to enable training of very deep networks (50-152+ layers).

**U-Net**
Encoder-decoder architecture with skip connections for image segmentation tasks.

**Autoencoder**
Neural network learning compressed representation (encoding) and reconstruction (decoding) of input.

**Variational Autoencoder (VAE)**
Autoencoder learning probabilistic latent space for generative modeling.

**Generative Adversarial Network (GAN)**
Two networks (generator and discriminator) competing: generator creates fake data, discriminator distinguishes real from fake.

---

## Training and Optimization

**Loss Function (Cost Function, Objective Function)**
Measures difference between predictions and actual targets, guiding optimization.

**Cross-Entropy Loss**
Loss function for classification tasks measuring difference between predicted and true probability distributions.

**Mean Squared Error (MSE)**
Loss function for regression: average of squared differences between predictions and targets.

**Mean Absolute Error (MAE)**
Loss function for regression: average of absolute differences. Less sensitive to outliers than MSE.

**Gradient Descent**
Optimization algorithm iteratively adjusting parameters in direction that reduces loss.

**Stochastic Gradient Descent (SGD)**
Gradient descent variant updating weights after each training example or mini-batch.

**Learning Rate**
Hyperparameter controlling step size for parameter updates. Critical for convergence.

**Momentum**
Technique accumulating gradient direction over time for faster convergence and reduced oscillation.

**Adam (Adaptive Moment Estimation)**
Optimization algorithm combining momentum and adaptive per-parameter learning rates. Common default choice.

**Optimizer**
Algorithm for updating model parameters to minimize loss function.

**Hyperparameter**
Configuration choice not learned during training (learning rate, batch size, architecture choices).

**Overfitting**
When model memorizes training data, performing well on training set but poorly on new data.

**Underfitting**
When model is too simple to capture data patterns, performing poorly on both training and test sets.

**Generalization**
Model's ability to perform well on new, unseen data.

**Validation Set**
Dataset used to tune hyperparameters and monitor training, separate from training and test sets.

**Test Set**
Dataset used for final evaluation of model performance, held out during training.

**Early Stopping**
Regularization technique halting training when validation performance stops improving.

---

## Regularization

**Regularization**
Techniques preventing overfitting by constraining model complexity or introducing noise.

**L1 Regularization (Lasso)**
Adding penalty proportional to absolute value of weights, encouraging sparsity.

**L2 Regularization (Ridge/Weight Decay)**
Adding penalty proportional to squared weights, encouraging smaller weights.

**Dropout**
Randomly setting neurons to zero during training with probability p, preventing co-adaptation.

**Batch Normalization**
Normalizing layer inputs to have zero mean and unit variance per mini-batch, stabilizing and accelerating training.

**Layer Normalization**
Normalizing across features instead of batch dimension. Better for RNNs and small batches.

**Data Augmentation**
Artificially expanding training set through transformations (rotation, cropping, color jittering).

**Label Smoothing**
Using soft targets instead of hard 0/1 labels to prevent overconfidence.

---

## Natural Language Processing (NLP)

**Tokenization**
Splitting text into smaller units (tokens) such as words, subwords, or characters.

**Token**
Basic unit of text after tokenization (word, subword, or character).

**Vocabulary**
Set of all unique tokens known to model.

**Embedding**
Dense vector representation of discrete tokens in continuous space.

**Word2Vec**
Algorithm learning word embeddings by predicting context words or target word from context.

**Contextual Embedding**
Word representation that varies based on surrounding context, unlike fixed embeddings.

**Language Model**
Model predicting probability distribution over sequences of tokens.

**Masked Language Model**
Training approach predicting masked tokens from bidirectional context (used in BERT).

**Autoregressive Model**
Model generating sequences one token at a time, conditioning on previous tokens (used in GPT).

**Fine-tuning**
Adapting pre-trained model to specific task by continuing training on task-specific data.

**Prompt**
Input text designed to elicit desired output from language model.

**Prompt Engineering**
Crafting effective prompts to guide model behavior.

**In-Context Learning**
Model learning from examples provided within prompt without parameter updates.

**Chain-of-Thought**
Prompting technique encouraging step-by-step reasoning for complex problems.

**Hallucination**
When model generates false information confidently, not grounded in training data or input.

**BERT (Bidirectional Encoder Representations from Transformers)**
Encoder-only transformer trained via masked language modeling for understanding tasks.

**GPT (Generative Pre-trained Transformer)**
Decoder-only transformer trained via next token prediction for generation tasks.

**Named Entity Recognition (NER)**
Task of identifying and classifying entities in text (people, organizations, locations).

**Sentiment Analysis**
Determining emotional tone of text (positive, negative, neutral).

---

## Computer Vision

**Image Classification**
Assigning single label to entire image.

**Object Detection**
Locating and classifying multiple objects in image with bounding boxes.

**Semantic Segmentation**
Classifying every pixel in image by category.

**Instance Segmentation**
Identifying and delineating each object instance in image.

**Bounding Box**
Rectangle defined by coordinates enclosing detected object.

**Feature Map**
Output of convolutional layer representing detected patterns.

**Receptive Field**
Region of input image that influences particular neuron's activation.

**Stride**
Step size when sliding filter across input in convolution or pooling.

**Padding**
Adding border pixels to input to control output dimensions.

**Max Pooling**
Pooling operation taking maximum value in each region.

**Global Average Pooling**
Pooling operation averaging entire feature map to single value.

**Transfer Learning (Vision)**
Using CNN pre-trained on ImageNet for other vision tasks.

**Data Augmentation (Vision)**
Applying transformations like rotation, flipping, cropping to training images.

**ImageNet**
Large image dataset (1.2M images, 1000 classes) used for pre-training vision models.

---

## Multimodal AI

**Multimodal Model**
Model processing multiple modalities (text, images, audio, video).

**CLIP (Contrastive Language-Image Pre-training)**
Model learning aligned representations of images and text for zero-shot classification.

**Vision Transformer (ViT)**
Applying transformer architecture to image patches for classification.

**Text-to-Image Generation**
Creating images from text descriptions using models like DALL-E, Stable Diffusion.

**Diffusion Model**
Generative model learning to reverse gradual noise-adding process.

**Zero-Shot Classification**
Classifying images into categories not seen during training using text descriptions.

---

## Evaluation Metrics

**Accuracy**
Proportion of correct predictions among all predictions.

**Precision**
Proportion of true positives among predicted positives: TP/(TP+FP).

**Recall (Sensitivity, True Positive Rate)**
Proportion of actual positives correctly identified: TP/(TP+FN).

**F1 Score**
Harmonic mean of precision and recall: 2×(Precision×Recall)/(Precision+Recall).

**Confusion Matrix**
Table showing true positives, false positives, true negatives, false negatives.

**ROC Curve (Receiver Operating Characteristic)**
Plot of true positive rate vs false positive rate at various thresholds.

**AUC (Area Under Curve)**
Area under ROC curve, measuring classification performance across thresholds.

**Mean Average Precision (mAP)**
Evaluation metric for object detection averaging precision across classes and IoU thresholds.

**IoU (Intersection over Union)**
Overlap between predicted and ground truth bounding boxes or segmentation masks.

**Perplexity**
Language model evaluation metric: exponential of average negative log-likelihood. Lower is better.

**BLEU (Bilingual Evaluation Understudy)**
Metric for machine translation quality based on n-gram overlap with references.

---

## AI Ethics and Safety

**Bias**
Systematic unfairness in model predictions across different groups.

**Fairness**
Equitable treatment of individuals and groups. Multiple competing definitions exist.

**Demographic Parity**
Fairness criterion requiring equal outcome rates across groups.

**Equal Opportunity**
Fairness criterion requiring equal true positive rates across groups.

**Interpretability**
Ability to understand how model makes decisions.

**Explainability**
Providing human-understandable explanations for model predictions.

**Black Box**
Model whose internal workings are opaque and difficult to interpret.

**Adversarial Example**
Input with small perturbation causing misclassification, often imperceptible to humans.

**Adversarial Training**
Training with adversarial examples to improve robustness.

**Out-of-Distribution (OOD)**
Data significantly different from training distribution.

**Distribution Shift**
When test data distribution differs from training data.

**Alignment**
Ensuring AI objectives match human values and intentions.

**Reward Hacking**
AI exploiting loopholes in reward function rather than achieving intended goal.

**Constitutional AI**
Training approach using explicit principles and self-critique for value alignment.

**RLHF (Reinforcement Learning from Human Feedback)**
Training method using human preferences to align model behavior.

**Red Teaming**
Adversarial testing to discover vulnerabilities and failure modes.

**Differential Privacy**
Mathematical guarantee that individual data points don't significantly influence model outputs.

**Deepfake**
Synthetic media (video, audio, images) created by AI, often depicting fake events.

**Hallucination (AI Safety)**
Model confidently generating false information not grounded in reality.

---

## Technical Concepts

**Parameter**
Learnable variable in model (weights and biases) adjusted during training.

**Hyperparameter**
Configuration choice set before training (learning rate, architecture, regularization strength).

**Feature**
Individual measurable property or characteristic used as input to model.

**Feature Engineering**
Manual process of creating useful features from raw data.

**Feature Extraction**
Automatic learning of useful representations from data (especially in deep learning).

**Dimensionality Reduction**
Reducing number of input features while preserving important information.

**Principal Component Analysis (PCA)**
Linear dimensionality reduction finding orthogonal axes of maximum variance.

**t-SNE (t-Distributed Stochastic Neighbor Embedding)**
Non-linear dimensionality reduction for visualization, preserving local structure.

**Clustering**
Grouping similar data points without predefined labels.

**K-Means**
Clustering algorithm partitioning data into K clusters based on centroids.

**Anomaly Detection**
Identifying unusual patterns that don't conform to expected behavior.

**Ensemble**
Combining multiple models to improve predictions (bagging, boosting, stacking).

**Random Forest**
Ensemble of decision trees trained on random subsets of features and data.

**Gradient Boosting**
Ensemble method sequentially training models to correct previous models' errors.

**Cross-Validation**
Technique for assessing model performance by training/testing on different data subsets.

**K-Fold Cross-Validation**
Dividing data into K folds, training on K-1 folds and testing on remaining fold, repeating K times.

---

## Specialized Terms

**Vanishing Gradient**
Problem where gradients become too small in early layers during backpropagation, preventing learning.

**Exploding Gradient**
Problem where gradients become too large during backpropagation, causing instability.

**Gradient Clipping**
Limiting gradient magnitude to prevent exploding gradients.

**Catastrophic Forgetting**
Neural networks forgetting previously learned tasks when learning new ones.

**Mode Collapse**
GAN failure where generator produces limited variety of outputs.

**Latent Space**
Compressed representation learned by autoencoder or other generative model.

**Attention Weight**
Scalar indicating how much to focus on particular input element in attention mechanism.

**Positional Encoding**
Adding position information to embeddings in transformers (which lack inherent position awareness).

**Skip Connection (Residual Connection)**
Direct pathway allowing gradients to flow through network, enabling very deep architectures.

**Batch Size**
Number of training examples processed before updating model weights.

**Mini-Batch**
Small subset of training data (typically 32-256 examples) used for single gradient update.

**Inference**
Using trained model to make predictions on new data.

**Pre-training**
Initial training phase on large general dataset before task-specific fine-tuning.

**Foundation Model**
Large model trained on broad data, adaptable to many downstream tasks.

**Scaling Laws**
Empirical relationships showing how model performance improves with scale (parameters, data, compute).

**Compute**
Processing resources (GPU/TPU time) required for training or inference.

**GPU (Graphics Processing Unit)**
Specialized hardware for parallel computation, essential for training deep learning models.

**TPU (Tensor Processing Unit)**
Google's custom hardware optimized for tensor operations in neural networks.

---

## Data and Datasets

**Training Data**
Dataset used to train model by adjusting parameters.

**Validation Data**
Dataset used to tune hyperparameters and monitor training progress.

**Test Data**
Dataset used for final evaluation, never seen during training or hyperparameter tuning.

**Labeled Data**
Data with corresponding correct outputs or annotations.

**Unlabeled Data**
Data without annotations, used in unsupervised or self-supervised learning.

**Data Leakage**
When test set information inappropriately influences training, leading to overly optimistic performance estimates.

**Class Imbalance**
When some classes have many more examples than others in dataset.

**Synthetic Data**
Artificially generated data used to augment training sets.

**Benchmark**
Standard dataset and evaluation protocol for comparing model performance.

**ImageNet**
Large-scale image classification dataset (1.2M images, 1000 classes).

**MNIST**
Dataset of handwritten digits (60K training, 10K test), common benchmark for beginners.

**COCO (Common Objects in Context)**
Dataset for object detection, segmentation, and captioning.

---

## Model Deployment

**Model Serving**
Making trained model available for inference in production environment.

**Latency**
Time required to process single inference request.

**Throughput**
Number of inference requests processed per unit time.

**Model Compression**
Reducing model size and computational requirements while maintaining performance.

**Quantization**
Reducing numerical precision of weights and activations (e.g., 32-bit to 8-bit).

**Pruning**
Removing unnecessary weights or neurons from trained model.

**Knowledge Distillation**
Training small model to mimic larger model's behavior.

**Edge Deployment**
Running models on local devices (phones, IoT) rather than cloud servers.

**A/B Testing**
Comparing two model versions by routing fraction of traffic to each.

**Model Monitoring**
Tracking model performance and behavior in production.

**Model Drift**
Degradation of model performance over time as data distribution changes.

---

## Research and Development

**Ablation Study**
Systematically removing model components to understand their contribution.

**Baseline**
Simple model or approach for comparison to measure improvement.

**State-of-the-Art (SOTA)**
Best-performing approach on particular task or benchmark at given time.

**Benchmark**
Standardized task and dataset for comparing model performance.

**Paper with Code**
Website tracking machine learning papers and their implementations.

**ArXiv**
Preprint server where most AI research papers are first published.

**NeurIPS, ICML, ICLR**
Major machine learning research conferences.

**CVPR**
Major computer vision research conference.

**ACL, EMNLP**
Major natural language processing research conferences.

---

## Summary

This glossary covers essential AI and machine learning terminology organized by category. Understanding these terms is fundamental for reading research papers, implementing models, and discussing AI concepts. As the field evolves rapidly, new terms emerge while some become obsolete. Core concepts around neural networks, training, and evaluation remain foundational. Ethical considerations including bias, fairness, and alignment have become increasingly central to AI discourse. Practical deployment concerns around efficiency, monitoring, and serving complete the AI lifecycle. This reference serves as starting point for deeper exploration of each concept—many terms merit entire courses or books. Regular engagement with AI literature and hands-on practice solidifies understanding of these interconnected ideas forming modern artificial intelligence.
