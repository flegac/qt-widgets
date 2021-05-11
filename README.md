# qt-widgets

Reusable Qt widgets library.

## Browser Widget

Automatic layout for similar objects.

![](docs/img/browser.jpg)

```python
model: List[str] = [f'data {_}' for _ in range(10_000)]

browser = BrowserWidget(
    config=BrowserConfig(
        item=Item(
            # width=200,
        ),
        page=Page(
            index=4,
            size=25
        ),
    ),
    builder=lambda item: QPushButton(item),
    model=model,
)
```

# Gallery Widget

Based on Browser Widget with auto-resize behavior.

![](docs/img/gallery.jpg)

```python
def builder(path: str):
    def reader() -> numpy.ndarray:
        return cv2.imread(path)

    return reader


widget = GalleryWidget(
    images=[
        builder('image1.jpg'),
        builder('image2.jpg')
    ],
    config=BrowserConfig(
        page=Page(size=20)
    )
)
```

# Install

```
pip install qt-widgets
```

## Requirements

PyQt5

```
pip install pyqt5
pip install pyqt5-tools
```

## Usage

Run any script from the [test folder](tests).
