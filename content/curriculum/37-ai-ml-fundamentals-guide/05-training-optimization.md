# Training and Optimization

## Overview

Training neural networks involves finding optimal parameters (weights and biases) that minimize prediction errors. This optimization process requires careful selection of loss functions to measure error, gradient descent algorithms to update parameters, regularization techniques to prevent overfitting, and hyperparameter tuning to balance competing objectives. Modern deep learning success stems not just from architecture design but from sophisticated training techniques enabling convergence of models with millions to billions of parameters on massive datasets.

## Loss Functions

Loss functions quantify the difference between model predictions and actual targets, providing the optimization objective for training.

### Classification Loss Functions

#### Binary Cross-Entropy (Log Loss)

**Use Case**: Binary classification (two classes)

**Formula**:
```
L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]

Where:
y = actual label (0 or 1)
ŷ = predicted probability
```

**Intuition**: Heavily penalizes confident wrong predictions

**Example**:
- Actual: 1, Predicted: 0.9 → Loss: 0.105 (good)
- Actual: 1, Predicted: 0.1 → Loss: 2.303 (bad)

**Applications**: Spam detection, medical diagnosis (yes/no), sentiment (positive/negative)

#### Categorical Cross-Entropy

**Use Case**: Multi-class classification (mutually exclusive classes)

**Formula**:
```
L = -Σ yᵢ·log(ŷᵢ)

Where:
yᵢ = one-hot encoded true class
ŷᵢ = predicted probabilities (from softmax)
```

**Example**: Image classification (cat vs dog vs bird)

**Requirements**: Output layer with softmax activation

#### Sparse Categorical Cross-Entropy

**Variant**: Same as categorical but accepts integer labels instead of one-hot encoding

**Advantage**: Memory efficient for large number of classes

**Example**: Language modeling (vocabulary of 50,000 words)

### Regression Loss Functions

#### Mean Squared Error (MSE)

**Use Case**: Regression tasks, penalizes large errors heavily

**Formula**:
```
L = (1/n)·Σ(yᵢ - ŷᵢ)²
```

**Properties**:
- Differentiable everywhere
- Sensitive to outliers (squared term)
- Measures average squared deviation

**Applications**: House price prediction, temperature forecasting

#### Mean Absolute Error (MAE)

**Use Case**: Regression when outliers present

**Formula**:
```
L = (1/n)·Σ|yᵢ - ŷᵢ|
```

**Properties**:
- Less sensitive to outliers than MSE
- All errors weighted equally
- Not differentiable at zero

**Applications**: Robust regression, financial forecasting

#### Huber Loss

**Use Case**: Combines MSE and MAE benefits

**Formula**:
```
L = {
  0.5·(y-ŷ)²           if |y-ŷ| ≤ δ
  δ·(|y-ŷ| - 0.5·δ)    otherwise
}
```

**Properties**:
- Quadratic for small errors (smooth gradients)
- Linear for large errors (robust to outliers)

**Applications**: Robust regression with smooth optimization

### Comparison of Loss Functions

| Loss Function | Task Type | Sensitivity to Outliers | Differentiability | Typical Range |
|---------------|-----------|------------------------|-------------------|---------------|
| **MSE** | Regression | High | Smooth | [0, ∞) |
| **MAE** | Regression | Low | Not at 0 | [0, ∞) |
| **Huber** | Regression | Medium | Smooth | [0, ∞) |
| **Binary Cross-Entropy** | Binary classification | Medium | Smooth | [0, ∞) |
| **Categorical Cross-Entropy** | Multi-class | Medium | Smooth | [0, ∞) |

### Specialized Loss Functions

**Hinge Loss** (SVM-style):
- Use case: Binary classification with margin
- Formula: `L = max(0, 1 - y·ŷ)`

**KL Divergence** (Kullback-Leibler):
- Use case: Comparing probability distributions
- Formula: `KL(P||Q) = Σ P(x)·log(P(x)/Q(x))`
- Application: Variational autoencoders, knowledge distillation

**Contrastive Loss**:
- Use case: Learning embeddings (similarity learning)
- Application: Face verification, metric learning

**Triplet Loss**:
- Use case: Embedding learning (anchor, positive, negative)
- Application: Face recognition, recommendation systems

## Gradient Descent and Optimization Algorithms

Gradient descent iteratively updates parameters in the direction that reduces loss.

### Basic Gradient Descent

**Update Rule**:
```
θₜ₊₁ = θₜ - η·∇L(θₜ)

Where:
θ = parameters (weights)
η = learning rate
∇L = gradient of loss
```

