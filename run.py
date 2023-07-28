from dubinsko import create_app, cli

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {"app":app}

if __name__ == "__main__":
    app.run(debug=True)

    
