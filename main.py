from website import create_app

"""main.py serves to run the app"""
app = create_app()
if __name__ == "__main__":
       app.run(debug=True)
