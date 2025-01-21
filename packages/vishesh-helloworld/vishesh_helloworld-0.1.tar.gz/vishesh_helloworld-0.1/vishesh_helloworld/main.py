# vishesh_helloworld/main.py

def create_helloworld_file(filename="helloworld.py"):
    content = '''print("Hello, World!")'''

    # Create the file in the current directory
    with open(filename, 'w') as file:
        file.write(content)

    print(f"File '{filename}' created successfully!")
