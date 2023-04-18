# 🚀 Rossmann Sales ML  Model Building and Deployment

# **Description**

![rossman end to end ML.png](%F0%9F%9A%80%20Rossmann%20Sales%20ML%20Model%20Building%20and%20Deployment%209dc2377669ea4afb9903207b7c99a68a/rossman_end_to_end_ML.png)

This is an end-to-end machine learning project which makes use of Rossmann Sales dataset to predict sales. The project is composed of 3 tasks: **Model Building**, **Flask API Creation**, **CI/CD Model Deployment Pipeline**.

---

# Model Building

Random Forest Regressor was used for the model.  Its ability to construct multiple decision trees makes it a good model that can handle large amounts of data, as well as the volatility of the data. Since it is trained on a random subset and features of the training data, the algorithm can still efficiently and accurately make predictions.

## Data Exploration

Two datasets were given: Train and Store. However, according to our sales prediction problem, the input values are `Store, DayOfWeek, Date, Customers, Open, Promo, StateHoliday, SchoolHoliday, and Sales`. As such, we’ll only consider **Train** dataset.

## Feature Engineering

- Split `Date` column to `Year, Month, Day`
- Converted `StateHoliday` values to int counterpart

## Train-Test Split

The dataset was split into 80-20 for training and testing sets.

## Hyperparameter Tuning

A Grid Search was used to optimize the hyperparameters of the decision tree regressor model. A range of values was specified for each hyperparameter, and used grid search to evaluate all possible combinations of hyperparameters within that range. A total of three grid searches were generated. However, since setting `max_depth` to `None` yielded a heavy model, only the two grid searches were considered:

```python
grid_space_1 = {
	'max_depth':[3,7,10],
	'n_estimators':[5,10,20],
	'max_features':[1,5,7],
	'min_samples_leaf':[1,2,3],
	'min_samples_split':[1,2,3]
}
```

```python
grid_space_2 = {
	'max_depth':[10],
	'n_estimators':[20,50,100],
	'max_features':[7,8],
	'min_samples_leaf':[2],
	'min_samples_split':[3,4]
}
```

There were 243 and 12 tests generated, respectively.

## Final Model

The model with the following hyperparameters yielded the best score of **`89.48` (R^2)**:

- '**max_depth**': 10
- '**max_features**': 8
- '**min_samples_leaf**': 2
- '**min_samples_split**': 4
- '**n_estimators**': 50

**Model Metrics:**

- **Mean Squared Error**: 1554189.193997423
- **Mean Absolute Error**: 836.4053360465724
- **R^2**: 0.894732420470625

---

# Flask API Creation

A Flask API was developed to serve the machine learning model.

## Endpoints

The model API can be accessed through the endpoint */predict* which calls a POST request.

```bash
POST: http://localhost:5000/predict
```

A health check endpoint */health* can also be accessed.

```bash
GET: http://localhost:5000/health
```

This will simply print `“Welcome to Rossmann Sales API!”`

## Parameters

The API accepts eight parameters: **Store**, **DayOfWeek**, **Date**, **Customers**, **Open**, **Promo**, **StateHoliday**, **SchoolHoliday** in JSON format, and outputs a JSON object that contains the **Sales** prediction in data type float.

| Parameter | Type | Sample | Limit |
| --- | --- | --- | --- |
| Store | int | 1111 |  |
| DayOfWeek | int | 4 |  |
| Date | str | “2014-07-10” |  |
| Customers | int | 4100 |  |
| Open | int | 1 | only accepts 1 |
| Promo | int | 1 |  |
| StateHoliday | str | “a” | string = “a” “b” “c” “0”; int = 0 |
| SchoolHoliday | int | 1 |  |

> 💡 The API only accepts **Open** with value of **1** since closed stores from refurbishment will have no sales. 💡
>

> 💡 The API only accepts **StateHoliday** values of string “a”, “b”, “c”,”0” and int 0. 💡
>

### Sample Request and Response 1:

Here is a sample input and output request in JSON format:

```json

{
    "Store":1111,
    "DayOfWeek":4,
    "Date":"2014-07-10",
    "Customers":4100,
    "Open":1,
    "Promo":1,
    "StateHoliday":"a",
    "SchoolHoliday":1
}
```

will output:

