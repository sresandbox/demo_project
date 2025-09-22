# Flask GitHub Gist API

This project is a Flask application that allows users to fetch public gists from GitHub. It provides a simple HTML interface for user interaction.

## Project Structure

```
demo_project
├── app.py                # Flask application code
├── requirements.txt      # Python dependencies
├── .github
│   └── workflows
│       └── deploy.yml    # GitHub Actions CI/CD workflow
└── README.md             # Project documentation
```

## Requirements

To run this application, you need to have Python 3.x installed along with the required dependencies listed in `requirements.txt`.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd demo_project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your GitHub token as an environment variable:
   ```
   export GITHUB_TOKEN=<your_github_token>
   ```

## Running the Application

To run the Flask application, execute the following command:
```
python app.py
```

The application will be accessible at `http://localhost:8080`.

## Usage

- Navigate to the homepage to enter a GitHub username and fetch their public gists.
- The API endpoint can also be accessed directly via `GET /<github-username>`.

## CI/CD

This project includes a GitHub Actions workflow defined in `.github/workflows/deploy.yml` for Continuous Integration and Continuous Deployment. It automates the deployment process whenever changes are pushed to the main branch.

## License

This project is licensed under the MIT License.