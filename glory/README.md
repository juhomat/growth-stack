# Growth Stack - Digital Marketing and Sales Tools

Growth Stack is a comprehensive collection of digital marketing, sales, and website tools built using the Hexagonal Architecture framework.

## Features

- **Marketing Tools**: Campaign management, email marketing, and content creation
- **Sales Tools**: Lead tracking, conversion optimization, and sales analytics
- **Website Tools**: SEO analysis, performance monitoring, and website optimization
- **Analytics**: Real-time metrics, custom reports, and performance dashboards

## Architecture

This application is built using the Hexagonal Architecture (Ports and Adapters) pattern, which provides clean separation between:

- **Core Domain Logic**: The business rules and domain models
- **Ports**: Interfaces that define the capabilities
- **Adapters**: Implementations of those interfaces
- **UI Layer**: The web interface built with responsive design

## Technology Stack

- **Backend**: Python 3.12+ with the Hexagonal Architecture framework
- **Frontend**: HTML5, CSS3 (with Tailwind CSS), and vanilla JavaScript
- **UI Components**: Chart.js for data visualization
- **APIs**: Integration with various marketing and sales APIs

## Getting Started

### Prerequisites

- Python 3.12+
- Poetry (optional, for dependency management)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e ".[all]"
   ```
3. Set up environment variables (see below)
4. Run the application:
   ```bash
   python -m growth_stack.main
   ```

### Environment Variables

Copy the example environment file and update it with your API keys:

```bash
cp example_env_vars.py .env
```

Required variables include:
- `OPENAI_API_KEY`: For AI-powered content generation
- `TAVILY_API_KEY`: For web search capabilities
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Development

### Project Structure

```
growth_stack/
├── static/              # Static assets
│   ├── css/             # CSS styles
│   ├── js/              # JavaScript files
│   └── assets/          # Images, icons, etc.
├── templates/           # HTML templates
├── __init__.py          # Package initialization
└── main.py              # Application entry point
```

### Adding New Features

The application follows the Hexagonal Architecture pattern. To add a new feature:

1. Define a new port interface in the appropriate module
2. Create an adapter implementation for that interface
3. Register the adapter in the container
4. Add UI components as needed

## License

This project is licensed under the MIT License.

## Acknowledgements

- Built on top of the Hexagonal Architecture framework
- Uses various open-source libraries and tools 