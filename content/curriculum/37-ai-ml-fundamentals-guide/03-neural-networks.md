# Neural Networks

## Overview

Neural networks are computing systems inspired by biological neural networks in animal brains. They consist of interconnected nodes (neurons) organized in layers that process information through weighted connections. By adjusting these weights during training, neural networks learn to recognize patterns, classify data, and make predictions. From simple perceptrons to complex deep architectures, neural networks form the foundation of modern AI breakthroughs in vision, language, and decision-making.

## The Biological Inspiration

### Biological Neurons

**Components**:
- **Dendrites**: Receive signals from other neurons
- **Cell Body**: Processes incoming signals
- **Axon**: Transmits output signal
- **Synapses**: Connections between neurons

**Process**: Neurons fire when combined input signals exceed a threshold, sending electrical impulses to connected neurons.

### Artificial Neurons

**Components**:
- **Inputs (x₁, x₂, ..., xₙ)**: Numeric values
- **Weights (w₁, w₂, ..., wₙ)**: Connection strengths
- **Bias (b)**: Threshold adjustment
- **Activation Function (f)**: Introduces non-linearity

**Mathematical Formula**:
```
output = f(w₁x₁ + w₂x₂ + ... + wₙxₙ + b)
output = f(Σ(wᵢxᵢ) + b)
```

| Biological | Artificial | Purpose |
|------------|------------|---------|
| Dendrites | Inputs | Receive signals |
| Synaptic strength | Weights | Signal importance |
| Cell body | Summation + activation | Process inputs |
| Firing threshold | Bias | Adjust sensitivity |
| Axon | Output | Send signal forward |

## Perceptrons: The Foundation

### Single-Layer Perceptron

The simplest neural network, invented by Frank Rosenblatt in 1958.

**Architecture**:
- Input layer: Raw features
- Single output neuron: Binary decision
- Step activation function

**Capability**:
- Can learn linearly separable patterns
- Example: AND, OR gates

**Limitation**:
- Cannot solve XOR problem (not linearly separable)
- Led to first AI winter in 1970s

### Multi-Layer Perceptron (MLP)

Adding hidden layers between input and output solved the XOR problem and enabled learning complex patterns.

**Architecture**:
```
Input Layer → Hidden Layer(s) → Output Layer
```

**Components**:
- **Input Layer**: Receives raw data
- **Hidden Layers**: Extract features, transform data
- **Output Layer**: Produces final prediction

**Advancement**: With non-linear activation functions and backpropagation, MLPs can approximate any continuous function (universal approximation theorem).

## Activation Functions

Activation functions introduce non-linearity, allowing networks to learn complex patterns. Without them, multiple layers would collapse to equivalent single-layer model.

### Common Activation Functions

