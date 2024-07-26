# Concert Reservation System

This application allows users to book tickets for a concert and generates PDF tickets with QR codes, which are then sent via email.

## Features

- Generates PDF tickets with QR codes.
- Sends PDF tickets via email to the user.

## Prerequisites

- `pipenv` for dependency management

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yanis-san/concert-reservation-system.git
    cd concert-reservation-system
    ```

2. Create a virtual environment and install dependencies using `pipenv`:

    ```bash
    pipenv install
    ```

3. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

## Usage

1. Run the application:

    ```bash
    streamlit run main.py
    ```

2. Fill in the required information on the form.

3. Click the "Generate Ticket" button to receive your e-ticket via email.

## Project Structure

- `main.py`: Main script that runs the Streamlit application.
- `tickets.db`: SQLite database file where ticket information is stored. Note that while SQLite is used for simplicity in this project, it is recommended to use a more robust database like PostgreSQL or MySQL for production environments.
- `ticket.jpg`: Image file used as a background for the PDF ticket.
