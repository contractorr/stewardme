# Natural Language Processing and Computer Vision

## Overview

Natural Language Processing (NLP) and Computer Vision represent the two dominant application domains of modern deep learning. NLP enables machines to understand, generate, and manipulate human language—powering chatbots, translation systems, and content generation. Computer vision allows machines to interpret visual information—enabling autonomous vehicles, medical diagnosis, and facial recognition. Both fields have undergone revolutionary transformations through deep learning, evolving from hand-crafted features to end-to-end learned representations. This guide covers fundamental concepts, techniques, and applications in both domains.

## Natural Language Processing (NLP)

### Text Representation Fundamentals

#### Tokenization

**Definition**: Breaking text into smaller units (tokens)

**Levels**:
- **Character**: Individual characters
- **Word**: Whitespace/punctuation splitting
- **Subword**: Balance between character and word (BPE, WordPiece, Unigram)

**Example**:
```
Text: "Natural Language Processing"
Word tokens: ["Natural", "Language", "Processing"]
Subword (BPE): ["Nat", "ural", "Language", "Process", "ing"]
```

**Modern Standard**: Subword tokenization (handles rare words, efficient vocabulary size)

#### Vocabulary and Token IDs

**Process**:
1. Build vocabulary from training corpus
2. Assign unique integer ID to each token
3. Convert text to sequence of IDs

**Example**:
```
Vocabulary: {"hello": 1, "world": 2, "[UNK]": 3}
Text: "hello world" → [1, 2]
Text: "hello universe" → [1, 3]  # "universe" unknown
```

**Special Tokens**:
- `[PAD]`: Padding shorter sequences
- `[UNK]`: Unknown/out-of-vocabulary words
- `[CLS]`: Classification token (BERT)
- `[SEP]`: Separator between sentences
- `[MASK]`: Masked tokens for training

### Word Embeddings

**Problem**: Token IDs are discrete, no semantic relationship

**Solution**: Map tokens to continuous vector space where similar words are close

#### One-Hot Encoding (Baseline)

**Representation**: Binary vector, 1 at token position, 0 elsewhere

**Example**:
```
Vocabulary size: 10,000
"cat" → [0, 0, ..., 1, ..., 0]  (length 10,000)
```

**Problems**:
- High dimensionality
- No semantic relationships
- Sparse representation

#### Word2Vec

**Concept**: Learn embeddings by predicting context words

**Architectures**:
- **CBOW** (Continuous Bag of Words): Predict word from context
- **Skip-gram**: Predict context from word

**Example**:
```
Sentence: "The cat sat on the mat"
Skip-gram task: Given "sat", predict ["cat", "on"]
```

**Properties**:
- Captures semantic similarity: vec("king") - vec("man") + vec("woman") ≈ vec("queen")
- Typical dimension: 100-300

**Limitation**: Fixed representation (same word always same vector regardless of context)

#### GloVe (Global Vectors)

**Concept**: Factorize word co-occurrence matrix

**Advantage**: Leverages global corpus statistics

#### Contextual Embeddings (Modern Approach)

**Key Insight**: Word meaning depends on context

**Example**:
```
"The bank of the river" (riverbank)
"The bank approved my loan" (financial institution)
```

**Solution**: Transformer-based models (BERT, GPT) generate context-dependent embeddings

**Process**:
1. Pass sentence through pre-trained model
2. Extract hidden states for each token
3. Same word gets different embeddings in different contexts

### Language Models

**Definition**: Models that predict probability of text sequences

#### N-gram Language Models (Traditional)

**Concept**: Predict next word based on previous N-1 words

**Example (Bigram)**:
```
P("cat" | "the") = count("the cat") / count("the")
```

**Limitations**:
- Fixed context window
- Sparsity issues
- No generalization

#### Neural Language Models

**Architecture**: RNN/LSTM or Transformer

**Training Objective**: Predict next token given previous tokens

**Autoregressive Generation**:
```
1. Start with prompt: "The cat"
2. Predict next token: "sat"
3. Append and repeat: "The cat sat"
4. Continue until [END] token
```

**Examples**: GPT series, LLaMA, Claude

#### Masked Language Models

**Training**: Randomly mask tokens, predict masked tokens from context

**Example (BERT)**:
```
Input: "The [MASK] sat on the mat"
Task: Predict "cat"
```

**Advantage**: Bidirectional context (sees both left and right)

**Use Cases**: Text understanding tasks (classification, QA) rather than generation

### Key NLP Architectures

