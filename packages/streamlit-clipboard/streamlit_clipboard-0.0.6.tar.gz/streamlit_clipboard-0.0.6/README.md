# streamlit-clipboard

Streamlit component that support copy and paste clipboard

## Installation instructions

```sh
pip install streamlit-clipboard
```

## Usage instructions

```python
import streamlit as st
from clipboard_component import copy_component, paste_component

st.subheader("文本内容复制到剪贴板示例")
user_input = st.text_area(
    "输入要复制的内容:",
    value="在这里输入文本，然后点击下方按钮复制到剪贴板",
    height=200
)
copy_component("复制按钮", content=user_input)

st.subheader("剪贴板读取组件")
clipboard_content = paste_component("读取剪贴板")
if clipboard_content:
    st.markdown("### 当前剪贴板内容:")
    st.code(clipboard_content)
else:
    st.markdown("点击按钮读取剪贴板内容")
```