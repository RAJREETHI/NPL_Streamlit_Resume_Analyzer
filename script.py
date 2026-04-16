with open("soft_skills.txt", "r") as f:
    text = f.read()

# remove spaces, replace commas with newline
cleaned = text.replace("-", "")

with open("output.txt", "w") as f:
    f.write(cleaned)
