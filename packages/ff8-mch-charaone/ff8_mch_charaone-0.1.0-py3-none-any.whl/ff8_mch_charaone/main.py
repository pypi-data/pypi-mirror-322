from .parse.headers.__parser import HeaderParser
from .parse.model.__parser import ModelParser

from .format.formatted_model import FormattedModel

from .export.exporter import Exporter

def main():
  with open("./INPUT/chara.one", "rb") as f:
    file_data = f.read()

  model_headers = HeaderParser(file_data)
  print(f"Found {model_headers.model_count} models")

  for model_header in model_headers.model_headers:
    print(f"Processing model {model_header.model_name}")
    model = ModelParser(header=model_header, data=file_data)
    print(f"Model {model.header.model_name} parsed successfully")

    formatted_model = FormattedModel(model=model)
    print(formatted_model)
    exporter = Exporter(
      name=model_header.model_name,
      model=formatted_model
    )
    exporter.export_as_obj(filepath=f"./OUTPUT/{formatted_model.name}.obj")

if __name__ == "__main__":
    main()