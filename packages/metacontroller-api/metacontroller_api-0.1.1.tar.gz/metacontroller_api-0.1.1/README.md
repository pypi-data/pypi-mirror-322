# python-metacontroller-api

[Metacontroller]: https://github.com/metacontroller/metacontroller/

API for implementing Kubernetes controllers via [Metacontroller].

## Example

```python
from metacontroller_api import DecoratorController, DecoratorSyncRequest, DecoratorSyncResponse, Factories
from metacontroller_api.contrib.flask import MetacontrollerBlueprint
from flask import Flask

class MyController(DecoratorController):

    def sync(self, request: DecoratorSyncRequest) -> DecoratorSyncResponse:
        # ...
        return {
            "labels": {},
            "annotations": {},
            "status": {},
            "attachments": [
                # ...
            ],
            "resyncAfterSeconds": 0,
        }

app = Flask(__name__)
app.register_blueprint(MetacontrollerBlueprint(MyController()))
app.run()
```
