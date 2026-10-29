# TATVA

# TATVA — Understand What You Eat.

**TATVA** is an AI-powered food label intelligence system that transforms confusing nutrition labels into clear, structured, and goal-oriented insights.

A simple photo of a packaged food product becomes a breakdown of its nutritional value, ingredients, potential concerns, and suitability for different fitness and nutrition goals.

> **One product. Multiple perspectives. Better-informed choices.**

---

## Overview

Nutrition labels contain valuable information, but understanding serving sizes, nutrient quantities, ingredient lists, and marketing claims can be confusing.

TATVA aims to make that information easier to understand.

Using Optical Character Recognition (OCR), computer vision, Python-based nutritional analysis, and Large Language Models (LLMs), TATVA extracts information from food packaging and converts it into meaningful insights.

Instead of giving every product a single, generic health score, TATVA evaluates it from multiple perspectives — because the best choice depends on what you are looking for.

## Key Features

### 📸 1. AI-Powered Label Scanning
- Capture or upload a photograph of a packaged food label.
- Detect and extract text from nutrition tables and ingredient lists.
- Process imperfect images using image preprocessing techniques.
- Validate extracted information before calculating scores.

### 🎯 2. Goal-Based Nutrition Scoring

Evaluate products against different nutritional goals:

| Score | Purpose |
|---|---|
| 💪 Muscle Gain | Evaluate protein, energy, and other relevant nutritional factors. |
| ⚖️ Weight Loss | Assess calorie density, protein, and other relevant factors. |
| 🥚 Protein Quality | Evaluate protein content per serving and per 100 g. |
| 🥗 Low-Calorie / High-Volume | Identify products that may fit lower-calorie eating patterns. |
| 🌿 Nutrient Quality | Assess relevant nutrients and nutritional trade-offs. |
| 🔍 Ingredient Analysis | Highlight noteworthy ingredients and potential concerns. |
| ⭐ Overall Score | Provide a general-purpose nutritional overview. |

*Scores are intended as transparent, rule-based estimates rather than clinically validated health ratings.*

### 🧪 3. Ingredient Intelligence
- Extract and organize ingredient lists.
- Identify ingredients worth examining more closely.
- Explain nutritional terminology in simple language.
- Highlight relevant information such as added sugars, sodium, and types of fat when the label provides sufficient data.

### 🤖 4. AI-Generated Explanations
Use an LLM to turn structured nutritional data into understandable explanations.

Examples:
- Why might this product suit a high-protein diet?
- What nutritional trade-offs should I consider?
- Which ingredients deserve a closer look?
- How does this product compare with another option?

AI-generated explanations will be grounded in extracted and validated data rather than relying on the language model to invent nutritional values.

### 📊 5. Product Comparison *(Planned)*
Compare products side by side using:
- Calories and macronutrients.
- Protein per serving and per 100 g.
- Ingredient differences.
- Goal-specific scores.
- Data quality and extraction confidence.

### 🗂️ 6. Scan History *(Planned)*
Store previously analyzed products and revisit their nutritional information through a simple dashboard.

---

## How TATVA Works

The system follows a pipeline that transforms an image into a structured nutritional analysis.

```text
        FOOD LABEL IMAGE
                |
                v
     IMAGE PREPROCESSING
       OpenCV / Python
                |
                v
          TEXT EXTRACTION
       OCR: Tesseract or
          PaddleOCR
                |
                v
       STRUCTURED DATA
     Nutrition + Ingredients
                |
                v
       VALIDATION & CLEANUP
   Units, serving sizes, ranges
                |
                v
       NUTRITIONAL ENGINE
      Transparent Python Rules
                |
                v
       LLM-POWERED INSIGHTS
      Explanations and Context
                |
                v
         TATVA DASHBOARD
    Scores, Insights, Comparisons
```

The nutritional engine and the LLM have separate responsibilities: Python performs the scoring calculations, while the LLM helps explain the results in human-friendly language.

---

## Technology Stack

The initial implementation is planned around Python and locally runnable AI components.

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Core application logic and scoring |
| Image processing | OpenCV | Image enhancement and preprocessing |
| OCR | Tesseract OCR / PaddleOCR | Extract text from food labels |
| AI / LLM | Ollama with a local Llama model | Explain and interpret structured results |
| Data validation | Pydantic | Validate extracted nutritional data |
| Backend API | FastAPI | Expose analysis functionality through API endpoints |
| Initial interface | Streamlit | Build an interactive dashboard |
| Database | SQLite | Store products and scan history |
| Optional data verification | Open Food Facts | Cross-check available product information |