| Model | Type | Training Objective | Strengths | Use Cases |
|-------|------|-------------------|-----------|-----------|
| **Word2Vec** | Embeddings | Context prediction | Fast, simple | Word similarity |
| **LSTM** | Recurrent | Next token prediction | Sequential processing | Early NLP (largely superseded) |
| **BERT** | Encoder | Masked language modeling | Bidirectional context | Classification, QA, NER |
| **GPT** | Decoder | Next token prediction | Text generation | Chatbots, content creation |
| **T5** | Encoder-Decoder | Text-to-text | Unified framework | Translation, summarization |
| **BART** | Encoder-Decoder | Denoising | Generation + understanding | Summarization |

### Common NLP Tasks

#### Text Classification

**Task**: Assign category label to text

**Examples**:
- Sentiment analysis (positive/negative/neutral)
- Spam detection
- Topic categorization
- Intent detection

**Approach**:
1. Encode text with pre-trained model (BERT)
2. Pass [CLS] token representation to classifier
3. Train on labeled examples

#### Named Entity Recognition (NER)

**Task**: Identify and classify entities in text

**Example**:
```
Text: "Apple CEO Tim Cook announced new iPhone in California"
Entities:
- Apple: Organization
- Tim Cook: Person
- iPhone: Product
- California: Location
```

**Approach**: Token-level classification (BIO tagging scheme)

#### Question Answering

**Task**: Answer questions based on context

**Types**:
- **Extractive**: Select span from provided text
- **Generative**: Generate answer from knowledge

**Example**:
```
Context: "The Eiffel Tower is located in Paris, France."
Question: "Where is the Eiffel Tower?"
Answer: "Paris, France"
```

**Models**: BERT (extractive), GPT (generative)

#### Machine Translation

**Task**: Translate text between languages

**Architecture**: Sequence-to-sequence with attention (encoder-decoder)

**Example**:
```
English: "How are you?"
French: "Comment allez-vous?"
```

**Modern Approach**: Transformer encoder-decoder (T5, BART) or large multilingual models

#### Text Summarization

**Types**:
- **Extractive**: Select important sentences from source
- **Abstractive**: Generate new summary text

**Approaches**:
- Encoder-decoder models (BART, T5)
- Large language models with prompting (GPT-4, Claude)

#### Text Generation

**Applications**:
- Content creation
- Dialogue systems
- Code generation
- Creative writing

**Techniques**:
- **Greedy Decoding**: Always pick most likely next token
- **Beam Search**: Keep top K candidates
- **Sampling**: Sample from probability distribution
- **Top-K Sampling**: Sample from top K most likely tokens
- **Nucleus (Top-P) Sampling**: Sample from smallest set with cumulative probability P

### Modern NLP: Large Language Models

**Scale**: Billions to trillions of parameters

**Capabilities**:
- **Few-Shot Learning**: Learn from examples in prompt
- **Zero-Shot Learning**: Perform tasks without examples
- **In-Context Learning**: Learn patterns within conversation
- **Chain-of-Thought**: Solve complex reasoning by thinking step-by-step

**Prompt Engineering**: Carefully crafting inputs to elicit desired outputs

**Examples**:
- GPT-4 (OpenAI): 1T+ parameters estimated
- Claude (Anthropic): Constitutional AI approach
- PaLM 2 (Google): Efficient training
- LLaMA (Meta): Open weights

## Computer Vision

### Image Representation

**Digital Image**: Grid of pixels, each with intensity values

**Formats**:
- **Grayscale**: Single channel (0-255)
- **RGB**: Three channels (Red, Green, Blue)
- **Common Size**: 224×224×3 (ImageNet standard)

**Example Representation**:
```
Grayscale 3×3 image:
[120, 130, 140]
[110, 150, 160]
[100, 140, 180]
```

### Image Preprocessing

**Common Operations**:
- **Resizing**: Standardize to fixed dimensions
- **Normalization**: Scale pixel values (e.g., 0-1 or standardize)
- **Augmentation**: Random transformations (rotation, flip, crop, color jitter)

**ImageNet Normalization** (Standard):
```
mean = [0.485, 0.456, 0.406]  # RGB
std = [0.229, 0.224, 0.225]
normalized = (image - mean) / std
```

### Image Classification

**Task**: Assign single label to entire image

**Process**:
1. **Input**: Image (e.g., 224×224×3)
2. **Feature Extraction**: CNN layers detect patterns
3. **Classification**: Fully-connected layers produce class probabilities
4. **Output**: Class label and confidence