| Function | Formula | Range | Use Case | Pros | Cons |
|----------|---------|-------|----------|------|------|
| **Sigmoid** | σ(x) = 1/(1+e⁻ˣ) | (0, 1) | Binary classification output | Smooth, probabilistic | Vanishing gradients |
| **Tanh** | tanh(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | (-1, 1) | Hidden layers | Zero-centered | Vanishing gradients |
| **ReLU** | f(x) = max(0, x) | [0, ∞) | Hidden layers (most common) | Fast, no vanishing gradient | Dying ReLU problem |
| **Leaky ReLU** | f(x) = max(0.01x, x) | (-∞, ∞) | Hidden layers | Fixes dying ReLU | Small negative slope |
| **ELU** | f(x) = x if x>0 else α(eˣ-1) | (-α, ∞) | Hidden layers | Smooth, self-normalizing | Slower than ReLU |
| **Softmax** | exp(xᵢ)/Σexp(xⱼ) | (0, 1), sum=1 | Multi-class output | Probability distribution | Only for output layer |

### Activation Function Selection Guide

**Hidden Layers**: Start with ReLU (default choice for most architectures)
- ReLU for fast training
- Leaky ReLU if experiencing dying neurons
- ELU for self-normalizing properties

**Output Layer**:
- **Binary classification**: Sigmoid
- **Multi-class classification**: Softmax
- **Regression**: Linear (no activation)
- **Multi-label classification**: Sigmoid per label

### The Vanishing Gradient Problem

**Issue**: In deep networks, gradients become exponentially small in early layers during backpropagation, preventing learning.

**Cause**: Sigmoid/tanh derivatives are small (max 0.25), multiplied across layers.

**Solution**:
- Use ReLU family (derivative is 0 or 1)
- Batch normalization
- Residual connections (ResNet)
- Better weight initialization (Xavier, He)

## Neural Network Architectures

### Feedforward Neural Networks (FNN)

**Structure**: Information flows in one direction: input → hidden → output

**Characteristics**:
- No cycles or loops
- Each layer fully connected to next
- Most basic architecture

**Use Cases**:
- Tabular data classification
- Simple regression tasks
- Pattern recognition

**Example**: Credit scoring, iris classification

### Fully Connected (Dense) Layers

Every neuron in layer L connects to every neuron in layer L+1.

**Parameters**: If layer L has m neurons and layer L+1 has n neurons:
- Weights: m × n
- Biases: n
- Total: m×n + n

**Pros**: Maximum representational power
**Cons**: Many parameters, prone to overfitting, slow

### Convolutional Neural Networks (CNNs)

**Structure**: Specialized for grid-like data (images, time series)

**Key Layers**:
- **Convolutional**: Apply filters to detect local patterns
- **Pooling**: Reduce spatial dimensions
- **Fully Connected**: Final classification

**Advantages**:
- Parameter sharing (same filter across image)
- Translation invariance
- Hierarchical feature learning

**Use Cases**: Image classification, object detection, segmentation

### Recurrent Neural Networks (RNNs)

**Structure**: Connections form cycles, creating memory of previous inputs

**Variants**:
- **Vanilla RNN**: Simple feedback loop (vanishing gradient issues)
- **LSTM** (Long Short-Term Memory): Gating mechanisms for long-term memory
- **GRU** (Gated Recurrent Unit): Simplified LSTM

**Use Cases**:
- Time series forecasting
- Natural language processing
- Speech recognition
- Video analysis

**Limitation**: Sequential processing (slow), largely replaced by transformers

### Modern Architectures

| Architecture | Innovation | Primary Use | Notable Example |
|--------------|-----------|-------------|-----------------|
| **ResNet** | Skip connections | Very deep networks | Image classification |
| **Inception** | Multi-scale filters | Efficient feature extraction | GoogLeNet |
| **Transformer** | Self-attention mechanism | Sequence modeling | GPT, BERT, Claude |
| **U-Net** | Encoder-decoder with skip connections | Image segmentation | Medical imaging |
| **GAN** | Generator vs discriminator | Generative modeling | Image synthesis |
| **Autoencoder** | Compression + reconstruction | Dimensionality reduction | Anomaly detection |

## Backpropagation: How Networks Learn

### The Learning Process

**Goal**: Adjust weights to minimize difference between predictions and actual outputs

**Steps**:

1. **Forward Pass**
   - Input data flows through network
   - Each layer computes outputs
   - Final layer produces prediction

2. **Loss Calculation**
   - Compare prediction to actual label
   - Compute error using loss function

3. **Backward Pass (Backpropagation)**
   - Calculate gradient of loss with respect to each weight
   - Use chain rule to propagate gradients backward
   - Determine how much each weight contributed to error

4. **Weight Update**
   - Adjust weights in direction that reduces error
   - Update rule: w_new = w_old - learning_rate × gradient

5. **Iteration**
   - Repeat for many examples (epochs)
   - Network gradually improves

### Mathematical Foundation: Chain Rule

Backpropagation applies the calculus chain rule to compute gradients efficiently.

**Chain Rule**: If y = f(u) and u = g(x), then:
```
dy/dx = (dy/du) × (du/dx)
```

**In Neural Networks**:
For loss L, output y, and weight w in earlier layer:
```
dL/dw = (dL/dy) × (dy/dw)
```

This propagates backward through all layers.

### Gradient Descent Variants

| Method | Update Rule | Pros | Cons |
|--------|-------------|------|------|
| **Batch GD** | Use all data | Stable, convergent | Slow, memory intensive |
| **Stochastic GD** | Use one example | Fast updates | Noisy, unstable |
| **Mini-batch GD** | Use small batches | Balance speed/stability | Most common choice |
| **Momentum** | Accumulate gradient direction | Faster convergence | Extra hyperparameter |
| **Adam** | Adaptive learning rates | Fast, effective | Default choice for most |
| **RMSprop** | Adaptive per-parameter | Good for RNNs | Less common than Adam |

## Network Depth and Width

### Depth (Number of Layers)

**Shallow Networks (2-3 layers)**:
- Learn simple patterns
- Fast training
- Limited expressiveness

**Deep Networks (10+ layers)**:
- Learn hierarchical features
- More representational power
- Require more data and compute
- Risk of vanishing gradients

**Very Deep Networks (50-1000+ layers)**:
- State-of-art performance
- Need architectural innovations (ResNet skip connections)
- Example: ResNet-152, GPT-3 (96 layers)

### Width (Neurons per Layer)

**Narrow Layers**:
- Fewer parameters
- Faster training
- May underfit

**Wide Layers**:
- More capacity
- Can overfit without regularization
- Slower training

### Depth vs Width Trade-off

**General Principle**: Depth is more important than width for learning complex hierarchical patterns.

**Example**: 5 layers of 100 neurons often outperforms 2 layers of 500 neurons with same parameter count.

**Modern Trend**: Both deeper AND wider (GPT-3: 96 layers, 12,288-dimensional)

## Real-World Examples

### Image Classification (CNN)

**Task**: Identify object in photo
**Architecture**: ResNet-50
**Process**:
1. Early layers detect edges, textures
2. Middle layers detect parts (wheels, eyes)
3. Late layers detect full objects (cars, faces)
4. Output layer predicts class

### Language Modeling (Transformer)

**Task**: Predict next word
**Architecture**: GPT-style decoder
**Process**:
1. Token embeddings
2. Positional encoding
3. Self-attention across sequence
4. Feedforward transformation
5. Output probability distribution over vocabulary

### Time Series Forecasting (LSTM)

**Task**: Predict stock prices
**Architecture**: Stacked LSTM
**Process**:
1. Process historical prices sequentially
2. LSTM cells maintain long-term patterns
3. Output layer predicts future values

### Recommendation System (Autoencoder)

**Task**: Collaborative filtering
**Architecture**: Deep autoencoder
**Process**:
1. Encode user-item interactions
2. Compressed representation learns latent factors
3. Decode to predict missing ratings

**Key Terms**
- **Perceptron**: Simplest neural network with single layer
- **Activation Function**: Non-linear transformation enabling complex learning
- **Backpropagation**: Algorithm for computing gradients via chain rule
- **Gradient Descent**: Optimization algorithm adjusting weights to minimize loss
- **Epoch**: One complete pass through training dataset
- **Hidden Layer**: Intermediate layers between input and output
- **Vanishing Gradient**: Problem where gradients become too small in early layers
- **Universal Approximation Theorem**: Neural networks can approximate any function

## Summary

Neural networks revolutionized machine learning by mimicking brain-inspired computation through interconnected layers of artificial neurons. From the simple perceptron to modern deep architectures, the key breakthrough was combining multiple layers with non-linear activation functions and the backpropagation algorithm. Activation functions like ReLU introduce non-linearity while avoiding vanishing gradients that plagued earlier sigmoid-based networks. Architecture choices matter: depth enables hierarchical feature learning while width provides capacity. Different architectures suit different data types—CNNs for images, RNNs/LSTMs for sequences, transformers for language. Backpropagation efficiently computes gradients using the chain rule, enabling gradient descent to optimize millions or billions of parameters. Modern networks are both deeper and wider than ever, with innovations like skip connections, attention mechanisms, and normalization techniques enabling training. Understanding these fundamentals is essential for both using pre-trained models and designing custom architectures for specific problems.