*These are the planned technologies; exact selections may evolve during implementation.*

---

## Project Structure

The following is the proposed structure as the project grows.

```text
TATVA/
│
├── app.py                     # Streamlit application
├── requirements.txt           # Python dependencies
├── README.md
├── .gitignore
├── .env.example
│
├── backend/
│   └── main.py                # FastAPI entry point
│
├── core/
│   ├── image_processing.py    # Image preprocessing
│   ├── ocr_engine.py          # Text extraction
│   ├── data_extraction.py     # Structured data parsing
│   ├── validation.py          # Data validation
│   ├── nutrition_engine.py    # Nutritional scoring
│   └── llm_insights.py        # AI-generated explanations
│
├── models/
│   └── schemas.py             # Data models and schemas
│
├── database/
│   ├── db.py                  # Database connection
│   └── operations.py          # Database operations
│
├── tests/
│   ├── test_ocr.py
│   ├── test_validation.py
│   └── test_scoring.py
│
└── data/
    └── sample_labels/         # Test images, not private user data
```

*This is a proposed layout, not a claim that all these files have already been implemented.*

---

## Nutritional Scoring Philosophy

TATVA is designed around three principles.

### 1. Context matters
A product suitable for increasing protein intake may not be the best choice for reducing calorie intake. TATVA therefore provides multiple goal-specific scores rather than treating one score as universally correct.

### 2. Calculations should be transparent
Nutritional scores should be calculated using documented Python rules and configurable weights. Users should be able to understand which factors influenced a result.

### 3. Data quality comes first
Incorrect OCR results can produce misleading analysis. TATVA will validate extracted values, account for serving sizes, distinguish missing values from zero, and communicate uncertainty when information cannot be reliably extracted.

Where possible, nutritional information should be normalized to both **per serving** and **per 100 g / 100 ml**, while preserving the original label values.

---

## Development Roadmap

The project will be developed incrementally, with each phase building on the previous one.

- [ ] **Phase 1 — OCR Foundation:** Upload an image, preprocess it, and extract readable text.
- [ ] **Phase 2 — Structured Extraction:** Convert OCR output into nutritional fields and ingredient lists.
- [ ] **Phase 3 — Validation:** Validate values, serving sizes, units, and missing fields.
- [ ] **Phase 4 — Scoring Engine:** Implement and test goal-specific nutritional scoring rules.
- [ ] **Phase 5 — AI Insights:** Integrate an LLM for explanations grounded in validated data.
- [ ] **Phase 6 — Dashboard:** Display extracted values, scores, ingredients, and explanations.
- [ ] **Phase 7 — Persistence:** Add SQLite storage and scan history.
- [ ] **Phase 8 — Product Comparison:** Compare multiple products and improve the user experience.

**Initial milestone:** Build a working pipeline that can extract nutritional information from a sample food label and calculate a score from validated data before adding more advanced AI features.

---

## Getting Started

TATVA is currently in the planning and early development stage.

### Prerequisites

- Python 3.10 or later.
- Git.
- A code editor such as Visual Studio Code.
- Tesseract OCR installed locally when using the Tesseract engine.
- Ollama and a compatible local language model when enabling LLM-powered explanations.

### Initial setup

Clone the repository:

```bash
git clone <your-repository-url>
cd TATVA
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies once `requirements.txt` has been created:

```bash
pip install -r requirements.txt
```

*The repository URL, dependency list, and runnable entry points must be configured as implementation progresses.*

---

## Responsible Use

TATVA is an informational nutrition-analysis tool, not a medical diagnostic system or a substitute for professional dietary advice.

- Its scores are estimates based on available label data and documented rules.
- Packaging information may be incomplete, outdated, or incorrectly extracted.
- A product's nutritional value depends on serving size, dietary needs, and overall eating patterns.
- Ingredient flags and marketing-claim assessments should be evidence-based and should not imply risks that the available data cannot establish.
- Users should be shown when extracted data is incomplete or uncertain.

TATVA will prioritize transparent calculations, explainable results, and honest communication of limitations.

---

## Vision

TATVA aims to make nutritional information accessible without requiring users to decode complicated packaging or rely solely on marketing claims.

The long-term vision is a system where people can scan a product, understand its nutritional composition, evaluate it against their goals, and make more informed food choices.

**TATVA — Understand the label. Understand the food.**

---

## License

The project's license has not yet been selected. A license should be added before distributing or accepting contributions under defined open-source terms.