**Architectures**:
- **AlexNet** (2012): First deep CNN breakthrough
- **VGG** (2014): Simple, deep architecture with 3×3 filters
- **ResNet** (2015): Skip connections enable very deep networks (50-152 layers)
- **EfficientNet** (2019): Compound scaling for efficiency
- **Vision Transformer (ViT)** (2020): Transformer applied to image patches

**Evaluation Metrics**:
- Top-1 Accuracy: Correct label is #1 prediction
- Top-5 Accuracy: Correct label in top 5 predictions

### Object Detection

**Task**: Locate and classify multiple objects in image

**Output**: For each object:
- Bounding box coordinates (x, y, width, height)
- Class label
- Confidence score

**Approaches**:

#### Two-Stage Detectors

**Example: Faster R-CNN**

**Process**:
1. **Region Proposal**: Identify candidate object locations
2. **Feature Extraction**: Extract features from each region
3. **Classification**: Classify and refine boxes

**Pros**: High accuracy
**Cons**: Slower inference

#### One-Stage Detectors

**Example: YOLO (You Only Look Once), SSD**

**Process**:
1. Divide image into grid
2. Each grid cell predicts bounding boxes and classes
3. Single forward pass through network

**Pros**: Fast (real-time capable)
**Cons**: Slightly lower accuracy than two-stage

**Modern Standard**: YOLO variants, EfficientDet

### Semantic Segmentation

**Task**: Classify every pixel in image

**Output**: Segmentation map (same size as input, each pixel labeled)

**Example Use Cases**:
- Autonomous driving (road, car, pedestrian, sky)
- Medical imaging (tumor, healthy tissue)
- Satellite imagery (buildings, vegetation, water)

**Architecture: U-Net**

**Structure**:
```
Encoder (Downsampling):
Input → Conv → Pool → Conv → Pool → ... (extract features)

Decoder (Upsampling):
... → Upsample → Conv → Upsample → Output (reconstruct resolution)

Skip Connections:
Connect encoder layers to decoder layers (preserve spatial info)
```

**Why It Works**: Combines high-level semantic info with low-level spatial details

**Variants**: DeepLab, Mask R-CNN (instance segmentation)

### Image Generation

#### Generative Adversarial Networks (GANs)

**Architecture**: Two networks competing

**Components**:
1. **Generator**: Creates fake images from random noise
2. **Discriminator**: Distinguishes real from fake

**Training**:
- Generator tries to fool discriminator
- Discriminator tries to detect fakes
- Both improve through competition

**Applications**:
- Photorealistic face generation (StyleGAN)
- Image-to-image translation (Pix2Pix)
- Super-resolution
- Art generation

**Challenges**: Training instability, mode collapse

#### Diffusion Models

**Concept**: Learn to reverse noise-adding process

**Training**:
1. Take real image
2. Gradually add noise
3. Train model to remove noise

**Generation**:
1. Start with pure noise
2. Iteratively denoise
3. Obtain clean image

**Advantages**: More stable training than GANs, high quality

**Examples**: DALL-E 2, Stable Diffusion, Midjourney

#### Variational Autoencoders (VAEs)

**Architecture**: Encoder compresses to latent code, decoder reconstructs

**Advantage**: Smooth latent space enables interpolation

**Use Cases**: Image generation, anomaly detection

### Object Tracking

**Task**: Follow object across video frames

**Approaches**:
- Optical flow
- Correlation filters
- Deep learning (Siamese networks)

**Applications**: Sports analysis, surveillance, autonomous vehicles

### Face Recognition

**Pipeline**:
1. **Face Detection**: Locate faces in image
2. **Face Alignment**: Normalize pose/scale
3. **Feature Extraction**: Generate embedding vector
4. **Matching**: Compare embeddings (cosine similarity)

**Key Architecture**: FaceNet (triplet loss)

**Applications**: Phone unlocking, security systems, photo organization

### Image Captioning

**Task**: Generate text description of image

**Architecture**: CNN encoder + Transformer/LSTM decoder

**Process**:
1. CNN extracts visual features
2. Decoder generates caption word-by-word
3. Attention mechanism focuses on relevant image regions

**Example**:
```
Image: [Photo of dog playing in park]
Caption: "A golden retriever playing fetch in a sunny park"
```

**Models**: Show and Tell, Show-Attend-and-Tell, modern: CLIP + GPT variants

### Visual Question Answering (VQA)

**Task**: Answer questions about images

**Input**: Image + question
**Output**: Answer

**Example**:
```
Image: [Kitchen scene]
Question: "How many apples are on the table?"
Answer: "Three"
```

**Architecture**: Multimodal fusion of image and text encodings

### Transfer Learning in Computer Vision

