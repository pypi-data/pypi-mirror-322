# VIPAS AI Platform SDK
The Vipas AI Python SDK provides a simple and intuitive interface to interact with the Vipas AI platform. This SDK allows you to easily make predictions using pre-trained models hosted on the Vipas AI platform.

## Table of Contents

- [VIPAS AI Platform SDK](#vipas-ai-platform-sdk)
  - [Requirements](#requirements)
  - [Installation & Usage](#installation--usage)
    - [pip install](#pip-install)
  - [Prerequisites](#prerequisites)
    - [Step 1: Fetching the Auth Token](#step-1-fetching-the-auth-token)
    - [Step 2: Setting the Auth Token as an Environment Variable](#step-2-setting-the-auth-token-as-an-environment-variable)
  - [Getting Started](#getting-started)
    - [Basic Usage](#basic-usage)
    - [Handling Exceptions](#handling-exceptions)
  - [Asynchronous Inference Mode](#asynchronous-inference-mode)
    - [Asynchronous Inference Mode Example](#asynchronous-inference-mode-example)
  - [Real-Time Inference Mode](#real-time-inference-mode)
    - [Real-Time Inference Mode Example](#real-time-inference-mode-example)
  - [Creating Model on Vipas.AI Platform](#create-model-on-vipas.ai-platform)
  - [Generating MLflow Configuration Files](#generate-mlflow-configuration-files)
  - [Publishing Model](#publishing-model)
    - [Publishing Process Overview](#publishing-process-overview)
  - [Retrieving Model Deployment Logs with the Vipas.AI SDK](#retrieving-model-deployment-logs-with-the-vipas.AI-SDK)
  - [Evaluating a Model against a Challenge](#evaluating-a-model-against-a-challenge)
  - [Listing the submissions of a Challenge](#listing-the-submissions-of-a-challenge)
  - [Logging](#logging)
    - [LoggerClient Usage](#loggerclient-usage)
    - [Example of LoggerClient](#example-of-loggerclient)
  - [License](#license)

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

You can install vipas sdk from the pip repository, using the following command:

```sh
pip install vipas
```
(you may need to run `pip` with root permission: `sudo pip install vipas`)

Then import the package:
```python
import vipas
```
## Prerequisites
Before using the Vipas.AI SDK to manage and publish models, you need to fetch your VPS Auth Token from the Vipas.AI platform and configure it as an environment variable.

#### Step 1: Fetching the Auth Token:-
This section explains how to fetch the VPS Auth Token required to authenticate your SDK requests. You can use one of two methods to obtain the token.

##### Method 1: Using the Vipas.AI Platform

1. **Login to Vipas.AI**:  
   Visit the [Vipas.AI platform](https://vipas.ai/) and log in to your account.

2. **Access Settings**:  
   Click on your user profile icon in the top-right corner and navigate to the **Settings** page.

3. **Generate the Token**:  
   Locate the **Temporary Access Token** section, enter your password, and click the button to generate a new token.

4. **Copy the Token**:  
   Copy the generated token, as you will need it to configure the SDK.

---

##### Method 2: Using the `generate_token` SDK Function

---


The Vipas.AI SDK allows users to programmatically retrieve their authentication token using the `generate_token` function. This token is essential for authenticating SDK requests and ensuring secure access to the platform.

---

### Function Signature

```python
vipas.user.UserClient.generate_token(username: str, password: str) → Dict[str, Any]
```

---

### Parameters

- **`username` (str) [Required]**:  
  The registered username of your Vipas.AI account.  
  - **Constraints**: Required field, must be a valid username.

- **`password` (str) [Required]**:  
  The registered password of your Vipas.AI account.  
  - **Constraints**: Required field, must be a valid password.

---

### Return Value

The `generate_token` function returns a dictionary containing the generated token:
- **`vps_auth_token`**: The generated authentication token.

---

### Example Usage

Here’s how you can use the `generate_token` function to generate an authentication token:

```python
from vipas.user import UserClient
from vipas.exceptions import ClientException

try:
    # Define user credentials
    username = "your_username"
    password = "your_password"

    # Create a UserClient instance
    user_client = UserClient()

    # Generate the Auth Token
    auth_response = user_client.generate_token(username=username, password=password)

    # Extract and print the token
    auth_token = auth_response.get('vps_auth_token')
    print(f"Authentication Token: {auth_token}")

except ClientException as e:
    print(f"Error generating token: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

### Handling the Response

The response from the `generate_token` function is structured as follows:

```json
{
  "vps_auth_token": "<Your generated authentication token>"
}
```

This response provides the token that can be set as an environment variable as mentioned further steps,.

---

### Error Handling

The `generate_token` function raises exceptions for various error scenarios:

| Exception                                | Description                                                                            |
|------------------------------------------|----------------------------------------------------------------------------------------|
| **`vipas.exceptions.ClientException`**  | Raised when the provided username or password is incorrect.                            |
| **`vipas.exceptions.UnauthorizedException`** | Raised if the authentication request is unauthorized (e.g., invalid credentials).   |


---

By leveraging the `generate_token` function, users can efficiently authenticate their SDK requests and securely interact with the Vipas.AI platform.

#### Step 2: Setting the Auth Token as an Environment Variable:-
You need to set the VPS_AUTH_TOKEN as an environment variable to use it within your SDK.

##### For linux and macOS
1. Open a **Terminal**.
2. Run the following command to export the token:

    ```bash
    export VPS_AUTH_TOKEN=<TOKEN>
    ```
   Replace <TOKEN> with the actual token you copied from the Vipas.AI UI.
3. To make it persistent across sessions, add the following line to your **~/.bashrc, ~/.zshrc**, or the corresponding shell configuration file

    ```bash
    export VPS_AUTH_TOKEN=<TOKEN>
    ```
    Then use this command to source it to the current running 
    session
    ```bash
    source ~/.bashrc.
    ```
##### For Windows
1. Open **Command Prompt** or **PowerShell**.
2. Run the following command to set the token for the current session:
    ```powershell
    set VPS_AUTH_TOKEN=<TOKEN>
    ```
3. To set it permanently, follow these steps:
    1. Open the Start menu, search for **Environment Variables**, and open the **Edit the system environment variables** option.
    2. In the **System Properties** window, click on **Environment Variables**.
    3. Under **User variables**, click **New**.
    4. Set the **Variable name** to **VPS_AUTH_TOKEN** and the Variable value to <TOKEN>.
    5. Click **OK** to save.

Once you’ve set the environment variable, you can proceed with using the SDK, as it will automatically pick up the token from the environment for authentication.





## Getting Started

To get started with the Vipas AI Python SDK, you need to create a ModelClient object and use it to make predictions. Below is a step-by-step guide on how to do this.

### `vipas.model.ModelClient.predict(model_id: str, input_data: str, async_mode: bool = True) → dict`

Make a prediction using a deployed model.

#### Parameters:
- `model_id` (str) [Required]: The unique identifier of the model.
- `input_data` (Any) [Required]: The input data for the prediction, usually in string format (e.g., base64 encoded image or text data).
- `async_mode` (bool) [Optional]: Whether to perform the prediction asynchronously (default: True).

#### Returns:
- `dict`: A dictionary containing the result of the prediction process.

### Basic Usage

1. Import the necessary modules:
```python
from vipas import model
```

2. Create a ModelClient object:
```python
vps_model_client = model.ModelClient()
```

3. Make a prediction:

```python
model_id = "<MODEL_ID>"
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>")
```

### Handling Exceptions
The SDK provides specific exceptions to handle different error scenarios:

1. UnauthorizedException: Raised when the API key is invalid or missing.
2. NotFoundException: Raised when the model is not found.
3. BadRequestException: Raised when the input data is invalid.
4. ForbiddenException: Raised when the user does not have permission to access the model.
5. ConnectionException: Raised when there is a connection error.
6. RateLimitException: Raised when the rate limit is exceeded.
7. ClientException: Raised when there is a client error.

### Asynchronous Inference Mode
---
Asynchronous Inference Mode is a near-real-time inference option that queues incoming requests and processes them asynchronously. This mode is suitable when you need to handle `large payloads` as they arrive or run models with long inference processing times that do not require sub-second latency. `By default, the predict method operates in asynchronous mode`, which will poll the status endpoint until the result is ready. This is ideal for batch processing or tasks where immediate responses are not critical.


#### Asynchronous Inference Mode Example
```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=True)
```
### Real-Time Inference Mode
---
Real-Time Inference Mode is designed for use cases requiring real-time predictions. In this mode, the predict method processes the request immediately and returns the result without polling the status endpoint. This mode is ideal for applications that need quick, real-time responses and can afford to handle potential timeouts for long-running inferences. It is particularly suitable for interactive applications where users expect immediate feedback.

#### Real-Time Inference Mode Example
```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=False)
```

### Detailed Explanation
#### Asynchronous Inference Mode
---
##### Description:
This mode allows the system to handle requests by queuing them and processing them as resources become available. It is beneficial for scenarios where the inference task might take longer to process, and an immediate response is not necessary.

##### Behavior:
The system polls the status endpoint to check if the result is ready and returns the result once processing is complete.

##### Ideal For:
Batch processing, large payloads, long-running inference tasks.

##### Default Setting:
By default, async_mode is set to True to support heavier inference requests.

##### Example Usage:

```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=True)
```

#### Real-Time Inference Mode
---
##### Description:
This mode is intended for use cases that require immediate results. The system processes the request directly and returns the result without polling.

##### Behavior:
The request is processed immediately, and the result is returned. If the inference takes longer than 29 seconds, a 504 Gateway Timeout error is returned.

##### Ideal For:
Applications requiring sub-second latency, interactive applications needing immediate feedback.

##### Example Usage:

```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=False)
```

By understanding and choosing the appropriate mode for your use case, you can optimize the performance and responsiveness of your AI applications on Vipas.AI.


### Example Usage for ModelClient using asychronous inference mode

```python
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException
from vipas.logger import LoggerClient

logger = LoggerClient(__name__)

def main():
    # Create a ModelClient object
    vps_model_client = model.ModelClient()

    # Make a prediction
    try:
        model_id = "<MODEL_ID>"
        api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>")
        logger.info(f"Prediction response: {api_response}")
    except UnauthorizedException as err:
        logger.error(f"UnauthorizedException: {err}")
    except NotFoundException as err:
        logger.error(f"NotFoundException: {err}")
    except ClientException as err:
        logger.error(f"ClientException: {err}")

main()

```
# Creating Model on Vipas.AI Platform

The **Vipas.AI SDK** provides functionality to create new models on the platform, allowing users to define specific parameters and configurations. The `create_model` function enables users to create a model with a unique ID, configure its attributes, and set permissions for its usage.

## Key Features of the `create_model` Function

- **Project Initialization**: Define a project with the type `model` to register it on the platform.
- **Customizable Parameters**: Specify attributes like project name, project description, price, currency, and permissions.
- **Permission-Based Pricing**: If `api_access` permission is set to private, the price is automatically set to zero, ensuring proper access control.
- **Unique Model ID Generation**: Each created model is assigned a unique identifier (`model_id`) for tracking and future operations.

---

## Basic Usage

The `create_model` function simplifies the process of creating a new model on the Vipas.AI platform. Below is a step-by-step guide to creating a model using the SDK:

### `vipas.model.ModelClient.create_model(project_name: str, project_description: str, price: Optional[float] = 0.00, currency: Optional[str] = "INR", permissions: dict) → str`


### Parameters

- **`project_name` (str) [Required]**:  
 The name of the project (model). This is a required field and must not be empty. It supports only alphanumeric characters and non-consecutive hyphens (-). The maximum length is 30 characters.

- **`project_description` (str) [Required]**:  
  A brief description of the project. This is a required field and must not be empty. It supports only alphanumeric characters and spaces. The maximum length is 60 
  characters.

- **`price` (float) [Optional]**:  
  The price of the model. This is an optional field with a default value of 0.0. It is only applicable if api_access is set to public. The price must be between 0.00 and 999.00.

- **`currency` (str) [Optional]**:  
  Specifies the currency. This is an optional field that accepts only the following values: USD, EUR, INR. The default value is INR.

- **`permissions` (dict) [Optional]**:  
  A dictionary defining permissions for the project. This is a required field and accepts the following keys: `search_visibility`, `api_access`, `share_model`.

  - **`search_visibility` (Optional[str])**: Determines whether the project is visible in search results. Allowed values: `public` or `private`. Default: `private`.
  - **`api_access` (Optional[str])**: Grants or restricts access to use the model via API. Allowed values: `public` or `private`. Default: `private`.
  - **`share_model` (Optional[str])**: Allows or restricts sharing of the model. Allowed values: `public` or `private`. Default: `private`.

---

### Return Value

- **`str`**: A unique `model_id` in string format.


---

## Example Usage

Here's a basic example demonstrating how to create a model using the Vipas.AI SDK:

```python
from vipas.model import ModelClient
from vipas.exceptions import ClientException
from vipas.logger import LoggerClient

# Create a LoggerClient instance
logger_client = LoggerClient(__name__)

try:
    # Define model details
    project_name = "Image-Classification-AI"
    project_description = "ResNet50 based image classification model"
    price = 10.0
    currency = "USD"
    permissions = {
        "search_visibility": "public",
        "api_access": "public",
        "share_model": "private"
    }

    # Create a ModelClient instance
    model_client = ModelClient()

    # Call the create_model method to create a new model
    response = model_client.create_model(
        project_name=project_name,
        project_description=project_description,
        price=price,
        currency=currency,
        permissions=permissions
    )
    logger_client.info(f"Model created successfully: {response}")

except ClientException as e:
    logger_client.error(f"ClientException occurred: {e}")
except Exception as e:
    logger_client.error(f"An unexpected error occurred: {e}")
```

---

## Logging Example for Model Creation

The **Vipas.AI SDK** includes detailed logging to provide insights into the model creation process. Below is an example log sequence:

```
2024-11-20 13:03:57,301 - vipas.model - INFO - Initiating model creation. Name: 'sample-project1', Price: 100.0, Currency: 'USD'
2024-11-20 12:32:49,042 - vipas.model - INFO - Model successfully created with ID: <model-id>. You can view your model at: https://vipas.ai/models/<model-id>.
```

In this log sequence:
- The model creation process starts with logging the model's name.
- The second log confirms that the model was successfully created and provides the unique `model_id`

---

## Handling the Response

The response returned from the `create_model` function contains a `model_id` in string format:
- A `model_id` is a unique identifier for the model.
- You can use the model_id to find and manage your model on [Vipas.AI](https://vipas.ai).

---

## Error Handling

The SDK raises custom exceptions for API responses. Below is a list of possible exceptions and their meanings:

| **Exception**                           | **Description**                                                                                 |
|-----------------------------------------|-------------------------------------------------------------------------------------------------|
| `vipas.exceptions.ClientException` (409)| If the project name already exists.                                                            |
| `vipas.exceptions.UnauthorizedException` (401) | Authentication token is missing, invalid, or expired.                                           |
| `vipas.exceptions.ClientException` (422)| The input data was malformed or incomplete.                                                    |
| `vipas.exceptions.ConnectionException`  | Network connectivity issue or server is unreachable.                                           |
| `vipas.exceptions.ClientException`      | A generic client-side error occurred.                                                          |

## Generating MLflow Configuration Files
The Vipas.AI SDK provides functionality to generate and retrieve the necessary configuration files for deploying MLflow models on the platform. The mlflow_configuration_files function allows users to fetch a preconfigured zip file containing a Dockerfile and a model-settings.json file tailored for MLflow deployment.

## Key Features

### `mlflow_configuration_files` Function

- **Configuration Retrieval**: Fetch a preconfigured zip file that includes deployment essentials such as Dockerfile and model settings.
- **Customizable Runtime**: Option to specify whether a custom runtime is required.
- **Unique Output Path**: Each zip file is uniquely named based on the provided `model_id`.
- **Automatic Reformatting**: Ensures the `model-settings.json` file is correctly formatted.
- **Error Handling**: Provides detailed logging and raises appropriate exceptions for failures.

## Basic Usage

### Function Signature
```python
vipas.model.ModelClient.mlflow_configuration_files(
    model_id: str,                          # Required: unique identifier for the model
    custom_runtime: Optional[bool] = False  # Optional: Indicates whether to use a custom runtime configuration. This is applicable only if a custom runtime is supported. The default value is False
) -> str
```

### Parameters
- `model_id` *(Required)*: The unique identifier for the model. This ID is used to track the model across the platform.
- `custom_runtime` *(Optional)*: Indicates whether to use a custom runtime configuration. This is applicable only if a custom runtime is supported. The default value is `False`.

### Return Value
- `str`: The absolute file path of the saved configuration zip file.

### Example
```bash
/path/to/mlflow_config_<model_id>.zip
```

⚠️ **Note**: The function will generate a zip file that needs to be extracted. Once extracted, you will get a Dockerfile and a model-settings.json file. These files, along with the model folder, must be placed in the artifacts directory.

```
mlrun/
├── 0/
│   └── <run-id>/
│       └── artifacts/
│           ├── model/
|           |   ├── MLmodel
│           │   ├── model.pkl
│           │   ├── conda.yaml
│           │   ├── requirements.txt
│           ├── Dockerfile
│           ├── model-settings.json
```

### Important
- Ensure the Python version specified in the `Dockerfile` matches the version used to train the model. Update the `Dockerfile` if needed.

---

## Building and Publishing an MLflow-Based Model

### Step 1: Run the command to build a docker image 
```bash
docker build -t <dockerhub-username>/<repository-name>:<tag-name> .
```

### Step 2: Run the command to push the docker image to dockerhub
```bash
docker push <dockerhub-username>/<repository-name>:<tag-name>
```

### Step 3:Create a `mlflow_config.json`
```json
{
  "docker_image": "<dockerhub-username>/<repository-name>:<tag-name>",
  "docker_token": "<your dockerhub personal access token>"
}
```
To publish an MLflow-based model, pass the mlflow_config file path along with model_id and model_framework_type to the publish function:


#### Example Usage
```python
from vipas.model import ModelClient
from vipas.exceptions import ClientException
from vipas.logger import LoggerClient

# Create a LoggerClient instance
logger_client = LoggerClient(__name__)

try:
    # Define model details
    model_id = "mdl-abc123xyz"  # Required, unique identifier for the model
    custom_runtime = True       # Optional, Indicates whether to use a custom runtime configuration. This is applicable only if a custom runtime is supported. The default value is False.
    framework_type = "mlflow"   # Framework type for the model. In this case, it's "mlflow" to indicate the model uses the MLflow framework.
    mlflow_config_path = "/path/to/mlflow_config.json"  # Path to the MLflow JSON configuration file, containing settings like the model's Docker image and personal access token

    # Create a ModelClient instance
    model_client = ModelClient()

    # Call the mlflow_configuration_files method to retrieve the configuration zip file
    zip_file_path = model_client.mlflow_configuration_files(
        model_id=model_id, 
        custom_runtime=custom_runtime
    )
    logger_client.info(f"Configuration file saved at: {zip_file_path}")

    # Publish the model
    model_response = model_client.publish(
        model_id=model_id,
        model_framework_type=framework_type,
        mlflow_config_path=mlflow_config_path # The mlflow_config_path file is generated from the above Step 3 (creating mlflow_config.json).
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True, If set to False, the model will be placed in a staged state.
        override_model=True  # Whether to override existing model deployments, Default True
    )

    # Log the model publish response
    logger_client.info(model_response)

except ClientException as e:
    logger_client.error(f"ClientException occurred: {e}")
except Exception as e:
    logger_client.error(f"An unexpected error occurred: {e}")
```

---

## Logging Example for Configuration File Generation
The SDK provides detailed logging to ensure visibility into the configuration file retrieval process. Below is an example log sequence:

```log
2024-11-20 10:15:45,125 - vipas.mlflow - INFO - Fetching MLflow configuration files for model ID: mdl-abc123xyz.
2024-11-20 10:16:15,302 - vipas.mlflow - INFO - MLFlow configuration files successfully saved for model ID: mdl-abc123xyz at /path/to/mlflow_config_mdl-abc123xyz.zip.
```

---

## Error Handling
The SDK raises the following custom exceptions:

| Exception                            | Description                                            |
|--------------------------------------|--------------------------------------------------------|
| `vipas.exceptions.ClientException(404)` | Model or challenge ID not found.                     |
| `vipas.exceptions.UnauthorizedException (401)` | Authentication token is missing, invalid, or expired. |
| `vipas.exceptions.ConnectionException` | Network connectivity issue or server unreachable.    |
| `vipas.exceptions.ClientException`   | Generic client-side error.                            |

---

## Publishing Model
The Vipas.AI SDK provides a simple and powerful interface for developers to publish, manage, and deploy AI models. With this SDK, developers can upload their models, configure model processors, and deploy them to the Vipas platform seamlessly. This documentation will guide you through the process of using the SDK to publish and manage models built on various machine learning frameworks, including TensorFlow, PyTorch, ONNX, XGBoost, Scikit-learn, Hugging Face qwen 2.5, Hugging Face llama 3, Hugging Face google t5, Hugging Face google mt5, Hugging Face coedit large, Hugging Face dslim bert, Hugging Face distilbert, MLflow and more.


### Getting Started
---
### `vipas.model.ModelClient.publish(model_id: str, model_folder_path: Optional[str] = None, model_framework_type: str, onnx_config_path: Optional[str] = None, hf_config_path: Optional[str] = None, mlflow_config_path: Optional[str] = None, processor_folder_path: Optional[str] = None, processor_image: Optional[str] = None, auto_launch: bool = True, override_model: bool = True) → dict`

Publish a model to the Vipas AI platform.

#### Parameters:
- `model_id` (str) [Required]: The unique identifier of the model.
- `model_folder_path` (Optional[str]): The path to the folder containing the model files.
- `model_framework_type` (str) [Required]: The framework type of the model (e.g., 'tensorflow', 'pytorch', etc.).
- `onnx_config_path` (Optional[str]): The path to the ONNX config file (if applicable).
- `hf_config_path` (Optional[str]): The path to the Hugging Face config file (if applicable).
- `mlflow_config_path` (Optional[str]): The path to the MLflow config file (if applicable).
- `processor_folder_path` (Optional[str]): The path to the processor folder (if using a custom processor).
- `processor_image` (Optional[str]): The Docker image to use for the processor.
- `auto_launch` (Optional[bool]): Whether to automatically launch the model after publishing (default: True).
- `override_model` (Optional[bool]): Whether to override the existing model (default: True).

#### Returns:
- `dict`: A dictionary containing the status and details of the model publishing process.

#### Example: Publishing a Model with Frameworks like TensorFlow, PyTorch, XGBoost, or Scikit-learn

```python
from vipas.model import ModelClient
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException


# Paths to model and processor files
model_folder_path = "/path/to/your/model"
processor_folder_path = "/path/to/your/processor"

# Unique model ID to identify the model in Vipas.AI
model_id = "your_model_id" # mdl-xxxxxxxxx

try:
    # Initialize the ModelClient
    model_client = ModelClient()

    # Publish the model
    model_client.publish(
        model_id=model_id,
        model_folder_path=model_folder_path,
        model_framework_type="tensorflow",  # Supported: tensorflow, pytorch, onnx, xgboost, sklearn, hugging_face_qwen_2.5, hugging_face_llama_3, hugging_face_google_t5, hugging_face_google_mt5, hugging_face_coedit_large, hugging_face_dslim_bert, hugging_face_distilbert, mlflow etc.        
        processor_folder_path=processor_folder_path,  # Required only when using a custom processor; otherwise, it is Optional
        processor_image="your-processor-image:latest",  # allowed value are ["vps-processor-base:1.0"]
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True, If set to False, the model will be placed in a staged state.
        override_model=True  # Whether to override existing model deployments, Default True
    )
except UnauthorizedException as e:
    print(f"UnauthorizedException: {e}")
except NotFoundException as e:
    print(f"NotFoundException: {e}")
except ClientException as e:
    print(f"ClientException: {e}")
except Exception as e:
    print(f"Exception: {e}")
```
#### Example: Publishing an ONNX Model with Configuration

```python
from vipas.model import ModelClient
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException


# Paths to model and processor files
model_folder_path = "/path/to/your/model"
onnx_config_path = "/path/to/config/config.pbtxt"  # Optional, depends on framework
processor_folder_path = "/path/to/your/processor"

# Unique model ID to identify the model in Vipas.AI
model_id = "your_model_id" # mdl-xxxxxxxxx

try:
    # Initialize the ModelClient
    model_client = ModelClient()

    # Publish the model
    model_client.publish(
        model_id=model_id,
        model_folder_path=model_folder_path,
        model_framework_type="onnx",  # Supported: tensorflow, pytorch, onnx, xgboost, sklearn, hugging_face_qwen_2.5, hugging_face_llama_3, hugging_face_google_t5, hugging_face_google_mt5, hugging_face_coedit_large, hugging_face_dslim_bert, hugging_face_distilbert, mlflow etc.
        onnx_config_path=onnx_config_path,  # Required for the ONNX model framework        
        processor_folder_path=processor_folder_path,  # Required only when using a custom processor; otherwise, it is Optional
        processor_image="your-processor-image:latest",  # allowed value are ["vps-processor-base:1.0"]
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True, If set to False, the model will be placed in a staged state.
        override_model=True  # Whether to override existing model deployments, Default True
    )
except UnauthorizedException as e:
    print(f"UnauthorizedException: {e}")
except NotFoundException as e:
    print(f"NotFoundException: {e}")
except ClientException as e:
    print(f"ClientException: {e}")
except Exception as e:
    print(f"Exception: {e}")
```
> ⚠️ **Note:** For ONNX models, you must provide an ONNX configuration file with extensions like `.pbtxt`, `.config`, or `.txt` that describe the input-output mapping.
> 
> Below is an example ONNX configuration for input and output details needed by the model:
> 
> ```yaml
> input [
>  {
>    name: "input1"  # Name of the input going to the model (input tensor)
>    data_type: TYPE_FP32  # Data type of the input, FP32 stands for 32-bit floating point (commonly used in deep learning)
>    dims: [1, 3, 224, 224]  # Dimensions of the input tensor: [Batch size, Channels, Height, Width]
>  }
> ]
> output [
>  {
>    name: "output1"  # Name of the output from the model (output tensor)
>    data_type: TYPE_FP32  # Data type of the output, FP32 represents 32-bit floating point
>    dims: [1, 3, 224, 224]  # Dimensions of the output tensor: [Batch size, Channels, Height, Width]
>  }
> ]
> ```

#### Example: Publishing a Hugging Face Model

```python
from vipas.model import ModelClient
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException


# Paths to hugging face config files
hugging_face_config_path = "/path/to/config/config.json"  # Optional, Path to the Hugging Face config file which contains essential details like the Hugging Face access token, model ID, and maximum token limit.

# Unique model ID to identify the model in Vipas.AI
model_id = "your_model_id" # mdl-xxxxxxxxx

try:
    # Initialize the ModelClient
    model_client = ModelClient()

    # Publish the model
    model_client.publish(
        model_id=model_id,
        model_framework_type="hugging_face_llama_3",  # Supported: tensorflow, pytorch, onnx, xgboost, sklearn, hugging_face_qwen_2.5, hugging_face_llama_3, hugging_face_google_t5, hugging_face_google_mt5, hugging_face_coedit_large, hugging_face_dslim_bert, hugging_face_distilbert, mlflow etc.
        hf_config_path=hugging_face_config_path,  # Required for the Hugging Face model framework
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True, If set to False, the model will be placed in a staged state.
        override_model=True  # Whether to override existing model deployments, Default True
    )
except UnauthorizedException as e:
    print(f"UnauthorizedException: {e}")
except NotFoundException as e:
    print(f"NotFoundException: {e}")
except ClientException as e:
    print(f"ClientException: {e}")
except Exception as e:
    print(f"Exception: {e}")
```
| **Hugging Face Framework Types**                           | **Hugging Face Model Ids**                                                                                 |
|-----------------------------------------|-------------------------------------------------------------------------------------------------|
| `hugging_face_qwen_2.5`                 | Qwen/Qwen2.5-1.5B                                                                               |
| `hugging_face_llama_3`                  | meta-llama/meta-llama-3-8b-instruct                                                             |
| `hugging_face_google_t5`                | google-t5/t5-small                                                                              |
| `hugging_face_google_mt5`               | google/mt5-base                                                                                 |
| `hugging_face_coedit_large`             | grammarly/coedit-large                                                                          |
| `hugging_face_dslim_bert`               | dslim/bert-base-NER                                                                             |
| `hugging_face_distilbert`               | distilbert/distilbert-base-uncased-finetuned-sst-2-english                                      |


> ⚠️ **Note:** For the Hugging Face models you must provide the above framework       types.
>For Hugging Face models, you must provide a Hugging face configuration file with extensions like .json or .txt that has the Hugging face access token, Hugging Face model id and Hugging Face max tokens.
>
>Below is an example Hugging Face configuration:
> ```json
> {
>    "hf_access_token":"<hugging face access token>",  # Required, a valid Hugging Face access token for model creation. You can obtain your Hugging Face access token from your account's 'Access Tokens' section on the Hugging Face website.
>    "hf_model_id":"<hugging face model id>", # Required, The unique identifier of the Hugging Face model. Framework-specific IDs are listed in the above table. 
>    "hf_max_token": 100   # The maximum token limit, which is an integer value between 1 and 500. If not specified, the default value is 100.
>}
> ```
#### Example: Publishing a MLflow Model
```python
from vipas.model import ModelClient
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException


# Paths to MLflow config files
mlflow_config_path = "/path/to/mlflow_config.json"  # Optional, Path to the MLflow config file which contains details like the model docker image and a valid docker personal access token. Both are required.

# Unique model ID to identify the model in Vipas.AI
model_id = "your_model_id" # mdl-xxxxxxxxx

try:
    # Initialize the ModelClient
    model_client = ModelClient()

    # Publish the model
    model_client.publish(
        model_id=model_id,
        model_framework_type="mlflow",  # Supported: tensorflow, pytorch, onnx, xgboost, sklearn, hugging_face_qwen_2.5, hugging_face_llama_3, hugging_face_google_t5, hugging_face_google_mt5, hugging_face_coedit_large, hugging_face_dslim_bert, hugging_face_distilbert, mlflow etc.
        mlflow_config_path=mlflow_config_path,  # Required for the MLflow model framework
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True, If set to False, the model will be placed in a staged state.
        override_model=True  # Whether to override existing model deployments, Default True
    )
except UnauthorizedException as e:
    print(f"UnauthorizedException: {e}")
except NotFoundException as e:
    print(f"NotFoundException: {e}")
except ClientException as e:
    print(f"ClientException: {e}")
except Exception as e:
    print(f"Exception: {e}")
```
### Publishing Process Overview
---
When you publish a model using the Vipas SDK, the following steps occur behind the scenes:
1. **Model Upload**: The SDK uploads the model files from the specified directory. The total size of the files is calculated, and the upload process is logged step-by-step.
2. **Processor Upload (Optional)**: If you are using a custom processor (a custom Python script), the SDK uploads the processor files. This step is optional but can be critical for advanced use cases where model input needs specific transformations.
3. **Processor Staging(Optional)**: After the processor upload, the processor will get staged if the files are properly uploaded.
4. **Model Staging And Building Processor**: Once the model and its associated files (including the processor, if applicable) are uploaded, the model is placed in a staging state. This stage ensures that all files are correctly uploaded and prepares the model for deployment.
5. **Model Launch (Optional)**: If the auto_launch parameter is set to True, the model will be automatically launched. This means that the model will be deployed and become available for real-time and asynchronous inference. The launch status is logged until the process is completed successfully.
6. **Rollback Mechanism**: If a model is already deployed and a new version is being uploaded, the SDK ensures that the previous version is rolled back in case of any issues during the new model deployment. 
> **Note:** The Rollback Mechanism will not occur if you make override_model=False.

#### Key parameters
1. **model_id [Required]**: The unique identifier for the model. This ID is used to track the model across the platform.
2. **model_folder_path [Optional]**: The path to the directory containing the model files that need to be uploaded.
3. **model_framework_type [Required]**: The framework used for the model (e.g., TensorFlow, PyTorch, ONNX, XGBoost, Scikit-learn). Each framework has its own nuances in terms of model configuration.
4. **onnx_config_path[Optional]**: The path to the ONNX configuration file required by the ONNX framework.
5. **hf_config_path[Optional]**: The path to the Hugging Face configuration file required for the Hugging Face framework. 
6. **mlflow_config_path[Optional]**: The path to the MLflow configuration file required for the MLflow framework.
7. **processor_folder_path[Optional]**: The path to the folder containing custom processor file, such as Python script, if applicable. Optional if using a processor.
8. **processor_image[Optional]**: The Docker base image for the processor. Currently supporting “vps-processor-base:1.0”.
9. **auto_launch[Optional - Default: True]**: A boolean flag indicating whether to automatically launch the model after publishing. Default is True.
10. **override_model[Optional - Default: True]**: A boolean flag indicating whether to override any existing model deployment. Default is True.

#### Supported Frameworks
The SDK supports the following machine learning frameworks:
1. TensorFlow: Native TensorFlow SavedModel format.
2. PyTorch: Model files saved as .pt or .pth.
3. ONNX: ONNX models typically require a configuration file with extensions like (.pbtxt, .config, .txt) for setting input and output shapes.
4. XGBoost: For tree-based models exported from XGBoost.
5. Scikit-learn: For traditional machine learning models exported from scikit-learn.
6. hugging_face_qwen2.5-1.5B: is a lightweight, 1.5-billion-parameter language model designed for efficient natural language processing tasks.
7. hugging_face_llama_3: A high-performance large language model designed for conversational AI and text generation.
8. hugging_face_google_t5: A versatile text-to-text model capable of handling diverse NLP tasks by framing them as text generation problems.
9. hugging_face_google_mt5: A multilingual version of T5, fine-tuned for translation and cross-lingual understanding.
10. hugging_face_coedit_large: This model was obtained by fine-tuning the corresponding google/flan-t5-large model on the CoEdIT dataset.
11. hugging_face_dslim_bert: A fine-tuned BERT model designed for named entity recognition and sequence classification tasks.
12. hugging_face_distilbert: A lightweight, distilled version of BERT offering faster inference with comparable performance on NLP tasks.
13. MLflow: An open-source platform for managing the end-to-end machine learning lifecycle, including experimentation, reproducibility, and deployment

#### Expected Behavior
1. **Successful Upload**: The model and processor files will be uploaded, and the model will be placed in the staged state.
2. **Automatic Launch**: If auto_launch=True, the model will be launched after the upload completes, making it available for real-time and asynchronous inference.
3. **Override of Existing Models**: If a model with the same model_id is already deployed, the new model will override the previous deployment if override_model=True.

#### Logs Example
Once you run the publish() method, you can expect logs similar to the following:
```bash
2024-10-08 16:15:15,043 - vipas.model - INFO - Publishing model mdl-ikas2ot2ohsux with framework type onnx.
2024-10-08 16:15:19,818 - vipas.model - INFO - File processor.py uploaded successfully.
2024-10-08 16:16:22,952 - vipas.model - INFO - Model mdl-ikas2ot2ohsux and related processor launched successfully.
```

This log sequence shows the entire process of publishing the model, uploading the processor, and successfully launching the model. Any errors or warnings will also be captured in the logs, which can help troubleshoot issues.

## Error Handling

The SDK raises custom exceptions for API responses. Below is a list of possible exceptions and their meanings:

| **Exception**                           | **Description**                                                                                 |
|-----------------------------------------|-------------------------------------------------------------------------------------------------|
| `vipas.exceptions.NotFoundException` (404)| If the model id was not found.                                                           |
| `vipas.exceptions.UnauthorizedException` (401) | Authentication token is missing, invalid, or expired.                                    |
| `vipas.exceptions.ClientException` (400)| If model framework type is not supported.                                                     |
| `vipas.exceptions.ConnectionException`      | Network connectivity issue or server is unreachable..                                                       |



# Retrieving Model Deployment Logs with the Vipas.AI SDK

The Vipas.AI SDK provides the `get_logs` function, enabling users to retrieve detailed logs for a specific model. This functionality supports debugging and monitoring by fetching logs associated with the provided `model_id`.

## Key Features of the `get_logs` Function
- **Log Retrieval by Model ID**: Retrieve deployment logs of a specific model by providing its unique identifier.
- **Secure API Access**: Uses the `vps-auth-token` for authentication and ensures secure communication with the API.
- **Detailed Logging**: Provides comprehensive logs for each step of the deployment log retrieval process to ensure transparency and traceability.

## Function Signature
```python
vipas.model.ModelClient.get_logs(model_id: str) → str
```

### Parameters
- `model_id (str)` [Required]:  
  The unique identifier of the model whose logs are to be retrieved.  
  **Constraints**:  
  - Required field.  
  - Must be a valid and existing `model_id`.

### Return Value
**`dict`**: A dictionary containing metadata about the logs, including:
- **`filename`**: Name of the log file.
- **`presigned_url`**: A temporary, secure URL to access the log file.
- **`size`**: Size of the log file in bytes.
- **`last_modified`**: Timestamp indicating when the log file was last updated.

The logs provide insights into the model's operation and are structured for easy interpretation.

## Example Usage
Below is an example demonstrating how to use the `get_logs` function to retrieve logs for a specific model:

```python
from vipas.model import ModelClient
from vipas.exceptions import ClientException
from vipas.logger import LoggerClient

# Create a LoggerClient instance
logger_client = LoggerClient(__name__)

try:
    # Define model ID
    model_id = "mdl-1234abcd5678efgxy"

    # Create a ModelClient instance
    model_client = ModelClient()

    # Call the get_logs method to retrieve logs for the model
    logs = model_client.get_logs(model_id=model_id)

    # Display retrieved logs
    logger_client.info(f"Logs retrieved successfully: {logs}")

except ClientException as e:
    logger_client.error(f"ClientException occurred while retrieving logs: {e}")
except Exception as e:
    logger_client.error(f"An unexpected error occurred: {e}")
```

## Handling the Response
The `get_logs` function returns a dictionary containing the model and processor logs. Below is an example response structure:

```json
{
  "model": {},
  "processor": {
    "2024": {
      "11": {
        "21": [
          {
            "filename": "<Name of the log file>",
            "presigned_url": "<A temporary, secure URL to access the log file>",
            "size": "Size of the log file in bytes",
            "last_modified": "Timestamp indicating when the log file was last updated"
          }
        ]
      }
    }
  }
}
```

## Error Handling
The `get_logs` function raises custom exceptions to handle various error scenarios:

| Exception                                | Description                                                                                  |
|------------------------------------------|----------------------------------------------------------------------------------------------|
| `vipas.exceptions.ClientException (409)` | If the `model_id` does not exist or is invalid.                                              |
| `vipas.exceptions.UnauthorizedException (401)` | If the authentication token is missing, invalid, or expired.                                 |
| `vipas.exceptions.ClientException (422)` | If the request parameters are malformed or incomplete.                                       |
| `vipas.exceptions.ConnectionException`   | If there is a network connectivity issue or the API server is unreachable.                   |
| `vipas.exceptions.ClientException`       | A generic client-side error occurred during the log retrieval process.                       |


## Evaluating a Model against a Challenge
The Vipas.AI SDK provides functionality to evaluate your models against specific challenges hosted on the Vipas platform. The evaluate function allows you to submit a model for evaluation against a challenge and track its progress until completion.

### Key Features of the evaluate Function:
---
1. **Model and Challenge Pairing**: You must provide both a model_id and a challenge_id to evaluate your model against a particular challenge.
2. **Progress Tracking**: The SDK tracks the progress of the evaluation in the background and logs the status at regular intervals.
3. **Error Handling**: Specific exceptions like ClientException and general exceptions are captured and handled to ensure smooth operations.


### Basic Usage
---
### `vipas.model.ModelClient.evaluate(model_id: str, challenge_id: str) → dict`

Evaluate a model against a challenge.

#### Parameters:
- `model_id` (str) [Required]: The unique identifier of the model.
- `challenge_id` (str) [Required]: The unique identifier of the challenge.

#### Returns:
- `dict`: A dictionary containing the result of the model evaluation process.

Here's a basic example demonstrating how to evaluate a model against a challenge using the Vipas.AI SDK:
```python
from vipas.model import ModelClient
from vipas.exceptions import ClientException
from vipas import config, _rest

try:
    model_id = "mdl-bosb93njhjc97"  # Replace with your model ID
    challenge_id = "chg-2bg7oqy4halgi"  # Replace with the challenge ID

    # Create a ModelClient instance
    model_client = ModelClient()

    # Call the evaluate method to submit the model for evaluation against the challenge
    response = model_client.evaluate(model_id=model_id, challenge_id=challenge_id)

    print(response)

except ClientException as e:
    print(f"ClientException occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

### Logging Example for evaluate
The SDK logs detailed information about the evaluation process, including the model ID and challenge ID being evaluated, as well as the progress of the evaluation. Below is an example of the log output:
```bash
2024-10-17 15:25:19,706 - vipas.model - INFO - Evaluating model mdl-bosb93njhjc97 against the challenge chg-2bg7oqy4halgi.
2024-10-17 15:25:20,472 - vipas._rest - INFO - Evaluate model for model: mdl-bosb93njhjc97 against the challenge: chg-2bg7oqy4halgi is in progress.
2024-10-17 15:25:28,261 - vipas._rest - INFO - Evaluate model for model: mdl-bosb93njhjc97 against the challenge: chg-2bg7oqy4halgi is in progress.
2024-10-17 15:26:10,805 - vipas._rest - INFO - Evaluate model for model: mdl-bosb93njhjc97 against the challenge: chg-2bg7oqy4halgi completed successfully.
```
In this log sequence:

* The evaluation process begins by logging the model ID and challenge ID.
* The progress of the evaluation is tracked and logged at regular intervals.
* Finally, upon successful completion, a message indicates the evaluation was successful.

### Handling the Response
---
The response returned from the evaluate function contains detailed information about the evaluation, including:

* Evaluation status (e.g., inprogress, completed, failed).
* Any associated results or metrics generated during the evaluation process.
* Potential error messages, if the evaluation encounters any issues.

By integrating the evaluate function into your workflow, you can efficiently evaluate your models against challenges on the Vipas platform and gain insights into their performance.

## Listing the Submissions of a Challenge

The `get_challenge_submissions` function is a convenient method in the Vipas.AI Python SDK for retrieving all submissions made to a specific challenge on the Vipas AI platform. This function allows developers to programmatically access challenge submissions by providing the unique challenge identifier.

---

### Getting Started

To use the `get_challenge_submissions` function, ensure that the Vipas.AI SDK is installed and properly configured in your environment.

---

### Example: Getting Submissions of a Challenge

```python
from vipas.challenge import ChallengeClient

client = ChallengeClient()

print(client.get_challenge_submissions(challenge_id=<challenge_id>))
```

---

### Key Parameters

- **challenge_id [Required]**:  
  The unique identifier for the challenge. This ID is used to track the challenge across the platform.

---

### Returns

- **total_count**:  
  Indicates the total number of challenge runtimes retrieved.

- **challenge_runtimes**:  
  A list of challenge runtime objects, where each object contains:
  - **challenge_id**: Unique identifier for the challenge.
  - **entity_id**: The unique identifier of the user who submitted the model.
  - **entity_name**: Name of the entity (e.g., user's name).
  - **model_id**: ID of the associated model.
  - **transaction_id**: Unique transaction ID for the specific runtime.
  - **challenge_runtime_metrics**: Contains system metrics related to the runtime, including:
    - **latency**: Execution latency in milliseconds.
    - **cpu_metric**: CPU utilization metric in cores.
    - **memory_metric**: Memory utilization metric in MBs.
  - **created_at**: Timestamp when the runtime was created.
  - **updated_at**: Timestamp when the runtime was last updated.
  - **presigned_urls**: Contains list of temporary URLs objects to download files related to the runtime:
    - **input_temporary_url**: URL to download the input file.
    - **output_temporary_url**: URL to download the expected output file.
    - **actual_output_temporary_url**: URL to download the actual output file generated by the model.
    - **input_file_name**: Input file name.
    - **expected_output_filename**: Expected output file name.
    - **actual_output_filename**: Actual output file name.

---

### Response Handling

The response provides detailed information for each user's runtime submission. This includes options to download the input, expected output, and actual output of each submission separately. Additionally, users can access runtime metrics associated with each submission to gain insights into performance and resource utilization.

---

### Error Handling

In case of errors, the SDK raises exceptions:

- **NotFoundException**:  
  Raised when the challenge or submission is not found.
- **ClientException**:  
  Raised for SDK-related errors, such as invalid parameters or authentication issues.
- **Other Exceptions**:  
  Raised for general Python exceptions (e.g., file not found, network errors).

---


## Logging
The SDK provides a LoggerClient class to handle logging. Here's how you can use it:

### LoggerClient Usage

1. Import the `LoggerClient` class:
```python
from vipas.logger import LoggerClient
```

2. Initialize the `LoggerClient`:
```python
logger = LoggerClient(__name__)
```

3. Log messages at different levels:
```python
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

```

### Example of LoggerClient
Here is a complete example demonstrating the usage of the LoggerClient:

```python
from vipas.logger import LoggerClient

def main():
    logger = LoggerClient(__name__)
    
    logger.info("Starting the main function")
    
    try:
        # Example operation
        result = 10 / 2
        logger.debug(f"Result of division: {result}")
    except ZeroDivisionError as e:
        logger.error("Error occurred: Division by zero")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
    finally:
        logger.info("End of the main function")

main()
``` 

## Author
VIPAS.AI

## License
This project is licensed under the terms of the [vipas.ai license](LICENSE.md).

By following the above guidelines, you can effectively use the VIPAS AI Python SDK to interact with the VIPAS AI platform for making predictions, handling exceptions, and logging activities.




