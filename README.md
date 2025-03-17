# DFD Generator with Streamlit

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-oj2v73jhrsg.streamlit.app/)

This Streamlit app allows users to generate Data Flow Diagrams (DFD) from textual descriptions using the [`data-flow-diagram`](https://github.com/pbauermeister/dfd) command-line tool.

## Features
- Enter DFD text manually in a text area.
- Generate a DFD diagram in various formats (`svg`, `png`, `pdf`, `jpg`).
- Use `Cmd+Enter` or `Ctrl+Enter` to generate the DFD automatically.
- Copy the generated diagram URL to share with others.
- Supports URL parameters for preloading DFD text.

## Installation

Ensure you have `streamlit` installed:

```sh
pip install streamlit
```

Install `data-flow-diagram` following the instructions from [its repository](https://github.com/pbauermeister/dfd).

```sh
pip install git+https://github.com/pbauermeister/dfd.git
```

### Additional Dependencies

If you are using Debian-based systems, install the following dependencies:

```sh
apt install graphviz fonts-ipaexfont
```


## Running the App

To start the Streamlit app, run:

```sh
streamlit run streamlit_app.py
```

## Usage

1. **Enter DFD text**: Write your DFD structure in the text area.
2. **Choose output format**: Select `svg`, `png`, `pdf`, or `jpg`.
3. **Generate DFD**:
   - Press **Cmd+Enter** (Mac) or **Ctrl+Enter** (Windows/Linux) to generate the diagram.
   - Alternatively, click the **Generate DFD** button.
4. **View Output**:
   - The generated diagram appears below the button.
   - If `pdf` format is selected, a download button is available.
5. **Copy URL**: The URL containing the encoded DFD text is generated automatically and copied to the clipboard.

## DFD Syntax Reference

For details on the DFD syntax, refer to the [DFD Syntax Documentation](https://github.com/pbauermeister/dfd/blob/main/doc/README.md).

## URL Parameter Support

You can pre-load DFD text using a URL parameter:

```
https://your-app-url/?text=encoded_dfd_text
```

Replace `encoded_dfd_text` with your DFD text URL-encoded.

## Example DFD Input

```
process Process1
process Process2
Process1 -> Process2 Data Transfer
```

## Troubleshooting

- Ensure `data-flow-diagram` is installed and accessible from the command line.
- Check the environment variable `BASE_URL` if the generated URL is incorrect.

## License

This project is licensed under the MIT License.
