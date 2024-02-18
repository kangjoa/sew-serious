# Homework 3: Grocery Fabric

_For instructions on how to complete this assignment, see [part 1](https://github.com/Tech-at-DU/ACS-1220-Authentication-and-Associations/blob/master/Assignments/grocery-fabric.md) and [part 2](https://github.com/Tech-at-DU/ACS-1220-Authentication-and-Associations/blob/master/Assignments/grocery-fabric-part-2.md)._

To run this code, start by cloning this repository to your computer. Then in a terminal, navigate to the project folder.

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
python3 app.py
```

When you are finished coding, simply close the terminal or type `deactivate` to terminate the virtual environment.