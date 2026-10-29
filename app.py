
import streamlit as st


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TATVA | Food Intelligence",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #F7F8F4;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1150px;
        }

        .hero {
            padding: 2rem;
            border-radius: 18px;
            background: linear-gradient(120deg, #173D32, #28644D);
            color: white;
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            color: white;
        }

        .hero p {
            font-size: 1.05rem;
            color: #E0EDE4;
        }

        .section-title {
            color: #173D32;
            font-weight: 700;
        }

        .disclaimer {
            color: #666666;
            font-size: 0.82rem;
            margin-top: 2rem;
        }

        [data-testid="stFileUploader"] {
            background: white;
            padding: 1rem;
            border: 1px dashed #7A9A83;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🥗 TATVA")
    st.caption("FOOD LABEL INTELLIGENCE")
    st.divider()

    st.markdown("### Your nutrition goal")

    goal = st.selectbox(
        "Choose your primary goal",
        [
            "Overall Nutrition",
            "Muscle Gain",
            "Weight Loss",
            "High Protein",
            "Low Calorie, High Volume",
            "Nutrient Balance",
        ],
    )

    st.divider()

    st.markdown("### How it works")
    st.markdown(
        """
        1. Upload a food-label image.
        2. Extract nutrition information.
        3. Review detected values.
        4. Evaluate the product for your goal.
        """
    )

    st.caption("TATVA • Early Development Version")


# ---------------- HERO SECTION ----------------
st.markdown(
    """
    <div class="hero">
        <h1>TATVA</h1>
        <p><b>Know what goes into your food.</b></p>
        <p>
            Turn packaged food labels into useful nutrition insights.
            Understand what you eat and how it aligns with your goals.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------- INTRODUCTION ----------------
st.markdown(
    '<h3 class="section-title">Analyse your food</h3>',
    unsafe_allow_html=True,
)

st.write(
    "Upload a clear picture of the nutrition label on your "
    "packaged food. TATVA will prepare it for nutrition analysis."
)


# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload a nutrition label",
    type=["png", "jpg", "jpeg"],
    help="Use a clear, well-lit image with readable text.",
)


# ---------------- IMAGE ANALYSIS ----------------
if uploaded_file is not None:
    st.divider()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("### Uploaded label")

        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True,
        )

    with right:
        st.markdown("### Analysis settings")
        st.write("**Selected goal:**", goal)

        if st.button(
            "Analyze nutrition label",
            type="primary",
            use_container_width=True,
        ):
            try:
                from nutriscan.app_pipeline import (
                    analyze_uploaded_image,
                )

                with st.spinner(
                    "Processing image and extracting nutrition data..."
                ):
                    result = analyze_uploaded_image(
                        uploaded_file.getvalue()
                    )

                st.session_state["tatva_result"] = result
                st.session_state["selected_goal"] = goal

                st.success("Image processing completed!")

            except Exception as error:
                st.error(f"Analysis failed: {error}")

    # Display results outside the button block so they remain
    # visible after Streamlit reruns the app.
    result = st.session_state.get("tatva_result")

    if result is not None:
        st.divider()
        st.markdown("### Extracted nutrition data")

        st.caption(
            "Review these extracted values against the original label "
            "before relying on them."
        )

        nutrition = result["nutrition"]
        #st.caption(f"OCR method : {result.get()'ocr_method', 'Tesseract OCR')}")
        st.write("**SELECTED OCR METHOD:**", result["ocr_method"])
        st.json(nutrition)

        with st.expander("INspect all OCR attempts",expanded = True) :
            for candidate in result["ocr_candidates"] :
                st.markdown(
                    f"**{candidate['method']}** "
                    f"(score: {candidate['score']})"
                )
                st.text(candidate["text"] or "[No text recognized]")

        with st.expander("View selected raw OCR text") :
            st.text(result["ocr_text"])

        st.info(
            "Do not use the extracted values for scoring until "
            "they have been verified against the original label."
        )
        
        '''st.caption(f"OCR method: {result.get('ocr_method', 'Tesseract OCR')}")
        st.json(nutrition)

        with st.expander("View raw OCR text"):
            st.text(result["ocr_text"])

        st.info(
            "Nutrition scoring is not connected yet. "
            "First verify the extracted values."
        )'''

else:
    # Clear previous results when no image is uploaded.
    st.session_state.pop("tatva_result", None)

    st.markdown("### What you'll be able to explore")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔬 Nutrition facts")
        st.write(
            "Extract energy, protein, carbohydrates, sugars, "
            "fats and sodium from food labels."
        )

    with col2:
        st.markdown("#### 🎯 Goal-based insights")
        st.write(
            "Understand how a product aligns with your "
            "selected nutrition goal."
        )

    with col3:
        st.markdown("#### 🧠 AI-powered analysis")
        st.write(
            "Combine OCR and language-model extraction "
            "to make food-label data easier to understand."
        )


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    """
    <div class="disclaimer">
        TATVA is a food-label information project. Its insights are
        intended for informational purposes only and are not medical
        advice. Results depend on label readability and extraction accuracy.
    </div>
    """,
    unsafe_allow_html=True,
)
