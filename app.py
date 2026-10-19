
import os
import streamlit as st
from compliance import check_compliance
from dotenv import load_dotenv
from google import genai

from rag.knowledge_base import (
    process_brand_guide,
    retrieve_brand_rules
)

load_dotenv()

st.set_page_config(
    page_title="AI Marketing Studio",
    page_icon="📣",
    layout="wide"
)

st.title("AI Marketing Campaign & Brand Compliance Studio")

st.write(
    "Generate marketing campaigns using AI and your brand guidelines."
)

st.divider()
st.header("Campaign Details")

with st.form("campaign_form"):

    product = st.text_input(
        "Product Name",
        placeholder="Example: Eco-friendly water bottle"
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="Example: College students"
    )

    platform = st.selectbox(
        "Social Media Platform",
        ["Instagram", "LinkedIn", "Facebook"]
    )

    tone = st.selectbox(
        "Campaign Tone",
        ["Friendly", "Professional", "Energetic"]
    )

    goal = st.text_area("Campaign Objective")

    brand_guide = st.file_uploader(
        "Upload Brand Guide",
        type=["pdf", "txt"]
    )

    submitted = st.form_submit_button("Generate Campaign")

if submitted:

    if not product.strip() or not audience.strip():
        st.warning("Enter the product and target audience.")

    else:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            st.error("API key not found. Check your .env file.")

        else:
            try:
                client = genai.Client(api_key=api_key)

                brand_rules = []

                if brand_guide is not None:
                    with st.spinner("Reading brand guide..."):
                        summary = process_brand_guide(brand_guide)

                    st.success(
                        f"Brand guide processed: "
                        f"{summary['stored_chunks']} chunks stored."
                    )

                    question = f"""
                    Find brand rules relevant to this campaign.
                    Product: {product}
                    Audience: {audience}
                    Platform: {platform}
                    Tone: {tone}
                    Objective: {goal}

                    Focus on tone, keywords, prohibited phrases,
                    claims and visual guidelines.
                    """

                    brand_rules = retrieve_brand_rules(
                        question,
                        top_k=5
                    )

                else:
                    st.warning(
                        "No brand guide uploaded. "
                        "Campaign will be generated without retrieved brand rules."
                    )

                rules_text = (
                    "\n".join(f"- {rule}" for rule in brand_rules)
                    if brand_rules
                    else "No brand rules were retrieved."
                )

                prompt = f"""
You are an AI marketing campaign assistant.

CAMPAIGN DETAILS
Product: {product}
Target audience: {audience}
Platform: {platform}
Tone: {tone}
Objective: {goal}

RETRIEVED BRAND GUIDELINES
{rules_text}

INSTRUCTIONS
1. Generate a campaign title and idea.
2. Generate three different social media captions.
3. Provide a catchy headline.
4. Suggest relevant hashtags.
5. Provide a call-to-action.
6. Create an image-generation prompt.
7. Follow the retrieved brand rules where applicable.
8. Do not invent product facts or unsupported claims.
9. If rules conflict or are unclear, flag the issue instead
   of claiming full compliance.
10. Do not claim that compliance has been verified.

Clearly label each section.
"""

                with st.spinner("Gemini is generating your campaign..."):
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                if response.text:
                    st.success("Campaign generated successfully!")

                    if brand_rules:
                        with st.expander("Retrieved Brand Rules"):
                            for rule in brand_rules:
                                st.write("- ", rule)

                    st.subheader("Your AI-Generated Campaign")
                    st.markdown(response.text)

                    
                    # Run basic brand compliance checks
                    findings = check_compliance(response.text)

                    st.divider()
                    st.subheader("Brand Compliance Check")

                    high_issues = [
                        item for item in findings
                        if item["severity"] == "High"
                    ]

                    warnings = [
                        item for item in findings
                        if item["severity"] in ["Warning", "Review"]
                    ]

                    if high_issues:
                        st.error(
                            f"{len(high_issues)} high-severity "
                            "issue(s) detected."
                        )

                    elif warnings:
                        st.warning(
                            f"{len(warnings)} warning/review "
                            "item(s) detected."
                        )

                    else:
                        st.success(
                            "No issues detected by the basic checks."
                        )

                    for item in findings:
                        st.write(
                            f"**{item['severity']} — {item['type']}**"
                        )
                        st.write(item["message"])


                    st.download_button(
                        "Download Campaign Text",
                        data=response.text,
                        file_name="marketing_campaign.txt",
                        mime="text/plain"
                    )

                else:
                    st.warning("Gemini returned an empty response.")

            except Exception as error:
                st.error("Campaign generation failed.")
                st.code(str(error))
