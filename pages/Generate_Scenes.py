import streamlit as st
import openai
import os
import fitz
import base64
import json

openai.api_key = os.getenv("API_KEY")

# Define default values
default_xml_structure = """<Course>
            <Topics>
                <Topic>
                    <Topic_name></Topic_name>			
                    <Contents>
                    </Contents>
                    <sub_Topics>
                        <sub_Topic>
                            <sub_Topic_name></sub_Topic_name>
                            <sub_Topic_Contents>
                            </sub_Topic_Contents>
                        </sub_Topic>
                    </sub_Topics>
                </Topic>
            </Topics>
</Course>"""
default_xml_conversion_instructions =  """Only content with the following numbers should be tagged as follows
1.1 and same levels to Topic
1.1.1 and same levels to Sub-Topic
1.1-1 and same levels to Sub-Topic
For example, 1.5-2 would be a sub-topic 
Include the Level Numbers in the XML exactly as in the original content
Sub_topic_Contents should  not be empty or concise
"""

# Create expandable container for input fields
with st.expander("Input Configurations"):
    # Add input fields with default values
    xml_structure = st.text_area("XML Structure", default_xml_structure, height=430, )
    xml_conversion_instructions = st.text_area("XML Conversion Instructions", default_xml_conversion_instructions,height=280)

    # Save button to save input values to session state
    if st.button("Save"):
        st.session_state.xml_structure = xml_structure
        st.session_state.xml_conversion_instructions = xml_conversion_instructions

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    
    with st.expander("Pdf data"):
        # Add a multi-select field to get the page numbers from the user
        page_numbers = range(1, len(pdf_doc) + 1)
        
        # Extract text from the selected page numbers
        page_content = []
        for page_number in page_numbers:
            page = pdf_doc[page_number - 1] # page numbers are 0-indexed in PyMuPDF
            page_content.append(page.get_text())
        
        st.write(f"Number of pages extracted: {len(page_content)}")
        
    # Process pages using OpenAI API
    butn = st.button("Process")
    if butn:
        st.write("Processing pages...")
        
        # Set OpenAI API parameters
        model = "text-davinci-003"
        temperature = 0.56
        max_tokens = 1000
        top_p = 1
        frequency_penalty = 0.35
        presence_penalty = 0
        
        # Split pages into batches of size 5
        batch_size = 1
        batches = [page_content[i:i+batch_size] for i in range(0, len(page_content), batch_size)]
        
        # Process batches and save XML output to text files
        # file_links

                # Loop through batches and process pages using OpenAI API
        output_data = []
        for i, batch in enumerate(batches):
            st.write(f"Processing batch {i+1} of {len(batches)}...")
            # st.write(batch)
            # Combine pages in batch into a single input prompt
            input_prompt = "\n".join(batch)
            inputPrompt = " Convert the following pdf contents :" + input_prompt + " As it is with the Level Numbers into the following XML Structure : " + xml_structure + " while following these instructions : " + xml_conversion_instructions

            
            # Generate XML output using OpenAI API
            response = openai.Completion.create(
                model=model,
                prompt=inputPrompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            xml_output = response.choices[0].text
            # st.write(xml_output)
            
            # # Save XML output to text file
            # filename = f"output_batch_{i+1}.txt"
            # with open(filename, "w") as f:
            #     f.write(xml_output)
            
            # Store XML output and filename in output_data list
            output_data.append(xml_output)
            
        st.write("Done processing pages.")
        all_xml_output = "\n".join(output_data)
        filename = f"output.txt"
            with open(filename, "w") as f:
                f.write(all_xml_output)
        
        # Generate download links for text files
        st.write("Download XML output:")
        # for xml_output, filename in output_data:
        b64 = base64.b64encode(all_xml_output.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">{filename}</a>'
        st.markdown(href, unsafe_allow_html=True)