**Intuition**: Move downhill on loss landscape

### Gradient Descent Variants

| Variant | Batch Size | Pros | Cons |
|---------|------------|------|------|
| **Batch GD** | All data | Stable convergence | Slow, memory intensive |
| **Stochastic GD (SGD)** | 1 example | Fast, can escape local minima | Noisy, unstable |
| **Mini-batch GD** | Small batch (32-256) | Balance speed/stability | Most common choice |

**Mini-batch GD** is the standard in practice:
- Batch size 32-256 typical
- Provides stable estimates with efficient computation
- Leverages GPU parallelism

### Momentum-Based Methods

#### SGD with Momentum

**Concept**: Accumulate gradient direction over time

**Update Rule**:
```
vₜ = β·vₜ₋₁ + ∇L(θₜ)
θₜ₊₁ = θₜ - η·vₜ

Where:
v = velocity (accumulated gradient)
β = momentum coefficient (typically 0.9)
```

**Advantages**:
- Faster convergence
- Dampens oscillations
- Helps escape shallow local minima

#### Nesterov Accelerated Gradient (NAG)

**Concept**: Look ahead before computing gradient

**Advantage**: More responsive to changes, often faster than standard momentum

### Adaptive Learning Rate Methods

#### AdaGrad

**Concept**: Adapt learning rate per parameter based on historical gradients

**Problem**: Learning rate can decay too aggressively

#### RMSprop

**Concept**: Use exponentially decaying average of squared gradients

**Update Rule**:
```
sₜ = β·sₜ₋₁ + (1-β)·(∇L)²
θₜ₊₁ = θₜ - η·∇L/√(sₜ + ε)
```

**Advantage**: Prevents learning rate from decaying too fast

#### Adam (Adaptive Moment Estimation)

**Concept**: Combines momentum and adaptive learning rates

**Update Rules**:
```
mₜ = β₁·mₜ₋₁ + (1-β₁)·∇L     # First moment (mean)
vₜ = β₂·vₜ₋₁ + (1-β₂)·(∇L)²  # Second moment (variance)
m̂ₜ = mₜ/(1-β₁ᵗ)              # Bias correction
v̂ₜ = vₜ/(1-β₂ᵗ)              # Bias correction
θₜ₊₁ = θₜ - η·m̂ₜ/√(v̂ₜ + ε)
```

**Default Hyperparameters**:
- β₁ = 0.9 (momentum)
- β₂ = 0.999 (RMSprop)
- η = 0.001 (learning rate)
- ε = 10⁻⁸ (numerical stability)

**Why Popular**: Works well across wide range of problems with minimal tuning

#### AdamW

**Improvement**: Decoupled weight decay (better regularization)

**Current Status**: Often preferred over Adam for deep learning

### Optimizer Comparison

| Optimizer | Learning Rate | Memory | Convergence Speed | Typical Use |
|-----------|---------------|--------|-------------------|-------------|
| **SGD** | Manual tuning required | Low | Slow but can find better minima | Fine-tuning, when time permits |
| **SGD+Momentum** | Manual tuning | Low | Medium | Computer vision |
| **RMSprop** | Adaptive | Medium | Medium | RNNs (historically) |
| **Adam** | Adaptive | Medium | Fast | Default choice, NLP |
| **AdamW** | Adaptive | Medium | Fast | Modern default |

### Learning Rate Schedules

Rather than fixed learning rate, adapt during training:

**Step Decay**:
```
Reduce learning rate by factor every N epochs
Example: η = η₀ × 0.1 every 30 epochs
```

**Exponential Decay**:
```
η = η₀ × e^(-kt)
Smooth continuous decay
```

**Cosine Annealing**:
```
η = η_min + 0.5(η_max - η_min)(1 + cos(πt/T))
Smooth reduction with potential restarts
```

**Warm-up then Decay**:
```
Gradually increase learning rate initially (warm-up)
Then apply decay schedule
Common in transformer training
```

**One Cycle Policy**:
```
Increase learning rate to maximum
Then decrease to minimum
Often achieves faster convergence
```

## Regularization Techniques

Regularization prevents overfitting by constraining model complexity or introducing noise during training.

### L1 and L2 Regularization

#### L2 Regularization (Weight Decay)

**Concept**: Penalize large weights

**Modified Loss**:
```
L_total = L_data + λ·Σwᵢ²

Where:
λ = regularization strength
```

**Effect**:
- Weights prefer smaller values
- Smoother decision boundaries
- Most common form

