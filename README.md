# Project Title

Sydney House Price Predictor

## Description

This project is a basic API interface that uses a multivariable regression model, which takes in internal and external features of a house (some of which made using an external API), to make a prediction on it's value. The types of user inputted features include number of bedrooms, bathrooms, garage spaces, the suburb and the suburbs median income. The other features are created using external API's and processing. The purpose of this model is to grant individuals with the ability to securely recieve a general guide for a house's value, without having to go through hurdles such as deceptive real-estate agents or signing up to realestate websites that force users to provide sensitive information.

## Getting Started

### Dependencies

- The libraries required to run are listed in the required are listed in requirements.txt so are automatically installed when opening a code environment
- OS Requirements: Windows 10+, MacOS Sierra

### IMPORTANT INFO WHEN NAVIGATING THE NOTEBOOKS

- LR = Linear Regression
- MV = Multivariable Regression
- PR = Polynomial Regression
- A = House Model
- B = Apartment Model

Some notebooks and datasets have \_1 or \_2 infront of them, the larger the number the later the version it is (So choose the later notebook or csv versions if required)

### Executing program

- Navigate to the operations directory

```bash
  cd operations
```

- Now navigate to the API_deployment directory

```bash
  cd API_Deployment
```

- Now run the API

```
  python api.py
```

- Then run the main python file

```
  python main.py
```

## Help

Any advise for common problems or issues.

```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Mr Jones
ex. [@benpaddlejones](https://github.com/benpaddlejones)

## Version History

- 0.6
  - Revisted deployment and fledged out API
- 0.5
  - Increased documentation from previous attempts
  - Initiated deployment
- 0.4
  - Completed model testing and deployment
  - Went back into feature engineering to improve scores
- 0.3
  - Completed Feature Engineering
  - Engineered 2 features based off pre-existing and one hot encoded types of house
- 0.2
  - Completed Data Wrangling
  - Removed 5 features
- 0.1
  - Initial Release

## License

This project is licensed under the [Harry Connors-Le] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.

- [Github md syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [TempeHS Jupyter-Notebook template](https://github.com/TempeHS/TempeHS_Jupyter-Notebook_DevContainer)
- [Kaggle Model Initial Implementation](https://www.kaggle.com/code/minmyomin/prediction-of-nsw-house-pricing)
- [Open Cage API documentation](https://opencagedata.com/api)
- [Haversine documentation](https://pypi.org/project/haversine/)
