# Deep Learning

## Overview

Deep learning refers to neural networks with multiple layers (typically 10+) that learn hierarchical representations of data. The "deep" aspect enables learning increasingly abstract features at each layer—from edges in early layers to complete objects in later layers. Recent breakthroughs in computer vision, natural language processing, and generative AI stem from deep learning architectures like CNNs, RNNs, and transformers. Enabled by massive datasets, GPU acceleration, and architectural innovations, deep learning has achieved superhuman performance on many tasks previously considered impossible for machines.

## Convolutional Neural Networks (CNNs)

### Architecture and Purpose

CNNs are specialized for processing grid-structured data like images, leveraging spatial relationships through localized connectivity and parameter sharing.

**Core Principle**: Instead of connecting every pixel to every neuron, use small filters that scan across the image, detecting local patterns.

### Key Components

#### 1. Convolutional Layers

**Operation**: Slide filter (kernel) across input, computing dot product at each position

**Parameters**:
- **Filter size**: Typically 3×3, 5×5, or 7×7
- **Number of filters**: Creates multiple feature maps
- **Stride**: Step size when sliding filter
- **Padding**: Border handling (valid, same)

**Example**:
```
3×3 filter on 28×28 image with stride 1
Output size: 26×26 per filter
With 32 filters: 26×26×32 output
```

**Purpose**: Detect patterns like edges, textures, shapes

#### 2. Activation Functions

Apply non-linearity after convolution (typically ReLU)

#### 3. Pooling Layers

**Purpose**: Reduce spatial dimensions, create translation invariance

**Types**:
- **Max pooling**: Take maximum value in region (most common)
- **Average pooling**: Take average value
- **Global pooling**: Reduce entire feature map to single value

**Example**: 2×2 max pooling reduces 26×26 to 13×13

#### 4. Fully Connected Layers

Flatten spatial dimensions and perform final classification

### CNN Architecture Patterns

| Architecture | Year | Key Innovation | Use Case |
|--------------|------|----------------|----------|
| **LeNet-5** | 1998 | First successful CNN | Digit recognition (MNIST) |
| **AlexNet** | 2012 | Deep CNN + GPU + ReLU | ImageNet breakthrough |
| **VGG** | 2014 | Deep with small 3×3 filters | Image classification |
| **GoogLeNet/Inception** | 2014 | Multi-scale filters in parallel | Efficient feature extraction |
| **ResNet** | 2015 | Skip connections | Very deep networks (152+ layers) |
| **EfficientNet** | 2019 | Compound scaling | Efficiency + accuracy |

### How CNNs Learn Hierarchically

**Layer 1 (Early)**: Edges, colors, simple textures
- Horizontal, vertical, diagonal edges
- Color gradients

**Layer 2-3 (Middle)**: Parts and textures
- Corners, circles
- Complex textures (fur, wood grain)
- Simple shapes

**Layer 4-5 (Late)**: Object parts
- Eyes, wheels, windows
- Faces, car parts

**Output Layer**: Complete objects
- Cat, dog, car, airplane
- Full scene understanding

### Real-World CNN Applications

**Computer Vision**:
- Image classification (ImageNet, medical imaging)
- Object detection (YOLO, Faster R-CNN)
- Semantic segmentation (U-Net, Mask R-CNN)
- Face recognition
- Autonomous vehicles

**Beyond Images**:
- Audio classification (spectrograms)
- Time series analysis (1D convolutions)
- Natural language processing (text as 1D sequences)

### Example: Object Detection Pipeline

1. **Input**: Raw image
2. **Backbone CNN**: Extract feature maps (ResNet, VGG)
3. **Region Proposal**: Identify candidate object locations
4. **Classification**: Classify objects in each region
5. **Bounding Box Regression**: Refine object locations
6. **Output**: Objects with locations and confidence scores

## Recurrent Neural Networks (RNNs)

### Architecture and Purpose

RNNs process sequential data by maintaining hidden state that acts as memory across time steps. Unlike feedforward networks, RNNs have feedback connections enabling them to use previous inputs to influence current predictions.

### Vanilla RNN Structure

**Components**:
- **Input sequence**: x₁, x₂, ..., xₜ
- **Hidden state**: h₁, h₂, ..., hₜ (memory)
- **Output sequence**: y₁, y₂, ..., yₜ

**Update Equations**:
```
hₜ = tanh(Wₓₕ·xₜ + Wₕₕ·hₜ₋₁ + bₕ)
yₜ = Wₕᵧ·hₜ + bᵧ
```

**Problem**: Vanishing gradient—difficult to learn long-term dependencies

### Long Short-Term Memory (LSTM)

**Innovation**: Gating mechanisms control information flow

**Gates**:
1. **Forget Gate**: What to remove from cell state
2. **Input Gate**: What new information to store
3. **Output Gate**: What to output from cell state

**Cell State**: Separate memory channel preserving long-term information

