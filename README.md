# Render Backend for Gemini Integration

This backend service receives user input from a Netlify frontend, forwards it to the Gemini API, and returns the generated output.

## Features

- Receives user input from a Netlify frontend
- Forwards requests to the Gemini API
- Returns Gemini-generated responses to the frontend
- Simple and lightweight backend logic

## Getting Started

### Prerequisites

- Python 3.7+
- Flask or FastAPI (or your preferred web framework)
- Gemini API access and credentials
- Other dependencies (see `requirements.txt`)

### Installation

```bash
git clone https://github.com/Sar-Hal/Video_Understanding_Models.git
cd Video_Understanding_Models
pip install -r requirements.txt
```

### Usage

Start the backend server:

```bash
python main.py
```

The backend exposes an endpoint (e.g., `/api/generate`) that accepts user input and returns Gemini's output.

## Example API Request

```http
POST /api/generate
Content-Type: application/json

{
    "user_input": "Your prompt here"
}
```

## Directory Structure

```
.
├── main.py             # Main backend server code
├── requirements.txt   # Python dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.