**Standard Practice**: Pre-train on ImageNet, fine-tune on target task

**Process**:
1. Train large CNN on ImageNet (1.2M images, 1000 classes)
2. Use learned weights as initialization
3. Fine-tune on smaller target dataset

**Benefits**:
- Faster convergence
- Better performance with limited data
- Learned features are general-purpose

**Common Backbones**: ResNet-50, EfficientNet, Vision Transformer

**When to Fine-tune**:
- **Feature Extraction**: Freeze backbone, train only classifier (small dataset)
- **Full Fine-tuning**: Train all layers (medium/large dataset)
- **Train from Scratch**: Only if massive domain-specific dataset

## Multimodal AI

**Definition**: Models processing multiple modalities (text, images, audio, video)

### CLIP (Contrastive Language-Image Pre-training)

**Training**: Match images with text descriptions

**Capability**: Zero-shot image classification via text prompts

**Architecture**: Separate image and text encoders, aligned embedding space

**Applications**:
- Image search with text queries
- Zero-shot classification
- Foundation for many multimodal systems

### Vision-Language Models

**Examples**: GPT-4V, Claude 3, Gemini

**Capabilities**:
- Image understanding
- Visual question answering
- Diagram interpretation
- Screenshot analysis

**Architecture**: Vision encoder + large language model

### Text-to-Image Models

**Examples**: DALL-E 3, Midjourney, Stable Diffusion

**Input**: Text prompt
**Output**: Generated image

**Techniques**: Diffusion models, attention mechanisms

**Applications**: Creative design, content creation, concept visualization

## Comparison: NLP vs Computer Vision

| Aspect | NLP | Computer Vision |
|--------|-----|-----------------|
| **Input Structure** | Sequential (1D) | Spatial (2D/3D) |
| **Primary Challenge** | Ambiguity, context | Variation, occlusion |
| **Dominant Architecture** | Transformers | CNNs (increasingly transformers) |
| **Data Efficiency** | Requires large corpora | Transfer learning helps small datasets |
| **Evaluation** | Perplexity, BLEU, accuracy | Accuracy, IoU, mAP |
| **Pre-training** | Language modeling | ImageNet classification |

## Practical Considerations

### Data Requirements

**NLP**:
- Pre-training: Billions of tokens (web text)
- Fine-tuning: 1K-100K examples depending on task

**Computer Vision**:
- Pre-training: Millions of images (ImageNet)
- Fine-tuning: 100-10K images with transfer learning

### Computational Costs

**Training**:
- Large language models: Weeks on hundreds of GPUs/TPUs
- Vision models: Days to weeks on multiple GPUs

**Inference**:
- Text generation: 10-100ms per token
- Image classification: 1-10ms per image
- Object detection: 10-100ms per image

### Common Pitfalls

**NLP**:
- Biased training data leading to biased outputs
- Hallucination (generating false information)
- Context length limitations

**Computer Vision**:
- Domain shift (train/test distribution mismatch)
- Adversarial examples (small perturbations fool models)
- Annotation quality/cost

**Key Terms**
- **Tokenization**: Splitting text into units for processing
- **Word Embedding**: Dense vector representation of words
- **Language Model**: Model predicting text probability distributions
- **Transformer**: Attention-based architecture for sequence modeling
- **CNN**: Convolutional neural network for spatial data
- **Object Detection**: Locating and classifying objects in images
- **Semantic Segmentation**: Per-pixel classification
- **Transfer Learning**: Using pre-trained weights for new tasks
- **CLIP**: Vision-language model with aligned embeddings
- **Diffusion Model**: Generative model learning to denoise

## Summary

Natural Language Processing and Computer Vision represent the two pillars of modern AI applications. NLP has evolved from rule-based systems and n-grams to transformer-based language models capable of understanding context and generating human-like text. Key breakthroughs include contextual embeddings (BERT, GPT), attention mechanisms enabling long-range dependencies, and scaling to models with hundreds of billions of parameters. Computer vision progressed from hand-crafted features to deep CNNs learning hierarchical representations, with architectures like ResNet enabling very deep networks through skip connections. Recent years have seen transformers entering computer vision (Vision Transformers) and the rise of multimodal models combining vision and language (CLIP, GPT-4V). Both domains benefit enormously from transfer learning—pre-training on massive datasets then fine-tuning on specific tasks. Modern AI increasingly combines modalities, with text-to-image generation, visual question answering, and unified vision-language models. Understanding both domains and their techniques is essential for developing comprehensive AI systems addressing real-world problems spanning multiple data types.
