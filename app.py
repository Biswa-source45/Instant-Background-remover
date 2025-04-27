import streamlit as st
from rembg import remove
from PIL import Image
import io
import traceback
import time
import psutil


# Streamlit app configuration
st.set_page_config(page_title="Image Background Remover", page_icon="🖼️", layout="centered")

# Custom CSS for styling and responsiveness
st.markdown("""
    <style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    /* App background gradient */
    .main {
        background: linear-gradient(135deg, #e0e7ff, #f3e8ff);
        padding: 20px;
    }
    /* Center images and buttons */
    .stImage, .stDownloadButton, .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
    }
    /* Ensure images are centered with fixed width on desktop */
    .stImage img {
        width: 400px;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: opacity 0.3s ease-in-out;
        position: relative;
    }
    /* Add gradient overlay to images */
    .stImage img::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(to bottom, rgba(255, 255, 255, 0.1), rgba(0, 0, 0, 0.05));
        pointer-events: none;
    }
    /* Style file uploader with subtle border */
    .stFileUploader {
        border: 1px solid #4facfe;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        transition: border-color 0.2s;
    }
    .stFileUploader:hover {
        border-color: #00f2fe;
    }
    /* Style buttons */
    .stDownloadButton button, .stButton button {
        width: 400px;
        font-size: 16px;
        background: linear-gradient(to right, #4facfe, #00f2fe);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        transition: background 0.2s, color 0.2s;
    }
    .stDownloadButton button:hover, .stButton button:hover {
        background: #ffffff;
        color: #4facfe;
    }
    /* Style selectbox, slider, and text input for touch */
    .stSelectbox, .stSlider, .stTextInput {
        padding: 5px;
    }
    /* Responsive styles for mobile and tablets */
    @media (max-width: 768px) {
        .stImage img {
            width: 100% !important;
            max-width: 100%;
            height: auto;
        }
        .stDownloadButton button, .stButton button {
            width: 100%;
            max-width: 300px;
            font-size: 14px;
            padding: 12px;
        }
        .stMarkdown h1 {
            font-size: 1.8em !important;
        }
        .stSelectbox, .stSlider, .stTextInput {
            padding: 10px;
        }
        .stMarkdown.stText {
            font-size: 0.9em;
        }
    }
    /* Ultra-narrow screens */
    @media (max-width: 400px) {
        .stMarkdown, .stText, .stError, .stSuccess {
            font-size: 0.9em;
        }
        .stDownloadButton button, .stButton button {
            font-size: 12px;
            padding: 10px;
        }
    }
    /* Ensure text is readable */
    .stMarkdown, .stText, .stError, .stSuccess {
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    /* Add spacing between elements */
    .stImage, .stDownloadButton, .stButton, .stSelectbox, .stSlider, .stTextInput, .stProgress {
        margin-bottom: 20px;
    }
    /* Style expander */
    .stExpander {
        border: 1px solid transparent;
        
        border-radius: 20px;
        margin-bottom: 20px;
    }
    /* Style progress bar */
    .stProgress > div > div {
        background: linear-gradient(to right, #4facfe, #00f2fe);
        transition: width 0.3s ease-in-out;
    }
    /* Style success message */
    .stSuccess::before {
        content: '✅ ';
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for caching
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "input_image" not in st.session_state:
    st.session_state.input_image = None
if "resized_image" not in st.session_state:
    st.session_state.resized_image = None
if "cancel_processing" not in st.session_state:
    st.session_state.cancel_processing = False

# Title with gradient
st.markdown("""
    <h1 style='background: linear-gradient(to right, #4facfe, #00f2fe); -webkit-background-clip: text; color: transparent; font-size: 3.0em; text-align: center;'>
        Image Background Remover
    </h1>
""", unsafe_allow_html=True)
st.markdown("Upload a JPG, JPEG, or PNG image and click 'Remove Background' to process. Download the result as a PNG.", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"],
    help="Upload a JPG, JPEG, or PNG image",
    key="uploader"
)

# Placeholder message
if uploaded_file is None:
    st.markdown("Please upload an image to get started.", unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Read the uploaded image
        input_image = Image.open(uploaded_file).convert("RGB")
        st.session_state.input_image = input_image

        # Resize image for processing if large
        if max(input_image.size) > 1000:
            scale = 1000 / max(input_image.size)
            new_size = (int(input_image.size[0] * scale), int(input_image.size[1] * scale))
            resized_image = input_image.resize(new_size, Image.Resampling.LANCZOS)
            st.session_state.resized_image = resized_image
        else:
            st.session_state.resized_image = input_image

        # Display original image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(st.session_state.input_image, caption="Original Image", width=400, use_container_width="auto", output_format="PNG")

        # Remove Background button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Remove Background", key="remove_bg", help="Start background removal"):
                st.session_state.cancel_processing = False
                # Check available memory
                available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
                if available_memory < 500:
                    st.warning("Low system memory detected. Processing large images may fail.")

                # Process image
                try:
                    start_time = time.time()
                    progress_bar = st.progress(0)
                    with st.spinner("Removing background..."):
                        output_image = remove(st.session_state.resized_image)
                        # Simulate progress based on estimated time
                        elapsed = time.time() - start_time
                        estimated_total = min(30, max(5, input_image.size[0] * input_image.size[1] / 1e6))  # Rough estimate
                        for i in range(100):
                            if st.session_state.cancel_processing:
                                st.warning("Background removal cancelled.")
                                progress_bar.empty()
                                raise InterruptedError("Processing cancelled by user")
                            time.sleep(0.01)
                            progress_bar.progress(min(i + 1, int((elapsed / estimated_total) * 100)))
                        if time.time() - start_time > 30:  # 30-second timeout
                            raise TimeoutError("Background removal took too long. Try a smaller image.")
                        st.session_state.processed_image = output_image
                    progress_bar.empty()
                    st.success(f"Background removed successfully!")
                except (RuntimeError, TimeoutError, InterruptedError) as e:
                    if not st.session_state.cancel_processing:
                        st.error("Error during processing. Try a smaller image or lower resolution.")
                        st.error(f"Error details: {str(e)}")
                    raise e


        # Display processed image and output settings if processed
        if st.session_state.processed_image is not None:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(st.session_state.processed_image, caption="Image with Background Removed", width=400, use_container_width="auto", output_format="PNG")

            # Output settings in an expander
            with st.spinner("Applying output settings..."):
                with st.expander("Output Settings", expanded=True):
                    # Background fill option
                    bg_option = st.selectbox(
                        "Background Fill:",
                        ("Transparent", "White"),
                        help="Choose the background for the output image.",
                        key="bg_option"
                    )

                    # Output size scaling
                    scale_percent = st.slider(
                        "Output Size (%):",
                        10, 100, 100, step=10,
                        help="Scale the output image size (100% = original size).",
                        key="scale"
                    )

                    # Quality slider
                    quality = st.slider(
                        "Output Quality:",
                        10, 100, 95, step=5,
                        help="Higher quality increases file size.",
                        key="quality"
                    )

                    # Custom filename
                    default_filename = "background_removed.png"
                    filename = st.text_input(
                        "Download Filename:",
                        value=default_filename,
                        help="Enter a filename for the downloaded image (include .png extension)",
                        key="filename"
                    )
                    if not filename.lower().endswith(".png"):
                        filename = filename + ".png"

            # Prepare output image with scaling
            output_image = st.session_state.processed_image
            if scale_percent != 100:
                scale_factor = scale_percent / 100
                new_size = (int(output_image.size[0] * scale_factor), int(output_image.size[1] * scale_factor))
                output_image = output_image.resize(new_size, Image.Resampling.LANCZOS)

            # Estimate output file size and dimensions
            buf = io.BytesIO()
            if bg_option == "White":
                white_bg = Image.new("RGBA", output_image.size, (255, 255, 255, 255))
                white_bg.paste(output_image, (0, 0), output_image)
                white_bg.save(buf, format="PNG", quality=quality)
            else:
                output_image.save(buf, format="PNG", quality=quality)
            byte_im = buf.getvalue()
            file_size_kb = len(byte_im) / 1024
            st.markdown(
                f"Output dimensions: {output_image.size[0]}x{output_image.size[1]}px | Estimated file size: {file_size_kb:.2f} KB",
                unsafe_allow_html=True
            )

            # Center the download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Image",
                    data=byte_im,
                    file_name=filename,
                    mime="image/png",
                    help="Download the processed image as a PNG",
                    key="download"
                )

            # Clean up memory
            buf.close()
            if st.session_state.resized_image is not input_image:
                st.session_state.resized_image = None

    except Exception as e:
        if not st.session_state.cancel_processing:
            st.error("An error occurred while processing the image.")
            st.error(f"Error details: {str(e)}")
            st.markdown("Please ensure the image is valid and try again.", unsafe_allow_html=True)
        traceback.print_exc()

# Footer
st.markdown("---")
st.markdown("© 2025 Image Background Remover. All rights reserved. Powered by Streamlit and rembg. Developed by Biswabhusan Sahoo", unsafe_allow_html=True)