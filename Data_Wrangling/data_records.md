# Data Records

When the ML model goes into opperation it will be provided with **new** data to make predictions. The **new** data will need to be scaled or encoded by your app or API before predictions can be made. To help design this process this is a record for any scaling/encoding applied during data wrangling and feature engineering or the approach taken to engineering new features or feature interactions.

## Scalled Data

| Data   | Min/Max | Scale Min/Max |
| ------ | ------- | ------------- |
| sqm    | 7/59100 | 40/1270       |
| km_CBD | 0.3/85  | 0.3/82        |

## Encoded Data

| Data | Unencoded       | Encoded |
| ---- | --------------- | ------- |
| Type | House/apartment | -1/1    |

## Engineered Features

| Data      | Engineering                                                                         |
| --------- | ----------------------------------------------------------------------------------- |
| tot_rooms | `data_frame['tot_rooms'] = data_frame['num_bed'] + data_frame['num_bath']`          |
| prop_cbd  | `data_frame['prop_cbd'] = (data_frame['property_size'] * data_frame['km_from_cbd']` |