**Implementation**: Add weight decay parameter to optimizer

#### L1 Regularization (Lasso)

**Modified Loss**:
```
L_total = L_data + λ·Σ|wᵢ|
```

**Effect**:
- Encourages sparse weights (many exactly zero)
- Automatic feature selection
- Less common in deep learning

### Dropout

**Concept**: Randomly set neurons to zero during training with probability p

**Mechanism**:
```
Training: Randomly drop units with probability p
Testing: Use all units, scale outputs by (1-p)
```

**Typical Values**: p = 0.2 to 0.5

**Advantages**:
- Prevents co-adaptation of neurons
- Ensemble effect (training many sub-networks)
- Widely used in fully-connected layers

**Variants**:
- **Spatial Dropout**: Drop entire feature maps in CNNs
- **DropConnect**: Drop connections instead of neurons

### Batch Normalization

**Concept**: Normalize layer inputs to have zero mean and unit variance per mini-batch

**Formula**:
```
x̂ = (x - μ_batch) / √(σ²_batch + ε)
y = γ·x̂ + β

Where:
γ, β = learnable parameters
```

**Benefits**:
- Accelerates training (allows higher learning rates)
- Reduces sensitivity to initialization
- Acts as regularizer (slight)
- Stabilizes deep networks

**Placement**: Typically after linear/conv layer, before activation

**Variants**:
- **Layer Normalization**: Normalize across features (better for RNNs)
- **Group Normalization**: Hybrid approach
- **Instance Normalization**: Normalize each sample separately (style transfer)

### Early Stopping

**Concept**: Monitor validation loss, stop when it stops improving

**Implementation**:
1. Track validation loss each epoch
2. If no improvement for N epochs (patience)
3. Stop training
4. Restore weights from best validation epoch

**Advantages**:
- Simple, effective
- Prevents overfitting without modifying model

**Typical Patience**: 5-20 epochs depending on task

### Data Augmentation

**Concept**: Artificially expand training set with transformations

**Image Augmentation**:
- Rotation, flipping, cropping
- Color jittering
- Random erasing
- Mixup (blend two images)
- CutMix (paste image patches)

**Text Augmentation**:
- Synonym replacement
- Back-translation
- Random insertion/deletion
- Paraphrasing

**Benefit**: Model learns invariances, reduces overfitting

### Other Regularization Techniques

**Gradient Clipping**:
- Limit gradient magnitude to prevent exploding gradients
- Common in RNNs, transformers

**Label Smoothing**:
- Use soft targets instead of hard 0/1 labels
- Example: [0, 1, 0] → [0.05, 0.9, 0.05]
- Prevents overconfidence

**Weight Constraints**:
- Limit weight magnitude directly
- Example: Max-norm constraint

## Hyperparameter Tuning

Hyperparameters are configuration choices not learned during training (learning rate, architecture size, regularization strength).

### Key Hyperparameters

| Category | Hyperparameters | Typical Range |
|----------|----------------|---------------|
| **Optimization** | Learning rate | 1e-5 to 1e-1 |
|  | Batch size | 16 to 512 |
|  | Optimizer choice | Adam, AdamW, SGD+momentum |
| **Regularization** | Dropout rate | 0.1 to 0.5 |
|  | L2 penalty | 1e-6 to 1e-3 |
|  | Early stopping patience | 5 to 20 epochs |
| **Architecture** | Number of layers | 2 to 100+ |
|  | Layer width | 64 to 4096 |
|  | Activation functions | ReLU, LeakyReLU, ELU |
| **Training** | Number of epochs | 10 to 1000+ |
|  | Learning rate schedule | Constant, decay, cosine |

### Hyperparameter Search Strategies

#### Grid Search

**Concept**: Try all combinations of predefined values

**Example**:
```
learning_rate: [0.001, 0.01, 0.1]
dropout: [0.2, 0.5]
Total: 3 × 2 = 6 experiments
```

**Pros**: Thorough, reproducible
**Cons**: Exponentially expensive, wastes computation

#### Random Search

**Concept**: Sample hyperparameters randomly from distributions

**Advantage**: Often finds good solutions faster than grid search

**Why It Works**: Important hyperparameters explored more thoroughly

#### Bayesian Optimization

**Concept**: Build probabilistic model of hyperparameter-performance relationship

**Process**:
1. Try initial random points
2. Fit surrogate model (Gaussian process)
3. Select next point to maximize expected improvement
4. Repeat

**Tools**: Optuna, Hyperopt, Ray Tune

