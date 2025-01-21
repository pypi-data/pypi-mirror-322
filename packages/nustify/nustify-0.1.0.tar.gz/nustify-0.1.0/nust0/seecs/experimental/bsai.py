# bsai.py

class ICT:
    def __init__(self):
        self.name = "Habeel Ahmed"
        self.specialty = "ICT"
    
    def lecture(self):
        return "Trying to decipher the lecture... 'What's he saying?!'"

class CPlusPlus:
    def __init__(self):
        self.name = "Mehwish Kiran"
        self.specialty = "C++"
    
    def exam_preparation(self):
        return "Surprise! The syllabus is a mystery. Best of luck on the exam!"

class Math:
    def __init__(self, teacher="Ahtasham"):
        self.teacher = teacher
    
    def feedback(self):
        if self.teacher == "Ahtasham":
            return "A well-balanced teacher. Explains everything nicely!"
        elif self.teacher == "Atifa Kanwal":
            return (
                "Syllabus completed at the speed of light! Students scratching their heads in confusion."
            )
        else:
            return "Math: a subject of infinite possibilities... and teacher quirks!"

class English:
    def __init__(self):
        self.name = "Samia Tahir"
        self.specialty = "English"
    
    def lecture(self):
        return "Reading slides with the same energy as an audiobook narrator."

def experimental_vibe():
    return (
        "Welcome, pioneers of BSAI at SEECS! Let's make history, "
        "one confused lecture at a time. First Semester!"
    )

def semester_1():
    # Combining everything into the semester_1 function
    return (
        f"{experimental_vibe()}\n"
        f"Habeel Ahmed (ICT): {ICT().lecture()}\n"
        f"Mehwish Kiran (C++): {CPlusPlus().exam_preparation()}\n"
        f"Feedback on Sir Ahtasham (Math): {Math(teacher='Ahtasham').feedback()}\n"
        f"Feedback on Atifa Kanwal (Math): {Math(teacher='Atifa Kanwal').feedback()}\n"
        f"Samia Tahir (English): {English().lecture()}"
    )
