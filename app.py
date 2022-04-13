from chalice import Chalice
from chalicelib.handlers.batch import batch

app = Chalice(app_name='aws-batch-with-chalice')


app.register_blueprint(batch)