```python
{
    "sales": 25565.772841401882
}
```

### Sample Request and Response 2 (closed store):

```python
{
    "Store":1111,
    "DayOfWeek":4,
    "Date":"2014-07-10",
    "Customers":4100,
    "Open":0,
    "Promo":0,
    "StateHoliday":"0",
    "SchoolHoliday":1
}
```

```python
{
    "error": "ERROR: Store should be open.",
    "status": 400
}
```

### Sample Request and Response 3 (invalid StateHoliday):

```python
{
    "Store":1111,
    "DayOfWeek":4,
    "Date":"2014-07-10",
    "Customers":4100,
    "Open":1,
    "Promo":0,
    "StateHoliday":"z",
    "SchoolHoliday":1
}
```

```python
{
    "error": "ERROR: State Holiday unknown.",
    "status": 400
}
```

## Running the API Locally

Before running the API, create a virtual environment and install the dependencies in the **requirements.txt** file in the root folder.

```python
$ virtualenv API
$ source API/bin/activate
(API)$ pip3 install -r path/to/requirements.txt
```

Run the python file **app.py** in the root folder using the virtual environment:

```python
(API)$ python3 app.py
```

---

# **CI/CD Model Deployment Pipeline**

![ci:cd pipeline.png](%F0%9F%9A%80%20Rossmann%20Sales%20ML%20Model%20Building%20and%20Deployment%209dc2377669ea4afb9903207b7c99a68a/cicd_pipeline.png)

The CI/CD Model Deployment pipeline is made from Github Actions Workflow yaml files. It contains the **Linter**, **Unit Testing**, **Deployment to Heroku**, **Integration Testing.**

## Containerization using Dockerfile and Heroku

The **[Dockerfile](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/Dockerfile)** specifies the necessary dependencies and commands for running the application. This is used to build the application container that will be deployed to Heroku. A **[heroku.yaml](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/heroku.yaml)** and **[Procfile](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/Procfile)** is also needed for the deployment.

See code for more details

## Github Actions

There are two workflows in the project: `Lint` and `Deploy to Heroku`

- `Lint` checks the code on all push and pull requests to `all branches` to ensure code quality.
- `Deploy to Heroku` is triggered when a push is made into the `Master` branch. It contains the following:
    - built-in linter as well
    - unit test script
    - deployment proper
    - integration test script
    - load test script

### Linter

Runs the pre-commit hook to check for linting issues.

[See code for more details](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/.github/workflows/lint_all_branches.yaml)

### Unit Testing

Runs the [unit testing script](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/unit_test.py) to check if application will accept the input format, will output the correct format, and will send out a success response. Uses `unittest` library.

[See code for more details.](https://github.com/meredithjas/Rossmann-Sales-API/blob/88a2208fece97e0bb087cb8619ba139e985d784d/.github/workflows/deploy_and_test.yaml#L26-L43)

### Deployment to Heroku

Deploys the docker container to heroku. Makes use of [gonuit/heroku-docker-deploy@v1.3.3](https://github.com/marketplace/actions/build-push-and-release-a-docker-container-to-heroku?version=v1.3.3) from Github Marketplace.

[See code for more details](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/.github/workflows/deploy_and_test.yaml#L45-L67)

### Integrated Testing

After deployment, this runs the [integrated testing script](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/test/integration_test.py) from `test` folder to ensure that the deployed model in heroku is working as expected for production use.

[See code for more details](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/.github/workflows/deploy_and_test.yaml#L69-L90)

### Load Testing

Runs the [load testing script](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/test/load_test.py) from `test` folder using [Locust](https://docs.locust.io/en/stable/index.html) to ensure that the API can handle a certain amount of load — simulating a large number of concurrent users that will be using the API in production. A pre-made [configuration file](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/test/configuration.conf) is made with the following details:

- users = 20
- spawn-rate = 20
- run-time = 3m

This will output response time, request rate, user count, error rate, exceptions.

![load test result.png](%F0%9F%9A%80%20Rossmann%20Sales%20ML%20Model%20Building%20and%20Deployment%209dc2377669ea4afb9903207b7c99a68a/load_test_result.png)

[See the code for more details](https://github.com/meredithjas/Rossmann-Sales-API/blob/master/.github/workflows/deploy_and_test.yaml#L92-L115)