**Equations**:
```
fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)  # Forget gate
iₜ = σ(Wi·[hₜ₋₁, xₜ] + bi)  # Input gate
C̃ₜ = tanh(WC·[hₜ₋₁, xₜ] + bC)  # Candidate values
Cₜ = fₜ * Cₜ₋₁ + iₜ * C̃ₜ  # Update cell state
oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)  # Output gate
hₜ = oₜ * tanh(Cₜ)  # Hidden state
```

**Advantage**: Can learn dependencies across hundreds of time steps

### Gated Recurrent Unit (GRU)

**Simplification**: Fewer gates than LSTM, faster training

**Gates**:
1. **Update Gate**: How much past information to keep
2. **Reset Gate**: How much past information to forget

**No separate cell state**—simpler than LSTM

**Performance**: Similar to LSTM, often faster to train

### RNN Variants and Patterns

| Type | Structure | Use Case |
|------|-----------|----------|
| **Many-to-Many** | Sequence input → Sequence output | Machine translation, video captioning |
| **Many-to-One** | Sequence input → Single output | Sentiment analysis, video classification |
| **One-to-Many** | Single input → Sequence output | Image captioning, music generation |
| **Bidirectional** | Process sequence forward and backward | Text understanding (BERT-style) |
| **Stacked** | Multiple RNN layers | Deeper representation learning |

### Real-World RNN Applications

**Natural Language Processing**:
- Machine translation
- Text generation
- Speech recognition
- Sentiment analysis

**Time Series**:
- Stock price prediction
- Weather forecasting
- Anomaly detection

**Other Sequences**:
- Video analysis
- Music generation
- Handwriting recognition

### RNN Limitations

1. **Sequential Processing**: Cannot parallelize across time steps (slow)
2. **Vanishing Gradients**: Still problematic for very long sequences despite LSTM/GRU
3. **Memory Constraints**: Hidden state has fixed size
4. **Long-Range Dependencies**: Difficult beyond ~100-1000 tokens

**Result**: Largely replaced by transformers for NLP tasks

## Transformers: The Modern Standard

### The Attention Revolution

**Paper**: "Attention Is All You Need" (Vaswani et al., 2017)

**Key Insight**: Replace recurrence with attention mechanisms—allowing parallel processing and better long-range dependencies

### Architecture Components

#### Self-Attention Mechanism

**Purpose**: Compute relevance between all pairs of tokens in sequence

**Process**:
1. **Create Q, K, V**: Transform input into Query, Key, Value vectors
2. **Compute Attention Scores**: How much each token should attend to others
3. **Apply Softmax**: Normalize scores to probabilities
4. **Weighted Sum**: Combine Values weighted by attention scores

**Formula**:
```
Attention(Q, K, V) = softmax(QK^T / √dₖ) V
```

**Benefit**: Each token can directly access any other token (no sequential bottleneck)

#### Multi-Head Attention

**Concept**: Run multiple attention mechanisms in parallel, each learning different relationships

**Example**: 8 heads might separately learn:
- Syntactic relationships (subject-verb)
- Semantic similarity
- Positional relationships
- Long-range dependencies

**Advantage**: Richer representation than single attention

#### Position Encoding

**Problem**: Attention has no inherent notion of token order

**Solution**: Add positional information to embeddings

**Methods**:
- Sinusoidal encoding (original transformer)
- Learned position embeddings
- Relative position encoding (T5, etc.)

#### Layer Normalization

Normalizes activations across features, stabilizing training

#### Feedforward Networks

After attention, each position processed independently through dense layers

### Transformer Architectures

| Architecture | Type | Purpose | Examples |
|--------------|------|---------|----------|
| **Encoder-Only** | Bidirectional context | Understanding tasks | BERT, RoBERTa |
| **Decoder-Only** | Causal (left-to-right) | Generation tasks | GPT, Claude, LLaMA |
| **Encoder-Decoder** | Both components | Sequence-to-sequence | T5, BART, original Transformer |

### Encoder Architecture (BERT-style)

**Structure**:
```
Input Tokens
    ↓
Token + Position Embeddings
    ↓
Multi-Head Self-Attention (bidirectional)
    ↓
Add & Norm
    ↓
Feedforward Network
    ↓
Add & Norm
    ↓
(Repeat N layers)
    ↓
Output Representations
```

**Use Cases**:
- Text classification
- Named entity recognition
- Question answering
- Sentence similarity

### Decoder Architecture (GPT-style)

**Structure**:
```
Input Tokens
    ↓
Token + Position Embeddings
    ↓
Masked Multi-Head Self-Attention (causal)
    ↓
Add & Norm
    ↓
Feedforward Network
    ↓
Add & Norm
    ↓
(Repeat N layers)
    ↓
Output Logits (next token prediction)
```

**Masking**: Tokens can only attend to previous tokens (causality)

**Use Cases**:
- Text generation
- Code completion
- Conversation
- Creative writing

### Why Transformers Dominate

