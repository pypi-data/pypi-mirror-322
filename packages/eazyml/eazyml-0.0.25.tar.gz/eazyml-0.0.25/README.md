## Eazyml Modeling
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)  ![PyPI package](https://img.shields.io/badge/pypi%20package-0.0.22-brightgreen) ![Code Style](https://img.shields.io/badge/code%20style-black-black)

![EazyML](https://eazyml.com/static/media/EazyML%20XAI%20blue.b7696b7a.png)

This API allows you to initialize machine learning model parameters. It provides the user with various options on model building such as type of the model, dependency removal, derivation from numeric or text predictors derivations and many more.

### Features
- Build model and predict on test data for given model.
- Provides utils function which can be used to beautify dataframe, dict or markdown format data.

## Installation
### User installation
The easiest way to install eazyml modeling is using pip:
```bash
pip install -U eazyml
```
### Dependencies
Eazyml Augmented Intelligence requires :
- werkzeug,
- unidecode,
- pandas,
- scikit-learn,
- nltk,
- pyyaml,
- requests

## Usage
Initialize and build a predictive model based on the provided dataset and options. 
Perform prediction on the given test data based on model options.

```python
from eazyml_augi import ez_init, ez_augi
# Replace 'your_license_key' with your actual EazyML license key
ez_init(license_key="your_license_key")

ez_init_model(
            df='train_dataframe'
            options={
                "model_type": "predictive",
                "accelerate": "yes",
                "outcome": "target",
                "remove_dependent": "no",
                "derive_numeric": "yes",
                "derive_text": "no",
                "phrases": {"*": []},
                "text_types": {"*": ["sentiments"]},
                "expressions": []
            }
    )
ez_predict(
            test_data ='test_dataframe'
            options={
                "extra_info": {
                },
                "model": "Specified model to be used for prediction",
                "outcome": "target",
            }
    )

```
You can find more information in the [documentation](https://eazyml.readthedocs.io/en/latest/packages/eazyml_model.html).


## Useful Links
- [Documentation](https://docs.eazyml.com)
- [Homepage](https://eazyml.com)
- If you have more questions or want to discuss a specific use case please book an appointment [here](https://eazyml.com/trust-in-ai)

## License
This project is licensed under the [Proprietary License](https://github.com/EazyML/eazyml-docs/blob/master/LICENSE).

---

*Maintained by [EazyML](https://eazyml.com)*  
*© 2025 EazyML. All rights reserved.*

