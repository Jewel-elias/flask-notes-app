from website import create_app

app = create_app()

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)