**Advantages over RNNs**:
1. **Parallelization**: Process entire sequence simultaneously
2. **Long-Range Dependencies**: Direct connections between distant tokens
3. **Scalability**: Performance improves with more parameters/data
4. **Transfer Learning**: Pre-train once, fine-tune for many tasks

**Computational Cost**: O(n²) in sequence length (quadratic attention)

**Recent Innovations** to address cost:
- Sparse attention patterns
- Linear attention approximations
- Efficient attention mechanisms (FlashAttention)

### Scaling Laws

**Observation**: Transformer performance predictably improves with:
- More parameters (model size)
- More training data
- More compute

**Implication**: Led to race toward larger models (GPT-3: 175B, GPT-4: estimated 1T+ params)

## Attention Mechanisms

### Types of Attention

| Type | Description | Use Case |
|------|-------------|----------|
| **Self-Attention** | Tokens attend to tokens in same sequence | Transformers |
| **Cross-Attention** | Tokens attend to different sequence | Translation, image captioning |
| **Global Attention** | Attend to all positions | Standard transformer |
| **Local Attention** | Attend to nearby window | Long sequences |
| **Sparse Attention** | Attend to subset of positions | Very long sequences |

### Attention Visualization

**Example: Translation**
```
Source: "The cat sat on the mat"
Target: "Le chat"

When generating "chat", attention focuses on:
- "cat" (high weight: 0.8)
- "The" (medium weight: 0.15)
- Other tokens (low weights: <0.05)
```

Attention weights reveal what the model "looks at" when making predictions

### Multi-Modal Attention

**Vision Transformers (ViT)**:
- Split image into patches
- Treat patches as tokens
- Apply transformer architecture
- State-of-art image classification

**CLIP (Contrastive Language-Image Pre-training)**:
- Cross-attention between image and text
- Learn joint embedding space
- Zero-shot image classification

**Multi-Modal Transformers**:
- Process text, images, audio simultaneously
- Examples: GPT-4V, Gemini, Claude 3

## Deep Learning in Practice

### Pre-training and Fine-tuning

**Two-Stage Paradigm**:

1. **Pre-training**: Learn general representations on massive unlabeled data
   - Example: Train on all of Wikipedia, web crawl
   - Objective: Next token prediction, masked language modeling

2. **Fine-tuning**: Adapt to specific task with smaller labeled dataset
   - Example: Sentiment analysis on movie reviews
   - Trains much faster than from scratch

**Transfer Learning Benefits**:
- Reduced training time
- Better performance with less data
- Leverages general knowledge

### Foundation Models

**Definition**: Large models trained on broad data, adaptable to many downstream tasks

**Examples**:
- **Language**: GPT-4, Claude, PaLM
- **Vision**: CLIP, DINOv2
- **Multi-Modal**: GPT-4V, Gemini

**Paradigm Shift**: Rather than training task-specific models, adapt one foundation model to many tasks via:
- Fine-tuning
- Prompt engineering
- Few-shot learning
- In-context learning

### Real-World Deep Learning Pipeline

1. **Data Collection**: Gather training data
2. **Preprocessing**: Clean, normalize, augment data
3. **Model Selection**: Choose architecture (CNN, transformer, etc.)
4. **Training**: Optimize on training data
5. **Validation**: Tune hyperparameters
6. **Testing**: Evaluate on held-out data
7. **Deployment**: Serve predictions in production
8. **Monitoring**: Track performance, detect drift

**Key Terms**
- **Deep Learning**: Neural networks with many layers learning hierarchical features
- **Convolutional Layer**: Filter-based layer for spatial data
- **Pooling**: Downsampling operation reducing spatial dimensions
- **Recurrent Neural Network**: Architecture for sequential data with memory
- **LSTM/GRU**: RNN variants handling long-term dependencies
- **Attention Mechanism**: Computing relevance between sequence elements
- **Transformer**: Architecture based entirely on attention, no recurrence
- **Self-Attention**: Attention within single sequence
- **Pre-training**: Learning general representations on large unlabeled data
- **Fine-tuning**: Adapting pre-trained model to specific task

## Summary

Deep learning revolutionized AI through architectures learning hierarchical representations across many layers. CNNs transformed computer vision by exploiting spatial structure through convolution and pooling, enabling superhuman image classification and object detection. RNNs and LSTMs brought sequence modeling to NLP and time series but suffered from sequential processing bottlenecks. The transformer architecture solved this through self-attention mechanisms, enabling parallel processing and better long-range dependencies. Attention allows models to dynamically focus on relevant information, powering breakthroughs in language understanding and generation. Modern deep learning follows a pre-train then fine-tune paradigm, where foundation models learn general representations from massive datasets then adapt to specific tasks. Transformers now dominate not just NLP but increasingly vision and multi-modal tasks. The combination of scale (billions of parameters), data (internet-scale training), and architectural innovation (attention, skip connections, normalization) enables today's AI capabilities. Understanding these architectures—their strengths, limitations, and appropriate use cases—is essential for anyone working with modern AI systems.
