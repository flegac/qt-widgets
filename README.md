# qt-widgets

Reusable library of Qt Widgets.

# Flow Widget

Automatic layout for similar objects.

![](docs/img/flow.jpg)

```python
model: List[str] = [f'data {_}' for _ in range(10_000)]

flow = FlowWidget(
    config=FlowConfig(
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
