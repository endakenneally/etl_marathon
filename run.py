from app import create_app

# Create app instance
app = create_app()

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