**Advantage**: Efficient, requires fewer trials

#### Learning Rate Finder

**Concept**: Gradually increase learning rate, plot loss

**Process**:
1. Start with very small learning rate
2. Train for few iterations, exponentially increase learning rate
3. Plot loss vs learning rate
4. Choose learning rate where loss decreases fastest

**Popular**: Fast.ai library implements this

### Practical Tuning Strategy

**Phase 1: Architecture Selection**
- Choose baseline architecture (ResNet, Transformer, etc.)
- Determine model size based on data/compute budget

**Phase 2: Coarse Search**
- Use random or Bayesian search
- Broad ranges for learning rate, regularization
- Quick evaluation (few epochs)

**Phase 3: Fine-tuning**
- Narrow ranges around promising values
- Longer training
- Multiple seeds for robustness

**Phase 4: Final Training**
- Best hyperparameters
- Full training schedule
- Ensemble multiple runs if budget allows

### Practical Hyperparameter Guidelines

**Learning Rate**:
- Start with default (Adam: 0.001)
- Too high: Loss explodes or oscillates
- Too low: Slow convergence
- Use learning rate finder or start high and decay

**Batch Size**:
- Larger: Faster training, more stable, may hurt generalization
- Smaller: More regularization, less memory
- Sweet spot often 32-128

**Regularization**:
- Start without, add if overfitting observed
- Dropout 0.2-0.5 for fully-connected layers
- Weight decay 1e-4 to 1e-5

**Epochs**:
- Train until validation loss plateaus
- Use early stopping
- Undertrain rather than overtrain initially

## Training Best Practices

### Data Splitting

**Standard Split**:
- Training: 70-80%
- Validation: 10-15%
- Test: 10-15%

**Cross-Validation**: When data is limited, use K-fold CV

**Stratification**: Maintain class distribution across splits

### Weight Initialization

**Why It Matters**: Poor initialization causes vanishing/exploding gradients

**Methods**:
- **Xavier/Glorot**: For sigmoid/tanh activations
- **He Initialization**: For ReLU (default choice)
- **Pre-trained Weights**: Transfer learning (best when available)

### Monitoring Training

**Metrics to Track**:
- Training loss: Should decrease
- Validation loss: Should decrease then plateau
- Training vs validation gap: Indicates overfitting
- Learning rate: Monitor schedule
- Gradient norms: Check for vanishing/exploding

**Signs of Problems**:
- **Overfitting**: Training loss << validation loss
- **Underfitting**: Both losses high
- **Exploding Gradients**: Loss becomes NaN
- **Vanishing Gradients**: No learning (flat loss)

### Debugging Strategies

1. **Overfit Single Batch**: Ensure model can learn at all
2. **Check Data Pipeline**: Visualize inputs, verify labels
3. **Start Simple**: Small model, minimal regularization
4. **Compare Baselines**: Random guessing, simple models
5. **Gradual Complexity**: Add components incrementally

**Key Terms**
- **Loss Function**: Measures prediction error, optimization objective
- **Gradient Descent**: Iterative optimization following loss gradient
- **Learning Rate**: Step size for parameter updates
- **Momentum**: Accumulating gradient direction for faster convergence
- **Adam**: Adaptive optimizer combining momentum and per-parameter learning rates
- **Regularization**: Techniques preventing overfitting
- **Dropout**: Randomly zeroing neurons during training
- **Batch Normalization**: Normalizing layer inputs per mini-batch
- **Hyperparameters**: Configuration choices not learned during training
- **Early Stopping**: Halting training when validation performance degrades

## Summary

Successfully training neural networks requires careful attention to loss functions, optimization algorithms, regularization, and hyperparameter tuning. Loss functions translate problem objectives into differentiable targets—cross-entropy for classification, MSE for regression, with specialized variants for particular needs. Gradient descent and its variants power the optimization, with Adam/AdamW serving as robust defaults and SGD with momentum preferred when training time permits. Learning rate schedules like cosine annealing and warm-up improve convergence. Regularization techniques including L2 penalty, dropout, and batch normalization prevent overfitting while stabilizing training. Data augmentation expands effective dataset size. Hyperparameter tuning dramatically impacts performance, with Bayesian optimization offering efficient search. Best practices include proper data splitting, appropriate weight initialization, continuous monitoring for overfitting/underfitting, and systematic debugging when issues arise. Modern deep learning success stems from the interplay of these techniques rather than any single component. Practitioners must balance competing objectives—convergence speed, generalization, computational efficiency—through iterative experimentation guided by validation performance.
