<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DevByEagle/pygdk/master/logo/pygdk_logo_dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DevByEagle/pygdk/master/logo/pygdk_logo_light.png">
    <img src="https://raw.githubusercontent.com/DevByEagle/pygdk/master/logo/pygdk_logo_light.png">
  </picture>
</p>

**Pygdk** is a lightweight Python library for building modern, interactive graphical user interfaces with simplicity and flexibility.

## Installation

Pygdk is available via `pip`. To install the latest version of Pygdk, simply run:

```bash
pip install pygdk
```

Once installed, you can import the library into your Python scripts to start creating your GUI applications.

## Basic Example

Here’s a simple example that demonstrates how to create a window and text:

```python
import pygdk as gdk

app = gdk.Gk() # Create a Gk window in the same way you create a Tk window.
app.title("Simple Example")
app.geometry("800x600")

label = gdk.GkLabel(app, text="Hello, World")
label.pack()

app.mainloop()
```
