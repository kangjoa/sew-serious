# Final Project
## Sewing App
This sewing app helps users keep track of their fabric stash and sewing pattern collection. Users can create new fabrics or sewing pattern records and add them to their fabric lists or patterns lists.

### Set up

Create virtual environment and activate:
```
python3 -m venv venv
source venv/bin/activate
```

To install dependencies, run:

```
pip3 install -r requirements.txt
```

Then rename the `.env.example` file as `.env`:

This command copies the file `.env.example` to a new file named `.env`
Use this when you want to keep both files, both `.env.example` and `.env`
```
cp .env.example .env
```

Use `mv .env.example .env` when you want to rename the file.

Then you can run the server:

```
python app.py
```

When you are finished coding, simply close the terminal or type `deactivate` to terminate the virtual environment.