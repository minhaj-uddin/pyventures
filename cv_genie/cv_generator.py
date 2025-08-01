import json
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, 'Curriculum Vitae', align="C",
                  new_x="LMARGIN", new_y="NEXT")

    def add_section_title(self, title, style="B", size=12):
        self.set_font("helvetica", style, size)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

    def add_text(self, text, style="I", size=10):
        self.set_font("helvetica", style, size)
        self.multi_cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")

    def add_bullet_list(self, items):
        self.set_font("helvetica", "", 10)
        for item in items:
            self.cell(0, 7, f". {item}", new_x="LMARGIN", new_y="NEXT")

    def add_numbered_list(self, items):
        self.set_font("helvetica", "", 10)
        for idx, item in enumerate(items, 1):
            self.cell(0, 7, f"{idx}. {item}", new_x="LMARGIN", new_y="NEXT")

    def add_table(self, header, rows):
        self.set_font("helvetica", "B", 10)
        col_widths = [100, 40, 30]
        for i, col in enumerate(header):
            self.cell(col_widths[i], 10, col, border=1, align="C")
        self.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "", 10)
        for row in rows:
            for i, col in enumerate(row):
                self.cell(col_widths[i], 10, col, border=1, align="C")
            self.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")

    def add_image(self, img_path, x=10, y=10, w=40):
        self.image(img_path, x, y, w)
        self.cell(0, 20, "", new_x="LMARGIN", new_y="NEXT")


# Read the JSON file
with open('cv_template.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

# Create PDF instance
pdf = PDF()
pdf.add_page()

# 1. Header - Name, Contact, and Image
pdf.set_font("helvetica", "B", 16)
pdf.cell(0, 10, data["name"], new_x="LMARGIN", new_y="NEXT")

# Add Profile Image (e.g., "profile.jpg")
pdf.add_image(data["image"], x=10, y=10, w=30)

pdf.set_font("helvetica", "", 12)
pdf.cell(
    0, 10, f"Email: {data['contact']['email']} | LinkedIn: {data['contact']['linkedin']}")
pdf.cell(0, 15, "", new_x="LMARGIN", new_y="NEXT")

# 2. Bio Section
pdf.add_section_title("Bio")
pdf.add_text(data["bio"])

# 3. Education Section (Table)
pdf.add_section_title("Education")
education_header = ["Degree", "University", "Year"]
education_rows = [(item["degree"], item["university"], item["year"])
                  for item in data["education"]]
pdf.add_table(education_header, education_rows)

# 4. Work Experience Section
pdf.add_section_title("Work Experience")
for work in data["work_experience"]:
    pdf.add_section_title(
        work["title"] + f" at {work['company']} ({work['years']})")
    pdf.add_bullet_list(work["responsibilities"])

# 5. Skills Section (Bullet List)
pdf.add_section_title("Skills")
pdf.add_bullet_list(data["skills"])

# 6. Certifications Section (Numbered List)
pdf.add_section_title("Certifications")
pdf.add_numbered_list(data["certifications"])

# Output the CV to a file
pdf.output("generated_cv.pdf")

print("CV generated successfully!")
